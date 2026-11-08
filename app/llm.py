import os

from dotenv import load_dotenv
from groq import Groq
from groq import APIConnectionError, APIStatusError, RateLimitError

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY is missing. Check your .env configuration."
    )

client = Groq(api_key=api_key)

MODEL_NAME = "openai/gpt-oss-120b"



def generate_response(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            max_completion_tokens=1024,
        )

        if not response.choices:
            raise RuntimeError("The LLM returned no response choices.")

        generated_text = response.choices[0].message.content

        if not isinstance(generated_text, str) or not generated_text.strip():
            raise RuntimeError("The LLM returned an empty or invalid response.")

        return generated_text.strip()

    except RateLimitError as e:
        raise RuntimeError("The LLM service rate limit was exceeded.") from e

    except APIConnectionError as e:
        raise RuntimeError("Unable to connect to the LLM service.") from e

    except APIStatusError as e:
        raise RuntimeError("The LLM service returned an API error.") from e
