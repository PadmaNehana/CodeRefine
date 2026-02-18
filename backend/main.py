from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from github_webhook import handle_github_webhook
from database import init_db, get_latest_review

app = FastAPI(title="CodeRefine AI Backend 🚀")

# Enable CORS so React can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for hackathon
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    init_db()


# Health check
@app.get("/")
def home():
    return {"message": "CodeRefine AI Backend Running 🚀"}


# GitHub webhook endpoint
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


# Latest AI review endpoint (used by frontend)
@app.get("/latest-review")
def latest_review():
    return get_latest_review()
