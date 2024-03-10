import uvicorn


def serve_dev():
    uvicorn.run(
        "center_django.asgi:application",
        host="127.0.0.1",
        port=5000,
        log_level="debug",
        reload=True,
        reload_delay=2,
    )


def serve_prd():
    uvicorn.run(
        "center_django.asgi:application",
        host="0.0.0.0",
        port=5000,
        log_level="info",
        reload=False,
        workers=4,
    )
