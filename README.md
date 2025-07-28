📌 Challenge Overview

Round 1A focuses on building the core document understanding engine. The goal is to extract a structured outline (Title, H1, H2, H3 headings with page numbers) from a given PDF document. This will serve as the foundation for the subsequent rounds of the hackathon.

🚀 Solution Approach

Implemented a PDF parsing pipeline that analyzes text blocks, font sizes, and styles to detect document structure.

Uses text hierarchy detection with heuristics + optional lightweight ML-based heading classifier (≤ 200MB).

Handles multilingual PDFs.

Outputs a clean JSON format matching the given specification.

🛠️ Technologies and Libraries

Language: Python 3

Libraries:

pdfminer.six / PyMuPDF (fitz) – for text and font metadata extraction

regex – for pattern-based heading identification

json – for structured output

Environment: Docker (linux/amd64), CPU-only

🏗️ Project Structure

├── Dockerfile
├── input
├── output
├── README.md  
└── extract_outline.py
    
⚡ Building the Docker Image

docker build --platform linux/amd64 -t pdf-outline-extractor:latest .

▶️ Running the Container

Place PDFs in the input folder and run:


docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-outline-extractor:latest
  
Output JSON files will be saved in output/ for each input PDF.

✅ Features
Fast execution (≤ 10s for 50 pages).

Model size < 200MB.

No internet dependency (fully offline).

CPU-only execution.

Supports multiple PDFs in a single run.

📊 Example Output
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
