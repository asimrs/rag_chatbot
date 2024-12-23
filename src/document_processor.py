import logging
from bs4 import BeautifulSoup  # For extracting text from webpages
import requests
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.parsers.pdf import (
    extract_from_images_with_rapidocr,
)
from langchain.schema import Document

def process_pdf(source):
    """Process a PDF file and split it into chunks."""
    logging.info(f"Processing PDF: {source}")
    loader = PyPDFLoader(source)
    documents = loader.load()

    # Filter out scanned pages
    unscanned_documents = [doc for doc in documents if doc.page_content.strip() != ""]
    scanned_pages = len(documents) - len(unscanned_documents)

    if scanned_pages > 0:
        logging.info(f"Omitted {scanned_pages} scanned page(s) from the PDF.")

    if not unscanned_documents:
        raise ValueError(
            "All pages in the PDF appear to be scanned. Please use a PDF with text content."
        )

    return split_documents(unscanned_documents)


def process_image(source):
    """Process an image file and split it into chunks using OCR."""
    logging.info(f"Processing image: {source}")
    try:
        with open(source, "rb") as image_file:
            image_bytes = image_file.read()
        extracted_text = extract_from_images_with_rapidocr([image_bytes])
        if not extracted_text.strip():
            raise ValueError("No text extracted from the image.")
        documents = [Document(page_content=extracted_text, metadata={"source": source})]
        return split_documents(documents)
    except Exception as e:
        logging.error(f"OCR failed for {source}: {e}")
        raise


def extract_text_from_webpage(url):
    """Extract visible text content from a webpage."""
    try:
        logging.info(f"Fetching webpage content from: {url}")
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        text_content = soup.get_text(separator="\n").strip()  # Extract all visible text
        if not text_content:
            raise ValueError("No visible text found on the webpage.")
        return [Document(page_content=text_content, metadata={"source": url})]
    except Exception as e:
        logging.error(f"Failed to extract text from URL: {url}, Error: {e}")
        raise ValueError(f"Failed to extract text from URL: {e}")


def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    """Split documents into smaller chunks."""
    logging.info(f"Splitting documents into chunks (chunk_size={chunk_size}, overlap={chunk_overlap})")
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)


def process_document(source):
    """Determine the file type and process the document accordingly."""
    logging.info(f"Processing document: {source}")
    if source.lower().endswith(".pdf"):
        return process_pdf(source)
    elif source.lower().endswith((".png", ".jpg", ".jpeg")):
        return process_image(source)
    elif source.lower().startswith("http"):
        # Process URL (Webpage)
        documents = extract_text_from_webpage(source)
        return split_documents(documents)
    else:
        logging.error(f"Unsupported file type: {source}")
        raise ValueError(f"Unsupported file type: {source}")
