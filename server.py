import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from fastmcp import FastMCP
from tavily import TavilyClient

def _load_env_file() -> None:
    env_file = Path(__file__).with_name(".env")
    if not env_file.is_file():
        return

    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        os.environ.setdefault(name.strip(), value)


_load_env_file()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("Please set the TAVILY_API_KEY environment variable before starting the server.")

tavily = TavilyClient(api_key=TAVILY_API_KEY)
mcp = FastMCP(name="MarketIntel")

def _tsearch(query: str, **kw) -> Dict[str, Any]:
    resp = tavily.search(query=query, **kw)
    return {
        "query_used": query,
        "answer": resp.get("answer"),
        "results": [
            {k: r.get(k) for k in ("title", "url", "content", "score", "published_date")}
            for r in resp.get("results", [])
        ],
    }

@mcp.resource("resource://market/topics")
def market_topics() -> List[str]:
    return [
        "Competitor overview", "Pricing snapshot",
        "Product portfolio mapping", "Market landscape",
        "Feature comparison", "Regional GTM"
    ]

@mcp.tool(annotations={"title": "Company Overview"})
def company_overview(name: str, region: Optional[str] = None, max_results: int = 8):
    reg = f" in {region}" if region else ""
    q = f"Company overview of {name}{reg}: founding, HQ, products, business model, recent news"
    return _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")

@mcp.tool(annotations={"title": "List Competitors"})
def list_competitors(name: str, category: Optional[str] = None, region: Optional[str] = None, max_results: int = 10):
    cat = f" in {category}" if category else ""
    reg = f" in {region}" if region else ""
    q = f"Top competitors of {name}{cat}{reg}; include upstart challengers"
    return _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")

@mcp.tool(annotations={"title": "Product Portfolio Map"})
def product_portfolio(company: str, focus_keywords: Optional[List[str]] = None, max_results: int = 12):
    kws = f" ({', '.join(focus_keywords)})" if focus_keywords else ""
    q = f"{company} product portfolio{kws}: product list, suites, tiers, segments"
    search_res = _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")
    product_like = [r["url"] for r in search_res.get("results", []) if r.get("url") and any(tok in r["url"].lower() for tok in ["product", "products", "pricing", "solutions"])]
    extracted: Dict[str, Any] = {}
    if product_like:
        try:
            extracted = tavily.extract(urls=product_like[:10], extract_depth="advanced", format="markdown")  # content extraction :contentReference[oaicite:6]{index=6}
        except Exception as e:
            extracted = {"error": f"extract_failed: {e}"}
    return {"search": search_res, "extracted": extracted}

@mcp.tool(annotations={"title": "Pricing Snapshot"})
def pricing_snapshot(product_or_company: str, region: Optional[str] = None, currency_hint: Optional[str] = None, max_results: int = 10):
    reg = f" in {region}" if region else ""
    cur = f" in {currency_hint}" if currency_hint else ""
    q = f"Pricing for {product_or_company}{reg}{cur}: list price, tiers, billing cycles, discounts, hidden fees"
    return _tsearch(q, max_results=max_results, search_depth="advanced", include_answer="advanced")

@mcp.tool(annotations={"title": "Recent News Pulse"})
def recent_news_pulse(company: str, days: int = 30, max_results: int = 10):
    q = f"Recent news about {company}: funding, acquisitions, launches, leadership"
    return _tsearch(q, topic="news", days=days, max_results=max_results, search_depth="advanced", include_answer="advanced")

@mcp.prompt
def competitor_analysis_prompt(company: str, region: str = "", category: str = "") -> str:
    return (
        f"Build a competitor brief for '{company}'"
        + (f" in '{region}'" if region else "")
        + (f" within '{category}'" if category else "")
        + ". Steps: 1) Company Overview 2) List Competitors 3) Portfolio & Pricing 4) News Pulse 5) SWOT+Five Forces."
    )

def main():
    print("\n Starting MarketIntel MCP server...")
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()