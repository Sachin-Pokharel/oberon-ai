import openai
from llm.base import LLMProvider


class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "gpt-4o-mini"):
        openai.api_key = api_key
        self.model = model

    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text based on the provided prompt using OpenAI API."""
        response = openai.responses.create(
            model=self.model, input=[{"role": "user", "content": prompt}], **kwargs
        )
        return response.output_text

    def generate_stream(self, prompt: str, **kwargs):
        """Generate text based on the provided prompt using OpenAI API with streaming."""
        response = openai.responses.create(
            model=self.model,
            input=[{"role": "user", "content": prompt}],
            stream=True,
            **kwargs,
        )

        return response
