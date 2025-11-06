"""
PDF Text Extractor with Azure AI Document Intelligence
Extracts text from PDF documents with preserved structure and formatting
"""

import os
import sys
import time
import json
import hashlib
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from dotenv import load_dotenv
from tqdm import tqdm

try:
    from azure.ai.formrecognizer import DocumentAnalysisClient
    from azure.core.credentials import AzureKeyCredential
except ImportError:
    print("[ERROR] Azure Form Recognizer SDK not installed!")
    print("Please run: pip install azure-ai-formrecognizer")
    sys.exit(1)


# ============================================================================
# SECTION 1: Configuration and Setup
# ============================================================================

# Load environment variables
load_dotenv()

# Get script directory for relative paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load configuration from environment
AZURE_ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
AZURE_KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")
PDF_FOLDER_PATH = os.getenv("PDF_FOLDER_PATH", "./pdfs")
OUTPUT_FILE_NAME = os.getenv("OUTPUT_FILE", "extracted_notes.md")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, OUTPUT_FILE_NAME)

# Cache file for tracking processed PDFs
CACHE_FILE = os.path.join(SCRIPT_DIR, ".processed_pdfs.json")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(SCRIPT_DIR, 'processing.log'), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Suppress Azure SDK verbose logging (only show warnings and errors)
logging.getLogger('azure').setLevel(logging.WARNING)
logging.getLogger('azure.core.pipeline.policies.http_logging_policy').setLevel(logging.WARNING)


# ============================================================================
# SECTION 2: Helper Functions
# ============================================================================

def get_file_info(file_path: str) -> Dict:
    """Get file metadata for caching and display."""
    file_stat = os.stat(file_path)
    return {
        "size": file_stat.st_size,
        "mtime": file_stat.st_mtime,
        "name": os.path.basename(file_path)
    }


def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def load_processed_cache() -> Dict:
    """Load cache of previously processed PDFs."""
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("Cache file corrupted, starting fresh")
            return {}
    return {}


