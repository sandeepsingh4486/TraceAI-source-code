# Architecture

```mermaid
flowchart LR
    A[PDF / DOCX / TXT / Email / ECN] --> B[Local text extraction]
    B --> C[Prompt + project context]
    C --> D[LLM semantic analysis]
    D --> E[Structured Pydantic schema]
    E --> F[Requirement register]
    E --> G[Impact analysis]
    E --> H[Risk register]
    E --> I[Test cases]
    E --> J[Traceability matrix]
    E --> K[Actions + clarifications]
    F --> L[Human engineering review]
    G --> L
    H --> L
    I --> L
    J --> L
    K --> L
```

## Key design decisions

1. **Local extraction first**: the MVP extracts text from common documents before sending the text to the LLM.
2. **Structured output**: the model is constrained to a typed schema rather than returning an unstructured essay.
3. **Explicit vs inferred**: impact rows must state whether they are directly specified or inferred.
4. **No invented standards**: the prompt forbids adding standards/numeric requirements absent from source documents.
5. **Human-in-the-loop**: output is positioned as decision support and draft verification material.
6. **Demo reliability**: a bundled analysis lets you present the complete UX even if internet/API access fails.
