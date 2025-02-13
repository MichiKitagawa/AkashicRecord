from sqlalchemy.ext.asyncio import AsyncSession
from app.models.diagnosis import Diagnosis

async def create_diagnosis(db: AsyncSession, name: str, birth_date: str, result: str):
    db_diagnosis = Diagnosis(
        name=name,
        birth_date=birth_date,
        result=result
    )
    db.add(db_diagnosis)
    await db.commit()
    await db.refresh(db_diagnosis)
    return db_diagnosis 