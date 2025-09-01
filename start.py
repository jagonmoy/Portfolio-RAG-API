#!/usr/bin/env python3

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

def main():
    """Start the Portfolio RAG API server"""
    print("🚀 Starting Portfolio RAG API")
    print("📋 Recommended: Use './scripts/dev.sh' for development")
    print("=" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True,
        log_level="info"
    )

if __name__ == "__main__":
    main()