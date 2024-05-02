"""
This module focuses on the extraction of text from PDF documents using OCR
(Optical Character Recognition). It provides functionalities to extract plain
text, text from images as well as text from embedded diagrams in the PDF.
"""

import io

import fitz
import pytesseract
from PIL import Image, UnidentifiedImageError


class PDFInfo:
    """
    Provides information about PDF documents, such as the number of pages.
    """

    @classmethod
    def get_page_count(cls, doc_path):
        """
        Returns the total number of pages in a PDF document.

        Args:
            doc_path (str): Path to the PDF document.

        Returns:
            int: Total number of pages in the document.
        """
        with fitz.open(doc_path) as document:
            return document.page_count


class PDFExtract:
    """
    Extracts text from the specified pages of a PDF document using OCR for
    visible text, text from images and text from embedded diagrams.
    """

    def __init__(self, document_path, pages, threshold=100000, zoom=10):
        """
        Initializes the PDFExtract instance with the document path and specific
        pages to extract from.

        Args:
            document_path (str): Path to the PDF document.
            pages (iterable): A collection of page numbers to extract text
            from.
            threshold (int): The minimum size of content streams to be
            considered for image-based OCR. Defaults to 100000.
            zoom (int): Zoom level for OCR accuracy enhancement.
            Defaults to 10.
        """
        self.document_path = document_path
        self.pages = pages
        self.threshold = threshold
        self.zoom = zoom
        self.config = "--psm 11"
        self.debug = False

    def get_text(self):
        """
        Extracts text from the specified pages of the document, including OCR
        of images and embedded diagrams.

        Returns:
            tuple of str: Returns a tuple containing textual data from plain
            text extraction, image-based OCR, and full-page OCR.
        """
        document = fitz.open(self.document_path)

        text_text, text_images, text_pages = "", "", ""

        for page_num in self.pages:
            page = document.load_page(page_num)

            text_text += page.get_text()  # type: ignore
            text_images += self._get_text_from_images_ocr(document, page)
            text_pages += self._get_text_from_page_ocr(document, page)

        document.close()

        return text_text, text_images, text_pages

    def _get_text_from_images_ocr(self, document, page):
        text = ""
        for _index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = document.extract_image(xref)
            image = self._open_image_stream(base_image["image"])
            if not image:
                continue

            if self.debug:
                doc_path = document.name.split("/")[-1]
                image.save(f".debug/{doc_path}_{page.number}_{_index}.png")

            text += pytesseract.image_to_string(image, config=self.config)
            image.close()

        return text

    def _open_image_stream(self, image_bytes):
        with io.BytesIO(image_bytes) as image_stream:
            image_stream.seek(0)

            try:
                image = Image.open(image_stream)
                image.load()
                return image
            except UnidentifiedImageError:
                return None
            except ValueError:
                return None

    def _get_text_from_page_ocr(self, document, page):
        if not self._contains_stream_above_threshold(document, page):
            return ""

        mat = fitz.Matrix(self.zoom, self.zoom)
        pix = page.get_pixmap(matrix=mat)  # type: ignore
        dims = [pix.width, pix.height]
        image = Image.frombytes("RGB", dims, pix.samples)

        if self.debug:
            doc_path = document.name.split("/")[-1]
            image.save(f".debug/{doc_path}_{page.number}_ocr.png")

        text = pytesseract.image_to_string(image, config=self.config)
        image.close()

        return text

    def _contains_stream_above_threshold(self, document, page):
        for content in page.get_contents():
            stream = document.xref_stream(content)
            if len(stream) > self.threshold:
                return True

        return False
