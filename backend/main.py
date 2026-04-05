from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
import os

# Add backend directory to path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from risk_engine import compute_risk
from output_validator import validate_output
from behavioral_analysis import add_to_history, analyze_behavior
from red_team import run_red_team
from llm_handler import query_llm
from siem_logger import log_event, get_recent_events, get_log_stats


# ─────────────────────────────────────────
# APP SETUP
# ─────────────────────────────────────────
app = FastAPI(
    title="Sentinel AI",
    description="Agentic Defense System for Prompt Abuse Prevention",
    version="1.0.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

@app.middleware("http")
async def add_ngrok_header(request, call_next):
    response = await call_next(request)
    response.headers["ngrok-skip-browser-warning"] = "true"
    return response

# ─────────────────────────────────────────
# STATS TRACKER
# ─────────────────────────────────────────
stats = {
    "total_requests": 0,
    "blocked": 0,
    "warned": 0,
    "allowed": 0,
}

# ─────────────────────────────────────────
# REQUEST/RESPONSE MODELS
# ─────────────────────────────────────────
class PromptRequest(BaseModel):
    prompt: str
    user_id: str = "anonymous"

class PromptResponse(BaseModel):
    status: str
    decision: str
    risk_score: float
    ml_score: float
    rule_triggered: bool
    harmful_detected: bool 
    message: str
    llm_response: str = ""
# ─────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────
@app.get("/")
def root():
    return {
        "name": "Sentinel AI",
        "status": "running",
        "version": "1.0.0",
        "message": "Agentic Defense System for Prompt Abuse Prevention"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model": "loaded",
        "vectorizer": "loaded"
    }

@app.get("/stats")
def get_stats():
    return {
        "total_requests": stats["total_requests"],
        "blocked": stats["blocked"],
        "warned": stats["warned"],
        "allowed": stats["allowed"],
        "block_rate": f"{(stats['blocked'] / max(stats['total_requests'], 1)) * 100:.1f}%"
    }

@app.get("/red-team")
def red_team_test():
    results = run_red_team()
    return results

@app.get("/siem/events")
def siem_events():
    events = get_recent_events(50)
    return {"events": events}

@app.get("/siem/stats")
def siem_stats():
    return get_log_stats()

@app.post("/chat", response_model=PromptResponse)
def chat(request: PromptRequest):
    prompt = request.prompt.strip()

    # Validate input
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    if len(prompt) > 5000:
        raise HTTPException(status_code=400, detail="Prompt too long")

    # Step 1 - Run risk engine on prompt
    result = compute_risk(prompt)

    # Step 1b - Run behavioral analysis
    behavior = analyze_behavior(request.user_id)

    # If high threat user boost the risk score
    if behavior["threat_level"] == "high":
        result["final_score"] = min(result["final_score"] + 0.4, 1.0)
        result["decision"] = "BLOCK"
    elif behavior["threat_level"] == "medium":
        result["final_score"] = min(result["final_score"] + 0.2, 1.0)

    # Recalculate decision AFTER boost
    if result["final_score"] >= 0.7:
        result["decision"] = "BLOCK"
    elif result["final_score"] >= 0.5:
        result["decision"] = "WARN"
    else:
        result["decision"] = "ALLOW"

    # Add to history
    add_to_history(
        request.user_id,
        prompt,
        result["final_score"],
        result["decision"]
    )

    # Log to SIEM
    log_event(
        user_id=request.user_id,
        prompt=prompt,
        decision=result["decision"],
        risk_score=result["final_score"],
        ml_score=result["ml_score"],
        rule_triggered=result["rule_triggered"],
        harmful_detected=result["harmful_detected"],
        anomaly_detected=behavior["anomaly_detected"],
        threat_level=behavior["threat_level"]
    )

    # Update stats
    stats["total_requests"] += 1

    # Step 2 - Block if risk is too high
    if result["decision"] == "BLOCK":
        stats["blocked"] += 1
        return PromptResponse(
            status="blocked",
            decision="BLOCK",
            risk_score=result["final_score"],
            ml_score=result["ml_score"],
            rule_triggered=result["rule_triggered"],
            harmful_detected=result["harmful_detected"],
            message="⛔ Prompt blocked by Sentinel AI. Potential prompt injection or jailbreak detected."
        )

    # Step 3 - Simulate LLM response for now
    llm_response = query_llm(prompt)

    # Step 4 - Validate LLM output
    output_check = validate_output(llm_response)

    if not output_check["is_safe"]:
        stats["blocked"] += 1
        return PromptResponse(
            status="output_blocked",
            decision="BLOCK",
            risk_score=result["final_score"],
            ml_score=result["ml_score"],
            rule_triggered=result["rule_triggered"],
            harmful_detected=result["harmful_detected"],
            message=f"⛔ Response blocked by Sentinel AI. {output_check['reason']}"
        )

    # Step 5 - Allow safe response
    if result["decision"] == "WARN":
        stats["warned"] += 1
        return PromptResponse(
            status="warning",
            decision="WARN",
            risk_score=result["final_score"],
            ml_score=result["ml_score"],
            rule_triggered=result["rule_triggered"],
            harmful_detected=result["harmful_detected"],
            message="⚠️ Prompt is suspicious but allowed. Proceed with caution."
        )

    stats["allowed"] += 1
    return PromptResponse(
        status="success",
        decision="ALLOW",
        risk_score=result["final_score"],
        ml_score=result["ml_score"],
        rule_triggered=result["rule_triggered"],
        harmful_detected=result["harmful_detected"],
        message="✅ Prompt is safe. Processing allowed.",
        llm_response=llm_response
    )