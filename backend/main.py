from fastapi import FastAPI
from .api.endpoints import router
from .database.db import init_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Learning Coach API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
init_db()

# Include Routers
app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "AI Learning Coach API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
