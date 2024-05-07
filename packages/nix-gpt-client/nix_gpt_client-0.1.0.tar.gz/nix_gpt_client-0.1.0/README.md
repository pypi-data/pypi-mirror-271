# nix-gpt-client

nix-gpt-client is a simple Python library for working with the GPT API. It uses Pydantic to add input and output
schemas, allowing you to manage data structures with ease.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

To install `nix-gpt-client`, you can use `pip`. Python 3.11 or higher is required.

```bash
pip install nix-gpt-client
```

## Usage

1. If you want to use typing, create Pydantic schemas for input and output data structures:

```python
from datetime import datetime
from pydantic import BaseModel, Field


class GPTInput(BaseModel):
    time: datetime = Field(description="The current time")
    timezone: str = Field(description="The timezone of the current time")
    target_timezone: str = Field(description="The target timezone")


class GPTOutput(BaseModel):
    target_time: datetime = Field(description="The target time")
```

2. Then create GPTClient object, set schemas, and add system message:

```python
from nix.gptclient import GPTClient, GPTModel, GPTMessageRole, GPTSchemaType

gpt_client = GPTClient(
    model=GPTModel.GPT_3_5_TURBO,
    top_p=0.5,
    presence_penalty=0,
    frequency_penalty=0,
    temperature=0)

gpt_client.set_schema(GPTInput, GPTSchemaType.input)
gpt_client.set_schema(GPTOutput, GPTSchemaType.output)

gpt_client.add_message(GPTMessageRole.system, """
Take from \'Input JSON schema\' the fields 'time', 'timezone', and 'target_timezone'.
Then generate an Output JSON schema with the field 'target_time', which represents the given 'time' converted 
from 'timezone' to 'target_timezone'.
""")
```

3. Add data like user message and call `run` method to get the response:

```python
input_data = {
    "time": datetime.now().__str__(),
    "timezone": "UTC",
    "target_timezone": "America/New_York"
}

gpt_client.add_message(GPTMessageRole.user, input_data)

response = json.loads(gpt_client.run())
```

4. The response will be:

```json
{
  "target_time": "2024-05-06T13:04:38.621713-04:00"
}
```

Full example:

```python
import json
from datetime import datetime
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from src import GPTClient, GPTModel, GPTMessageRole, GPTSchemaType

load_dotenv()


class GPTInput(BaseModel):
    time: datetime = Field(description="The current time")
    timezone: str = Field(description="The timezone of the current time")
    target_timezone: str = Field(description="The target timezone")


class GPTOutput(BaseModel):
    target_time: datetime = Field(description="The target time")


gpt_client = GPTClient(
    model=GPTModel.GPT_3_5_TURBO,
    top_p=0.5,
    presence_penalty=0,
    frequency_penalty=0,
    temperature=0)

gpt_client.set_schema(GPTInput, GPTSchemaType.input)
gpt_client.set_schema(GPTOutput, GPTSchemaType.output)

gpt_client.add_message(GPTMessageRole.system, """
Take from \'Input JSON schema\' the fields 'time', 'timezone', and 'target_timezone'.
Then generate an Output JSON schema with the field 'target_time', which represents the given 'time' converted 
from 'timezone' to 'target_timezone'.
""")

input_data = {
    "time": datetime.now().__str__(),
    "timezone": "UTC",
    "target_timezone": "America/New_York"
}

gpt_client.add_message(GPTMessageRole.user, input_data)

response = json.loads(gpt_client.run())

print(response)
```

## License

This project is licensed under the MIT License. See the LICENSE file for more details.