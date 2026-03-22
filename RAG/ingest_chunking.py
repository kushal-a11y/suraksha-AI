import os
import re
import json
import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path

# ==============================
# CONFIG
# ==============================

pytesseract.pytesseract.tesseract_cmd=r"D:\AllApps\ocr\tesseract.exe"

PDF_FOLDER = r"D:\PersonalProjects\Hackathons\Suraksha AI\knowledgeBase\ALL"   # folder containing your PDFs
OUTPUT_FILE = "All_chunks.json"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

# ==============================
# STEP 1: Extract text (normal)
# ==============================
def extract_text_from_pdf(path):
    text = ""
    try:
        doc = fitz.open(path)
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error reading {path}: {e}")
    return text


# ==============================
# STEP 2: OCR fallback
# ==============================
def ocr_pdf(path):
    print(f"[OCR] Processing scanned PDF: {path}")
    text = ""
    try:
        images = convert_from_path(path)
        for img in images:
            text += pytesseract.image_to_string(img)
    except Exception as e:
        print(f"OCR failed for {path}: {e}")
    return text


# ==============================
# STEP 3: Smart processor
# ==============================
def process_pdf(path):
    text = extract_text_from_pdf(path)

    # If very little text → probably scanned
    if len(text.strip()) < 100:
        text = ocr_pdf(path)

    return text


# ==============================
# STEP 4: Clean text
# ==============================
def clean_text(text):
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split())  # remove extra spaces
    return text


# ==============================
# STEP 5: Chunking
# ==============================
def chunk_text(text, size=CHUNK_SIZE):
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < size:
            current_chunk += " " + sentence
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# ==============================
# MAIN PIPELINE
# ==============================
def run_ingestion():
    all_chunks = []

    for file in os.listdir(PDF_FOLDER):
        if file.endswith(".pdf"):
            path = os.path.join(PDF_FOLDER, file)
            print(f"\n📄 Processing: {file}")

            text = process_pdf(path)
            text = clean_text(text)

            if len(text) < 50:
                print("⚠️ Skipping (too little content)")
                continue

            chunks = chunk_text(text)

            print(f"✅ Extracted {len(chunks)} chunks")

            for c in chunks:
                all_chunks.append({
                    "source": file,
                    "text": c
                })

    # Save output
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, indent=2, ensure_ascii=False)

    print(f"\n🎉 Done! Total chunks: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_FILE}")


# ==============================
# RUN
# ==============================
if __name__ == "__main__":
    run_ingestion()