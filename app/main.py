import base64, hmac, hashlib, os
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from pydantic_settings import BaseSettings
from loguru import logger

class Settings(BaseSettings):
    APP_NAME: str = "BizPilot"
    PUBLIC_API_BASE: str = "https://example.up.railway.app"
    # Shopify
    SHOPIFY_WEBHOOK_SECRET: str | None = None
    # Stripe
    STRIPE_WEBHOOK_SECRET: str | None = None
    class Config:
        env_file = ".env"

settings = Settings()
app = FastAPI(title=settings.APP_NAME)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/admin", response_class=HTMLResponse)
def admin():
    return """
    <html><head><title>BizPilot Admin</title></head>
    <body style="font-family:system-ui;padding:24px">
      <h1>BizPilot Admin</h1>
      <p>You're online. Next we’ll add DB + analytics.</p>
      <ul>
        <li>Health: <code>/health</code></li>
        <li>Shopify webhook: <code>/integrations/shopify/webhook</code></li>
        <li>Stripe webhook: <code>/integrations/stripe/webhook</code></li>
      </ul>
    </body></html>
    """

def verify_shopify_hmac(raw_body: bytes, hmac_header: str | None) -> bool:
    if not (settings.SHOPIFY_WEBHOOK_SECRET and hmac_header):
        return False
    digest = hmac.new(settings.SHOPIFY_WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(expected, hmac_header)

@app.post("/integrations/shopify/webhook")
async def shopify_webhook(request: Request):
    raw = await request.body()
    hmac_header = request.headers.get("X-Shopify-Hmac-Sha256")
    if not verify_shopify_hmac(raw, hmac_header):
        raise HTTPException(status_code=401, detail="Invalid Shopify signature")
    payload = await request.json()
    logger.info(f"Shopify topic={request.headers.get('X-Shopify-Topic')} id={payload.get('id')}")
    return {"ok": True}

def verify_stripe_sig(raw_body: bytes, sig_header: str | None) -> bool:
    # Minimal check: Stripe recommends library verification; this is a basic fallback.
    if not (settings.STRIPE_WEBHOOK_SECRET and sig_header):
        return False
    try:
        parts = dict(item.split("=", 1) for item in sig_header.split(","))
        t = parts.get("t"); v1 = parts.get("v1")
        if not (t and v1): return False
        signed_payload = f"{t}.{raw_body.decode()}".encode()
        digest = hmac.new(settings.STRIPE_WEBHOOK_SECRET.encode(), signed_payload, hashlib.sha256).hexdigest()
        return hmac.compare_digest(digest, v1)
    except Exception:
        return False

@app.post("/integrations/stripe/webhook")
async def stripe_webhook(request: Request):
    raw = await request.body()
    if not verify_stripe_sig(raw, request.headers.get("Stripe-Signature")):
        raise HTTPException(status_code=401, detail="Invalid Stripe signature")
    payload = await request.json()
    logger.info(f"Stripe event={payload.get('type')} id={payload.get('id')}")
    return {"received": True}
