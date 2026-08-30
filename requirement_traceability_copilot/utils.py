import json
from pathlib import Path


def load_demo_analysis():
    path = Path(__file__).parent / "sample_output" / "sli_demo_analysis.json"
    return json.loads(path.read_text(encoding="utf-8"))


def make_markdown_report(result, sources, manual_minutes, ai_seconds, reduction):
    lines = []
    lines.append("# TraceAI Engineering Analysis")
    lines.append("")
    lines.append(f"**Sources:** {', '.join(sources)}")
    lines.append(f"**Manual baseline:** {manual_minutes} minutes")
    lines.append(f"**AI analysis runtime:** {ai_seconds:.1f} seconds")
    lines.append(f"**Estimated effort reduction:** {reduction:.1f}%")
    lines.append("")
    lines.append("> Draft decision support only. Human engineering, safety, verification, and compliance review remain required.")
    lines.append("")
    lines.append("## Executive Summary")
    lines.append(result.get("executive_summary", ""))
    lines.append("")
    lines.append("## Detected Change")
    lines.append(result.get("detected_change", ""))
    lines.append("")

    sections = [
        ("Requirements", "requirements"),
        ("Impact Analysis", "impacts"),
        ("Risks", "risks"),
        ("Test Cases", "test_cases"),
        ("Traceability", "traceability"),
        ("Action Items", "action_items"),
    ]
    for title, key in sections:
        lines.append(f"## {title}")
        for item in result.get(key, []):
            lines.append(f"- {json.dumps(item, ensure_ascii=False)}")
        lines.append("")

    lines.append("## Clarification Questions")
    for item in result.get("clarification_questions", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("## Confidence Notes")
    for item in result.get("confidence_notes", []):
        lines.append(f"- {item}")

    return "\n".join(lines)
