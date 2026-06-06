# Static Site Generator

A custom static site generator written in Python that converts Markdown content into a fully styled HTML website.

## Features

- Converts Markdown to HTML with support for headings, paragraphs, bold, italic, inline code, code blocks, blockquotes, ordered lists, unordered lists, links, and images
- Recursive page generation — mirrors the `content/` directory structure into `docs/`
- Configurable base path for deployment to subdirectory hosts (e.g. GitHub Pages)
- Static asset copying from `static/` to the output directory

## Project Structure

```
.
├── content/          # Markdown source files
│   ├── index.md
│   ├── blog/
│   │   ├── glorfindel/index.md
│   │   ├── majesty/index.md
│   │   └── tom/index.md
│   └── contact/index.md
├── static/           # Static assets copied as-is
│   ├── index.css
│   └── images/
├── src/              # Python source
│   ├── main.py
│   ├── generate_page.py
│   ├── markdown_blocks.py
│   ├── inline_markdown.py
│   ├── textnode.py
│   ├── htmlnode.py
│   ├── leafnode.py
│   ├── parentnode.py
│   └── copy_static.py
├── docs/             # Generated output (served by GitHub Pages)
├── template.html     # HTML shell with {{ Title }} and {{ Content }} placeholders
├── main.sh           # Local development server
└── build.sh          # Production build for GitHub Pages
```

## Usage

### Local development

```bash
./main.sh
```

Builds the site with basepath `/` into `docs/`, then serves it at `http://localhost:8888`.

### Production build

```bash
./build.sh
```

Builds the site with basepath `/static/` for GitHub Pages deployment.

### Run tests

```bash
./test.sh
```

## How it works

1. `static/` is copied to `docs/` (existing `docs/` is wiped first for a clean build)
2. Every `.md` file under `content/` is converted to HTML using `template.html` and written to the matching path under `docs/`
3. All local `href="/` and `src="/` references in the generated HTML are rewritten to use the configured basepath
