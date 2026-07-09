import os

import uvicorn

from PokePY.api.application import create_app
from PokePY.api.settings import get_api_settings
from PokePY.config import API_CONFIG

app = create_app()


if __name__ == "__main__":
    settings = get_api_settings()
    port = int(os.getenv("PORT", str(API_CONFIG.port)))
    uvicorn.run(
        "PokePY.api.main:app",
        host=API_CONFIG.host,
        port=port,
        log_level=settings.log_level.lower(),
        reload=os.getenv("POKEPY_API_RELOAD", "1").strip().lower() not in {"0", "false", "no"},
    )
