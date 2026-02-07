# Paper Search Tool

A Streamlit-based academic paper search and analysis tool that supports:
- **Nature Journal crawling** with cookie-based authentication
- **Semantic Scholar API** for IEEE, Science, conference papers
- **DeepSeek translation** for batch abstract translation
- Keyword filtering (OR/AND logic)
- CSV export with deduplication

## Prerequisites

```bash
pip install streamlit requests pandas beautifulsoup4 openai pyyaml
```

## Configuration

Set your DeepSeek API key as an environment variable:
```bash
export DEEPSEEK_API_KEY="your-api-key-here"
```

## Usage

```bash
streamlit run paper_search.py
```

## Features

### Online Search Mode
1. Configure journals in the sidebar (Nature series + API journals)
2. Enter keywords (use `/` for OR, `;` for AND groups)
3. Optional: Configure proxy settings for network access
4. Click "Start Search" to begin parallel retrieval

### Result Analysis Mode
1. Upload 1-2 CSV files for analysis
2. Filter by journal, year range, and keywords
3. Batch translate abstracts to Chinese
4. Export filtered results

## Proxy Setup (Optional)
- Supports Clash API for automatic IP rotation
- Manual proxy pool configuration
- Cookie authentication for Nature subscriptions
