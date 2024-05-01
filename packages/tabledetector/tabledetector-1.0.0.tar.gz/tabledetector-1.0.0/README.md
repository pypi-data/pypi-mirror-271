# Tabledetector

Tabledetector is a Python package that takes PDFs or Images as input, checks the alignment, re-aligns if required, detects the table structure, extracts data, return as pandas dataframe for further use. The current implementation focuses on bordered, semibordered and unbordered table structures.

## Features

- **PDF Input:** Accepts PDF/Image files as input for table detection.
- **Alignment Check:** Verifies and adjusts alignment of input.
- **Table Detection:** Identifies bordered, semibordered and unbordered tables in the PDF/Image File.
- **Table Extraction:** Extract the tabular data in the form of dataframe.

## Libraries Used

- Python 3.x
- OpenCV
- NumPy
- pdf2image
- Pillow
- scipy
- jinja2
- easyocr
- pandas

## Create and Activate Environment
```bash
conda create -n <env_name> python=3.7
conda activate <env_name>
```
## Installation of package using pip

```bash
pip install tabledetector
```

## Clone the repository for latest development release

```bash
git clone https://github.com/rajban94/TableDetector.git
```

## Usage
For bordered table detection:
```bash
import tabledetector as td
result = td.detect(pdf_path="pdf_path", method="bordered")
```

For semibordered table detection:
```bash
import tabledetector as td
result = td.detect(pdf_path="pdf_path", method="semibordered")
```

For unbordered table detection:
```bash
import tabledetector as td
result = td.detect(pdf_path="pdf_path", method="unbordered")
```
If no method is mentioned in that case it will check for all the methods and will provide the result accordingly.