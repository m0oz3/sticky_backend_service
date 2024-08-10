import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "config.asgi:application",
        host="0.0.0.0",  # noqa: S104
        reload=True,
        reload_includes=[
            "*.html",
        ],
    )
