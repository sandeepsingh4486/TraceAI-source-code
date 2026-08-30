# Judge Q&A

## Why can't this be done with normal automation?
Normal automation works when the fields and rules are already known. Here, the input is arbitrary natural language. The system must infer semantic relationships, split compound requirements, distinguish explicit facts from inferred engineering impact, identify omissions, and generate test coverage connected to the requirement intent.

## Is the AI making safety decisions?
No. It generates decision-support drafts only. Final safety, design, verification, and compliance decisions remain with qualified engineers.

## How do you prevent hallucination?
The system prompt forbids adding standards, limits, approvals, or measurements absent from source documents. It marks inferred impact separately and turns missing information into clarification questions. Structured output also makes review easier.

## What is the measurable value?
Measure the manual first-pass process for one representative change package, then compare it with the app runtime plus human review time. The hackathon demo uses a 180-minute manual baseline as an editable value.

## Why is traceability important?
A summary can sound useful but is difficult to act on. Traceability connects each source-derived requirement to impacts, risks, and tests so reviewers can see coverage and gaps.

## Who would pay for this?
Engineering organizations with frequent requirement changes and expensive technical review cycles: embedded, industrial, automotive, medical devices, IoT, aerospace suppliers, and complex product-development teams.

## What would you build next?
Version-to-version requirement delta analysis and direct integration with Jira/ALM systems so approved draft items become real project artifacts.
