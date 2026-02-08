import json

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

from ocr import *
from model import get_model

model = get_model()
resume_text = clean_text(extract_text("resume.pdf"))
json_schema = """
{
  "name": null,
  "email": null,
  "phone": null,
  "location": null,
  "summary": null,
  "total_experience_years": null,
  "skills": [],
  "current_role": null,
  "current_company": null,
  "education": [
    {
      "degree": null,
      "institution": null,
      "year": null
    }
  ],
  "experience": [
    {
      "job_title": null,
      "company": null,
      "start_date": null,
      "end_date": null,
      "description": null
    }
  ],
  "certifications": [],
  "projects": [],
  "languages": []
}
"""
prompt = PromptTemplate.from_template(
    """
        Role: 
            You are an expert resume parser and HR data extraction system. 
            You specialize in extracting structured information from unstructured resume text.
            You never invent data and only extract what is explicitly present.

        Goal:
            Your goal is to convert the provided resume text into a clean, valid JSON object
            containing predefined resume fields that can be directly consumed by an ATS or backend system.
            If a field is not found, return null.
            If multiple values exist, return them as arrays.
            Do not include explanations or extra text.

        Task:
            1. Analyze the resume text provided below.
            2. Identify and extract relevant resume information.
            3. Output a single valid JSON object matching the exact schema below.
            4. Use only information explicitly present in the text.
            5. Do not guess, infer, or fabricate any data.
            6. If a field is missing, set its value to null.
            7. If a field has multiple values, return them as an array.
            8. Do not include any text outside the JSON.
            
        json Schema: {json_schema}
            
        resume text : {resume_text}

    """
)

chain = prompt | model | JsonOutputParser()

response = chain.invoke({"resume_text": resume_text, "json_schema": json_schema})

print(json.dumps(response, indent=2))
