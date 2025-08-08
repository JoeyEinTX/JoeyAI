# JoeyAI

Local-first AI assistant for Jetson Orin Nano

## Features
- Single chat system
- Neon black/cyan theme
- SQLite + FTS5
- Local Ollama (deepseek-r1:7b)

## Jetson Setup
1. Install Python 3.10+
2. Install Ollama: https://ollama.com/download
3. Pull model: `ollama pull deepseek-r1:7b`
4. Clone repo & run `scripts/dev.sh`

## Running
- Development: `bash scripts/dev.sh`
- Production: `bash scripts/run.sh`

## Environment
See `.env.example` for config variables.

## License
MIT
