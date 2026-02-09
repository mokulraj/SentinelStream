from pydantic import BaseModel

class FraudRuleCreate(BaseModel):
    name: str
    rule_type: str
    threshold: float = None
    enabled: bool = True

class FraudRuleOut(FraudRuleCreate):
    id: int
