# Serverless DevOps Log Analysis Agent 🤖

A serverless RAG (Retrieval-Augmented Generation) application built on AWS that analyzes server logs and provides actionable solutions using Google Gemini AI.


## 🚀 Features
* **Serverless Architecture:** Fully deployed on AWS Lambda, S3, and API Gateway using Terraform.
* **RAG Pipeline:** Retrieves relevant logs using FAISS vector search.
* **AI-Powered:** Uses Google Gemini 2.0 Flash to grade relevance and generate solutions.
* **Dual-Robot System:**
    * **Ingest Worker:** Automatically processes logs uploaded to S3.
    * **Chat Agent:** Answers user questions via a Streamlit UI.
* **Infrastructure as Code:** One-click deployment with Terraform.

---

## 🛠️ Prerequisites

Before running this project, ensure you have the following installed:
1.  **Docker Desktop** (Must be running).
2.  **Terraform** (v1.0+).
3.  **AWS CLI** (Configured with `aws configure`).
4.  **Python 3.10+** (For local frontend testing).
5.  **Google Gemini API Key** (Get one from [Google AI Studio](https://aistudio.google.com/)).

---

## 📦 Project Structure

```text
.
├── aws_cloud/          # Terraform Infrastructure code
│   ├── lambda.tf       # Defines Chat & Ingest functions
│   ├── s3.tf           # S3 Bucket & Event Triggers
│   └── ...
├── backend/            # Python Source Code
│   ├── agent.py        # LangGraph Workflow (The Brain)
│   ├── ingest.py       # Vector DB Creation (The Learner)
│   └── Dockerfile      # Container definition
└── frontend/           # Streamlit UI
    └── app.py          # Chat Interface