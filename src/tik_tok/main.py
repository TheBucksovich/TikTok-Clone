from fastapi import FastAPI
import uvicorn

from tik_tok.core.config import settings

app = FastAPI(
    title=settings.project_name,
    description=settings.project_descr,
    version=settings.app_version,
    redoc_url=None,
)

@app.get("/")
async def read_root():
    return {"message": f"Welcome to {settings.project_name}!"}

if __name__ == "__main__":
    uvicorn.run("tik_tok.main:app", host="0.0.0.0", port=3000, reload=True)