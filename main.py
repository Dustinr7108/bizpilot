from fastapi import FastAPI
from .config import settings
from .db import Base, engine
from .routers import crm, marketing, finance, ops, knowledge
from . import workflows

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME)
app.include_router(crm.router)
app.include_router(marketing.router)
app.include_router(finance.router)
app.include_router(ops.router)
app.include_router(knowledge.router)
app.include_router(workflows.router)

@app.get("/health")
def health():
    return {"status":"ok"}
