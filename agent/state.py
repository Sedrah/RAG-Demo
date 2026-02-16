from typing import TypedDict, List, Dict, Optional


class PricingAgentState(TypedDict):

    user_query: str

    intent: Optional[str]

    retrieved_docs: Optional[List[str]]
    metadatas: Optional[List[Dict]]
    distances: Optional[List[float]]

    confidence_score: Optional[float]
    confidence_label: Optional[str]

    escalation_required: Optional[bool]

    final_answer: Optional[str]
