# Overview

A web application for processing large text inputs. It splits the text into manageable chunks and sends each chunk to Google Gemini (currently Gemini Flash 2.0). The interface supports pasting or uploading prompt/content files, offers rate limiting controls, and provides a consolidated download of the model output.

> For a Russian translation, see [`readme.ru.md`](readme.ru.md).


## Example usage

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

Separator: `\n\n` (press Enter twice)

Parallel Requests: `15`

Max Requests per Minute: `15`

Chunk Size: `6500`

## Features

- Split large text inputs into manageable chunks using custom separators
- Process text chunks in parallel using Google's Gemini AI model
- Rate limiting to control API requests per minute
- Save individual chunk responses to separate files
- Upload prompt/input text from local files for quicker setup
- Download a single combined output file after processing
- Web interface for easy interaction with configurable chunk size and parallelism

## Prerequisites

- Python 3.10 or higher
- Google Cloud API key for Gemini AI
- Modern web browser

## Preferred installation (Docker)

The quickest way to get started is to run the app in Docker. This keeps dependencies isolated and matches the recommended setup.

1. Make sure you have Docker (and optionally Docker Compose) installed.
2. Create a `.env` file (or copy `.env.example`) and set `API_KEY`.
3. Launch the stack with Docker Compose:
   ```bash
   docker compose up --build
   ```
   The web UI becomes available at `http://localhost:5000`, and responses are written to the local `responses/` folder.
4. Stop the stack with:
   ```bash
   docker compose down
   ```

To run the container without Compose:
```bash
docker build -t give-in-chunks .
docker run --rm -p 5000:5000 --env-file .env -v %cd%/responses:/app/responses give-in-chunks
```
Replace `%cd%` with `$(pwd)` when using a Unix-like shell.

## Manual installation

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

3. Install the dependencies:
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

3. In the web interface, you can configure or supply:
   - Prompt for the AI model (paste text or select a prompt file)
   - Input text to be processed (paste text or select a text file)
   - Separator for splitting text into chunks (default: `\n\n\n`)
   - Number of parallel requests (default: `5`)
   - Maximum requests per minute (optional rate limiting)
   - Chunk size in characters (default: `8000`)

4. Click **Generate** to process your text. After completion, the page displays the model output along with a download link for the combined response.

## Configuration Options

- **Separator**: Custom text pattern for splitting chunks (e.g., `\n\n` for paragraphs)
- **Parallel Requests**: Number of chunks to process simultaneously
- **Max Requests per Minute**: Optional rate limiting for API requests
- **Chunk Size**: Controls the maximum size of each text chunk (in characters)

## Output

- Processed responses are displayed in the web interface
- A consolidated response file can be downloaded via the provided link
- Individual chunk responses remain saved in the `responses` directory with timestamped names for easy tracking

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

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to:
- Update `README.md` with details of your changes when relevant
- Update `requirements.txt` if you add new dependencies
- Follow existing code style and formatting
- Add comments to your code where necessary
- Test your changes thoroughly

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

The Apache License 2.0 is a permissive license that allows users to use the software freely while requiring attribution to the original author and maintaining the same license for derivative works.
