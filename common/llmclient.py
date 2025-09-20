import os
from openai import OpenAI

API_KEY = os.environ['LLM_API_KEY']
BASE_URL = "https://llm.t1v.scibox.tech/v1"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

class GenerativeLLM:

    history: list[dict]
    kwargs: dict
    save_context: bool

    def __init__(self, system_prompt: str, *, save_context=False, **kwargs):
        self.kwargs = kwargs
        self.history = [{
            "role": "system",
            "content": system_prompt,
        }]
        self.save_context = save_context

    def prompt(self, prompt: str) -> str:
        prompt_obj = {
            "role": "user",
            "content": prompt,
        }
        resp = client.chat.completions.create(
            model="Qwen2.5-72B-Instruct-AWQ",
            messages=self.history + [prompt_obj],
            temperature=0.7,
        )
        text_resp = resp.choices[0].message.content
        if self.save_context:
            self.history.append(prompt_obj)
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