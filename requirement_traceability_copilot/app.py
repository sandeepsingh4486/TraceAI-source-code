import io
import json
import os
import time
from pathlib import Path

import pandas as pd
import streamlit as st
from docx import Document
from pypdf import PdfReader
from google import genai
from google.genai import types

from prompts import SYSTEM_PROMPT, build_analysis_prompt
from schemas import AnalysisResult
from utils import load_demo_analysis, make_markdown_report


APP_TITLE = "TraceAI — Requirement-to-Test Copilot"
DEFAULT_MODEL = "gemini-3.7-flash"


def extract_text(uploaded_file) -> str:
    """Extract text from TXT/MD/PDF/DOCX without sending the file itself anywhere."""
    suffix = Path(uploaded_file.name).suffix.lower()
    data = uploaded_file.getvalue()

    if suffix in {".txt", ".md", ".csv"}:
        return data.decode("utf-8", errors="replace")

    if suffix == ".pdf":
        reader = PdfReader(io.BytesIO(data))
        chunks = []
        for i, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            chunks.append(f"\n--- Page {i} ---\n{text}")
        return "\n".join(chunks)

    if suffix == ".docx":
        doc = Document(io.BytesIO(data))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    raise ValueError(f"Unsupported file type: {suffix}")


def analyze_with_gemini(api_key: str, model: str, document_text: str, context: str) -> dict:
    client = genai.Client(api_key=api_key)
    prompt = build_analysis_prompt(document_text=document_text, context=context)

    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            response_schema=AnalysisResult,
            temperature=0.2,
        ),
    )

    if response.parsed is not None:
        parsed = response.parsed
        if hasattr(parsed, "model_dump"):
            return parsed.model_dump()
        return dict(parsed)

    return json.loads(response.text)


def show_metric_row(manual_minutes: int, ai_seconds: float):
    ai_minutes = ai_seconds / 60.0
    reduction = max(0.0, (1 - ai_minutes / max(manual_minutes, 1)) * 100)

    c1, c2, c3 = st.columns(3)
    c1.metric("Manual baseline", f"{manual_minutes} min")
    c2.metric("AI analysis", f"{ai_seconds:.1f} sec")
    c3.metric("Estimated effort reduction", f"{reduction:.1f}%")
    return reduction


def to_df(items):
    return pd.DataFrame(items) if items else pd.DataFrame()


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🔗",
    layout="wide",
)

st.title("🔗 TraceAI")
st.caption("AI Requirement → Impact → Risk → Test → Traceability Copilot")

st.info(
    "Engineering decision-support prototype. AI output is a draft for human review; "
    "it does not replace safety, compliance, verification, or engineering approval."
)

with st.sidebar:
    st.header("Run mode")
    mode = st.radio("Choose mode", ["Live AI", "Demo"], index=1)

    model = st.text_input("Gemini model", DEFAULT_MODEL)
    api_key = ""
    if mode == "Live AI":
        api_key = st.text_input(
            "Gemini API key",
            value=os.getenv("GEMINI_API_KEY", ""),
            type="password",
            help="You can also set GEMINI_API_KEY as an environment variable.",
        )

    st.divider()
    manual_minutes = st.number_input(
        "Typical manual analysis time (minutes)",
        min_value=10,
        max_value=1440,
        value=180,
        step=10,
    )

    st.markdown(
        "**Judging story**\n\n"
        "Unstructured engineering input → structured requirements → impact → risks → "
        "tests → traceability → actions."
    )

tab_input, tab_about = st.tabs(["Analyze", "Why this needs AI"])

with tab_about:
    st.subheader("Why this is not a rule engine")
    st.markdown(
        """
- Requirements arrive as natural language in PDFs, emails, specifications, meeting notes, and change requests.
- The same intent can be expressed in many different ways.
- The solution must connect one statement to multiple engineering consequences.
- It must identify ambiguity, infer likely impacted disciplines while marking inference, and draft traceable tests.
- A fixed form or keyword filter cannot reliably perform these semantic relationships end-to-end.
        """
    )

