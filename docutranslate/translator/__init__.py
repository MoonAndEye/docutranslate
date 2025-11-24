default_params = {
    "thinking": "disable",
    "chunk_size": 3000,
    "concurrent": 30,
    "temperature": 0.7,
    "timeout": 1200,
    "retry": 2,
    "system_proxy_enable": False,
    "max_completion_tokens": None,
    "reasoning_effort": None,
    "verbosity": None,
}

# GPT-5 推薦模型
GPT5_MODELS = {
    "gpt-5-nano": "gpt-5-nano-2025-08-07",  # 預設模型，最輕量
    "gpt-5-mini": "gpt-5-mini-2025-08-07",
    "gpt-5": "gpt-5-2025-08-07",
    "gpt-5-pro": "gpt-5-pro-2025-08-07",
}

DEFAULT_GPT5_MODEL = GPT5_MODELS["gpt-5-nano"]
