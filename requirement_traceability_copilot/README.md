# TraceAI — AI Requirement-to-Test Traceability Copilot

TraceAI converts unstructured engineering change information into a structured draft:

**Documents / email / ECN → Requirements → Impact → Risks → Test Cases → Traceability → Action Items**

It is designed as a hackathon MVP for engineering/project teams who currently spend hours manually reading change requests and producing review artifacts.

## Why this is a strong AI use case

A deterministic form can store known fields. It cannot reliably understand arbitrary engineering language, detect relationships across paragraphs, distinguish explicit requirements from inferred impact, identify ambiguity, and generate traceable verification ideas from many differently worded inputs.

TraceAI uses an LLM for semantic extraction and cross-document reasoning, while forcing structured output and preserving human review.

## Features

- Upload PDF, DOCX, TXT, MD, or CSV
- Paste customer email / requirement / meeting notes
- Atomic requirement extraction
- Acceptance criteria + ambiguity detection
- Cross-functional impact analysis
- RAID-style risk generation
- Traceable test-case drafting
- Requirement-to-risk-to-test matrix
- Clarification questions
- Action items by owner role
- Download Markdown and JSON reports
- Live AI mode
- Demo mode for reliable judging

## Run locally

1. Install Python 3.10+.
2. In this folder:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Optional: set your Gemini key.

Windows CMD:

```bash
set GEMINI_API_KEY=YOUR_KEY
```

PowerShell:

```powershell
$env:GEMINI_API_KEY="YOUR_KEY"
```

macOS/Linux:

```bash
export GEMINI_API_KEY="YOUR_KEY"
```

5. Run:

```bash
streamlit run app.py
```

## Live demo sequence

1. Open **Demo** mode first and click **Analyze engineering change** without uploading anything.
2. Show the requirements table.
3. Jump to **Traceability** and show that each requirement links to tests/risks.
4. Show **Clarifications** — this proves the system does not blindly invent missing data.
5. Show the time-saving metric.
6. Switch to **Live AI**, paste a short unseen change request, and run it with your API key.

## Safety / quality positioning

TraceAI does **not** claim engineering approval, regulatory compliance, verification completion, or safety certification. It generates a reviewable draft and explicitly calls out ambiguity. Qualified engineers remain responsible for decisions.

## Suggested product name

**TraceAI**
Tagline: **From engineering change to test traceability in minutes.**
