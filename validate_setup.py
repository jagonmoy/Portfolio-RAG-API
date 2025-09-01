#!/usr/bin/env python3

import sys
import os
from pathlib import Path

def validate_setup():
    print("🔍 Validating Portfolio RAG API Setup")
    print("=" * 50)
    
    # Check project structure
    print("\n📁 Checking project structure...")
    required_dirs = [
        "app", "app/api", "app/core", "app/services", "app/models",
        "data", "data/documents", "data/storage"
    ]
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ (missing)")
            return False
    
    # Check key files
    print("\n📄 Checking key files...")
    required_files = [
        "pyproject.toml", "app/main.py", "app/api/routes.py",
        "app/services/vector_store.py", "app/services/document_processor.py",
        "app/core/config.py", "app/models/schemas.py",
        ".env.example", "Dockerfile", "README.md"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (missing)")
            return False
    
    # Check imports
    print("\n🐍 Checking Python imports...")
    try:
        import llama_index
        print("✅ llama-index")
        
        import chromadb
        print("✅ chromadb")
        
        import fastapi
        print("✅ fastapi")
        
        from app.main import app
        print("✅ app.main")
        
        from app.services.vector_store import VectorStoreService
        print("✅ VectorStoreService")
        
        from app.services.document_processor import DocumentProcessor
        print("✅ DocumentProcessor")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Check environment setup
    print("\n🔧 Checking environment setup...")
    env_file = ".env"
    if os.path.exists(env_file):
        print(f"✅ {env_file} exists")
    else:
        print(f"⚠️  {env_file} not found (copy from .env.example)")
    
    # Check sample data
    print("\n📚 Checking sample data...")
    sample_file = "data/documents/sample_resume.txt"
    if os.path.exists(sample_file):
        print(f"✅ {sample_file}")
    else:
        print(f"❌ {sample_file} (missing)")
    
    print("\n🎉 Setup Validation Complete!")
    print("\n📋 Next Steps:")
    print("1. Copy .env.example to .env and add your OPENAI_API_KEY")
    print("2. Run: python start.py")
    print("3. Visit: http://localhost:8000/health")
    print("4. Upload documents via /api/v1/documents/upload")
    print("5. Query via /api/v1/query")
    
    return True

if __name__ == "__main__":
    if validate_setup():
        print("\n✅ All checks passed! Your RAG API is ready to use.")
        sys.exit(0)
    else:
        print("\n❌ Some checks failed. Please fix the issues above.")
        sys.exit(1)