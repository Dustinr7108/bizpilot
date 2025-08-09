from celery import Celery
from .config import settings

celery_app = Celery("bizpilot", broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery_app.task
def long_job(name: str, seconds: int = 5):
    import time; time.sleep(seconds)
    return {"name": name, "done": True}
