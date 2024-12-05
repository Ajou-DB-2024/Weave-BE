from fastapi.openapi.utils import get_openapi

def custom_openapi(app):
    """
    Customizes the OpenAPI schema to include Bearer authentication.
    """
    if app.openapi_schema:
        return app.openapi_schema

    # Generate base OpenAPI schema
    openapi_schema = get_openapi(
        title="Weave API",
        version="0.1.0",
        description="[Ajou Univ.] 2024-2 DB 팀 프로젝트 Backend",
        routes=app.routes,
    )

    # Add BearerAuth security schema
    openapi_schema["components"] = openapi_schema.get("components", {})
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }

    # Apply security globally to all endpoints
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema  # Cache the schema
    return openapi_schema