from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str  # Only query now

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        result = await run_agent(req.query)
        return {"response": result}
    except Exception as e:
        return {"error": str(e)}

@app.get("/")
def root():
    # Serve a simple frontend page here (see below)
    return {
        "status": "FDA Agent running",
        "message": "Use POST /chat with JSON {'query': 'your question here'}"
    }
