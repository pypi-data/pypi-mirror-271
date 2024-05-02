# PDFMicroarray

## Overview

PDFMicroarray is a Python CLI tool designed to assist with literature research for scientific papers and books.

It extracts text from multiples sources within PDF documents, including:

- Plain text
- Text from images (through OCR)
- Text from embedded diagrams (through page rendering and OCR)

and stores the extracted text in a designated output directory.

The processed text can then analyzed using the [Levenshtein distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to detect the occurrences of specified words. A graphical representation of these occurrences is offered in a microarray format.

## Installation

```bash
pip install pipx
pipx install pdf-microarray
```

## Usage

```bash
mkdir processed
pdf-microarray process -i documents -o processed
pdf-microarray analyze -i processed -w words.txt -o data.csv
pdf-microarray plot -i data.csv -o plot.png
```

The words in `words.txt` should be separated by newlines. If multiple words are on the same line, only the occurrence of all words is taken into account.

## Example

![Example](example.png)

## Technical details

The library uses document segmentation and multithreading to speed up the extraction process, so that even large books in PDF form can be parsed within a few minutes.

The library utilized [PyMuPDF](https://pypi.org/project/PyMuPDF) for OCR,  [pytesseract](https://pypi.org/project/pytesseract) for PDF page rendering and [thefuzz](https://pypi.org/project/thefuzz) to calculate the Levenshtein distance.

## Contributing

Contributions to PDFMicroarray are welcome! Please feel free to fork the repository, make changes, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

Distributed under the GNU General Public License v3.0 license. See LICENSE for more information.
