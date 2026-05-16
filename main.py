import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from google import genai
from google.genai import types

app = FastAPI(title="EcoLink AI Ecosystem Automation Backend")

# 1. ALLOW FRONTEND TO CONNECT (CORS Middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Ain't HTML file to call this API seamlessly
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. INITIALIZE GEMINI CLIENT
# Ensure you run 'export GEMINI_API_KEY="your-key"' or set it in your environment variables
try:
    client = genai.Client()
except Exception as e:
    print(f"Warning: Gemini Client initialization failed. Check your API key. Error: {e}")
    client = None

# 3. DATABASE MOCK DATA (Stores our Living Ecosystem Linkages)
db_issues = [
    {
        "title": "Clogged Major Monsoon Drain",
        "area": "Selangor Hub",
        "priority": "High",
        "reasoning": "AI Engine linked to Emergency Drainage Team. Bypassed manual routing queues to prevent localized flash flood risk."
    },
    {
        "title": "Illegal Rubbish Accumulation",
        "area": "Kuala Lumpur Central",
        "priority": "Medium",
        "reasoning": "AI flagged structural environmental mismatch. Scheduled for waste disposal cohort unit pickup within 24 hours."
    },
    {
        "title": "Minor Damaged Pathway Signage",
        "area": "Cyberjaya West",
        "priority": "Low",
        "reasoning": "Low risk factor. Logged into historical long-term ecosystem maintenance cycle automatically."
    }
]

# Pydantic models for incoming requests
class ChatRequest(BaseModel):
    message: str

# 4. ENDPOINT 1: ADMIN DASHBOARD MATRIX
@app.get("/dashboard/issues/")
async def get_dashboard_issues():
    return db_issues

# 5. ENDPOINT 2: CITIZEN SNAP & REPORT (Gemini Vision Processing)
@app.post("/api/classify/")
async def classify_issue(file: UploadFile = File(...)):
    if not client:
        raise HTTPException(status_code=500, detail="Gemini API Client is not configured.")
    
    try:
        # Read the uploaded file bytes
        image_bytes = await file.read()
        
        # Structure the prompt to force Gemini to return exactly what our data structures need
        prompt = """
        Analyze this community infrastructure/environmental issue image.
        Provide a JSON response with exactly two keys:
        1. "category": A concise title classification of the issue (e.g., "Structural Drainage Blockage", "Illegal Dumpsite").
        2. "priority": Determine the severity level based on urban risk. Must be exactly one of these strings: "High", "Medium", or "Low".
        3. "reasoning": Provide a 1-sentence engineering automated routing logic explanation showing why this is linked to a municipal crew without human intervention.
        
        Return ONLY valid JSON. No markdown wrappers.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=file.content_type
                ),
                prompt
            ],
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            )
        )
        
        # Parse the JSON response securely from Gemini
        import json
        result = json.loads(response.text)
        
        # Construct the new linkage object to feed into the state engine
        new_linkage = {
            "title": result.get("category", "Unidentified Infrastructure Issue"),
            "area": "Subang Jaya Command Center", # Default simulation area
            "priority": result.get("priority", "Medium"),
            "reasoning": result.get("reasoning", "Automated system deployment based on automated vision matrix verification thresholds.")
        }
        
        # Insert at the beginning of our database list so it appears at the top of Aleeya's UI
        db_issues.insert(0, new_linkage)
        
        return {
            "category": new_linkage["title"],
            "priority": new_linkage["priority"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image via Gemini: {str(e)}")

# 6. ENDPOINT 3: AI ECO-ASSISTANT CHAT
@app.post("/api/chat/")
async def chat_eco_assistant(request: ChatRequest):
    if not client:
        return {"reply": "Ecosystem Chat engine offline. However, I am ready to route system entities!"}
    
    try:
        system_instruction = """
        You are the EcoLink AI Neighborhood Assistant expert system. 
        Your job is to answer municipal compliance questions, recycling criteria, or clarify relationship tracking logic.
        Keep answers helpful, highly structured, concise, and focused on Malaysian local councils (e.g., MBPJ, MPSJ, DBKL) and SDG 11 framework goals.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=request.message,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                max_output_tokens=150
            )
        )
        return {"reply": response.text.strip()}
        
    except Exception as e:
        return {"reply": f"Sorry, my automated routing logic is recycling some processes. Error: {str(e)}"}