from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import api
from routers.mcp import mcp_app
import uvicorn

app = FastAPI(lifespan=mcp_app.lifespan)

# Configure CORS - Allow all origins in development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=False,  # Must be False when allow_origins is ["*"]
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router)
app.mount("/llm", mcp_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)