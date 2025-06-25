from abc import ABC, abstractmethod


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """Generate text based on the provided prompt."""
        pass

    @abstractmethod
    def generate_stream(self, prompt: str, **kwargs):
        """Generate text based on the provided prompt with streaming."""
        pass