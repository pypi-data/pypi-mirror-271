"""
Provides functionality for extracting and analyzing text from PDF documents,
by using the Levenshtein distance to search for specific words, visualizing
the results in a microarray plot format. It offers efficient processing by
segmenting documents and utilizing multithreading.
"""

import os
import re
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import NamedTuple

import pandas as pd
from thefuzz import fuzz

from pdf_microarray.pdf_extract import PDFExtract, PDFInfo
from pdf_microarray.plot_microarray import PlotMicroarray


class Segment(NamedTuple):
    """
    A NamedTuple that stores metadata about a segment of a PDF document.

    Attributes:
        document_path (str): Path to the source PDF document.
        processed_path (str): Path where the processed segment is to be stored.
        first_page (int): The first page of the segment.
        last_page (int): The last page of the segment.
    """

    document_path: str
    processed_path: str
    first_page: int
    last_page: int


class PDFMicroarray:
    """
    A class responsible for extracting and analyzing text from PDF documents.
    It also supports plotting the results in a microarray format.
    """

    @classmethod
    def process(cls, documents_path, processed_path, skip=False, threads=-1):
        """
        Processes PDF documents into text, splitting them into segments to
        improve the extraction performance.

        Args:
            documents_path (str): Path to the directory containing PDF files.
            processed_path (str): Directory where processed segments are to be
            stored.
            skip (bool): Whether to skip already processed documents.
            Defaults to False.
            threads (int): Number of concurrent threads to use. Defaults to -1,
            which uses all available CPU cores.
        """

        documents = cls._get_documents(documents_path)
        threads = os.cpu_count() if threads == -1 else threads

        document_segments = cls._compute_segments(
            documents, processed_path, skip, max_pages=20
        )

        print(
            f"Processing {len(documents)} PDFs",
            f"in {len(document_segments)} segments",
            f"using up to {threads} threads",
        )

        start_time = time.time()

        if threads == 1:
            for document_segment in document_segments:
                cls._process_document_segment(document_segment)
        else:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(cls._process_document_segment, document_segments)

        print(
            f"Processed {len(documents)} PDFs",
            f"in {round(time.time() - start_time, 1)} seconds",
        )

    @classmethod
    def analyze(cls, processed_path, words_path, data_path, threshold=90):
        """
        Analyzes extracted text using the Levenshtein distance to find the
        occurrence of specific words.

        Args:
            processed_path (str): Path where processed segments are stored.
            words_path (str): Path to a file containing words to search for.
            data_path (str): Path where the results dataframe will be saved.
            threshold (int): Minimum Levenshtein distance score (0-100) to
            consider a match. Defaults to 90.
        """

        text = cls._get_processed_text(processed_path)
        words = cls._get_words(words_path)

        df = cls._calculate_scores(text, words)
        df.map(lambda x: 1 if x >= threshold else 0)

        df.to_csv(data_path)

    @classmethod
    def plot(cls, data_path, image_path=None, width=30, height=60):
        """
        Generates a plot representing data as a microarray.

        Args:
            data_path (str): Path to the CSV file containing data to plot.
            image_path (str): Path where the plot image will be saved.
            If None, the plot is just displayed. Defaults to None.
            width (int): Width of the plot. Defaults to 30.
            height (int): Height of the plot. Defaults to 60.
        """
        df = pd.read_csv(data_path, index_col=0, dtype={0: str})

        return PlotMicroarray.plot(
            df, image_path=image_path, width=width, height=height
        )

    @classmethod
    def _compute_segments(cls, documents, processed_path, skip, max_pages):
        document_segments = []

        for document_path in documents:
            total_pages = PDFInfo.get_page_count(document_path)
            segments = (total_pages + max_pages - 1) // max_pages

            for segment in range(segments):
                first_page = segment * max_pages
                last_page = min(first_page + max_pages - 1, total_pages - 1)

                doc_proc_path = cls._get_processed_path(
                    document_path, processed_path, first_page, last_page
                )

                if skip and os.path.exists(doc_proc_path):
                    print(
                        f"Skipping {document_path}",
                        f"(pages {first_page + 1}-{last_page + 1})",
                    )
                    continue

                document_segment = Segment(
                    document_path, doc_proc_path, first_page, last_page
                )

                document_segments.append(document_segment)

        return document_segments

    @classmethod
    def _get_processed_path(cls, document_path, processed_path, first, last):
        name = os.path.splitext(os.path.basename(document_path))[0]
        filename = f"{name} [{first + 1}-{last + 1}].txt"
        return os.path.join(processed_path, filename)

    @classmethod
    def _process_document_segment(cls, document_segment):
        document_path, processed_path, first_page, last_page = document_segment

        pages = range(first_page, last_page + 1)
        try:
            pdf_extract = PDFExtract(document_path, pages)
            text_text, text_images, text_pages = pdf_extract.get_text()
        except Exception as e:  # pylint: disable=W0718
            print(f"Error processing {document_path}: {e}")
            return

        text = "".join([text_text, text_images, text_pages])

        avg_word_len = round(cls._get_average_word_length(text), 2)
        space_word_rat = round(cls._get_space_to_word_ratio(text), 2)
        checks = [avg_word_len < 3, space_word_rat < 0.5, space_word_rat > 2]

        pages_msg = f"{first_page + 1}-{last_page + 1}"
        text_msg = f"[{len(text_text)}, {len(text_images)}, {len(text_pages)}]"
        error_msg = f"[{avg_word_len}, {space_word_rat}]"

        print(
            f"Processed {document_path}",
            f"(pages: {pages_msg}, text: {text_msg})",
            f"ERROR: {error_msg}" if any(checks) else "",
        )

        with open(processed_path, "w", encoding="utf-8") as file:
            file.write("".join(text).replace("\n", " "))

    @classmethod
    def _get_average_word_length(cls, text):
        words = text.split()
        return sum(len(word) for word in words) / len(words) if words else 0

    @classmethod
    def _get_space_to_word_ratio(cls, text):
        words = text.split()
        return text.count(" ") / len(words) if words else float("inf")

    @classmethod
    def _calculate_scores(cls, processed_text, words):
        all_scores = []
        for filename, text in processed_text.items():
            scores = {word: fuzz.partial_ratio(word, text) for word in words}
            scores[""] = filename
            all_scores.append(scores)

        df = pd.DataFrame(all_scores)
        df.set_index("", inplace=True)
        df.sort_index(ascending=True, inplace=True)
        return df.T

    @classmethod
    def _get_documents(cls, documents_path):
        documents = []
        for file_name in os.listdir(documents_path):
            if file_name.endswith(".pdf"):
                documents.append(os.path.join(documents_path, file_name))
        return documents

    @classmethod
    def _get_processed_text(cls, processed_path):
        processed = {}
        for file_name in os.listdir(processed_path):
            if file_name.endswith(".txt"):
                full_path = os.path.join(processed_path, file_name)
                name = os.path.splitext(file_name)[0]
                with open(full_path, "r", encoding="utf-8") as file:
                    processed[name] = file.read()

        return cls._merge_processed_segments(processed)

    @classmethod
    def _merge_processed_segments(cls, processed):
        pattern = re.compile(r"(.+?)\s*\[(\d+)-(\d+)\]")

        sorted_processed = []
        for segment_path, text in processed.items():
            match = pattern.match(segment_path)
            if not match:
                print(f"Invalid segment: {segment_path}!")
                continue

            name = match.group(1)
            first_page = int(match.group(2))
            sorted_processed.append((first_page, name, text))
        sorted_processed.sort()

        merged_segments = defaultdict(str)
        for _, name, value in sorted_processed:
            merged_segments[name] += value

        return dict(merged_segments)

    @classmethod
    def _get_words(cls, words_path):
        with open(words_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file.readlines()]
