# AI Learning Partner

## Features

### 1. Mock Interview Bot
- Conducts mock interviews for **Data Science, AI, Analytics, and Generative AI roles**.  
- Analyzes uploaded resumes to tailor **scenario-based, real-world questions**.  
- Validates user answers using the **STAR methodology** and provides **detailed feedback**.  
- Generates a **final report** with questions, answers, and overall performance score.  

### 2. AI Tutor
- Acts as an **AI-powered tutor** for AI/Data Science topics.  
- Provides **context-aware, real-world explanations** to user queries.  
- Maintains conversation history for **coherent and personalized learning**.  
- Restricts answers to relevant topics, keeping learning focused.

### 3. ATS Resume Analyzer
- Compares **resume content** against a **job description** for compatibility.  
- Highlights **missing keywords** and calculates **percentage match**.  
- Detects **spelling and grammatical mistakes**.  
- Identifies **highly repetitive words** that do not add value.  
- Performs **section-wise analysis** to determine strong and weak areas.  
- Computes an **overall score** based on all evaluation criteria.  
- Provides **scope of improvement** suggestions to enhance resume quality.  

## 🚀 Future Improvements

Here are the upcoming enhancements planned for **AI Learning Partner**:

- [ ] **A) Add PDF parsing**  
  Integrate a library like `pdfplumber` to support direct PDF uploads for resumes, job descriptions, and course content.

- [ ] **B) Upgrade Tutor with FAISS + Sentence-Transformers**  
  Replace the current TF-IDF retrieval with a semantic search pipeline using FAISS and embeddings (e.g., `all-MiniLM-L6-v2` from Sentence Transformers) for more accurate knowledge retrieval.

- [ ] **C) Improve ATS with spaCy skill extraction & scoring rubric**  
  Use `spaCy` or specialized libraries to extract entities (skills, tools, experience years) from resumes and JDs, then create a structured scoring rubric for better ATS-style analysis.

- [ ] **D) Dockerize the app**  
  Add a `Dockerfile` and `requirements.txt` to containerize the Streamlit app, making it portable and ready for deployment to platforms like Hugging Face Spaces, Render, or AWS.

---
