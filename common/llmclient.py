import os
from openai import OpenAI

API_KEY = os.environ['LLM_API_KEY']
BASE_URL = "https://llm.t1v.scibox.tech/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

class GenerativeLLMContext:

    history: list[dict]
    kwargs: dict

    def __init__(self, system_prompt: str, **kwargs):
        self.kwargs = kwargs
        self.history = [{
            "role": "system",
            "content": system_prompt,
        }]

    def prompt(self, prompt: str) -> str:
        self.history.append({
            "role": "user",
            "content": prompt,
        })
        resp = client.chat.completions.create(
            model="Qwen2.5-72B-Instruct-AWQ",
            messages=self.history,
            temperature=0.7,
            top_p=0.9,
            max_tokens=256,
        )
        text_resp = resp.choices[0].message.content
        self.history.append({
            "role": "assistant",
            "content": text_resp,
        })
        return text_resp
    

class LLMEmbedder:
    def __init__(self):
        pass

    def embed(self, strings: list[str]):
        client = OpenAI(api_key="<YOUR_TOKEN>", base_url="https://llm.t1v.scibox.tech/v1")

        emb = client.embeddings.create(
            model="bge-m3",
            input=strings,
        )

        return emb