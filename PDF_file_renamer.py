import os
from datetime import datetime
import PyPDF2
from openai import OpenAI
from dotenv import load_dotenv

def get_file_creation_date(file_path):
    """Get file creation date and format as YYMMDD"""
    creation_time = os.path.getctime(file_path)
    date = datetime.fromtimestamp(creation_time)
    return date.strftime("%y%m%d")

def get_file_summary(file_content, client):
    """First get a summary of the file content, then generate a filename from that summary"""
    try:
        # Step 1: Get content summary
        summary_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Summarize the key points of this file content in 2-3 sentences."},
                {"role": "user", "content": file_content}
            ]
        )
        summary = summary_response.choices[0].message.content.strip()
        
        # Step 2: Generate filename from summary
        filename_response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                    {"role": "system", "content": """Generate a descriptive filename with these strict rules:
                        1. Start with document type (e.g., Whitepaper, Guide, Report, Proposal, Email, Contract, Invoice)
                        2. Use spaces between words
                        3. Be specific but concise
                        4. Maximum 50 characters total
                        5. No special characters except spaces
                        6. Format: 'DocumentType Key Descriptive Words'
                        
                        Examples:
                        - Whitepaper Quantum Computing Applications
                        - Guide Azure Cloud Migration
                        - Proposal Marketing Strategy 2024
                        - Report Q4 Financial Results
                        - Email Board Meeting Minutes"""},
                    {"role": "user", "content": summary}
                ]
        )
        suggested_filename = filename_response.choices[0].message.content.strip()
        
        return {
            'summary': summary,
            'filename': suggested_filename
        }
    except Exception as e:
        print(f"Error in file processing: {e}")
        return None


def read_pdf_content(file_path):
    """Read and extract text content from a PDF file"""
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text_content = []
            
            # Extract text from each page
            for page in reader.pages:
                text = page.extract_text()
                if text:  # Only append if text was extracted
                    text_content.append(text)
            
            return '\n'.join(text_content)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except PyPDF2.PdfReadError as e:
        print(f"Error reading PDF: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def process_folder(folder_path, api_key):
    """Process all files in the specified folder"""
    client = OpenAI(api_key=api_key)
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        
        # Skip if it's not a file
        if not os.path.isfile(file_path):
            continue
            
        # Get creation date
        date_prefix = get_file_creation_date(file_path)
        
        # Read file content
        content = read_pdf_content(file_path)
        if content is None:  # Skip if PDF reading failed
            print(f"Skipping {filename} due to reading error")
            continue
        
        # Get summary and suggested filename from OpenAI
        result = get_file_summary(content, client)
        if not result:
            print(f"Skipping {filename} due to summary generation error")
            continue
            
        # Create new filename
        file_extension = os.path.splitext(filename)[1]
        new_filename = f"{date_prefix}_{result['filename']}{file_extension}"
        new_filepath = os.path.join(folder_path, new_filename)
        
        # Rename file
        try:
            # Check if target filename already exists
            if os.path.exists(new_filepath):
                print(f"Warning: Target file {new_filename} already exists, skipping rename")
                continue
                
            os.rename(file_path, new_filepath)
            print(f"Renamed: {filename} -> {new_filename}")
            print(f"Summary: {result['summary']}")
        except Exception as e:
            print(f"Error renaming {filename}: {e}")

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OpenAI API key not found. Please check your .env file.")

folder_path = input("Drag your folder here: ").strip("'\"")

if not os.path.exists(folder_path):
    print("Folder does not exist!")
else:
    process_folder(folder_path, api_key)