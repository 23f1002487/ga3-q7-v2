from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import json
import os
import logging
import tempfile
import subprocess
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CLI Coding Agent API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def call_aipipe_api(task: str) -> str:
    """
    Call aipipe.org API to process the coding task.
    Uses OpenAI-compatible API endpoint as specified in PROMPT.md
    """
    try:
        # Get API key from environment variable
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            logger.error("OPENAI_API_KEY environment variable not set")
            return "Error: API key not configured"
        
        # Use aipipe.org endpoint as specified in PROMPT.md
        url = "https://aipipe.org/openai/v1/chat/completions"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Construct prompt for coding task
        system_prompt = """You are a coding assistant that can write and execute code to solve programming tasks. 
When given a task, analyze it carefully, write the necessary code, execute it, and provide the final output/result.
Return only the final result/answer that the task is asking for, not the code itself."""
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": task}
            ],
            "max_tokens": 500,
            "temperature": 0.1
        }
        
        logger.info(f"Calling aipipe.org API for task: {task}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            output = result['choices'][0]['message']['content'].strip()
            logger.info(f"API response: {output}")
            return output
        else:
            logger.error(f"API error: {response.status_code} - {response.text}")
            return f"API Error: {response.status_code}"
            
    except requests.exceptions.Timeout:
        logger.error("API request timed out")
        return "Error: Request timed out"
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        return f"Error: {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Error: {str(e)}"

def run_cli_agent(task: str) -> str:
    """
    Process the task using aipipe.org API as specified in PROMPT.md.
    No hardcoded solutions - all tasks outsourced to external AI service.
    """
    logger.info(f"Processing task: {task}")
    
    # Call aipipe.org API for task processing
    result = call_aipipe_api(task)
    
    # Log the result
    logger.info(f"Agent output: {result}")
    
    return result

@app.get("/task")
async def handle_task(q: str) -> Dict[str, Any]:
    """
    Handle coding task requests as specified in PROMPT.md.
    Returns JSON with task, agent, output, and email fields.
    """
    try:
        logger.info(f"Received task request: {q}")
        
        # Process the task using aipipe.org API
        output = run_cli_agent(q)
        
        # Return response in required format
        response = {
            "task": q,
            "agent": "openai-gpt-3.5-turbo",
            "output": output,
            "email": "23f1002487@ds.study.iitm.ac.in"
        }
        
        logger.info(f"Sending response: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing task: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "CLI Coding Agent API is running", "status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)