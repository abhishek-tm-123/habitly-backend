from fastapi import FastAPI

from app.api.routes.auth import router as auth_router
from app.api.routes.habits import router as habits_router


app = FastAPI(
    title="Habit Tracker API",
)


app.include_router(auth_router)
app.include_router(habits_router)


@app.get("/")
async def root():
    return {
        "message": "Habit Tracker API is running"
    }