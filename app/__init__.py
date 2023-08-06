import os

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import ORJSONResponse
from starlette.staticfiles import StaticFiles

from app.apis.router import api_router
from app.core.config import settings
from app.core.exception import register_exception
from app.core.middleware import register_cross, register_middleware, register_startup_and_shutdown


def create_app():
    app = FastAPI(
        title="peachTreePlanting",
        version="0.1.1",
        default_response_class=ORJSONResponse,
    )

    if settings.DEV_ENV:
        static_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "static"
        )

        app.mount("/static", StaticFiles(directory=static_dir), name="static")

        @app.get("/docs")
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url=app.openapi_url,
                title=app.title + " - Swagger UI",
                oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
                swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
                swagger_css_url="/static/swagger-ui/swagger-ui.css",
            )

    # 导入路由
    app.include_router(api_router, prefix="/api")

    register_exception(app)
    register_cross(app)
    register_middleware(app)
    register_startup_and_shutdown(app)

    return app


app = create_app()
