def get_reply(prompt: str, model: str | None = None, temperature: float | None = None, max_tokens: int | None = None, system: str | None = None) -> str:
    """
    Generate a reply using a local Ollama model.
    - model: e.g., "deepseek-r1:7b" (defaults to OLLAMA_MODEL env or "llama3.1")
    - temperature, max_tokens, system are optional and may be ignored by some models.
    - On any error, return a short fallback string (do NOT raise).
    """
    try:
        import os, requests, json
        base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        mdl = model or os.getenv("OLLAMA_MODEL", "llama3.1")
        payload = {
            "model": mdl,
            "prompt": prompt if not system else f"System: {system}\n\nUser: {prompt}",
            "options": {}
        }
        if temperature is not None:
            payload["options"]["temperature"] = float(temperature)
        if max_tokens is not None:
            payload["options"]["num_predict"] = int(max_tokens)

        r = requests.post(f"{base}/api/generate", json=payload, timeout=120)
        r.raise_for_status()

        # /api/generate can stream lines; if not streaming, it returns a single JSON.
        text = []
        try:
            data = r.json()
            if "response" in data:
                return data["response"]
        except Exception:
            # Fallback: treat as line-delimited JSON stream
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if "response" in obj:
                        text.append(obj["response"])
                except Exception:
                    continue
            if text:
                return "".join(text)

        return "(No reply)"
    except Exception as e:
        return f"(Model offline: {e})"
import os, requests, json

def get_reply(prompt: str, model: str | None = None, temperature: float | None = None, max_tokens: int | None = None, system: str | None = None) -> str:
    """
    Generate a reply using a local Ollama model.
    - model: e.g., "deepseek-r1:7b" (defaults to OLLAMA_MODEL env or "llama3.1")
    - temperature, max_tokens, system are optional and may be ignored by some models.
    - On any error, return a short fallback string (do NOT raise).
    """
    try:
        base = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        mdl = model or os.getenv("OLLAMA_MODEL", "llama3.1")
        payload = {
            "model": mdl,
            "prompt": prompt if not system else f"System: {system}\n\nUser: {prompt}",
            "options": {}
        }
        if temperature is not None:
            payload["options"]["temperature"] = float(temperature)
        if max_tokens is not None:
            payload["options"]["num_predict"] = int(max_tokens)

        r = requests.post(f"{base}/api/generate", json=payload, timeout=120)
        r.raise_for_status()

        # /api/generate can stream lines; if not streaming, it returns a single JSON.
        text = []
        try:
            data = r.json()
            if "response" in data:
                return data["response"]
        except Exception:
            # Fallback: treat as line-delimited JSON stream
            for line in r.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if "response" in obj:
                        text.append(obj["response"])
                except Exception:
                    continue
            if text:
                return "".join(text)

        return "(No reply)"
    except Exception as e:
        return f"(Model offline: {e})"
