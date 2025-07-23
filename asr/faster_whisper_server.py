# Entrypoint for faster-whisper-server
# TODO: Implement SSE streaming endpoint /v1/audio/stream for 8kHz PCM audio

def main():
    # Preload model(s) before starting the server
    import os
    import logging
    from faster_whisper_server.dependencies import get_config, get_model_manager

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    config = get_config()
    model_manager = get_model_manager()
    preload_models = config.preload_models or [config.whisper.model]
    logger.info(f"Preloading models: {preload_models}")
    for model_name in preload_models:
        logger.info(f"Loading model: {model_name}")
        model_manager.load_model(model_name)
    logger.info("All models loaded. Starting server...")

    import uvicorn
    from faster_whisper_server.main import create_app
    app = create_app()
    uvicorn.run(app, host=config.host, port=config.port)

if __name__ == "__main__":
    main() 