# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DocuTranslate is a Python-based document translation tool powered by Large Language Models. It supports translating various file formats (PDF, DOCX, XLSX, MD, TXT, JSON, EPUB, SRT, ASS, HTML) while preserving formatting. The project provides both a Web UI/API and programmatic SDK.

## Development Commands

```bash
# Install dependencies
uv sync

# Install with docling PDF parser support
uv sync --extra docling

# Run the Web UI (default port 8010)
uv run docutranslate -i

# Run on custom port
uv run docutranslate -i -p 8011

# Check version
uv run docutranslate --version
```

## Architecture

### Core Concept: Workflow Pattern

The central abstraction is **Workflow** - each file type has its own workflow class that orchestrates the entire translation pipeline:

```
File → [Converter] → Intermediate Representation → [Translator] → Translated IR → [Exporter] → Output
```

**Workflow classes** (`docutranslate/workflow/`):
- `MarkdownBasedWorkflow` - PDF, DOCX, MD, images → converts to Markdown first
- `TXTWorkflow`, `JsonWorkflow`, `DocxWorkflow`, `XlsxWorkflow`, `SrtWorkflow`, `EpubWorkflow`, `HtmlWorkflow`, `AssWorkflow` - format-specific workflows

Each workflow has:
- A `*Config` dataclass for configuration
- `read_path()` / `read_bytes()` to load input
- `translate()` / `translate_async()` for translation
- `export_to_*()` / `save_as_*()` for output

### Key Components

**Converters** (`docutranslate/converter/`):
- `x2md/` - Convert various formats to Markdown (docling, minerU engines for PDF)
- `x2xlsx/` - CSV to XLSX conversion

**Translators** (`docutranslate/translator/ai_translator/`):
- Format-specific translators that call LLM APIs
- All inherit from `AiTranslator` base class
- Support OpenAI-compatible APIs with configurable `base_url`, `api_key`, `model_id`

**Exporters** (`docutranslate/exporter/`):
- Convert translated intermediate representation to output formats
- Each format has its own exporter (md2html, docx2docx, xlsx2xlsx, etc.)

**Intermediate Representations** (`docutranslate/ir/`):
- `Document` - base class wrapping file content
- `MarkdownDocument` - specialized for markdown with image attachments

**Agents** (`docutranslate/agents/`):
- `GlossaryAgent` - auto-generates translation glossaries
- `MarkdownAgent` / `SegmentsAgent` - handle text chunking and LLM calls

### Web Application

`docutranslate/app.py` - FastAPI application providing:
- REST API for translation tasks
- Web UI at root path
- Swagger docs at `/docs`

### Configuration Pattern

All configuration uses dataclasses with `@dataclass(kw_only=True)`. Nested configs compose to form workflow configs:

```python
workflow_config = MarkdownBasedWorkflowConfig(
    convert_engine="mineru",
    converter_config=ConverterMineruConfig(...),
    translator_config=MDTranslatorConfig(...),
    html_exporter_config=MD2HTMLExporterConfig(...)
)
```

### PDF Parsing Engines

- `mineru` - Online API (recommended, requires token from mineru.net)
- `docling` - Local parsing (requires `docutranslate[docling]` install)

## Environment Variables

- `DOCUTRANSLATE_PORT` - Web server port (default: 8010)
- `DOCUTRANSLATE_CACHE_NUM` - PDF parsing cache size (default: 10)
- `HF_ENDPOINT` - Hugging Face mirror for docling models
