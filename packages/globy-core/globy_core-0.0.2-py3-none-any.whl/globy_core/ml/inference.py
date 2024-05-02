import requests
import json

class BaseModelInference:
    def __init__(self, api_key=None, endpoint=None):
        self.api_key = api_key
        self.endpoint = endpoint

    def _make_request(self, data, headers=None, method='POST'):
        """Make a generic HTTP request, can be overridden by subclasses."""
        if method.upper() == 'POST':
            response = requests.post(self.endpoint, headers=headers, json=data)
        elif method.upper() == 'GET':
            response = requests.get(self.endpoint, headers=headers, params=data)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")

        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def inference(self, data):
        """Perform an inference operation. This should be implemented by subclasses."""
        raise NotImplementedError("This method should be implemented by subclasses.")


class OpenAIModelInference(BaseModelInference):
    def __init__(self, api_key):
        super().__init__(api_key=api_key, endpoint="https://api.openai.com/v1/completions")
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def inference(self, prompt, model="text-davinci-003", max_tokens=150, temperature=0.5):
        """Generate text using the OpenAI model."""
        data = {
            'model': model,
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature
        }
        return self._make_request(data, headers=self.headers)

# Example usage
if __name__ == "__main__":
    api_key = 'your_api_key_here'
    openai_model = OpenAIModelInference(api_key)
    prompt = "Once upon a time in a land far, far away..."
    result = openai_model.inference(prompt)
    print(result)
