# PDF File Renaming Agent

A Python-based tool that automatically renames PDF files based on their content using AI-powered summarization. The tool analyzes the content of each PDF file and generates a descriptive filename that includes the creation date and a meaningful description of the document's content.

## Features

- Automatically processes all PDF files in a specified folder
- Extracts text content from PDF files
- Uses OpenAI's GPT-4 to generate meaningful summaries and filenames
- Adds creation date prefix to filenames (YYMMDD format)
- Maintains original file extensions
- Prevents duplicate filenames
- Provides detailed logging of the renaming process

## Requirements

- Python 3.x
- OpenAI API key
- Required Python packages:
  - `PyPDF2`
  - `openai`
  - `python-dotenv`

## Installation

1. Clone this repository:
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
   - Create a `.env` file in the project root
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY="your-api-key-here"
     ```

## Usage

1. Run the script:
```bash
python PDF_file_renamer.py
```

2. When prompted, drag and drop your folder containing PDF files into the terminal, or paste the folder path.

3. The script will process each PDF file and rename it using the following format:
```
YYMMDD_DocumentType Key Descriptive Words.pdf
```

Example: `230415_Report Financial Analysis Q1.pdf`

## File Naming Convention

The new filenames follow this structure:
- Date prefix (YYMMDD format)
- Underscore separator
- Document type (e.g., Report, Whitepaper, Guide)
- Descriptive words (based on content analysis)
- Original file extension

## Error Handling

The script includes robust error handling for:
- Invalid file paths
- PDF reading errors
- API communication issues
- Duplicate filenames
- File permission issues

## Security Note

- Keep your OpenAI API key secure
- Don't share the script with your API key embedded
- Consider using environment variables for API key storage

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is open source and available under the MIT License.