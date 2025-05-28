# PDF File Renamer

A simple tool that renames PDF files based on their content. It uses AI to read your PDFs and give them meaningful names.

## What you need

- Python 3.x
- OpenAI API key
- These Python packages:
  - `PyPDF2`
  - `openai`
  - `python-dotenv`

## Setup

1. Install the required packages:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file and add your OpenAI API key:
```
OPENAI_API_KEY="your-api-key-here"
```

## How to use

1. Run the script:
```bash
python PDF_file_renamer.py
```

2. When prompted, drag and drop your folder of PDFs into the terminal.

The script will rename your PDFs to include their creation date and a description of their content. For example: `230415_Report Financial Analysis.pdf`