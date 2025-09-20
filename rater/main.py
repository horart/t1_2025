import common.llmclient as llmclient
from fastapi import FastAPI

from .prompts import REVIEW_PROMPT, SELF_REVIEW_PROMPT
from .models import ReviewRequestModel, ReviewResponseModel


app = FastAPI()

review_client = llmclient.GenerativeLLM(REVIEW_PROMPT)
self_review_client = llmclient.GenerativeLLM(SELF_REVIEW_PROMPT)


@app.post("/review/")
def review(review_model: ReviewRequestModel) -> ReviewResponseModel:
    return ReviewResponseModel(review=review_client.prompt(review_model.body))

@app.post("/self-review/")
def selfreview(review_model: ReviewRequestModel) -> ReviewResponseModel:
    return ReviewResponseModel(review=self_review_client.prompt(review_model.body))