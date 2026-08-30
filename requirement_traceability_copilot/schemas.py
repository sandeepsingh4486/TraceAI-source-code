from typing import List
from pydantic import BaseModel, Field


class Requirement(BaseModel):
    id: str = Field(description="Unique requirement id such as REQ-001")
    requirement: str
    type: str = Field(description="Functional, non-functional, interface, safety, logging, performance, etc.")
    priority: str = Field(description="High, Medium, or Low")
    evidence: str = Field(description="Short source phrase or faithful paraphrase; do not invent")
    acceptance_criteria: str
    ambiguity: str = Field(description="None if clear; otherwise state what is unclear")


class ImpactItem(BaseModel):
    area: str = Field(description="Firmware, Hardware, System, UI, Test, Manufacturing, Cybersecurity, etc.")
    component: str
    impact: str
    rationale: str
    severity: str = Field(description="High, Medium, or Low")
    basis: str = Field(description="Explicit or Inferred")


class Risk(BaseModel):
    id: str
    risk: str
    cause: str
    impact: str
    probability: str = Field(description="High, Medium, or Low")
    severity: str = Field(description="High, Medium, or Low")
    mitigation: str
    linked_requirement_ids: List[str]


class TestCase(BaseModel):
    id: str
    requirement_ids: List[str]
    title: str
    type: str = Field(description="Functional, boundary, negative, fault-injection, interface, regression, performance, etc.")
    priority: str
    preconditions: str
    steps: List[str]
    expected_result: str


class TraceabilityRow(BaseModel):
    requirement_id: str
    impacted_areas: List[str]
    risk_ids: List[str]
    test_case_ids: List[str]


class ActionItem(BaseModel):
    action: str
    owner_role: str
    priority: str
    due_trigger: str


class AnalysisResult(BaseModel):
    executive_summary: str
    detected_change: str
    requirements: List[Requirement]
    impacts: List[ImpactItem]
    risks: List[Risk]
    test_cases: List[TestCase]
    traceability: List[TraceabilityRow]
    action_items: List[ActionItem]
    clarification_questions: List[str]
    confidence_notes: List[str]