def save_processed_cache(cache: Dict):
    """Save cache of processed PDFs."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save cache: {e}")


def is_file_processed(file_path: str, cache: Dict) -> bool:
    """Check if file has already been processed."""
    file_info = get_file_info(file_path)
    file_key = hashlib.md5(file_path.encode()).hexdigest()
    
    if file_key in cache:
        cached_info = cache[file_key]
        # Check if file hasn't changed (same size and modification time)
        if (cached_info.get("size") == file_info["size"] and
            cached_info.get("mtime") == file_info["mtime"]):
            return True
    return False


def format_document_content(result) -> str:
    """
    Format the extracted document into clean Markdown.
    Preserves headings, paragraphs, lists, and tables.
    """
    output = []
    
    for page in result.pages:
        # Extract text with reading order
        for line in page.lines:
            content = line.content.strip()
            if content:
                # Try to detect headings (ALL CAPS or short lines)
                if len(content) < 60 and (content.isupper() or content.istitle()):
                    # Likely a heading
                    if len(content) < 30:
                        output.append(f"\n## {content}\n")
                    else:
                        output.append(f"\n### {content}\n")
                else:
                    # Regular paragraph text
                    output.append(content)
        
        # Add page separator
        output.append("\n---\n")
    
    # Handle paragraphs (extracted from result.paragraphs if available)
    if hasattr(result, 'paragraphs') and result.paragraphs:
        output = []
        for paragraph in result.paragraphs:
            content = paragraph.content.strip()
            if content:
                # Detect heading-like paragraphs
                if paragraph.role == "title" or (len(content) < 60 and content.isupper()):
                    output.append(f"\n## {content}\n")
                elif paragraph.role == "sectionHeading":
                    output.append(f"\n### {content}\n")
                else:
                    output.append(f"{content}\n")
    
    # Handle tables if present
    if hasattr(result, 'tables') and result.tables:
        for table_idx, table in enumerate(result.tables):
            output.append(f"\n### Table {table_idx + 1}\n")
            
            # Create Markdown table
            for row_idx, cell in enumerate(table.cells):
                if cell.row_index == 0:
                    # Header row
                    if cell.column_index == 0:
                        output.append("\n|")
                    output.append(f" {cell.content} |")
                    if cell.column_index == table.column_count - 1:
                        output.append("\n|" + "---|" * table.column_count)
                else:
                    # Data rows
                    if cell.column_index == 0:
                        output.append("\n|")
                    output.append(f" {cell.content} |")
            
            output.append("\n\n")
    
    return "".join(output)


# ============================================================================
# SECTION 3: Script Initialization
# ============================================================================

# Validate configuration
if not AZURE_ENDPOINT or not AZURE_KEY:
    logger.error("Missing Azure credentials in .env file!")
    logger.error("Please set AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT and AZURE_DOCUMENT_INTELLIGENCE_KEY")
    sys.exit(1)

if not os.path.exists(PDF_FOLDER_PATH):
    logger.error(f"PDF folder not found: {PDF_FOLDER_PATH}")
    sys.exit(1)

# Load cache
processed_cache = load_processed_cache()

# Collect PDF files sorted by creation date
pdf_files = []
for file_path in Path(PDF_FOLDER_PATH).glob("*.pdf"):
    pdf_files.append(str(file_path))

# Sort by creation time (oldest first)
pdf_files.sort(key=lambda x: os.path.getctime(x))

if not pdf_files:
    logger.error(f"No PDF files found in: {PDF_FOLDER_PATH}")
    sys.exit(1)

# Calculate total size
total_size = sum(os.path.getsize(f) for f in pdf_files)

logger.info("=" * 60)
logger.info("PDF TEXT EXTRACTOR - Processing Started")
logger.info("=" * 60)
logger.info(f"Total PDFs found: {len(pdf_files)}")
logger.info(f"Total size: {format_file_size(total_size)}")
logger.info(f"Output file: {OUTPUT_FILE}")
logger.info(f"PDFs sorted by creation date (maintaining chronological order)")
logger.info("=" * 60)


# ============================================================================
# SECTION 4: Azure Document Intelligence Client
# ============================================================================

# Initialize Azure client
try:
    client = DocumentAnalysisClient(
        endpoint=AZURE_ENDPOINT,
        credential=AzureKeyCredential(AZURE_KEY)
    )
    logger.info("[SUCCESS] Connected to Azure Document Intelligence")
except Exception as e:
    logger.error(f"[ERROR] Failed to initialize Azure client: {e}")
    sys.exit(1)


# ============================================================================
# SECTION 5: PDF Processing Loop
# ============================================================================

all_documents = []
stats = {
    "processed": 0,
    "skipped": 0,
    "failed": 0,
    "total_pages": 0
}

start_time = time.time()

# Process each PDF
for pdf_path in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
    file_name = os.path.basename(pdf_path)
    
    # Check if already processed
    if is_file_processed(pdf_path, processed_cache):
        logger.info(f"[SKIP] Already processed: {file_name}")
        stats["skipped"] += 1
        
        # Load from cache
        file_key = hashlib.md5(pdf_path.encode()).hexdigest()
        cached_content = processed_cache[file_key].get("content", "")
        if cached_content:
            all_documents.append(cached_content)
        continue
    
    # Process new PDF
    logger.info(f"[INFO] Processing: {file_name}")
    
    try:
        # Read PDF file
        with open(pdf_path, "rb") as f:
            poller = client.begin_analyze_document("prebuilt-layout", document=f)
            result = poller.result()
        
        # Format extracted content
        document_content = format_document_content(result)
        
        # Add to output
        all_documents.append(f"\n\n# {file_name}\n\n{document_content}")
        
        # Update cache
        file_info = get_file_info(pdf_path)
        file_key = hashlib.md5(pdf_path.encode()).hexdigest()
        processed_cache[file_key] = {
            **file_info,
            "processed_at": datetime.now().isoformat(),
            "page_count": len(result.pages),
            "content": f"\n\n# {file_name}\n\n{document_content}"
        }
        
        # Update statistics
        stats["processed"] += 1
        stats["total_pages"] += len(result.pages)
        
        logger.info(f"[SUCCESS] Extracted {len(result.pages)} pages from {file_name}")
        
        # Small delay to avoid API throttling
        time.sleep(0.5)
        
    except Exception as e:
        logger.error(f"[ERROR] Failed to process {file_name}: {e}")
        stats["failed"] += 1
        continue

# Save cache
save_processed_cache(processed_cache)


# ============================================================================
# SECTION 6: Generate Output File
# ============================================================================

if all_documents:
    try:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            # Write header
            f.write(f"# Extracted PDF Notes\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"**Total Documents:** {len(all_documents)}\n")
            f.write(f"**Total Pages:** {stats['total_pages']}\n")
            f.write("---\n")

            # Write all documents
            f.write("\n".join(all_documents))
        
        logger.info(f"[SUCCESS] Output saved to: {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"[ERROR] Failed to save output file: {e}")


# ============================================================================
# SECTION 7: Final Statistics
# ============================================================================

end_time = time.time()
elapsed_time = end_time - start_time

logger.info("=" * 60)
logger.info("PROCESSING COMPLETE")
logger.info("=" * 60)
logger.info(f"Total files: {len(pdf_files)}")
logger.info(f"  Processed: {stats['processed']}")
logger.info(f"  Skipped (already processed): {stats['skipped']}")
logger.info(f"  Failed: {stats['failed']}")
logger.info(f"Total pages extracted: {stats['total_pages']}")
logger.info(f"Total time: {elapsed_time:.2f}s")
if stats["processed"] > 0:
    logger.info(f"Average time per document: {elapsed_time / stats['processed']:.2f}s")
logger.info("=" * 60)

print(f"\n[SUCCESS] Processing complete! Check '{OUTPUT_FILE}' for results.")
print(f"[INFO] Detailed logs saved to: processing.log")
