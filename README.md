# MarketIntel MCP Server

A lightweight Model Context Protocol (MCP) server for market research and competitive intelligence. It exposes tools to gather company overviews, competitor lists, product portfolios, pricing snapshots, and recent news using Tavily search APIs.

## Features

- Company overview research
- Competitor identification and landscape analysis
- Product portfolio mapping
- Pricing and tier analysis
- Recent news and market pulse summaries
- Prebuilt prompt templates for competitor brief generation

## Tech Stack

- Python 3.13+
- FastMCP
- Tavily API
- uv for dependency management

## Prerequisites

- Python 3.13 or later
- uv installed
- A Tavily API key

## Installation

```bash
cd /path/to/MCP_DEMO_1
uv sync
```

## Configuration

Create a `.env` file in the project root with your Tavily API key:

```env
TAVILY_API_KEY=your_api_key_here
```

## Running the Server

```bash
cd /path/to/MCP_DEMO_1
source .venv/bin/activate
python server.py
```

The server starts an MCP SSE endpoint and exposes the available tools/resources.

## Available Tools

- `company_overview`
- `list_competitors`
- `product_portfolio`
- `pricing_snapshot`
- `recent_news_pulse`
- `competitor_analysis_prompt`

## Project Structure

```text
.
├── server.py
├── pyproject.toml
├── README.md
├── src/
│   └── mcp_demo_1/
└── .env
```

## License

This project is provided as-is for demo and development purposes.

## Notes

This repository is intended as a market-intelligence MCP demo and may require a valid Tavily subscription for research queries to work successfully.
