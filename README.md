\# SmartAssist AI – Enterprise Helpdesk Support Platform



\## Overview



SmartAssist AI is an AI-powered Enterprise Helpdesk Support Platform designed to automate employee support and IT assistance using Retrieval-Augmented Generation (RAG), screenshot analysis, and automated ticket escalation.



The platform enables users to ask support-related questions, search enterprise knowledge base documents, upload screenshots of issues, and automatically generate support tickets when information is unavailable.



\---



\## Features



\* AI-Powered Support Chatbot

\* Retrieval-Augmented Generation (RAG)

\* PDF Knowledge Base Search

\* Screenshot Analysis

\* Automated Ticket Escalation

\* Confidence-Based Responses

\* Source Attribution

\* Analytics Dashboard



\---



\## Tech Stack



\### Frontend



\* Streamlit



\### Backend



\* Python



\### AI



\* Google Gemini API



\### Vector Database



\* FAISS



\### Embeddings



\* Sentence Transformers



\### Database



\* SQLite



\---



\## Project Architecture



User → Streamlit UI → FAISS Retrieval → Gemini AI → Response



Additional Modules:



\* Screenshot Analysis

\* Ticket Management

\* Analytics Dashboard



\---



\## Installation



1\. Clone the repository



```bash

git clone <repository-url>

```



2\. Install dependencies



```bash

pip install -r requirements.txt

```



3\. Create a .env file



```env

GEMINI\_API\_KEY=YOUR\_API\_KEY\_HERE

```



4\. Run the application



```bash

streamlit run app.py

```



\---



\## Use Cases



\* Employee Self-Service Support

\* IT Helpdesk Automation

\* Knowledge Base Search

\* Incident Reporting

\* Ticket Escalation



\---



\## Future Scope



\* Multi-user Authentication

\* Email Notifications

\* Advanced Analytics

\* Role-Based Access Control

\* Enterprise Integrations



