# Multi-Agent System with FastAPI

This project implements a **multi-agent system** using FastAPI and LangChain.  
The system integrates three specialized agents:
- **News Agent** → Finds the latest news about a topic using Tavily API.  
- **Book Agent** → Searches for information about books.  
- **Math Agent** → Solves math expressions or problems (basic arithmetic via `eval`, complex problems via LLM).  

The agents are orchestrated with a router agent that decides which one to use based on the input query.

---

## Features
- FastAPI-based REST API
- Agents powered by LangChain
- Tavily API integration for web/news/book search
- Groq LLM integration for reasoning
- Modular structure for scalability

---

## 🛠 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/tuntunssd/multi_agent_deployment.git
cd multi_agent_deployment

## Create & Activate Virtual Environment:

### Linux / macOS
python3 -m venv venv
source venv/bin/activate

### Windows
python -m venv venv
venv\Scripts\activate


## Install Dependencies:
pip install -r requirements.txt

## Configure Environment Variables

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key

## Run Instructions:

### Local Run:
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

#### API will be available at:
 http://localhost:8000

### Run with Docker:

#### Build Docker image
docker build -t multi-agents .

#### Run container
docker run -p 8000:8000 --env-file .env multi-agents

## API Usage Examples:

#### cURL Example:
curl -X POST "http://localhost:8000/multi-agents2" \
     -H "Content-Type: application/json" \
     -d '{"query": "Give me the latest news about AI"}'

#### Python Client Example:
import requests

url = "http://localhost:8000/multi-agents2"
payload = {"query": "Solve 15 * (3 + 2)"}

response = requests.post(url, json=payload)
print(response.json())

## Testing Instructions:

### Run with pytest:
pytest

### Example Unit Test (test_api.py):

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_math_agent():
    response = client.post("/multi-agents2", json={"query": "10 + 5"})
    assert response.status_code == 200
    assert "15" in response.json()["answer"]

## Project Structure:


project_root/
│── main.py                 # FastAPI entry point
│
├── services/               # Core business logic
│   ├── agents.py           # Agent definitions
│   ├── config.py           # Environment config
│   ├── graph.py            # Agent routing graph
│   ├── model.py            # LLM integration
│   └── tools.py            # Tools (news, book, math solver)
│
├── endpoints/
│   └── endpoint.py         # API endpoints
│
├── schemas/
│   └── schema.py           # Request/response schemas
│
├── tests/                  # Unit tests
│   └── test_api.py
│
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker setup
└── README.md               # Project documentation

## Deploy FastAPI Multi-Agent Project from GitHub to AWS:

### Prerequisites:
1. AWS account

2. EC2 instance (Ubuntu 22.04 recommended) with security group allowing port 22 (SSH) and port 8000 (API) or 80/443 if using Nginx/ALB

3. SSH access (ssh -i key.pem ubuntu@<EC2-Public-IP>)

4. GitHub repo ready with your project (Dockerfile, docker-compose.yml, etc.)

### Connect to AWS EC2:

ssh -i key.pem ubuntu@<EC2-Public-IP>

### Install Docker & Git:

sudo apt install -y docker.io docker-compose git
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

### Clone GitHub Repo:

git clone https://github.com/tuntunssd/multi_agent_deployment.git
cd multi_agent_deployment

### Build & Run with Docker:

docker-compose up -d --build


### Access the API:

http://<EC2-Public-IP>:8000/docs


## Unit Test:
### test with:

curl -X POST "http://<your-alb-dns>:80/multi-agents2" \
     -H "Content-Type: application/json" \
     -d '{"query": "Solve 12 * (5 + 3)"}'
### output:
{"answer": "96"}
