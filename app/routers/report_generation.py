from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum
from app.routers.resume_management import ParsedResume, upload_resume
from numerology_calculator import NumerologyCalculator
import aisuite as ai
from dotenv import load_dotenv
import os
import json

# Load environment variables
load_dotenv()

router = APIRouter(
    prefix="/report",
    tags=["report"],
    responses={404: {"description": "Not found"}}
)

# Initialize AI Suite client
client = ai.Client()

class CareerGoal(str, Enum):
    NEW_JOB = "Looking for a new job"
    CAREER_CHANGE = "Complete career change"
    ROLE_TRANSITION = "Transition to a new role"

class UserDetails(BaseModel):
    name: str
    email: str
    date_of_birth: str  # Format: DD/MM/YYYY
    city: str
    career_goal: CareerGoal

class SuitableRole(BaseModel):
    title: str
    explanation: str

class NumerologyReport(BaseModel):
    life_path_number: int
    life_path_explanation: str
    life_path_strengths: List[str]
    life_path_challenges: List[str]
    personality_number: int
    personality_explanation: str
    personality_traits: List[str]

class CareerReport(BaseModel):
    user_details: UserDetails
    numerology_report: NumerologyReport
    suitable_roles: List[SuitableRole]
    career_summary: str

def get_numerology_insights(life_path: int) -> dict:
    """Get strengths and challenges based on life path number"""
    strengths_map = {
        1: ["Leadership", "Innovation", "Independence", "Creativity"],
        2: ["Diplomacy", "Cooperation", "Sensitivity", "Balance"],
        3: ["Communication", "Creativity", "Self-expression", "Optimism"],
        4: ["Organization", "Stability", "Dedication", "Detail-oriented"],
        5: ["Adaptability", "Freedom", "Change", "Adventure"],
        6: ["Responsibility", "Harmony", "Nurturing", "Balance"],
        7: ["Analysis", "Wisdom", "Technical skills", "Research"],
        8: ["Authority", "Material success", "Power", "Achievement"],
        9: ["Humanitarianism", "Compassion", "Artistic", "Healing"],
        11: ["Inspiration", "Spiritual insight", "Innovation", "Idealism"],
        22: ["Master building", "Practical idealism", "Leadership", "Manifestation"]
    }
    
    challenges_map = {
        1: ["Ego", "Stubbornness", "Dominance", "Aggression"],
        2: ["Oversensitivity", "Timidity", "Indecision", "Dependence"],
        3: ["Scattered energy", "Superficiality", "Critical", "Impatience"],
        4: ["Rigidity", "Stubbornness", "Limited vision", "Work addiction"],
        5: ["Restlessness", "Inconsistency", "Excess", "Irresponsibility"],
        6: ["Anxiety", "Perfectionism", "Interference", "Self-sacrifice"],
        7: ["Isolation", "Skepticism", "Pessimism", "Secretiveness"],
        8: ["Materialism", "Control", "Intolerance", "Ruthlessness"],
        9: ["Martyrdom", "Resentment", "Detachment", "Scattered energy"],
        11: ["Anxiety", "Perfectionism", "Nervous tension", "Impracticality"],
        22: ["Overwhelm", "Impracticality", "Nervous tension", "Unfocused power"]
    }
    
    return {
        "strengths": strengths_map.get(life_path, strengths_map[life_path % 9 or 9]),
        "challenges": challenges_map.get(life_path, challenges_map[life_path % 9 or 9])
    }

