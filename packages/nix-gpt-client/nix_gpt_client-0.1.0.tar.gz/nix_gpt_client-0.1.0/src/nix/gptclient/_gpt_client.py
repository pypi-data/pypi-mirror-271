import json
import openai
from pydantic import BaseModel
from ._types import GPTMessageRole, GPTSchemaType, GPTModel
from ._validate import GPTSessionConstructorSchema


class GPTClient:
    def __init__(self, model: GPTModel, top_p: float, presence_penalty: float, frequency_penalty: float,
                 temperature: float):
        GPTSessionConstructorSchema.model_validate({
            "model": model,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "temperature": temperature
        })

        self._model = model
        self._top_p = top_p
        self._presence_penalty = presence_penalty
        self._frequency_penalty = frequency_penalty
        self._temperature = temperature

        self._messages: dict = []
        self._ai_client: openai.OpenAI = openai.OpenAI()

    def add_message(self, role: GPTMessageRole, data: str | dict | list):
        data_in_json = json.dumps(data)
        self._messages.append({
            "role": role,
            "content": data_in_json
        })

    def clear_messages(self):
        self._messages = []

    def set_schema(self, schema: BaseModel, schema_type: GPTSchemaType):
        json_schema = json.dumps(schema.model_json_schema())
        self._messages.append({
            "role": "system",
            "content": f"{schema_type} JSON schema: {json_schema}"
        })

    def run(self):
        try:
            response = self._ai_client.chat.completions.create(
                messages=self._messages,
                model=self._model,
                temperature=self._temperature,
                top_p=self._top_p,
                presence_penalty=self._presence_penalty,
                frequency_penalty=self._frequency_penalty
            )
            if response.choices:
                return response.choices[0].message.content
            else:
                return None
        except openai.OpenAIError as error:
            raise error
