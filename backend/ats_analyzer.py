import streamlit as st 
import PyPDF2 as pdf
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
groq_api_key=os.getenv("GROQ_API_KEY")

#initialize llm
llm= ChatGroq(groq_api_key=groq_api_key,model_name="gemma2-9b-it")

prompt_template="""
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

def ats():
    st.title('ATS Resume Analyzer')

    JD=st.text_area(label='Paste the job description here')

    file_up=st.file_uploader(label='upload your resume (PDF only)', type='pdf')

    if file_up and JD:
        with st.spinner('Processing your resume...'):
            reader=pdf.PdfReader(file_up)
            text=""
            for page in reader.pages:
                text+=page.extract_text() or ""

            #build chain
            prompt=PromptTemplate(template=prompt_template,input_variables=["text","JD"])
            output_parser=StrOutputParser()  #Ensures the AI output is returned as plain text (not JSON or structured format).
            chain = prompt | llm |output_parser

            #get response
            response=chain.invoke({'text':text,'JD':JD})

        st.subheader("ATS analysis result")
        st.write(response)    

# if __name__ == "__main__":
#      ats()







#prompt → formats the data properly
#llm → sends it to the AI model (like OpenAI GPT or Groq LLM)
#output_parser → cleans up the response
#This is like a pipeline: Input → Prompt → AI → Output.