def generate_career_summary(parsed_resume: ParsedResume) -> str:
    # Use the raw text from parsed resume for analysis
    prompt = f"""
    Analyze the following career information and provide a personalized, conversational career analysis in JSON format.
    Make it engaging and directly address the person by their name. Focus on their achievements, growth, and potential.
    
    Personal Info:
    {parsed_resume.personal_info}
    
    Work Experience:
    {parsed_resume.work_experience}
    
    Education:
    {parsed_resume.education}
    
    Skills:
    {parsed_resume.skills}
    
    Raw Text:
    {parsed_resume.raw_text}
    
    Please provide your analysis in the following JSON structure:
    {{
        "personal_greeting": "A warm, personalized greeting using their name",
        "career_journey": {{
            "overview": "A personalized narrative of their career journey",
            "key_achievements": [
                {{
                    "company": "company name",
                    "achievement": "specific achievement with impact",
                    "skills_demonstrated": ["skill1", "skill2"]
                }}
            ]
        }},
        "expertise_highlight": {{
            "primary_strengths": ["strength1", "strength2"],
            "notable_projects": [
                {{
                    "description": "project description",
                    "impact": "project impact"
                }}
            ]
        }},
        "growth_areas": {{
            "observed_progression": "analysis of their career progression",
            "potential_directions": ["direction1", "direction2"]
        }}
    }}
    
    Make sure to:
    1. Use their name naturally in the greeting and throughout the analysis
    2. Reference specific companies and achievements from their experience
    3. Highlight concrete examples of their impact
    4. Maintain a professional but warm tone
    5. Be specific about their unique contributions and skills
    """
    
    response = client.chat.completions.create(
        model="openai:gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a career analysis expert who provides warm, personalized career insights while maintaining professionalism."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    
    try:
        # Extract JSON from the response text
        response_text = response.choices[0].message.content
        # Find the JSON part in the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        analysis = json.loads(json_str)
        
        # Create a more personalized, narrative summary
        summary = f"""
{analysis['personal_greeting']}

Career Journey:
{analysis['career_journey']['overview']}

Key Achievements:
{chr(10).join(f"• At {achievement['company']}: {achievement['achievement']}" for achievement in analysis['career_journey']['key_achievements'])}

Your Core Strengths:
{chr(10).join(f"• {strength}" for strength in analysis['expertise_highlight']['primary_strengths'])}

Notable Projects and Impact:
{chr(10).join(f"• {project['description']} - {project['impact']}" for project in analysis['expertise_highlight']['notable_projects'])}

Professional Growth:
{analysis['growth_areas']['observed_progression']}

Potential Growth Directions:
{chr(10).join(f"• {direction}" for direction in analysis['growth_areas']['potential_directions'])}
"""
        return summary.strip()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing career information: {str(e)}")

def get_suitable_roles(life_path: int, personality: int, career_goal: CareerGoal) -> List[SuitableRole]:
    # Get numerology insights
    life_path_insights = get_numerology_insights(life_path)
    
    prompt = f"""
    Based on the following information, recommend suitable career roles. 
    Provide your response in JSON format with exactly 5 role recommendations.
    
    Life Path Number: {life_path}
    - Strengths: {', '.join(life_path_insights['strengths'])}
    - Challenges: {', '.join(life_path_insights['challenges'])}
    
    Personality Number: {personality}
    Explanation: {NumerologyCalculator.explain_number(personality)}
    
    Career Goal: {career_goal.value}
    
    Please provide your recommendations in the following JSON structure:
    {{
        "roles": [
            {{
                "title": "role title",
                "explanation": "detailed explanation",
                "alignment_score": number between 1 and 10
            }}
        ]
    }}
    """
    
    response = client.chat.completions.create(
        model="openai:gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a career counselor expert in numerology. Provide role recommendations in the specified JSON format."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    
    try:
        # Extract JSON from the response text
        response_text = response.choices[0].message.content
        # Find the JSON part in the response
        json_start = response_text.find('{')
        json_end = response_text.rfind('}') + 1
        json_str = response_text[json_start:json_end]
        recommendations = json.loads(json_str)
        
        sorted_roles = sorted(recommendations['roles'], key=lambda x: x['alignment_score'], reverse=True)[:5]
        return [
            SuitableRole(
                title=role['title'],
                explanation=f"{role['explanation']} (Alignment: {role['alignment_score']}/10)"
            )
            for role in sorted_roles
        ]
    except Exception:
        # Use numerology calculator's explanations for fallback recommendations
        return [
            SuitableRole(
                title="Career Advisor",
                explanation=NumerologyCalculator.explain_number(life_path)
            ),
            SuitableRole(
                title="Professional Consultant",
                explanation=NumerologyCalculator.explain_number(personality)
            )
        ]

@router.post("/generate-from-resume", response_model=CareerReport)
async def generate_report_from_resume(
    user_details: str = Form(...),
    resume_file: UploadFile = File(...)
):
    try:
        # Parse user details from JSON string using Pydantic V2 syntax
        user_details_obj = UserDetails.model_validate_json(user_details)
        
        # First, process the resume using the existing resume management functionality
        parsed_resume = await upload_resume(resume_file)
        
        # Calculate numerology numbers using the calculator
        life_path = NumerologyCalculator.calculate_life_path_number(user_details_obj.date_of_birth)
        personality = NumerologyCalculator.calculate_personality_number(user_details_obj.name)
        
        # Get numerology insights
        numerology_insights = get_numerology_insights(life_path)
        
        # Generate numerology report
        numerology_report = NumerologyReport(
            life_path_number=life_path,
            life_path_explanation=NumerologyCalculator.explain_number(life_path),
            life_path_strengths=numerology_insights["strengths"],
            life_path_challenges=numerology_insights["challenges"],
            personality_number=personality,
            personality_explanation=NumerologyCalculator.explain_number(personality),
            personality_traits=NumerologyCalculator.explain_number(personality).split(", ")
        )
        
        # Get suitable roles
        suitable_roles = get_suitable_roles(life_path, personality, user_details_obj.career_goal)
        
        # Generate career summary using parsed resume
        career_summary = generate_career_summary(parsed_resume)
        
        # Create final report
        report = CareerReport(
            user_details=user_details_obj,
            numerology_report=numerology_report,
            suitable_roles=suitable_roles,
            career_summary=career_summary
        )
        
        return report
        
    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Invalid user details format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}") 