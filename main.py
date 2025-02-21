from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from numerology_calculator import NumerologyCalculator
from typing import Optional
from app.routers import resume_management

app = FastAPI(
    title="CareerCupid Numerology API",
    description="API for calculating various numerology numbers",
    version="1.0.0"
)

# Include resume management router
app.include_router(resume_management.router)

class NameRequest(BaseModel):
    full_name: str

class DateRequest(BaseModel):
    birth_date: str  # Format: DD/MM/YYYY

class FullNumerologyRequest(BaseModel):
    full_name: str
    birth_date: str  # Format: DD/MM/YYYY

class NumerologyResponse(BaseModel):
    number: int
    explanation: Optional[str] = None

class FullNumerologyResponse(BaseModel):
    life_path_number: NumerologyResponse
    expression_number: NumerologyResponse
    soul_urge_number: NumerologyResponse
    personality_number: NumerologyResponse
    birth_number: NumerologyResponse

@app.get("/")
async def root():
    return {"message": "Welcome to CareerCupid Numerology API"}

@app.post("/life-path", response_model=NumerologyResponse)
async def calculate_life_path(request: DateRequest):
    try:
        number = NumerologyCalculator.calculate_life_path_number(request.birth_date)
        return {
            "number": number,
            "explanation": NumerologyCalculator.explain_number(number)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/expression", response_model=NumerologyResponse)
async def calculate_expression(request: NameRequest):
    try:
        number = NumerologyCalculator.calculate_expression_number(request.full_name)
        return {
            "number": number,
            "explanation": NumerologyCalculator.explain_number(number)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/soul-urge", response_model=NumerologyResponse)
async def calculate_soul_urge(request: NameRequest):
    try:
        number = NumerologyCalculator.calculate_soul_urge_number(request.full_name)
        return {
            "number": number,
            "explanation": NumerologyCalculator.explain_number(number)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/personality", response_model=NumerologyResponse)
async def calculate_personality(request: NameRequest):
    try:
        number = NumerologyCalculator.calculate_personality_number(request.full_name)
        return {
            "number": number,
            "explanation": NumerologyCalculator.explain_number(number)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/birth-number", response_model=NumerologyResponse)
async def calculate_birth_number(request: DateRequest):
    try:
        number = NumerologyCalculator.calculate_birth_number(request.birth_date)
        return {
            "number": number,
            "explanation": NumerologyCalculator.explain_birth_number(number)
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/full-numerology", response_model=FullNumerologyResponse)
async def calculate_full_numerology(request: FullNumerologyRequest):
    try:
        life_path = NumerologyCalculator.calculate_life_path_number(request.birth_date)
        expression = NumerologyCalculator.calculate_expression_number(request.full_name)
        soul_urge = NumerologyCalculator.calculate_soul_urge_number(request.full_name)
        personality = NumerologyCalculator.calculate_personality_number(request.full_name)
        birth = NumerologyCalculator.calculate_birth_number(request.birth_date)

        return {
            "life_path_number": {
                "number": life_path,
                "explanation": NumerologyCalculator.explain_number(life_path)
            },
            "expression_number": {
                "number": expression,
                "explanation": NumerologyCalculator.explain_number(expression)
            },
            "soul_urge_number": {
                "number": soul_urge,
                "explanation": NumerologyCalculator.explain_number(soul_urge)
            },
            "personality_number": {
                "number": personality,
                "explanation": NumerologyCalculator.explain_number(personality)
            },
            "birth_number": {
                "number": birth,
                "explanation": NumerologyCalculator.explain_birth_number(birth)
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) 