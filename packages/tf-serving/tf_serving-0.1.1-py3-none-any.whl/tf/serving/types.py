from pydantic import BaseModel

class ImagePreds(BaseModel):
  """Predictions of a single image
  - `preds[i], logprobs[i]`: one of the top paths word + logprobability, **with no order in particular**
  """
  preds: list[str]
  logprobs: list[float]

class TFSResponse(BaseModel):
  predictions: list[ImagePreds]
  