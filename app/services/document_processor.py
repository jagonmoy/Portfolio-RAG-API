import os
from pathlib import Path
from typing import Any, Dict, List

import git
import requests
from bs4 import BeautifulSoup
from llama_index.core import Document
from pypdf import PdfReader

from app.core.config import get_settings
from app.core.logging import StructuredLogger

logger = StructuredLogger(__name__)
settings = get_settings()

class DocumentProcessor:
    def __init__(self):
        self.supported_formats = {'.pdf', '.txt', '.md'}

    def process_pdf(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        try:
            reader = PdfReader(file_path)
            documents = []

            full_text = ""
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                full_text += page_text + "\n\n"

            doc_metadata = {
                "file_name": os.path.basename(file_path),
                "file_path": file_path,
                "file_type": "pdf",
                "page_count": len(reader.pages),
                **(metadata or {})
            }

            documents.append(Document(
                text=full_text.strip(),
                metadata=doc_metadata
            ))

            logger.info("PDF processed successfully",
                       file=file_path,
                       pages=len(reader.pages),
                       text_length=len(full_text))

            return documents

        except Exception as e:
            logger.error("Failed to process PDF", file=file_path, error=str(e))
            return []

    def process_text_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            doc_metadata = {
                "file_name": os.path.basename(file_path),
                "file_path": file_path,
                "file_type": Path(file_path).suffix[1:],
                **(metadata or {})
            }

            document = Document(
                text=content,
                metadata=doc_metadata
            )

            logger.info("Text file processed successfully",
                       file=file_path,
                       text_length=len(content))

            return [document]

        except Exception as e:
            logger.error("Failed to process text file", file=file_path, error=str(e))
            return []

    def process_github_repo(self, repo_url: str, clone_path: str = None) -> List[Document]:
        try:
            if clone_path is None:
                clone_path = f"./temp_repos/{repo_url.split('/')[-1]}"

            os.makedirs(os.path.dirname(clone_path), exist_ok=True)

            if os.path.exists(clone_path):
                repo = git.Repo(clone_path)
                repo.remotes.origin.pull()
                logger.info("Repository updated", repo=repo_url)
            else:
                repo = git.Repo.clone_from(repo_url, clone_path)
                logger.info("Repository cloned", repo=repo_url)

            documents = []

            readme_files = ['README.md', 'readme.md', 'README.txt', 'readme.txt']
            readme_content = ""

            for readme_file in readme_files:
                readme_path = os.path.join(clone_path, readme_file)
                if os.path.exists(readme_path):
                    with open(readme_path, 'r', encoding='utf-8', errors='ignore') as f:
                        readme_content = f.read()
                        break

            repo_info = {
                "name": repo_url.split('/')[-1],
                "url": repo_url,
                "description": readme_content[:500] + "..." if len(readme_content) > 500 else readme_content
            }

            try:
                with open(os.path.join(clone_path, 'package.json'), 'r') as f:
                    import json
                    package_data = json.load(f)
                    repo_info["technology"] = "Node.js/JavaScript"
                    repo_info["dependencies"] = list(package_data.get("dependencies", {}).keys())
            except:
                pass

            try:
                with open(os.path.join(clone_path, 'requirements.txt'), 'r') as f:
                    repo_info["technology"] = "Python"
                    repo_info["dependencies"] = [line.strip().split('==')[0] for line in f.readlines()]
            except:
                pass

            try:
                with open(os.path.join(clone_path, 'pyproject.toml'), 'r') as f:
                    repo_info["technology"] = "Python"
            except:
                pass

            document_text = f"""
            Repository: {repo_info['name']}
            URL: {repo_info['url']}
            Technology: {repo_info.get('technology', 'Unknown')}
            
            Description:
            {repo_info['description']}
            
            Dependencies: {', '.join(repo_info.get('dependencies', [])[:10])}
            """

            doc_metadata = {
                "source": "github_repo",
                "repo_name": repo_info['name'],
                "repo_url": repo_url,
                "technology": repo_info.get('technology', 'Unknown'),
                "file_type": "repository"
            }

            documents.append(Document(
                text=document_text.strip(),
                metadata=doc_metadata
            ))

            logger.info("GitHub repository processed",
                       repo=repo_url,
                       tech=repo_info.get('technology', 'Unknown'))

            return documents

        except Exception as e:
            logger.error("Failed to process GitHub repository", repo=repo_url, error=str(e))
            return []

    def process_portfolio_website(self, url: str = "https://jagonmoy.github.io") -> List[Document]:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            for script in soup(["script", "style"]):
                script.decompose()

            text_content = soup.get_text()
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)

            doc_metadata = {
                "source": "portfolio_website",
                "url": url,
                "file_type": "website",
                "title": soup.title.string if soup.title else "Portfolio Website"
            }

            document = Document(
                text=text,
                metadata=doc_metadata
            )

            logger.info("Portfolio website processed", url=url, text_length=len(text))

            return [document]

        except Exception as e:
            logger.error("Failed to process portfolio website", url=url, error=str(e))
            return []

    def process_file(self, file_path: str, metadata: Dict[str, Any] = None) -> List[Document]:
        file_extension = Path(file_path).suffix.lower()

        if file_extension == '.pdf':
            return self.process_pdf(file_path, metadata)
        elif file_extension in {'.txt', '.md'}:
            return self.process_text_file(file_path, metadata)
        else:
            logger.warning("Unsupported file format", file=file_path, extension=file_extension)
            return []

document_processor = DocumentProcessor()
