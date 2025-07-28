# Challenge-1a
# Challenge_1a: PDF Heading Extractor

This project is a Dockerized Python application designed to extract meaningful titles and hierarchical headings (H1, H2, H3) with page numbers from PDF files. It processes PDFs from the `sample_dataset/pdfs/` directory, generates JSON outputs in `sample_dataset/outputs/` conforming to the schema in `sample_dataset/schema/output_schema.json`, and is optimized for performance and resource constraints.


## Features
- Extracts titles based on structural indicators (e.g., keywords like "overview", "introduction").
- Identifies H1, H2, and H3 headings using numbering (e.g., "1.", "2.1") or keywords (e.g., "revision", "references").
- Filters out noise (e.g., "copyright", "version", "page").
- Supports multiple languages (English, Spanish, French, German, Italian, Portuguese, Russian, Simplified Chinese, Arabic) offline.
- Generates JSON outputs adhering to the schema in `sample_dataset/schema/output_schema.json`.

## Current Solution
The provided `process_pdfs.py` is a real implementation that:
- Scans PDF files from the input directory.
- Extracts text using Tesseract OCR and `pdf2image`.
- Parses document structure to identify titles and headings.
- Generates meaningful JSON output based on content analysis.

**Note**: This replaces the original dummy implementation. The solution avoids font size criteria, relying on numbering and keywords for detection.

## Prerequisites
- **Docker Desktop**: Installed and running with WSL 2 support (Windows) or native Docker (Linux/Mac).
- **Input PDFs**: Place PDF files in `sample_dataset/pdfs/`.

## Installation
1. **Set Up the Project**:
   - Ensure the project directory `Challenge_1a` is accessible.
   - Verify `sample_dataset/pdfs/` contains input PDF files (e.g., `file01.pdf`, `file02.pdf`).

2. **Build the Docker Image**:
   - Open a terminal in the `Challenge_1a` directory.
   - Run:- If a pipe error occurs (e.g., `open //./pipe/dockerDesktopLinuxEngine` on Windows), restart Docker Desktop and WSL with:
   - Then retry the build.

3. **Verify Setup**:
- Ensure Docker is running (`docker info` should return version info).

## Usage
1. **Run the Container**:
- Execute:- This maps the `pdfs` and `outputs` directories read-only and logs errors to `debug.log`.

2. **Check Output**:
- Go to `sample_dataset/outputs/`.
- Open generated JSON files (e.g., `file01.json`, `file02.json`) to verify titles and headings.
- Review `debug.log` for processing details or errors.

## Expected Output Format
Each PDF generates a corresponding JSON file conforming to the schema in `sample_dataset/schema/output_schema.json`. An example output for `file02.pdf` might be:
```json
{
"title": "ISTQB Foundation Level Agile Tester Overview",
"outline": [
{
 "level": "H2",
 "text": "2. Introduction to Foundation Level Agile Tester Extension",
 "page": 7
},
{
 "level": "H3",
 "text": "2.1 Intended Audience",
 "page": 7
}
]
}
