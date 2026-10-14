from .vllm_utils import VLLMServer

if __name__ == "__main__":
    server = VLLMServer(
        model_id="allenai/OLMo-2-0425-1B",
        gpu=0,
        logging_level="INFO",
        host="0.0.0.0",
    )
    try:
        server.start(wait_for_ready=False)
        print("Server launched; watch the vLLM logs for readiness on port 8000.")
        while input("Type q and press Enter to stop: ").strip().lower() != "q":
            pass
    finally:
        server.stop()
