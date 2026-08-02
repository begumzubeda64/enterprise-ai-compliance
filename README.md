# Enterprise AI Compliance Review Platform

## Overview

An AI-powered compliance assessment platform that evaluates organizational evidence against configurable compliance frameworks, generating traceable findings, recommendations, and audit-ready reports with human review. It leverages Retrieval-Augmented Generation (RAG), workflow orchestration with LangGraph, human-in-the-loop approvals, and AWS cloud services to generate explainable, evidence-backed compliance reports.

The project is designed as a real-world Proof of Concept (POC) following enterprise software engineering practices rather than a simple AI demo.

---

## Key Features

* AI-assisted compliance document analysis
* Retrieval-Augmented Generation (RAG)
* Multi-step workflow orchestration using LangGraph
* Human-in-the-loop approval workflow
* Evidence-backed compliance findings
* Audit trail and execution logging
* Role-Based Access Control (RBAC)
* Custom MCP (Model Context Protocol) server for enterprise tools
* Dockerized development and deployment
* AWS-native architecture

---

## Technology Stack

### Backend

* FastAPI
* LangGraph
* SQLAlchemy
* PostgreSQL
* Docker

### Frontend

* Streamlit

### AI & RAG

* Amazon Bedrock (Claude)
* Amazon Titan Embeddings
* pgvector (Local Development)
* Amazon OpenSearch Serverless (Production)

### Cloud

* Amazon S3
* Amazon RDS PostgreSQL
* Amazon Cognito
* Amazon ECS Fargate
* Amazon CloudWatch
* AWS Secrets Manager

---

## High-Level Architecture

```text
Streamlit
    │
FastAPI
    │
LangGraph
    │
 ├── Document Processing
 ├── Retrieval
 ├── Compliance Analysis
 ├── Guardrails
 ├── Human Review
 └── Report Generation
    │
AWS Services
```

---

## Repository Structure

```text
backend/
frontend/
docker/
docs/
infra/
scripts/
```

---

## Planned Workflow

1. User authentication
2. Document upload
3. Document parsing
4. Chunking and embedding generation
5. Vector indexing
6. Context retrieval
7. Compliance analysis
8. Human approval
9. Report generation
10. Audit logging

---

## Project Goals

* Build a production-grade AI application
* Demonstrate enterprise AI architecture
* Showcase LangGraph orchestration patterns
* Implement secure, explainable AI workflows
* Follow cloud-native design principles using AWS
* Maintain clean, modular, and testable code

---

## Local Development

> **Status:** Under active development.

Setup instructions and Docker Compose configuration will be added as the implementation progresses.

---

## License

This project is intended for educational and portfolio purposes.
