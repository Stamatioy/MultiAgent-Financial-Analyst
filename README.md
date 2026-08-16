# startup root commands

V.ENV: .\.venv\Scripts\Activate.ps1  

To start QWEN: .\scripts\start_llama_server.ps1

FastAPI: python .\scripts\run_api.py

NextJS (in ./frontend): npm run dev




# Multi-Agent Financial Analyst

A local multi-agent financial research system that combines market data, SEC fundamentals, valuation analysis, risk modeling, news retrieval, RAG, and a local LLM to produce evidence-grounded investment research.

The system uses **Qwen3-8B running locally through llama.cpp**. Specialist agents analyze different aspects of a company before an Investment Committee synthesizes their findings into a final recommendation.

> This project is intended for research and educational purposes and does not constitute financial advice.

---

## Overview

Traditional LLM-based stock analysis often relies on a single prompt containing large amounts of loosely structured information.

This project instead separates financial research into specialist components:

- Market Analyst
- Fundamental Analyst
- Valuation Analyst
- Risk Analyst
- News Intelligence Agent
- Investment Committee

Financial metrics are calculated deterministically in Python before being interpreted by the LLM.

News is retrieved using semantic search and RAG, while structured Pydantic schemas validate agent outputs.

The final Investment Committee receives the validated specialist research bundle and produces an evidence-grounded investment assessment.

---

## Screenshots

### Research Dashboard

![Dashboard](docs/screenshots/dashboard.png)

### Multi-Agent Research

![Research Progress](docs/screenshots/research-running.png)

### Investment Committee

![Investment Result](docs/screenshots/investment-result.png)

### Specialist Analysis

![Market Analysis](docs/screenshots/market-analysis.png)

### News Intelligence

![News Intelligence](docs/screenshots/news-intelligence.png)

### System Architecture

![Architecture](docs/screenshots/architecture.png)

---