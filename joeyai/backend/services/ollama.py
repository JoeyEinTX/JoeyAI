import requests
from .config import Config

OLLAMA_URL = Config.OLLAMA_URL

def generate(model: str, prompt: str) -> str:
	resp = requests.post(f"{OLLAMA_URL}/api/generate", json={
		"model": model,
		"prompt": prompt,
		"stream": False
	})
	if resp.status_code != 200:
		raise Exception(f"Ollama error: {resp.status_code} {resp.text}")
	data = resp.json()
	return data.get("response", "")
