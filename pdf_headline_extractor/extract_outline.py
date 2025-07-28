import os
import json
import unicodedata
from langdetect import detect
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

INPUT_DIR = "/app/input"
OUTPUT_DIR = "/app/output"

def is_bold(fontname):
    bold_keywords = ["Bold", "bold", "BD", "Bd"]
    return any(keyword in fontname for keyword in bold_keywords)

def normalize_text(text):
    return unicodedata.normalize("NFKC", text).strip()

def detect_language(text):
    try:
        return detect(text)
    except:
        return "unknown"

def extract_fonts_and_text(pdf_path):
    headings = []
    font_sizes = []

    for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line_text = normalize_text(text_line.get_text())
                    if not line_text:
                        continue

                    sizes = []
                    font_names = []
                    for char in text_line:
                        if isinstance(char, LTChar):
                            sizes.append(char.size)
                            font_names.append(char.fontname)

                    if not sizes:
                        continue

                    avg_size = sum(sizes) / len(sizes)
                    font_sizes.append(avg_size)

                    bold = any(is_bold(f) for f in font_names)

                    headings.append((line_text, avg_size, page_number, bold))

    return headings, font_sizes

def classify_headings(headings, font_sizes):
    if not headings:
        return "Untitled Document", [], "unknown"

    # Sort font sizes and map to heading levels
    unique_sizes = sorted(set(font_sizes), reverse=True)
    size_to_level = {size: f"H{i+1}" for i, size in enumerate(unique_sizes[:3])}

    title = headings[0][0]
    outline = []

    # Use ML to detect document language
    sample_text = " ".join(h[0] for h in headings[:5])
    language = detect_language(sample_text)

    for text, size, page, bold in headings:
        level = size_to_level.get(size)
        if not level:
            continue

        # For English PDFs, use bold to determine heading
        if language == "en":
            if bold:
                outline.append({
                    "level": level,
                    "text": text,
                    "page": page
                })
        else:
            # For multilingual PDFs, ignore bold, just use font size
            outline.append({
                "level": level,
                "text": text,
                "page": page
            })

    return title, outline, language

def process_pdf(pdf_filename):
    pdf_path = os.path.join(INPUT_DIR, pdf_filename)
    headings, font_sizes = extract_fonts_and_text(pdf_path)
    title, outline, language = classify_headings(headings, font_sizes)

    result = {
        "title": title,
        "language": language,
        "outline": outline
    }

    output_path = os.path.join(OUTPUT_DIR, pdf_filename.replace(".pdf", ".json"))
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

def main():
    for filename in os.listdir(INPUT_DIR):
        if filename.lower().endswith(".pdf"):
            print(f"Processing {filename}...")
            process_pdf(filename)

if __name__ == "__main__":
    main()
