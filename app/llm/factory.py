from llm.openai_provider import OpenAIProvider


def get_llm_provider(name: str, **kwargs):
    """Factory function to get the appropriate LLM provider based on the name."""
    if name == "openai":
        return OpenAIProvider(
            api_key=kwargs["api_key"], model=kwargs.get("model", "gpt-4o-mini")
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {name}")
