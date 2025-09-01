#!/bin/bash
set -e

# Setup function
setup() {
    echo "📦 Setting up Portfolio RAG API"
    
    # Install uv if not present
    if ! command -v uv &> /dev/null; then
        echo "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        source ~/.bashrc
    fi
    
    # Sync dependencies
    uv sync
    
    # Create .env if it doesn't exist
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "⚠️  Add your OPENAI_API_KEY to .env file"
    fi
    
    echo "✅ Setup complete!"
}

# Dev server function
dev() {
    echo "🚀 Starting development server"
    uv sync
    uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
}

# Test function
test() {
    echo "🧪 Running validation"
    uv sync --dev
    uv run python validate_setup.py
    uv run ruff check app/ --fix 2>/dev/null || echo "⚠️  ruff not available"
}

# Main command dispatcher
case "${1:-dev}" in
    setup)
        setup
        ;;
    test)
        test
        ;;
    dev|*)
        dev
        ;;
esac