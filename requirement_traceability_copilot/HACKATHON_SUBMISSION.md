# Hackathon Submission — TraceAI

## Project title
**TraceAI — AI Requirement-to-Test Traceability Copilot**

## One-line description
TraceAI converts unstructured engineering change documents into a structured, review-ready draft of requirements, cross-functional impacts, risks, test cases, traceability, actions, and clarification questions.

## The problem
Engineering teams receive changes through customer emails, PDFs, ECNs, meeting notes, and specifications. Before implementation can even begin, experienced engineers and project managers often spend hours manually interpreting the text, splitting it into requirements, identifying affected components, finding missing information, writing risk items, and preparing verification coverage.

The work is repetitive, but it is not a simple rules problem because the input is natural language and the relationships are contextual.

## Who has this problem
- Embedded-system teams
- Product engineering teams
- Technical project/program managers
- Systems engineers
- Verification and validation teams
- Industrial/automotive/medical/IoT engineering organizations

## Solution
A user uploads or pastes engineering change information. TraceAI uses an LLM to semantically analyze the source and generates:

1. Atomic requirements
2. Acceptance criteria
3. Ambiguity flags
4. Cross-functional impact analysis
5. Risk register
6. Test cases
7. Requirement-to-risk-to-test traceability
8. Action items
9. Clarification questions

## Why AI is essential
This is not a fixed form or keyword classifier. The same requirement can be written in many ways and may imply consequences across multiple engineering disciplines. AI is used to understand context, decompose compound statements, identify semantic relationships, distinguish explicit statements from inferred impact, and draft traceable verification ideas.

## Hours-to-seconds/minutes test
A medium engineering change can require roughly 2–5 hours for an experienced person to produce a first-pass requirement/impact/test package. TraceAI generates the first draft in minutes or seconds, depending on document size and model latency. Human engineering review is retained.

## What makes it trustworthy
- Structured schema instead of free-form prose
- Explicit vs inferred impact labeling
- Missing information becomes clarification questions
- No invented standards or numeric thresholds
- Every drafted test traces back to a requirement
- Human review disclaimer for safety/compliance decisions

## MVP
The working Streamlit app accepts PDF, DOCX, TXT, MD, CSV, or pasted text; runs live Gemini analysis; displays engineering tables; and exports Markdown/JSON. A demo mode ensures the complete presentation can be shown even if network access fails.

## Future roadmap
- Jira/Azure DevOps/DOORS/Polarion integration
- Requirement version comparison and change-delta view
- Organization-specific templates and terminology
- Review/approval workflow
- Test execution linkage
- Historical project knowledge retrieval
- Role-based collaboration
- Metrics dashboard for requirement quality and coverage

## Impact
TraceAI does not replace engineers. It compresses the expensive clerical first pass so engineers can focus on architecture, trade-offs, safety, verification, and decisions.
