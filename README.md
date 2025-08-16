# Academic Paper Discovery Platform

This repository provides an educational playground for discovering academic
papers and visualising their underlying concepts.  The project demonstrates how
Clean Architecture and SOLID principles can be applied in a full‑stack
application.  Each module aims to teach by example and is documented with
pedagogical comments explaining the *why* behind implementation choices.

## Features
- **Interactive concept graph** built with Next.js and D3.js.
- **Python backend** that aggregates papers from multiple sources.
- **Extensive documentation and comments** to support self‑guided learning.

## Getting Started
### Prerequisites
- Python 3.12+
- Node.js 18+
- npm 9+

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install front‑end dependencies
npm install
```

### Development
```bash
# Run the static front‑end in development mode
npm run dev

# Build production assets
npm run build
```
The concept graph reads its data from `/public/data/concept-graph-data.json`.
The `fetchGraphData` service loads this file using an absolute path (`/data/...`)
so the application functions correctly whether served from the domain root or a
sub‑path such as GitHub Pages.

## Testing
```bash
# JavaScript/TypeScript tests
npm test

# Python tests
python -m pytest tests/
```

## Repository Layout
```
components/   – React components for the web interface
pages/        – Next.js route definitions
services/     – Front‑end services (e.g., data loading)
types/        – Shared TypeScript interfaces
src/          – Python application code
```

## Contributing
Contributions are welcome.  Please focus on maintainability, clear code and
educational value.  Open an issue or pull request with a description of your
changes and any relevant documentation or tests.

## License
MIT
