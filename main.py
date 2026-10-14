import json
import re
from typing import get_type_hints, List, Dict, Optional, Union

class TypeLLM:
    def __init__(self, llm_func):
        self.llm_func = llm_func

    def __call__(self, prompt: str, output_type=None):
        raw = self.llm_func(prompt)
        if output_type is None:
            return raw
        return self._validate(raw, output_type)

    def _validate(self, raw: str, output_type):
        # Trim and parse based on type hint
        if output_type == int:
            return int(raw.strip())
        elif output_type == float:
            return float(raw.strip())
        elif output_type == str:
            return raw.strip()
        elif output_type == bool:
            return raw.strip().lower() in ['true', '1', 'yes']
        elif output_type == List[str]:
            return json.loads(raw)
        elif output_type == Dict[str, str]:
            return json.loads(raw)
        else:
            raise ValueError(f"Unsupported type: {output_type}")

# Mock LLM function for demo (replace with real API call)
def mock_llm(prompt: str) -> str:
    if 'number' in prompt:
        return "42"
    elif 'list' in prompt:
        return '["a", "b"]'
    elif 'dict' in prompt:
        return '{"name": "Alice"}'
    elif 'bool' in prompt:
        return "true"
    else:
        return "default string"

# Demo usage
if __name__ == "__main__":
    tllm = TypeLLM(mock_llm)
    # Use type hints to enforce output types
    print(tllm("Give me a number", output_type=int))
    print(tllm("Give me a list", output_type=List[str]))
    print(tllm("Give me a dict", output_type=Dict[str, str]))
    print(tllm("Is it true?", output_type=bool))
    # Without type hint, returns raw
    print(tllm("Just a string"))
