# Two-Provider AI Cost Tracker

A lightweight Python-based tool to compare AI API usage, response times, and estimated costs across two LLM providers: **Google Gemini** and **Groq**.

The project sends the same prompt to both providers, retrieves their responses, extracts actual token usage, calculates API costs using configurable pricing rates, and presents the results in a comparison table.

## Features

- **Dual-provider comparison:** Execute the same prompt using Google Gemini and Groq.
- **Token tracking:** Capture actual input and output token counts from API usage metadata.
- **Cost calculation:** Calculate estimated API costs using provider-specific input and output token pricing.
- **Execution time measurement:** Measure how long each provider takes to generate a response.
- **Response comparison:** Display both AI-generated responses.
- **JSON export:** Automatically save usage statistics and calculated costs to `results.json`.
- **Environment-based configuration:** Securely manage API keys and model names using environment variables.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.12+ | Core programming language |
| Google Gen AI SDK | Gemini API integration |
| Groq SDK | Groq API integration |
| python-dotenv | Environment variable management |
| JSON | Storing comparison results |
| uv | Python dependency and project management |

## Project Structure

```text
two-provider-cost-tracker/
│
├── src/
│   └── two_provider_cost_tracker/
│
├── tracker.py
├── results.json
├── pyproject.toml
├── uv.lock
├── .python-version
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Raaid-Yousuf/two-provider-cost-tracker.git

cd two-provider-cost-tracker
```

### 2. Install Dependencies

Make sure Python 3.12 or later and [uv](https://docs.astral.sh/uv/) are installed.

Install the project dependencies:

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=your_gemini_model

# Groq Configuration
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
```

Replace the placeholders with your actual API credentials and model identifiers.

**Important:** Never commit your `.env` file or expose your API keys publicly.

## Usage

Run the tracker with a prompt:

```bash
uv run tracker.py "Explain how Retrieval-Augmented Generation works."
```

The application will:

1. Send the prompt to Google Gemini.
2. Retrieve the generated response and token usage.
3. Send the same prompt to Groq.
4. Retrieve its response and token usage.
5. Calculate the estimated API cost for each provider.
6. Display a comparison of both providers.
7. Save the results to `results.json`.

## Cost Calculation

The tracker calculates costs using actual input and output token counts.

The formula is:

```text
Input Cost =
(Input Tokens × Input Price per Million) / 1,000,000

Output Cost =
(Output Tokens × Output Price per Million) / 1,000,000

Total Cost = Input Cost + Output Cost
```

The current pricing configuration in `tracker.py` is:

| Provider | Input Cost (per 1M tokens) | Output Cost (per 1M tokens) |
|---|---:|---:|
| Gemini | $0.30 | $2.50 |
| Groq | $0.075 | $0.30 |

**Note:** These are the pricing values currently configured in the project, not guaranteed current provider prices. Update them according to the selected models' official pricing.

## Results

The application displays a comparison table containing:

- Provider name
- Input tokens
- Output tokens
- Execution time (seconds)
- Estimated API cost (USD)

It also generates a `results.json` file containing the provider, model, generated response, token usage, pricing rates, and calculated costs.

## Error Handling

The application includes basic error handling for:

- Missing API credentials.
- Missing model configuration.
- Failed provider requests.
- Empty Gemini responses.
- Missing token usage metadata.
- Individual provider failures.

If one provider fails, the tracker can still display and save the successful provider's results.

## Future Improvements

Potential enhancements include:

- Support for additional LLM providers.
- Historical cost tracking across multiple executions.
- Interactive dashboards and visual analytics.
- Model-to-model benchmarking.
- Exporting reports to CSV.
- Configurable pricing through external configuration files.

## Author

**Raaid Yousuf**

GitHub: [@Raaid-Yousuf](https://github.com/Raaid-Yousuf)

---

If you find this project useful, consider giving the repository a ⭐ on GitHub!
