from fastapi import FastAPI
from routes.teen_routes import router as teen_router  # ✅ updated

app = FastAPI()
app.include_router(teen_router, prefix="/api/teen", tags=["Teen Endpoints"])
