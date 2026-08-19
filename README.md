#  ResearchMind — AI Multi-Agent Research Assistant

ResearchMind is a **multi-agent AI research assistant** that automatically searches the web, extracts detailed information from relevant sources, generates a structured research report, and evaluates the generated report using an AI critic.

The application provides a Streamlit interface where users can enter any research topic and run the complete research pipeline with a single click.

---

## 🚀 Features

* 🔎 **Web Search Agent** — Searches for recent and reliable information using Tavily.
* 📄 **Reader Agent** — Selects a relevant source and scrapes its content for deeper research.
* ✍️ **Writer Chain** — Generates a structured and professional research report.
* 🧐 **Critic Chain** — Reviews the generated report, identifies strengths and weaknesses, and provides a score.
* 🖥️ **Streamlit Web Interface** — Provides an interactive interface for running the research pipeline.
* 📥 **Report Download** — Allows users to download the generated research report as a Markdown file.
* 🤖 **Multi-Agent Architecture** — Divides the research workflow into specialized AI components.

---

## 🏗️ Architecture

The research workflow consists of four main stages:

```text
                 ┌─────────────────────┐
                 │    User enters      │
                 │   Research Topic    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Search Agent     │
                 │  Tavily Web Search  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Reader Agent     │
                 │  Web Scraping       │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Writer Chain     │
                 │  Research Report    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Critic Chain     │
                 │ Review & Score      │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Final Report +      │
                 │ Critic Feedback     │
                 └─────────────────────┘
```

## The Search Agent gathers information, the Reader Agent performs deeper extraction from a selected URL, the Writer creates the report, and the Critic evaluates the final result.

## 🛠️ Tech Stack

### AI & LLM

* Python
* LangChain
* LangChain Agents
* Groq
* Llama 3.1 8B Instant

### Search & Web Scraping

* Tavily API
* Requests
* BeautifulSoup
* lxml

### Frontend

* Streamlit
* HTML
* CSS

### Environment & Utilities

* python-dotenv
* Pydantic
* aiohttp
* pandas
* tiktoken
* Rich
* Tenacity

The project dependencies are listed in `requirements.txt`.

---

## 📁 Project Structure

```text
ResearchMind/
│
├── app.py
├── agents.py
├── pipeline.py
├── tools.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

### `app.py`

Contains the Streamlit application and user interface. It accepts a research topic and displays the progress and results of the four-stage pipeline.

### `agents.py`

Defines:

* Search Agent
* Reader Agent
* Writer Chain
* Critic Chain

The Search and Reader agents are created using LangChain agents, while the Writer and Critic use prompt-based chains.

### `pipeline.py`

Provides the complete command-line research pipeline:

```text
Search → Read → Write → Critic
```

It accepts a research topic and returns the research state containing search results, scraped content, generated report, and critic feedback.

### `tools.py`

Contains the two main tools:

* `web_search()` — searches the web using Tavily.
* `scrape_url()` — retrieves and cleans webpage content using Requests and BeautifulSoup.

---

## ⚙️ How It Works

### 1. Enter a Research Topic

The user enters a topic such as:

```text
Quantum computing breakthroughs in 2025
```

The Streamlit interface then starts the research pipeline.

### 2. Search Agent

The Search Agent uses Tavily to find recent and reliable information related to the topic.

### 3. Reader Agent

The Reader Agent receives the search results, selects a relevant URL, and scrapes it for deeper content.

### 4. Writer Chain

The Writer combines the search results and scraped content and generates a structured report containing:

* Introduction
* Key Findings
* Conclusion
* Sources

The writer prompt requires at least three well-explained key findings.

### 5. Critic Chain

The Critic reviews the generated report and provides:

* Score out of 10
* Strengths
* Areas to Improve
* One-line Verdict

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
TAVILY_API_KEY="your_tavily_api_key"
GROQ_API_KEY="your_groq_api_key"
```

The application loads these environment variables using `python-dotenv`.

**Important:** Never upload your real API keys to GitHub.

Add `.env` to your `.gitignore`:

```gitignore
.env
```

---

## 💻 Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ResearchMind.git
cd ResearchMind
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API keys

Create a `.env` file:

```env
TAVILY_API_KEY="your_tavily_api_key"
GROQ_API_KEY="your_groq_api_key"
```

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## 🖥️ Usage

1. Launch the Streamlit application.
2. Enter a research topic.
3. Click **Run Research Pipeline**.
4. The Search Agent gathers information.
5. The Reader Agent extracts deeper content.
6. The Writer generates the research report.
7. The Critic evaluates the report.
8. Review the final report and critic feedback.
9. Download the report as a `.md` file.

---

## 📊 Example Topics

You can try topics such as:

```text
LLM agents in 2025
```

```text
CRISPR gene editing
```

```text
Fusion energy progress
```

The application also includes these example topics in the Streamlit interface.

---

## 🎯 Project Objective

The goal of ResearchMind is to demonstrate how **multiple specialized AI agents can collaborate to automate a complete research workflow**.

Instead of relying on a single LLM response, the system separates the process into specialized stages for:

**Searching → Reading → Writing → Critiquing**

This architecture makes the research process more structured and modular.


## ⭐ If you find this project useful

Give the repository a ⭐ on GitHub!
