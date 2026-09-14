"""Azure Functions entry point (Python v2 programming model).

Wraps the FastAPI ASGI app so every HTTP request is forwarded to FastAPI.
The Functions host discovers the ``app`` object below automatically.
"""
import azure.functions as func

from app.main import app as fastapi_app

app = func.AsgiFunctionApp(
    app=fastapi_app,
    http_auth_level=func.AuthLevel.ANONYMOUS,
)
