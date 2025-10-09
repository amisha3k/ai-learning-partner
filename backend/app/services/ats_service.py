import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()  # Ensure GROQ_API_KEY is loaded

groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.3-70b-versatile")


prompt_template = """
You are a technical recruiter with lots of experience in computer science and engineering.
Analyze the resume and compare it with the Job Description (JD). Follow these instructions:

1) Percentage match - weightage:50%
2) Detect all sections (skills, experience, projects, etc.)
3) Missing keywords - weightage:20%
4) Spelling and grammatical mistakes - weightage:10%
5) Highly repetitive words - weightage:10%
6) Section-wise analysis (strong vs weak) - weightage:10%
7) Compute overall score

Return output **strictly in JSON format**, like this:

{{
  "percentage_match": 0,
  "missing_keywords": [],
  "overall_score": 0,
  "sections": {{
    "skills": {{"strength": "", "reason": ""}},
    "experience": {{"strength": "", "reason": ""}},
    "projects": {{"strength": "", "reason": ""}},
    "education": {{"strength": "", "reason": ""}},
    "profile": {{"strength": "", "reason": ""}}
  }},
  "grammar_issues": [],
  "repetitive_words": [],
  "improvement_scope": ""
}}

Resume:
{text}

Job Description:
{JD}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text", "JD"])
chain = prompt | llm | StrOutputParser()


def analyze_resume(resume_text: str, job_description: str) -> dict:
    fallback = {
        "percentage_match": 0,
        "overall_score": 0,
        "missing_keywords": [],
        "sections": {
            "skills": {"strength": "", "reason": ""},
            "experience": {"strength": "", "reason": ""},
            "projects": {"strength": "", "reason": ""},
            "education": {"strength": "", "reason": ""},
            "profile": {"strength": "", "reason": ""}
        },
        "grammar_issues": [],
        "repetitive_words": [],
        "improvement_scope": "Error analyzing resume."
    }

    try:
        response = chain.invoke({"text": resume_text, "JD": job_description})
        print("LLM raw response:\n", response)  # Debug output

        # Extract JSON from LLM response
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            data = json.loads(match.group())
        else:
            print("LLM response did not contain valid JSON. Using fallback.")
            data = fallback
    except Exception as e:
        print("Error in analyze_resume:", e)
        data = fallback

    return data
