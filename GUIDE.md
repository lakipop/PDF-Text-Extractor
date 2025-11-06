# Complete Setup Guide - PDF Text Extractor

This guide will walk you through setting up and using the PDF Text Extractor step-by-step.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Azure Setup](#azure-setup)
3. [Project Setup](#project-setup)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.8 or higher**
  - Download from: https://www.python.org/downloads/
  - During installation, check "Add Python to PATH"

- **Git** (optional, for cloning)
  - Download from: https://git-scm.com/downloads

- **Text Editor** (VS Code, Notepad++, etc.)

### Required Azure Resources

- Azure subscription (free tier available)
- Azure AI Document Intelligence resource

---

## Azure Setup

### Step 1: Create Azure Account

1. Go to https://azure.microsoft.com/
2. Click "Start free" or "Sign in"
3. Follow the registration process

### Step 2: Create Document Intelligence Resource

1. **Navigate to Azure Portal:**
   - Go to https://portal.azure.com/

2. **Create Resource:**
   - Click "+ Create a resource"
   - Search for "Document Intelligence"
   - Click "Create"

3. **Configure Resource:**
   - **Subscription:** Select your subscription
   - **Resource Group:** Create new or use existing
   - **Region:** Choose closest to you (e.g., "East US")
   - **Name:** Give it a unique name (e.g., "pdf-extractor-ai")
   - **Pricing Tier:** 
     - **Free (F0):** 500 pages/month free
     - **Standard (S0):** Pay-as-you-go

4. **Review + Create:**
   - Click "Review + create"
   - Click "Create"
   - Wait for deployment (1-2 minutes)

### Step 3: Get API Credentials

1. **Go to Resource:**
   - Click "Go to resource" after deployment

2. **Copy Endpoint:**
   - In the left menu, click "Keys and Endpoint"
   - Copy the **Endpoint URL**
   - Example: `https://pdf-extractor-ai.cognitiveservices.azure.com/`

3. **Copy API Key:**
   - Copy **KEY 1** or **KEY 2** (either works)
   - Example: `abc123def456ghi789jkl012mno345pq`

**Keep these credentials safe!** You'll need them in the next section.

---

## Project Setup

### Option 1: Clone from GitHub

```bash
git clone https://github.com/lakipop/PDF-Text-Extractor.git
cd PDF-Text-Extractor
```

### Option 2: Download ZIP

1. Download the project ZIP file
2. Extract to desired location
3. Open terminal/command prompt in the folder

### Install Dependencies

**Windows (using batch file):**

```bash
SETUP.bat
```

**Manual installation:**

```bash
pip install -r requirements.txt
```

This installs:
- `azure-ai-formrecognizer` - Azure Document Intelligence SDK
- `python-dotenv` - Environment variable management
- `tqdm` - Progress bars

---

## Configuration

### Step 1: Create Environment File

1. **Locate `.env.example` file** in the project folder

2. **Copy to `.env`:**
   ```bash
   copy .env.example .env
   ```

3. **Open `.env` in text editor**

### Step 2: Add Azure Credentials

Edit `.env` and replace placeholder values:

```env
# Azure AI Document Intelligence Configuration
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource-name.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=your-api-key-here

# Folder containing PDF files to process
PDF_FOLDER_PATH=./pdfs

# Output file name (Markdown format)
OUTPUT_FILE=extracted_notes.md
```

**Example:**

```env
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://pdf-extractor-ai.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=abc123def456ghi789jkl012mno345pq
PDF_FOLDER_PATH=D:/Documents/Lecture_PDFs
OUTPUT_FILE=extracted_notes.md
```

### Step 3: Prepare PDF Files

1. **Create PDF folder** (if using default `./pdfs`):
   ```bash
   mkdir pdfs
   ```

2. **Copy your PDF files** into this folder

3. **Verify files:**
   - Ensure files have `.pdf` extension
   - Check files are not corrupted
   - Recommended: Start with 1-2 small PDFs for testing

---

## Usage

### Running the Extractor

**Option 1: One-Click Run (Windows)**

Double-click `RUN.bat`

**Option 2: Command Line**

```bash
python process_pdfs.py
```

### What Happens

1. **Scanning:**
   ```
   Total PDFs found: 3
   Total size: 5.42 MB
   ```

2. **Processing:**
   ```
   Processing PDFs: 100%|████████████| 3/3 [00:15<00:00, 5.2s/file]
   ```

3. **Results:**
   ```
   [SUCCESS] Processing complete!
   Total pages extracted: 42
   Check 'extracted_notes.md' for results
   ```

### Output Files

- **`extracted_notes.md`** - Your formatted notes
- **`processing.log`** - Detailed processing log
- **`.processed_pdfs.json`** - Cache file (automatic)

---

## Understanding the Output

### Sample Output Format

```markdown
# Extracted PDF Notes

**Generated:** 2025-11-06 14:30:00
**Total Documents:** 3
**Total Pages:** 42

---

# lecture_01.pdf

## Chapter 1: Introduction

This is the extracted content with proper paragraph flow
and formatting preserved from the original PDF document.

### Key Concepts

- Bullet points are preserved
- Lists maintain their structure
- Reading order is correct

### Tables

| Concept | Description |
|---------|-------------|
| Data 1  | Value 1     |
| Data 2  | Value 2     |

---

# lecture_02.pdf

## Chapter 2: Advanced Topics

...
```

---

## Advanced Features

### Caching System

The tool automatically:
- Tracks processed PDFs in `.processed_pdfs.json`
- Skips unchanged files on re-runs
- Saves API costs and time

**Re-processing a file:**
1. Delete entry from `.processed_pdfs.json`, OR
2. Delete the entire cache file to reprocess all

### Logging

All activity logged to `processing.log`:

```log
2025-11-06 14:30:00 - INFO - Total PDFs found: 3
2025-11-06 14:30:02 - INFO - [SUCCESS] Connected to Azure
2025-11-06 14:30:05 - INFO - [SUCCESS] Extracted 15 pages from lecture_01.pdf
2025-11-06 14:30:10 - ERROR - [ERROR] Failed to process corrupted.pdf: Invalid PDF
```

---

## Troubleshooting

### "Missing Azure credentials in .env file"

**Problem:** `.env` file not configured correctly

**Solution:**
1. Verify `.env` file exists in project root
2. Check that values don't have quotes or extra spaces
3. Ensure endpoint ends with `/`

### "No PDF files found"

**Problem:** PDF folder is empty or path is wrong

**Solution:**
1. Check `PDF_FOLDER_PATH` in `.env`
2. Use absolute path if relative path doesn't work
3. Verify PDFs have `.pdf` extension

### "Authentication failed"

**Problem:** Invalid API credentials

**Solution:**
1. Verify endpoint and key from Azure Portal
2. Check that resource is active (not suspended)
3. Ensure no extra spaces in `.env` file

### "Rate limit exceeded"

**Problem:** Too many API calls too quickly

**Solution:**
1. Script already has 0.5s delay between files
2. For large batches, increase delay in code
3. Consider upgrading to Standard tier

### "Failed to process PDF"

**Problem:** PDF might be corrupted or encrypted

**Solution:**
1. Try opening PDF manually to verify it works
2. Remove password protection if present
3. Re-download or re-save the PDF

### Import Errors

**Problem:** Dependencies not installed

**Solution:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Cost Optimization

### Free Tier Strategy

- **Limit:** 500 pages/month free
- **Planning:** 
  - 1 textbook (200 pages) = ~40% of quota
  - 10 lecture notes (20 pages each) = ~40% of quota
  
### Best Practices

1. **Test first:** Process 1-2 PDFs before bulk processing
2. **Use cache:** Don't delete `.processed_pdfs.json` unnecessarily
3. **Monitor usage:** Check Azure Portal → Resource → Metrics
4. **Batch wisely:** Process in groups, not all at once

---

## Tips for Best Results

### PDF Quality

- ✅ **Good:** Typed text, clear scans
- ⚠️ **Okay:** Handwritten notes (accuracy varies)
- ❌ **Poor:** Very low-resolution scans

### Document Types

Works best with:
- Textbooks
- Lecture notes
- Research papers
- Reports and documentation

May struggle with:
- Forms (use prebuilt-document model)
- Receipts (use prebuilt-receipt model)
- Heavily formatted layouts

---

## Next Steps

1. **Test with sample PDFs** to verify setup
2. **Check output quality** and adjust if needed
3. **Process your documents** in batches
4. **Explore ROADMAP.md** for future features

---

## Getting Help

- **Logs:** Check `processing.log` for detailed errors
- **Issues:** Open issue on GitHub repository
- **Documentation:** See README.md for overview

---

**Happy extracting!** 📄✨
