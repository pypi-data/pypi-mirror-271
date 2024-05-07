from enum import Enum


class GPTMessageRole(str, Enum):
    system = "system",
    user = "user"


class GPTSchemaType(str, Enum):
    input = "Input"
    output = "Output"


class GPTModel(str, Enum):
    GPT_3_5_TURBO = "gpt-3.5-turbo"
