from pydantic import BaseModel, Field
from ._types import GPTModel


class GPTSessionConstructorSchema(BaseModel):
    model: GPTModel = Field(..., description="The model to use for the GPT session")
    top_p: float = Field(..., gt_or=0, lt_or=1, description="The top_p value for the GPT session")
    presence_penalty: float = Field(..., gt_or=0, lt_or=1, description="The presence_penalty value for the GPT session")
    frequency_penalty: float = Field(..., gt_or=0, lt_or=1, description="The frequency_penalty value for the GPT session")
    temperature: float = Field(..., gt_or=0, lt_or=1, description="The temperature value for the GPT session")
