from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from agents.main_agent import Agent
from observability.monitoring import process_request
from guardrails.safety import validate_input, validate_output
from error_handling.handler import retry
import yaml
import os

app = FastAPI()

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), "config", "config.yaml")
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/chat", response_model=ChatResponse)
@process_request
async def chat_endpoint(request: ChatRequest):
    message = validate_input(request.message)
    if message.startswith("Error:"):
        raise HTTPException(status_code=400, detail=message)

    agent = Agent()

    @retry
    def run_agent():
        return agent.run(message)

    try:
        response = run_agent()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running agent: {e}")

    validated_response = validate_output(response)
    if validated_response.startswith("Error:"):
        raise HTTPException(status_code=500, detail=validated_response)

    return ChatResponse(response=validated_response)

if __name__ == "__main__":
    import uvicorn, os, socket
    def _port_free(p):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.3)
            return s.connect_ex(("127.0.0.1", p)) != 0
    port = int(os.environ.get("PORT", 8081))
    while not _port_free(port):
        print(f"Port {port} is already in use.")
        try:
            ans = input(f"Try port {port + 1} instead? [Y/n]: ").strip().lower()
        except EOFError:
            ans = "y"
        if ans in ("", "y", "yes"):
            port += 1
        else:
            print("Exiting. Free the port and try again.")
            raise SystemExit(1)
    print(f"Starting server on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)