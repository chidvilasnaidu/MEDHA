# MEDHA! — Enterprise Knowledge Intelligence

> **M**ulti-document **E**nterprise **D**ata & **H**uman **A**ssistant  
> A glassmorphism-styled RAG chatbot powered by Amazon Bedrock Knowledge Bases & Nova Pro

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![AWS Bedrock](https://img.shields.io/badge/Amazon%20Bedrock-Nova%20Pro-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What is MEDHA!?

**MEDHA!** is a production-ready enterprise chatbot that lets your team ask natural language questions against your company's internal documents — and get accurate, cited answers grounded in your actual source material.

Built on **AWS Bedrock's `retrieve_and_generate` API**, MEDHA! handles the full RAG pipeline in a single API call:

```
User Question → Semantic Retrieval → Context Injection → LLM Generation → Cited Answer
```

No hallucinations. Every answer is backed by your documents.

---
## aws-ec2-url: http://16.16.204.180:8501/
## Features

- **Conversational RAG** — Multi-turn memory via Bedrock session IDs
- **Source Citations** — Every answer links back to the exact document chunk
- **Nova Pro Model** — Amazon's `amazon.nova-pro-v1:0` for fast, accurate responses
- **Glassmorphism UI** — Custom-designed Streamlit frontend with gold/teal aesthetic
- **Friendly AI Persona** — MEDHA! responds to greetings, thanks, and casual conversation
- **Configurable Retrieval** — Adjust chunk count (3–10) and temperature (0–1) via sidebar
- **Full-width Fixed Header** — Professional branding with live status indicator
- **Fixed Footer** — Version and attribution bar

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│                  Streamlit UI                    │
│         (main.py — glassmorphism frontend)       │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              BedrockKBClient                     │
│              (bedrock_client.py)                 │
│                                                  │
│   retrieve_and_generate()                        │
│   ├── generationConfiguration  (Nova Pro)        │
│   ├── orchestrationConfiguration (conversation)  │
│   └── retrievalConfiguration (SEMANTIC, k=5)     │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│         Amazon Bedrock Knowledge Base            │
│         (Vector Store — OpenSearch)              │
│                                                  │
│         Your S3 Documents → Embeddings           │
└─────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit + Custom CSS (Glassmorphism) |
| **LLM** | Amazon Nova Pro (`amazon.nova-pro-v1:0`) |
| **RAG API** | AWS Bedrock `retrieve_and_generate` |
| **Vector Store** | Amazon OpenSearch (via Bedrock KB) |
| **SDK** | `boto3` (bedrock-agent-runtime) |
| **Fonts** | Playfair Display · DM Sans · Space Mono |

---

## Project Structure

```
medha/
├── main.py              # Streamlit UI — header, sidebar, chat, footer
├── bedrock_client.py    # AWS Bedrock RAG client (retrieve_and_generate)
├── config.py            # Knowledge Base ID, Region, Model ID
└── README.md
```

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- AWS account with Bedrock access
- Amazon Bedrock Knowledge Base already created and synced
- AWS credentials configured (`~/.aws/credentials` or IAM role)

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/medha.git
cd medha
```

### 2. Install dependencies

```bash
pip install streamlit boto3
```

### 3. Configure

Edit `config.py`:

```python
KNOWLEDGE_BASE_ID = "YOUR_KB_ID"      # From AWS Bedrock console
REGION            = "us-east-1"
MODEL_ID          = "amazon.nova-pro-v1:0"
```

### 4. Run

```bash
streamlit run main.py
```

Open `http://localhost:8501` in your browser.

---

## AWS Bedrock Setup

### Enable Model Access

1. Go to **AWS Console → Amazon Bedrock → Model Access**
2. Enable **Amazon Nova Pro** (`amazon.nova-pro-v1:0`)

### Create Knowledge Base

1. Go to **Bedrock → Knowledge Bases → Create**
2. Connect your S3 bucket with documents (PDF, DOCX, TXT)
3. Choose an embeddings model (Titan Embeddings v2 recommended)
4. Sync your data source
5. Copy the **Knowledge Base ID** into `config.py`

### IAM Permissions Required

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:RetrieveAndGenerate",
        "bedrock:Retrieve",
        "bedrock:InvokeModel"
      ],
      "Resource": "*"
    }
  ]
}
```

---

## Configuration Reference

### `config.py`

| Variable | Description |
|---|---|
| `KNOWLEDGE_BASE_ID` | Your Bedrock Knowledge Base ID |
| `REGION` | AWS region (must match KB region) |
| `MODEL_ID` | `amazon.nova-pro-v1:0` (supports retrieve_and_generate) |

### Sidebar Controls

| Setting | Range | Effect |
|---|---|---|
| **Retrieved Chunks** | 3 – 10 | More chunks = more context, higher cost |
| **Temperature** | 0.0 – 1.0 | 0.1 recommended for factual Q&A |

---

## Pricing

Running on **Amazon Nova Pro** in `us-east-1`:

| Usage | Cost |
|---|---|
| Input tokens | $0.80 / 1M tokens |
| Output tokens | $3.20 / 1M tokens |
| ~1,000 queries/month | ≈ $0.50 |
| ~10,000 queries/month | ≈ $5.00 |

> Nova Pro is ~3× cheaper than Claude Sonnet and ~3× cheaper than GPT-4o.

---

## Why NOT GPT-OSS?

> GPT-OSS models (`gpt-oss-120b`) are available on Bedrock but **do not support `retrieve_and_generate`** yet. Knowledge Base integration for GPT-OSS is on AWS's roadmap. Nova Pro is the recommended model for Bedrock KB RAG today.

---

## Roadmap

- [ ] Streaming responses
- [ ] Document upload UI (S3 ingestion)
- [ ] Multi-KB support
- [ ] Authentication (Cognito / SSO)
- [ ] Export conversation as PDF
- [ ] Dark / Light theme toggle

---

## License

MIT License — free to use, modify, and deploy.

---

## Author

Built with ♥ using Amazon Bedrock, Streamlit, and a lot of CSS tweaking.

*MEDHA! — Ask anything. Know everything.*
