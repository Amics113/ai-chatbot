import os
from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.auth.auth import authenticate_user, register_user
from backend.ollama_client import generate_response
from backend.rag.retriever import retrieve_context
from backend.memory.chat_memory import add_message, get_memory

app = FastAPI()


# -----------------------------
# STATIC FILES
# -----------------------------
# Mount frontend folder only if it exists
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/health")
def health():
    return {"status": "running"}


# -----------------------------
# PAGE ROUTES
# -----------------------------

@app.get("/", response_class=HTMLResponse)
def login_page():
    path = "frontend/login.html"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return "<h1>Login page not found</h1>"


@app.get("/register", response_class=HTMLResponse)
def register_page():
    path = "frontend/register.html"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return "<h1>Register page not found</h1>"


@app.get("/chat", response_class=HTMLResponse)
def chat_page():
    path = "frontend/index.html"
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return f.read()
    return "<h1>Chat page not found</h1>"


# -----------------------------
# AUTH ROUTES
# -----------------------------

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...)):
    register_user(username, password)
    return RedirectResponse("/", status_code=302)


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    if authenticate_user(username, password):
        return {"status": "ok"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# -----------------------------
# CHAT REQUEST MODEL
# -----------------------------

class ChatRequest(BaseModel):
    username: str
    prompt: str


# -----------------------------
# CHAT API
# -----------------------------

@app.post("/chat")
def chat(req: ChatRequest):

    # Save user message
    add_message(req.username, "User", req.prompt)

    # Retrieve RAG context
    context = retrieve_context(req.prompt)

    # Get chat memory
    memory = get_memory(req.username)

    combined_context = f"{context}\n{memory}".strip()

    # Generate AI response
    answer = generate_response(req.prompt, combined_context)

    # Save bot reply
    add_message(req.username, "Bot", answer)

    return {"response": answer}