
import os
import time

from dotenv import load_dotenv
from google import genai
from groq import Groq
import json
import sys


# Load environment variables
load_dotenv()

# Pricing in USD per 1 million tokens
PRICING = {
    "gemini": {
        "input": 0.30,
        "output": 2.50
    },
    "groq": {
        "input": 0.075,
        "output": 0.30
    }
}


def calculate_cost(result):
    """Calculate API cost using actual token counts."""

    provider = result["provider"]

    prices = PRICING[provider]

    input_price = prices["input"]
    output_price = prices["output"]

    input_cost = (
        result["input_tokens"] * input_price
    ) / 1_000_000

    output_cost = (
        result["output_tokens"] * output_price
    ) / 1_000_000

    total_cost = input_cost + output_cost

    result["input_price_per_m"] = input_price
    result["output_price_per_m"] = output_price
    result["cost_usd"] = total_cost

    return result



def display_comparison(results):
    """Display provider metrics in a comparison table."""

    print("\n" + "=" * 90)
    print("              TWO PROVIDER COST COMPARISON")
    print("=" * 90)

    headers = [
        "Provider",
        "Input Tokens",
        "Output Tokens",
        "Seconds",
        "Cost (USD)"
    ]

    print(
        f"{headers[0]:<12}"
        f"{headers[1]:<16}"
        f"{headers[2]:<17}"
        f"{headers[3]:<13}"
        f"{headers[4]:<15}"
    )

    print("-" * 90)

    for result in results:
        print(
            f"{result['provider']:<12}"
            f"{result['input_tokens']:<16}"
            f"{result['output_tokens']:<17}"
            f"{result['seconds']:<13}"
            f"${result['cost_usd']:.8f}"
        )

    print("=" * 90)



def call_gemini(prompt):
    """Send a prompt to Gemini and return response and usage metrics."""

    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL")

    # Check configuration
    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing from .env")

    if not model:
        raise ValueError("GEMINI_MODEL is missing from .env")

    # Initialize Gemini client
    client = genai.Client(api_key=api_key)

    # Measure execution time
    start_time = time.perf_counter()

    response = client.models.generate_content(
        model=model,
        contents=prompt
    )
    
    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    end_time = time.perf_counter()

    # Extract actual token usage
    usage = response.usage_metadata

    if usage is None:
        raise RuntimeError("Gemini did not return token usage information.")

    result = {
        "provider": "gemini",
        "model": model,
        "reply": response.text,
        "input_tokens": usage.prompt_token_count,
        "output_tokens": usage.candidates_token_count,
        "seconds": round(end_time - start_time, 4)
    }

    return result



def call_groq(prompt):
    """Send a prompt to Groq and return response and usage metrics."""

    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL")

    # Check configuration
    if not api_key:
        raise ValueError("GROQ_API_KEY is missing from .env")

    if not model:
        raise ValueError("GROQ_MODEL is missing from .env")

    # Initialize Groq client
    client = Groq(api_key=api_key)

    # Measure execution time
    start_time = time.perf_counter()

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    end_time = time.perf_counter()

    # Extract actual token usage
    usage = response.usage

    if usage is None:
        raise RuntimeError("Groq did not return token usage information.")

    result = {
        "provider": "groq",
        "model": model,
        "reply": response.choices[0].message.content,
        "input_tokens": usage.prompt_tokens,
        "output_tokens": usage.completion_tokens,
        "seconds": round(end_time - start_time, 4)
    }

    return result



def save_results(results):
    """Save provider results to results.json."""

    required_fields = [
        "provider",
        "model",
        "reply",
        "input_tokens",
        "output_tokens",
        "input_price_per_m",
        "output_price_per_m",
        "cost_usd"
    ]

    json_results = []

    for result in results:
        json_results.append({
            field: result[field]
            for field in required_fields
        })

    with open("results.json", "w", encoding="utf-8") as file:
        json.dump(json_results, file, indent=4)

    print("\nResults successfully saved to results.json")








def main():
    """Run both providers and compare their results."""

    if len(sys.argv) < 2:
        print('Usage: uv run tracker.py "your prompt"')
        return

    prompt = " ".join(sys.argv[1:])

    providers = [
        ("Gemini", call_gemini),
        ("Groq", call_groq)
    ]

    results = []

    for provider_name, provider_function in providers:

        print(f"\nCalling {provider_name}...")

        try:
            result = provider_function(prompt)

            result = calculate_cost(result)

            results.append(result)

            print(f"\n========== {provider_name.upper()} RESPONSE ==========")
            print(result["reply"])

        except Exception as error:
            print(f"\n{provider_name} failed: {error}")

    if not results:
        print("\nNo provider returned a successful response.")
        return

    display_comparison(results)

    save_results(results)


if __name__ == "__main__":
    main()
