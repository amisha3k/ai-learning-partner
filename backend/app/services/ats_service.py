import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

groq_api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")

prompt_template = """
you are a technical recruiter with lots of experience in Data Science/AI.
Review the following resume and share precise summary. Compare it with the given job description(JD) and analyze the following:

1) Percentage match - weightage:50%  
2) Detect all the sections in the resume (example : skills, experience, projects, etc..)  
3) Missing Key words - weightage:20%  
4) Spelling and grammatical mistakes - weightage:10%  
5) Highly repetitive words (only if they are not key words and just a common word which does not add any value) - weightage:10%  
6) Section wise analysis (strong sections vs weak sections) - weightage:10%  
7) Compute overall score for the resume based on all the above criteria with respective weightage  
8) Interpret the overall score in detail without revealing the actual criteria  
9) Provide scope of improvement with respect to all the above points. 

be very accurate with requirements.

resume: {text}
JD: {JD}

percentage match(%):
missing key words:
overall score:
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text", "JD"])
chain = prompt | llm | StrOutputParser()

def analyze_resume(resume_text: str, job_description: str) -> float:
    response = chain.invoke({"text": resume_text, "JD": job_description})
    # For now, return dummy score
    return 85.0
