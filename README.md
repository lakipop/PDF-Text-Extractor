# PDF Text Extractor 📄

Extract and format text from PDF lecture notes and textbooks using Azure AI Document Intelligence.

## Overview

This tool processes PDF documents (lecture notes, textbooks, research papers) and converts them into well-formatted Markdown files with preserved structure including:

- ✅ **Continuous text flow** (book-style reading)
- ✅ **Chapter and section detection**
- ✅ **Proper reading order**
- ✅ **Tables and lists**
- ✅ **Headings hierarchy**
- ✅ **Smart caching** (avoid re-processing)
- ✅ **Professional logging**

## Key Differences from Slide-Text-Extractor

| Feature | Slide Extractor | PDF Extractor |
|---------|----------------|---------------|
| **Input** | Screenshots of slides | PDF documents |
| **Output** | Individual slides + captions | Continuous book-style text |
| **De-duplication** | Yes (slides repeat) | No (each page unique) |
| **Separation Logic** | Pixel-based caption split | Chapter/section detection |
| **Azure Service** | Computer Vision Read API | Document Intelligence |
| **Use Case** | Video lecture screenshots | Textbooks, lecture notes |

## Features

- 🔄 **Smart Processing**: Automatically skips already-processed PDFs
- 📊 **Detailed Logging**: Professional logging with timestamps and statistics
- 🎯 **Structure Preservation**: Maintains headings, paragraphs, lists, and tables
- ⚡ **Fast & Efficient**: Caching system for instant re-runs
- 🔐 **Secure**: Environment variables for API credentials
- 📝 **Clean Output**: Beautiful Markdown format for easy reading

## Prerequisites

- Python 3.8 or higher
- Azure AI Document Intelligence resource
- Azure subscription

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/lakipop/PDF-Text-Extractor.git
cd PDF-Text-Extractor
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or use the one-click setup:

```bash
SETUP.bat
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Azure credentials:

```bash
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your-api-key-here
PDF_FOLDER_PATH=path/to/your/pdfs
OUTPUT_FILE=extracted_notes.md
```

### 4. Run the Extractor

```bash
python process_pdfs.py
```

Or use the one-click run:

```bash
RUN.bat
```

## How It Works

1. **Scan**: Reads all PDF files from the configured folder
2. **Check Cache**: Skips already-processed files (saves time & API costs)
3. **Extract**: Uses Azure Document Intelligence to analyze document structure
4. **Format**: Converts to clean Markdown with preserved formatting
5. **Output**: Creates a single consolidated notes file

## Output Format

```markdown
# Document Title

## Chapter 1: Introduction

This is the extracted content with proper paragraph flow...

### Section 1.1: Key Concepts

- Bullet points are preserved
- Lists maintain their structure

### Section 1.2: Details

Continuous text flows naturally across pages...

## Chapter 2: Advanced Topics

Tables are also extracted:

| Header 1 | Header 2 |
|----------|----------|
| Data 1   | Data 2   |
```

## Configuration

Edit `.env` to customize:

- `AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT`: Your Azure endpoint URL
- `AZURE_DOCUMENT_INTELLIGENCE_KEY`: Your API key
- `PDF_FOLDER_PATH`: Folder containing PDF files to process
- `OUTPUT_FILE`: Name of the output Markdown file

## Logging

All processing activity is logged to `processing.log` with:

- Timestamps for each operation
- Success/failure status
- Processing statistics
- Error details for troubleshooting

## Caching

The tool creates `.processed_pdfs.json` to track processed files:

- Stores: filename, size, modification time, page count
- Automatically skips unchanged files
- Saves API costs and processing time

## Cost Estimation

Azure AI Document Intelligence pricing (as of 2024):

- **Free Tier**: 500 pages/month
- **Standard**: $1.50 per 1,000 pages

Example: A 50-page textbook costs ~$0.075 to process.

## Troubleshooting

### Import Errors

Make sure you've installed all dependencies:

```bash
pip install -r requirements.txt
```

### API Authentication Failed

- Verify your `.env` file has correct credentials
- Check that your Azure resource is active
- Ensure your API key hasn't expired

### No PDFs Found

- Check that `PDF_FOLDER_PATH` in `.env` points to the correct folder
- Ensure PDF files exist in that folder
- Verify folder path uses forward slashes or double backslashes

## Project Structure

```
PDF-Text-Extractor/
├── process_pdfs.py           # Main processing script
├── requirements.txt          # Python dependencies
├── .env                      # Configuration (create from .env.example)
├── .env.example             # Configuration template
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── GUIDE.md                 # Detailed setup guide
├── ROADMAP.md               # Future development plans
├── RUN.bat                  # One-click run (Windows)
├── SETUP.bat                # One-click setup (Windows)
├── processing.log           # Processing logs (generated)
├── .processed_pdfs.json     # Cache file (generated)
└── extracted_notes.md       # Output file (generated)
```

## Related Projects

- [Slide-Text-Extractor](https://github.com/lakipop/Slide-Text-Extractor) - For extracting text from lecture slide screenshots

## Technologies Used

- **Azure AI Document Intelligence**: Document analysis and text extraction
- **Python 3**: Core processing logic
- **python-dotenv**: Environment variable management
- **logging**: Professional logging system

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License.

## Author

Created by **Lakindu** - AI Projects

---

**Need help?** Check the [GUIDE.md](GUIDE.md) for detailed setup instructions.
