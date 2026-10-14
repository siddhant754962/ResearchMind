# 🔬 ResearchMind — Multi-Agent AI Research Assistant

ResearchMind is a Streamlit application that turns a research topic into a structured report through a sequential AI workflow. It combines web search, webpage content extraction, report writing, and an AI-powered critique.

🌐 **Live Demo:** https://researchmind-sidd.streamlit.app/  
💻 **Source Code:** https://github.com/siddhant754962/ResearchMind

## ✨ Features

- **Search Agent:** Finds relevant web information using the Tavily Search API.
- **Reader Agent:** Uses the webpage-scraping tool to extract useful content from a selected source.
- **Writer Chain:** Organizes the collected research into a report with an introduction, key findings, conclusion, and sources.
- **Critic Chain:** Reviews the report, identifies strengths and improvements, and provides a score and verdict.
- **Intermediate Results:** Explore outputs from the research stages in the Streamlit interface.
- **Markdown Export:** Download the generated report as a Markdown file.

## 🔄 How It Works

```text
Research Topic
     ↓
Search Agent (Tavily)
     ↓
Reader Agent (Webpage Extraction)
     ↓
Writer Chain (Structured Report)
     ↓
Critic Chain (Review and Score)
     ↓
Report + Critique
     ↓
Download Report (.md)
```

The workflow is sequential: each stage uses information produced by earlier stages. The critique is intended to help assess the generated report; it does not guarantee that every claim is correct. Verify important claims against the original sources.

## 🧰 Tech Stack

- **Python** — application logic
- **LangChain** — agent and chain orchestration
- **OpenRouter** — access to the configured LLM
- **Tavily Search API** — web search
- **Requests & BeautifulSoup** — webpage retrieval and text extraction
- **Streamlit** — user interface
- **uv** — Python dependency and environment management

## 🏗️ Project Structure

```text
ResearchMind/
├── app.py          # Streamlit user interface and workflow execution
├── agents.py       # Search/reader agents and writer/critic chains
├── tools.py        # Tavily search and webpage scraping tools
├── pipline.py      # Reusable research pipeline (filename as in repository)
├── pyproject.toml  # Project metadata and dependencies
├── uv.lock         # Locked dependency versions, if present
└── .env            # Local API keys (create locally; do not commit)
```

## ⚙️ Getting Started

### Prerequisites

- Python **3.12 or newer**
- [uv](https://docs.astral.sh/uv/)
- An OpenRouter API key
- A Tavily API key

### 1. Clone the repository

```bash
git clone https://github.com/siddhant754962/ResearchMind.git
cd ResearchMind
```

### 2. Install dependencies

Install the dependencies declared in `pyproject.toml`:

```bash
uv sync
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
TAVILY_API_KEY=your_tavily_api_key
```

Replace the placeholder values with your own API keys. Never commit your `.env` file or expose API keys in source code, screenshots, or public logs.

### 4. Run the app

```bash
uv run streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open it in your browser.

## 🔐 Deployment Secrets

For Streamlit Community Cloud, add `OPENROUTER_API_KEY` and `TAVILY_API_KEY` in the app's **Settings → Secrets** section. Do not upload your local `.env` file.

## ⚠️ Notes and Limitations

- Search results and scraped page content depend on the availability and accessibility of external websites.
- Some websites may block automated requests or return incomplete content.
- LLM-generated reports can contain errors or unsupported claims. Check the cited sources before relying on the report.
- API usage may be subject to provider rate limits, quotas, and pricing.
- The critic provides model-generated feedback, not an independent guarantee of factual accuracy.

## 🎯 What This Project Demonstrates

- Building tool-enabled AI agents
- Connecting LLMs to external search and webpage tools
- Orchestrating a multi-stage LLM workflow
- Designing prompts and parsing model outputs
- Managing application state and API credentials
- Building and deploying an interactive AI application

## 🚀 Future Improvements

Potential directions for future development:

- Add source-level citations linked directly to individual findings.
- Compare information across multiple sources rather than relying on one selected page.
- Add retrieval-augmented generation (RAG) for persistent research collections.
- Introduce automated factuality and citation checks.
- Add unit tests and more robust handling for network and model errors.

## 🤝 Feedback

Suggestions, issue reports, and constructive feedback are welcome. Try the [live demo](https://researchmind-sidd.streamlit.app/) or explore the [GitHub repository](https://github.com/siddhant754962/ResearchMind).

---

Built as a portfolio project to explore **Generative AI, LangChain, and multi-agent workflows**.
