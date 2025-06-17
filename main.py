from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from routes.todo_routes import todo_router
from routes.auth_routes import auth_router

app = FastAPI(
    title="Task Manager API",
    description="This API allows you to manage TODOs and user authentication.",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>Welcome to the Task Manager API</title>
            <style>
                body { font-family: Arial; text-align: center; padding: 50px; }
                h1 { color: #333; }
                a { color: #007bff; text-decoration: none; font-size: 18px; }
            </style>
        </head>
        <body>
            <h1>🚀 Welcome to the Task Manager API</h1>
            <p>Go to <a href="/docs">API Documentation</a> or <a href="/redoc">Redoc UI</a></p>
        </body>
    </html>
    """

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(todo_router)
app.include_router(auth_router)