with tab_input:
    uploaded = st.file_uploader(
        "Upload engineering documents",
        type=["pdf", "docx", "txt", "md", "csv"],
        accept_multiple_files=True,
    )

    pasted = st.text_area(
        "Or paste a requirement / email / change request",
        height=220,
        placeholder="Paste customer requirement, ECN, meeting notes, specification excerpt…",
    )

    context = st.text_area(
        "Optional project context",
        height=100,
        placeholder="Example: Embedded controller with firmware, CAN, sensors, display, relay outputs…",
    )

    if mode == "Demo":
        st.caption("Demo mode uses the bundled sample change request and pre-generated analysis for a guaranteed presentation flow.")

    run = st.button("Analyze engineering change", type="primary", use_container_width=True)

if run:
    combined = []
    source_names = []

    if uploaded:
        for f in uploaded:
            try:
                combined.append(f"\n### SOURCE: {f.name}\n{extract_text(f)}")
                source_names.append(f.name)
            except Exception as exc:
                st.error(f"Could not read {f.name}: {exc}")

    if pasted.strip():
        combined.append(f"\n### SOURCE: PASTED INPUT\n{pasted.strip()}")
        source_names.append("Pasted input")

    if mode == "Demo" and not combined:
        sample_path = Path(__file__).parent / "sample_data" / "sli_change_request.txt"
        combined.append(sample_path.read_text(encoding="utf-8"))
        source_names.append("Bundled SLI change request")

    document_text = "\n".join(combined).strip()

    if not document_text:
        st.error("Upload a document or paste requirement text first.")
        st.stop()

    if len(document_text) > 90000:
        st.warning("Input is long; only the first 90,000 characters are analyzed in this MVP.")
        document_text = document_text[:90000]

    with st.spinner("Building requirement-to-test traceability…"):
        start = time.perf_counter()
        try:
            if mode == "Demo":
                result = load_demo_analysis()
                # Small deterministic delay makes timing visible without pretending it was a live API call.
                time.sleep(0.25)
            else:
                if not api_key:
                    st.error("Enter a Gemini API key for Live AI mode.")
                    st.stop()
                result = analyze_with_gemini(api_key, model, document_text, context)
            elapsed = time.perf_counter() - start
        except Exception as exc:
            st.exception(exc)
            st.stop()

    st.success(f"Analysis complete — {len(source_names)} source(s): {', '.join(source_names)}")
    reduction = show_metric_row(int(manual_minutes), elapsed)

    st.subheader("Executive summary")
    st.write(result.get("executive_summary", ""))
    st.markdown(f"**Detected change:** {result.get('detected_change', '')}")

    tabs = st.tabs(
        ["Requirements", "Impact", "Risks", "Test Cases", "Traceability", "Actions", "Clarifications", "Raw JSON"]
    )

    with tabs[0]:
        df = to_df(result.get("requirements", []))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[1]:
        df = to_df(result.get("impacts", []))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[2]:
        df = to_df(result.get("risks", []))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[3]:
        tests = result.get("test_cases", [])
        for tc in tests:
            with st.expander(f"{tc.get('id', '')} — {tc.get('title', '')}"):
                st.markdown(f"**Requirement(s):** {', '.join(tc.get('requirement_ids', []))}")
                st.markdown(f"**Type / Priority:** {tc.get('type', '')} / {tc.get('priority', '')}")
                st.markdown(f"**Preconditions:** {tc.get('preconditions', '')}")
                steps = tc.get("steps", [])
                if steps:
                    st.markdown("**Steps**")
                    for idx, step in enumerate(steps, start=1):
                        st.write(f"{idx}. {step}")
                st.markdown(f"**Expected:** {tc.get('expected_result', '')}")

    with tabs[4]:
        df = to_df(result.get("traceability", []))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[5]:
        df = to_df(result.get("action_items", []))
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tabs[6]:
        qs = result.get("clarification_questions", [])
        if qs:
            for q in qs:
                st.write(f"• {q}")
        else:
            st.write("No clarification questions generated.")

    with tabs[7]:
        st.json(result)

    report = make_markdown_report(
        result=result,
        sources=source_names,
        manual_minutes=int(manual_minutes),
        ai_seconds=elapsed,
        reduction=reduction,
    )

    c1, c2 = st.columns(2)
    with c1:
        st.download_button(
            "Download Markdown report",
            data=report,
            file_name="traceai_engineering_analysis.md",
            mime="text/markdown",
            use_container_width=True,
        )
    with c2:
        st.download_button(
            "Download JSON",
            data=json.dumps(result, indent=2),
            file_name="traceai_analysis.json",
            mime="application/json",
            use_container_width=True,
        )
