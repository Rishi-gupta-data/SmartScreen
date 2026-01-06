import os
import requests
import json

class LLMEngine:
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.llm_enabled = self._check_ollama_status()
        self.default_model = os.getenv("OLLAMA_DEFAULT_MODEL", "llama2")

    def _check_ollama_status(self) -> bool:
        """Checks if the Ollama server is running."""
        try:
            response = requests.get(f"{self.ollama_url}/api/version", timeout=1)
            response.raise_for_status()
            print("Ollama server is running.")
            return True
        except requests.exceptions.ConnectionError:
            print(f"Ollama server not reachable at {self.ollama_url}. LLM functionality disabled.")
            return False
        except requests.exceptions.RequestException as e:
            print(f"Error checking Ollama status: {e}. LLM functionality disabled.")
            return False

    def _check_model_available(self, model_name: str) -> bool:
        """Checks if a specific model is available in Ollama."""
        if not self.llm_enabled:
            return False
        try:
            # Ollama's /api/show endpoint to check model details
            response = requests.post(f"{self.ollama_url}/api/show", json={"name": model_name}, timeout=5)
            response.raise_for_status()
            if response.status_code == 200:
                print(f"Ollama model '{model_name}' is available.")
                return True
            return False
        except requests.exceptions.RequestException as e:
            print(f"Ollama model '{model_name}' not available or error checking: {e}")
            return False

    def is_llm_ready(self, model_name: str = None) -> bool:
        """Checks if LLM functionality is ready (Ollama running and model available)."""
        if not self.llm_enabled:
            return False
        model_to_check = model_name if model_name else self.default_model
        return self._check_model_available(model_to_check)

    def generate_response(self, prompt: str, model: str = None) -> str:
        """Generates a response using the specified Ollama model."""
        if not self.llm_enabled:
            return "LLM functionality is disabled (Ollama not running)."

        target_model = model if model else self.default_model
        if not self.is_llm_ready(target_model): # Use is_llm_ready to re-check model availability
            return f"LLM model '{target_model}' not available in Ollama or Ollama not running."

        try:
            headers = {"Content-Type": "application/json"}
            data = {
                "model": target_model,
                "prompt": prompt,
                "stream": False # We want a single response
            }
            response = requests.post(f"{self.ollama_url}/api/generate", headers=headers, json=data, timeout=300)
            response.raise_for_status()
            result = response.json()
            return result.get("response", "No response generated.")
        except requests.exceptions.RequestException as e:
            return f"Error generating response from Ollama: {e}"

# Example usage (for testing, will be removed later or wrapped in a test)
if __name__ == '__main__':
    llm_engine = LLMEngine()
    if llm_engine.is_llm_ready():
        print("LLM is ready to generate responses.")
        test_prompt = "Tell me a short story about a brave knight."
        print(f"\nGenerating response for: '{test_prompt}'")
        response = llm_engine.generate_response(test_prompt)
        print(f"Response: {response}")
    else:
        print("LLM is not ready.")
