import os
import json
from pdf2image import convert_from_path
import pytesseract
from bs4 import BeautifulSoup

def clean_text(text):
    # Remove extra whitespace and join lines
    return ' '.join(word for word in text.split() if word)

def is_heading(text):
    # Check for H1, H2, H3 indicators based on numbering or keywords
    text_lower = text.lower()
    if any(text.startswith(f"{i}." or f"{i}.{j}") for i in range(1, 10) for j in range(10)):
        return True
    if any(kw in text_lower for kw in ["introduction", "overview", "revision", "acknowledgements", "references"]):
        return True
    return False

def extract_headings_and_pages(images):
    outline = []
    for page_num, image in enumerate(images, 1):
        hocr = pytesseract.image_to_pdf_or_hocr(image, extension='hocr', lang='eng+spa+fra+deu+ita+por+rus+chi_sim+ara')
        soup = BeautifulSoup(hocr, 'html.parser')
        
        # Collect candidate headings with font size and text
        candidates = []
        for elem in soup.find_all('span', class_='ocr_line'):
            text = clean_text(elem.get_text())
            if not text or any(noise in text.lower() for noise in ["copyright", "version", "page", "©", "international", "qualifications"]):
                continue
            
            title_attr = elem.get('title', '')
            font_size = 0
            for part in title_attr.split(';'):
                part = part.strip()
                if part.startswith('x_size'):
                    try:
                        font_size = int(part.split(' ')[1])
                    except (IndexError, ValueError):
                        font_size = 0
            
            candidates.append((font_size, text))
        
        # Determine max font size on page for H1 detection
        max_font_size = max((fs for fs, _ in candidates), default=0)
        
        for font_size, text in candidates:
            if font_size == max_font_size and font_size > 15:
                # Consider as H1
                outline.append({"level": "H1", "text": text, "page": page_num})
            elif font_size > 14 and is_heading(text):
                # H2: numbered sections or keywords
                outline.append({"level": "H2", "text": text, "page": page_num})
            elif font_size > 12 and any(f"{i}.{j}" in text for i in range(1, 10) for j in range(1, 10)):
                # H3: subsections
                outline.append({"level": "H3", "text": text, "page": page_num})
    return outline

def extract_title(images):
    # Extract main title from first page by largest font size line
    hocr = pytesseract.image_to_pdf_or_hocr(images[0], extension='hocr', lang='eng+spa+fra+deu+ita+por+rus+chi_sim+ara')
    soup = BeautifulSoup(hocr, 'html.parser')
    candidates = []
    for elem in soup.find_all('span', class_='ocr_line'):
        text = clean_text(elem.get_text())
        if not text or any(noise in text.lower() for noise in ["copyright", "version", "page", "©", "international", "qualifications"]):
            continue
        title_attr = elem.get('title', '')
        font_size = 0
        for part in title_attr.split(';'):
            part = part.strip()
            if part.startswith('x_size'):
                try:
                    font_size = int(part.split(' ')[1])
                except (IndexError, ValueError):
                    font_size = 0
        candidates.append((font_size, text))
    if not candidates:
        return "Untitled Document"
    max_font_size = max(candidates, key=lambda x: x[0])[0]
    # Return the text with max font size
    for font_size, text in candidates:
        if font_size == max_font_size and font_size > 15:
            return text
    # Fallback
    return "Untitled Document"

def process_pdf(pdf_path, output_dir):
    # Explicitly convert PDF to images for this file
    images = convert_from_path(pdf_path)
    if not images:
        return
    
    title = extract_title(images)
    outline = extract_headings_and_pages(images)
    
    # Filter outline to remove duplicates and keep important headings only
    filtered_outline = []
    seen_texts = set()
    for item in outline:
        if item['text'] not in seen_texts:
            filtered_outline.append(item)
            seen_texts.add(item['text'])
    
    output_file = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"title": title, "outline": filtered_outline}, f, indent=2, ensure_ascii=False)

input_dir = "input"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
for pdf in os.listdir(input_dir):
    if pdf.endswith(".pdf"):
        print(f"Processing {pdf}")  # Debug print to track files
        process_pdf(os.path.join(input_dir, pdf), output_dir)