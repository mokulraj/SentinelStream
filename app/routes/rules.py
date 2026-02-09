from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.session import get_db
from app.db.models.fraud_rule import FraudRule
from app.schemas.rules import FraudRuleCreate, FraudRuleOut

router = APIRouter(prefix="/rules", tags=["Rules"])

@router.post("/", response_model=FraudRuleOut)
async def create_rule(rule: FraudRuleCreate, db: AsyncSession = Depends(get_db)):
    new_rule = FraudRule(**rule.dict())
    db.add(new_rule)
    await db.commit()
    await db.refresh(new_rule)
    return new_rule

@router.get("/", response_model=List[FraudRuleOut])
async def list_rules(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FraudRule))
    rules = result.scalars().all()
    return rules
