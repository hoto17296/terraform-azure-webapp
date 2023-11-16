from os import getenv
import logging
import uvicorn

DEBUG = bool(int(getenv("DEBUG", "0")))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=getenv("PORT", 80),
        reload=DEBUG,
        log_level=logging.DEBUG if DEBUG else logging.WARNING,
    )
