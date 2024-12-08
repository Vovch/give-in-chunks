# Overview

A web application that processes large text inputs by splitting them into manageable chunks and processes each chunk through Google's Gemini AI model (Gemini Flash - 1.5, currently). The application includes rate limiting capabilities and parallel processing features. 


# Example usage:

Prompt:
```
This is the part of subtitles for the music man 1962 Movie. Please translate it to Russian Make sure that in the end you will get the correct subtitles In .srt format. Please do not format the result with the markdown leave only the subtitles as if they were in .srt file. Please leave the numbers of the subtitle entries and the times as is.

Example:
48
00:04:47,829 --> 00:04:48,871
What's the fella's line?
What's his line?

Result:
48
00:04:47,829 --> 00:04:48,871
Чем этот парень занимается?
Какая у него профессия?
```
Text:

```
1
00:02:38,408 --> 00:02:40,451
All aboard!

2
00:02:49,252 --> 00:02:50,461
Let him go, Orville.

3
00:02:50,670 --> 00:02:55,258
We made it plain we don't want
no more traveling salesmen in Brighton.

...
```

Separator: `\n\n` 
(double pressed enter)

Parallel Requests: `15`

Max Requests per Minute: `15`

Chunk Size: `6500`

## Features

- Split large text inputs into manageable chunks using custom separators
- Process text chunks in parallel using Google's Gemini AI model
- Rate limiting to control API requests per minute
- Save individual chunk responses to separate files
- Web interface for easy interaction
- Configurable chunk size and parallel processing

## Prerequisites

- Python 3.10 or higher
- Google Cloud API key for Gemini AI
- Modern web browser

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/give-in-chunks.git
cd give-in-chunks
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Google API key:
```bash
API_KEY=your_google_api_key_here
```

## Usage

1. Start the Flask server:
```bash
python main.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. In the web interface, you can configure:
   - Prompt for the AI model
   - Input text to be processed
   - Separator for splitting text into chunks (default: '\n\n')
   - Number of parallel requests (default: 3)
   - Maximum requests per minute (optional rate limiting)
   - Chunk size in characters (default: 2000)

4. Click "Generate" to process your text

## Configuration Options

- **Separator**: Custom text pattern for splitting chunks (e.g., '\n\n' for paragraphs)
- **Parallel Requests**: Number of chunks to process simultaneously
- **Max Requests per Minute**: Optional rate limiting for API requests
- **Chunk Size**: Controls the maximum size of each text chunk (in characters)

## Output

- Processed responses are displayed in the web interface
- Individual chunk responses are saved in the `responses` directory
- Each response file is named with timestamp and chunk index for easy tracking

## Error Handling

- Failed chunk processing is logged to separate error files
- Error messages are displayed in the web interface
- Rate limiting automatically adjusts parallel requests to stay within limits

## Project Structure

- `main.py`: Flask web application and route handlers
- `generate.py`: Core text processing and AI interaction logic
- `requirements.txt`: Python package dependencies
- `.env`: Configuration for API keys (not in repository)
- `responses/`: Directory for storing chunk processing results
