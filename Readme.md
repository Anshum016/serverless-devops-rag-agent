🚀 Serverless DevOps Log Analysis Agent (RAG + AWS + Gemini AI)

A fully serverless, production-ready Log Analysis Agent built on AWS + LangGraph + Google Gemini.
This system ingests logs, converts them into searchable vectors, retrieves the most relevant chunks, validates them using an AI grader, and finally produces actionable insights — all without managing servers.

⭐ Key Features
🔥 1. End-to-End Serverless Architecture

Fully deployed using AWS Lambda, S3, CloudWatch, API Gateway, and ECR.

Zero maintenance, auto-scalable, cost-efficient.

🤖 2. Dual AI Agents (LangGraph)

Ingest Worker Agent:
Processes logs uploaded to S3 → cleans → chunks → embeds → stores into FAISS vector DB.

Chat Retrieval Agent:
Accepts user queries → retrieves relevant log chunks → grades relevance → answers using Gemini AI.

🧠 3. RAG (Retrieval-Augmented Generation) Pipeline

FAISS Vector Search

Node Retrieval Agent (Retriever)

Node Grading Agent (Relevance Checker)

Best-result answer generator (Gemini)

📦 4. Infrastructure as Code

Entire cloud infra deployed via Terraform (one command).

💬 5. Streamlit Frontend

Clean chat UI

.
├── aws_cloud/            # Terraform Infrastructure code
│   ├── lambda.tf         # Chat & Ingest functions infra
│   ├── s3.tf             # S3 bucket + event triggers
│   ├── iam.tf            # IAM roles for Lambda
│   ├── ecr.tf            # ECR repo for containerized Lambda
│   └── variables.tf
│
├── backend/              # Python Source Code
│   ├── agent.py          # LangGraph RAG pipeline (Chat bot)
│   ├── ingest.py         # Log processor + FAISS vector creator
│   ├── Dockerfile        # Containerized Lambda image
│   └── requirements.txt
│
└── frontend/             # Streamlit Web UI
    ├── app.py            # Chat Interface
    └── styles.css


🚀 Deployment Guide
Step 1 — Clone Repository
git clone https://github.com/<your-repo>/log-analysis-rag-agent.git
cd log-analysis-rag-agent

Step 2 — Deploy AWS Resources
cd aws_cloud
terraform init
terraform apply

Step 3 — Build & Push Lambda Docker Image
cd backend
docker build -t log-agent .
aws ecr get-login-password | docker login ...
docker tag log-agent:latest <AWS_ACCOUNT>.dkr.ecr.<region>.amazonaws.com/log-agent
docker push <AWS_ECR_URL>

Step 4 — Run Frontend Locally
cd frontend
pip install -r ../backend/requirements.txt
streamlit run app.py
Sends POST request → triggers AWS Lambda → returns generated solution with logs context.
