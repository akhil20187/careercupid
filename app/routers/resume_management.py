from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict
import PyPDF2
import docx
import io
import os
import aisuite as ai
from dotenv import load_dotenv
from langchain_community.document_loaders import PyMuPDFLoader, UnstructuredPDFLoader, PDFPlumberLoader
from tempfile import NamedTemporaryFile
import json

# Load environment variables
load_dotenv()

router = APIRouter(
    prefix="/resume",
    tags=["resume"],
    responses={404: {"description": "Not found"}},
)

class WorkExperience(BaseModel):
    company: str
    position: str
    dates: str
    responsibilities: List[str]

class Education(BaseModel):
    degree: str
    institution: str
    graduation_date: str

class PersonalInfo(BaseModel):
    name: str
    email: str
    phone: str
    location: str
    date_of_birth: str | None = None  # Making it optional since not all resumes include DOB

class ParsedResume(BaseModel):
    personal_info: PersonalInfo
    work_experience: List[WorkExperience]
    education: List[Education]
    skills: List[str]
    raw_text: str

def extract_text_from_pdf(pdf_file: bytes) -> str:
    """
    Extract text from PDF using multiple LangChain loaders for better accuracy.
    Falls back to simpler loaders if more complex ones fail.
    """
    # Create a temporary file to save the PDF content
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(pdf_file)
        temp_path = temp_file.name

    try:
        # Try PyMuPDF first (best for maintaining layout)
        loader = PyMuPDFLoader(temp_path)
        documents = loader.load()
        text = "\n".join([doc.page_content for doc in documents])
    except Exception as e:
        try:
            # Fall back to Unstructured (good for complex PDFs)
            loader = UnstructuredPDFLoader(temp_path)
            documents = loader.load()
            text = "\n".join([doc.page_content for doc in documents])
        except Exception as e:
            try:
                # Last resort: PDFPlumber (reliable but basic)
                loader = PDFPlumberLoader(temp_path)
                documents = loader.load()
                text = "\n".join([doc.page_content for doc in documents])
            except Exception as e:
                # If all else fails, use PyPDF2
                with open(temp_path, "rb") as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text()

    # Clean up the temporary file
    os.unlink(temp_path)
    
    # Basic text cleaning
    text = text.replace('\x00', '')  # Remove null bytes
    text = ' '.join(text.split())  # Normalize whitespace
    return text

def extract_text_from_docx(docx_file: bytes) -> str:
    doc = docx.Document(io.BytesIO(docx_file))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def parse_resume_with_aisuite(text: str) -> ParsedResume:
    # Initialize AISuite client
    client = ai.Client()
    
    # Define the function schema for structured output
    function_schema = {
        "name": "parse_resume",
        "description": "Parse resume text into structured information",
        "parameters": {
            "type": "object",
            "properties": {
                "personal_info": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "email": {"type": "string"},
                        "phone": {"type": "string"},
                        "location": {"type": "string"},
                        "date_of_birth": {
                            "type": "string",
                            "description": "Date of birth in YYYY-MM-DD format if available"
                        }
                    },
                    "required": ["name", "email", "phone", "location"]
                },
                "work_experience": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company": {"type": "string"},
                            "position": {"type": "string"},
                            "dates": {"type": "string"},
                            "responsibilities": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["company", "position", "dates", "responsibilities"]
                    }
                },
                "education": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "degree": {"type": "string"},
                            "institution": {"type": "string"},
                            "graduation_date": {"type": "string"}
                        },
                        "required": ["degree", "institution", "graduation_date"]
                    }
                },
                "skills": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["personal_info", "work_experience", "education", "skills"]
        }
    }

    # Create the completion request with function calling
    response = client.chat.completions.create(
        model="openai:gpt-4o-mini",  # Using the correct model name
        messages=[
            {
                "role": "system",
                "content": """You are a resume parsing expert. Extract structured information from the provided resume text.
                Pay special attention to personal information including date of birth if available.
                Format the date of birth as YYYY-MM-DD if found."""
            },
            {
                "role": "user",
                "content": f"Parse this resume:\n\n{text}"
            }
        ],
        functions=[function_schema],
        function_call={"name": "parse_resume"},
        temperature=0.3
    )
    
    try:
        # Get the function call response
        parsed_content = response.choices[0].message.function_call.arguments
        if isinstance(parsed_content, str):
            parsed_content = json.loads(parsed_content)
        
        # Create ParsedResume object
        parsed_resume = ParsedResume(
            personal_info=PersonalInfo(**parsed_content["personal_info"]),
            work_experience=[WorkExperience(**exp) for exp in parsed_content["work_experience"]],
            education=[Education(**edu) for edu in parsed_content["education"]],
            skills=parsed_content["skills"],
            raw_text=text
        )
        return parsed_resume
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing resume: {str(e)}")

@router.post("/upload", response_model=ParsedResume)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    content = await file.read()
    
    # Extract text based on file type
    if file.filename.endswith('.pdf'):
        text = extract_text_from_pdf(content)
    else:
        text = extract_text_from_docx(content)
    
    # Parse resume using AIStudio
    parsed_resume = parse_resume_with_aisuite(text)
    
    return parsed_resume 