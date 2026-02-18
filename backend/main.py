from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from github_webhook import handle_github_webhook
from database import init_db
from ai_review import generate_ai_review

app = FastAPI(title="CodeRefine AI Backend 🚀")

# ✅ Enable CORS so React can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()


# ✅ Health check
@app.get("/")
def home():
    return {"message": "CodeRefine AI Backend Running 🚀"}


# ✅ GitHub webhook endpoint
@app.post("/webhook/github")
async def github_webhook(request: Request):
    try:
        payload = await request.json()
        result = handle_github_webhook(payload)

        return {
            "status": "success",
            "message": "Webhook processed",
            "review": result,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ✅ AI review endpoint (Groq/Gemini)
@app.get("/review")
def get_review():
    return {
        "bugs": ["Test bug"],
        "security": ["Test security issue"],
        "performance": [],
        "best_practices": ["Test best practice"],
        "score": 90
    }
latest_review = None


@app.post("/webhook/github")
async def github_webhook(request: Request):
    global latest_review

    payload = await request.json()
    result = handle_github_webhook(payload)

    # Save latest review in memory (simple for hackathon)
    latest_review = result

    return {"status": "received"}


@app.get("/latest-review")
def get_latest_review():
    return latest_review or {"message": "No PR reviewed yet"}
