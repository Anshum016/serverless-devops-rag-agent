# Serverless DevOps Log Analysis Agent 🤖

A fully **serverless RAG (Retrieval-Augmented Generation)** system built
using **AWS + LangGraph + Google Gemini AI** to analyze server logs and
provide intelligent, actionable solutions.

![Architecture Diagram](Architecture-log-rag-agent.png)

## 📖 Project Overview

This project is the **core intelligence (the Brain)** of an
enterprise-grade log analysis system.

In a real production environment, logs would continuously stream from
**AWS CloudWatch → Firehose → S3**.\
For this **Proof of Concept (PoC)**, the focus is on building the **core
AI logic**:

-   Ingesting historical error logs\
-   Transforming them into vector embeddings\
-   Using a self-corrective RAG pipeline to answer log-related questions
    intelligently

## 🚀 Key Features

### 🌩 Serverless Architecture

Uses AWS Lambda, S3, API Gateway, and ECR.\
**Costs \$0 when idle.**

### 🤖 Dual-Robot Pipeline

-   **Ingest Worker:** Converts uploaded logs into vector embeddings\
-   **Chat Agent:** LangGraph reasoning agent served via Streamlit

### 🧠 Intelligent RAG Workflow

-   FAISS for semantic search\
-   LangGraph for reasoning flows\
-   Self-grading AI avoids hallucinations and validates retrieved log
    entries

### ⚙️ Fully Automated Deployment

Infrastructure is provisioned with **Terraform**, including Lambda
container builds.

## 🛠️ Tech Stack

-   **AWS:** Lambda, API Gateway, S3, ECR, IAM\
-   **IaC:** Terraform\
-   **AI Model:** Google Gemini 2.0 Flash\
-   **Workflow Engine:** LangGraph + LangChain\
-   **Vector DB:** FAISS\
-   **Frontend:** Streamlit

## 📂 Project Structure

    .
    ├── aws_cloud/
    │   ├── lambda.tf
    │   ├── s3.tf
    │   ├── api_gateway.tf
    │   └── ...
    ├── backend/
    │   ├── agent.py
    │   ├── ingest.py
    │   ├── lambda_function.py
    │   └── Dockerfile
    └── frontend/
        └── app.py

## ⚡ Deployment Guide

### Prerequisites

-   Docker Desktop\
-   Terraform\
-   AWS CLI\
-   Google Gemini API Key

## Step 1: Clone the Repository

``` bash
git clone https://github.com/YOUR_USERNAME/serverless-devops-rag-agent.git
cd serverless-devops-rag-agent
```

## Step 2: Deploy AWS Infrastructure

``` bash
cd aws_cloud
terraform init
terraform apply -var="google_api_key=YOUR_ACTUAL_GEMINI_KEY"
```

## Step 3: Save Terraform Outputs

    s3_bucket_name = log-rag-agent-storage-xxxxx
    deploy_url     = https://xyz.execute-api.us-east-1.amazonaws.com/chat

# 🧠 How to Use the System

## Phase 1: Ingestion

Upload `dataset.txt` to `raw/` folder in S3 bucket.

## Phase 2: Querying

``` bash
cd frontend
pip install streamlit requests
streamlit run app.py
```

# 🧹 Clean Up

``` bash
cd aws_cloud
terraform destroy -var="google_api_key=YOUR_ACTUAL_GEMINI_KEY"
```

