# pylint: disable=W0622
"""
This module provides a command-line interface (CLI) for the PDFMicroarray
library. It allows users to process, analyze, and plot text occurrences
extracted from PDF documents, enabling literature research through a terminal
interface.
"""


import click

from pdf_microarray.pdf_microarray import PDFMicroarray

DIR = click.Path(exists=True, dir_okay=True)
FILE = click.Path(exists=True, file_okay=True)


@click.group()
def cli():
    """
    Command line interface for managing PDF data extraction, analysis, and
    visualization.
    """


P_INPUT = "Path to the directory containing the PDF documents."
P_OUTPUT = "Path where processed text segments will be stored."
P_SKIP = "Whether to skip the processing of files that have already been \
processed. Defaults to False."
P_THREADS = "Number of threads to use for concurrent processing. Defaults \
to using all available CPU cores (-1)."


@cli.command()
@click.option("-i", "--input", type=DIR, required=True, help=P_INPUT)
@click.option("-o", "--output", type=DIR, required=True, help=P_OUTPUT)
@click.option("--skip", type=bool, default=False, help=P_SKIP)
@click.option("--threads", type=int, default=-1, help=P_THREADS)
def process(input, output, skip, threads):
    """
    Processes PDF documents by extracting plain text, text from images and
    text from embedded diagrams, saving the results in the specified output
    directory.
    """
    PDFMicroarray.process(input, output, skip=skip, threads=threads)


A_INPUT = "Path to the directory where processed segments are stored."
A_WORDS = "Path to the file containing the list of words to search for."
A_OUTPUT = "Path where the analysis results in CSV format will be saved."
A_THRESHOLD = "Minimum score (0-100) to consider a word match using \
Levenshtein distance. Defaults to 90."


@cli.command()
@click.option("-i", "--input", type=DIR, required=True, help=A_INPUT)
@click.option("-w", "--words", type=FILE, required=True, help=A_WORDS)
@click.option("-o", "--output", required=True, help=A_OUTPUT)
@click.option("--threshold", type=int, default=90, help=A_THRESHOLD)
def analyze(input, words, output, threshold):
    """
    Analyzes extracted text from PDFs for specific word occurrences, using
    Levenshtein distance, and saves the results to a CSV file.
    """
    PDFMicroarray.analyze(input, words, output, threshold=threshold)


L_INPUT = "Path to the CSV file containing data to be visualized."
L_WIDTH = "Width of the generated plot in inches. Defaults to 60."
L_HEIGHT = "Height of the generated plot in inches. Defaults to 30."
L_OUTPUT = "Optional path to save the generated plot image as a PNG file."


@cli.command()
@click.option("-i", "--input", type=FILE, required=True, help=L_INPUT)
@click.option("-o", "--output", default=None, help=L_OUTPUT)
@click.option("--width", type=int, default=60, help=L_WIDTH)
@click.option("--height", type=int, default=30, help=L_HEIGHT)
def plot(input, output, width, height):
    """
    Plots the analysis results from the given CSV file, visualizing the data
    in a microarray format.
    """
    PDFMicroarray.plot(input, image_path=output, width=width, height=height)
