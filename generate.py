import google.generativeai as genai
import os
from dotenv import load_dotenv
import asyncio
import math
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def find_split_position(text, chunk_size, separator, threshold=100):
    """Find the best position to split text, preferring separator near chunk end."""
    if len(text) <= chunk_size:
        return len(text)
    
    # Look for separator in the threshold range near chunk_size
    search_start = max(0, chunk_size - threshold)
    search_end = min(len(text), chunk_size + threshold)
    search_text = text[search_start:search_end]
    
    if separator:
        # Find the last occurrence of separator in the search range
        last_sep = search_text.rfind(separator)
        if last_sep != -1:
            return search_start + last_sep + len(separator)
    
    # If no separator found or no separator provided, split at chunk_size
    return chunk_size

def split_text_into_chunks(text, chunk_size, separator):
    """Split text into chunks, trying to split at separator near chunk boundaries."""
    chunks = []
    current_pos = 0
    
    while current_pos < len(text):
        split_pos = find_split_position(text[current_pos:], chunk_size, separator)
        chunks.append(text[current_pos:current_pos + split_pos])
        current_pos += split_pos
    
    return chunks

def process_chunk(model, prompt, chunk, chunk_index):
    """Process a single chunk with the model and save response to a file."""
    try:
        final_prompt = f"{prompt}\n\nText chunk to process:\n{chunk}"
        response = model.generate_content(final_prompt)
        
        # Create responses directory if it doesn't exist
        os.makedirs('responses', exist_ok=True)
        
        # Generate timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"responses/chunk_{chunk_index}_{timestamp}.txt"
        
        # Write response to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        return response.text
    except Exception as e:
        error_msg = f"Error processing chunk: {str(e)}"
        
        # Write error to file as well
        os.makedirs('responses', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"responses/chunk_{chunk_index}_{timestamp}_error.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(error_msg)
            
        return error_msg

def generate(prompt, text, separator, parallel_requests, chunk_size):
    """Generate content using the Google Generative AI model."""
    genai.configure(api_key=os.getenv("API_KEY"))
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Calculate effective chunk size (chunk_size minus prompt size to ensure total size stays within limit)
    prompt_size = len(prompt)
    effective_chunk_size = chunk_size - prompt_size - 50  # 50 chars buffer for formatting
    if effective_chunk_size <= 0:
        return "Error: Chunk size must be larger than prompt size"

    # Split text into chunks, considering separator
    chunks = split_text_into_chunks(text, effective_chunk_size, separator)
    
    # Process chunks in parallel batches
    all_responses = []
    with ThreadPoolExecutor(max_workers=parallel_requests) as executor:
        for i in range(0, len(chunks), parallel_requests):
            batch = chunks[i:i + parallel_requests]
            futures = [executor.submit(process_chunk, model, prompt, chunk, i + j) for j, chunk in enumerate(batch)]
            batch_responses = [future.result() for future in futures]
            all_responses.extend(batch_responses)

    formatted_responses = []
    for i, response in enumerate(all_responses, 1):
        formatted_responses.append(f"{response}")

    return separator.join(formatted_responses)
