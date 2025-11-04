from tkinter import W
from typing import Optional
from flask import Flask, request, render_template_string, jsonify
from generate import generate
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>LLM Request Form</title>
    <style>
      body { padding: 20px; max-width: 800px; margin: 0 auto; }
      textarea, input { margin-bottom: 10px; }
      .response { white-space: pre-wrap; background: #f5f5f5; padding: 15px; margin-top: 20px; }
      #result { margin-top: 20px; }
    </style>
    <script>
      function submitForm(event) {
        event.preventDefault();
        const form = event.target;
        const formData = new FormData(form);

        fetch('/generate', {
          method: 'POST',
          body: formData
        })
        .then(response => response.json())
        .then(data => {
          document.getElementById('result').innerHTML = `<div class="response"><h2>Generated Content:</h2>${data.result}</div>`;
        })
        .catch(error => {
          console.error('Error:', error);
          document.getElementById('result').innerHTML = `<div class="response">Error: ${error}</div>`;
        });
      }

      function registerFileLoader(fileInputId, textareaId) {
        document.addEventListener('DOMContentLoaded', () => {
          const fileInput = document.getElementById(fileInputId);
          const textarea = document.getElementById(textareaId);

          if (!fileInput || !textarea) {
            return;
          }

          fileInput.addEventListener('change', () => {
            const [file] = fileInput.files;
            if (!file) {
              return;
            }

            const reader = new FileReader();
            reader.onload = (event) => {
              textarea.value = event.target?.result || '';
            };
            reader.onerror = () => {
              console.error(`Failed to read file: ${file.name}`);
            };
            reader.readAsText(file);
          });
        });
      }

      registerFileLoader('prompt_file', 'prompt');
      registerFileLoader('text_file', 'text');
    </script>
  </head>
  <body>
    <h1>Generate Content with LLM</h1>
    <form onsubmit="submitForm(event)" enctype="multipart/form-data">
      <label for="prompt">Prompt for LLM:</label><br>
      <textarea id="prompt" name="prompt" rows="10" cols="80">{{ prompt }}</textarea><br>
      <label for="prompt_file">Prompt File (optional):</label><br>
      <input type="file" id="prompt_file" name="prompt_file" accept=".txt,.md,.srt,.json,.csv"><br>

      <label for="text">Text:</label><br>
      <textarea id="text" name="text" rows="10" cols="80">{{ text }}</textarea><br>
      <label for="text_file">Text File (optional):</label><br>
      <input type="file" id="text_file" name="text_file" accept=".txt,.md,.srt,.json,.csv"><br>

      <label for="separator">Separator:</label><br>
      <textarea id="separator" name="separator" rows="3" cols="80">{{ separator }}</textarea><br>

      <label for="parallel_requests">Parallel Requests:</label><br>
      <input type="number" id="parallel_requests" name="parallel_requests" value="{{ parallel_requests if parallel_requests else 3 }}" min="1"><br>

      <label for="max_requests_per_minute">Max Requests per Minute (optional):</label><br>
      <input type="number" id="max_requests_per_minute" name="max_requests_per_minute" value="{{ max_requests_per_minute if max_requests_per_minute else '' }}" min="1"><br>

      <label for="chunk_size">Chunk Size:</label><br>
      <input type="number" id="chunk_size" name="chunk_size" value="{{ chunk_size if chunk_size else 2000 }}" min="100"><br>

      <input type="submit" value="Generate">
    </form>
    <div id="result"></div>
  </body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(
        HTML_TEMPLATE,
        prompt="""This is the part of subtitles for a movie. Please translate it to Russian. Make sure that in the end you will get the correct subtitles In .srt format. Please do not format the result with the markdown leave only the subtitles as if they were in .srt file. Please leave the numbers of the subtitle entries and the times as is.

Example:
48
00:04:47,829 --> 00:04:48,871
What's the fella's line?
What's his line?

Result:
48
00:04:47,829 --> 00:04:48,871
Чем этот парень занимается?
Какая у него профессия?""",
        text="",
        separator="\n\n",
        parallel_requests=5,
        chunk_size=8000,
        max_requests_per_minute=5,
    )


@app.route("/generate", methods=["POST"])
def generate_content():

    def read_uploaded_text(field_name: str) -> Optional[str]:
        uploaded_file = request.files.get(field_name)
        if not uploaded_file or not uploaded_file.filename:
            return None

        file_bytes = uploaded_file.read()
        if not file_bytes:
            return ""

        for encoding in ("utf-8-sig", "utf-8"):
            try:
                return file_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue

        return file_bytes.decode("utf-8", errors="replace")

    prompt = read_uploaded_text("prompt_file")
    if prompt is None:
        prompt = request.form.get("prompt", "")

    text = read_uploaded_text("text_file")
    if text is None:
        text = request.form.get("text", "")
    separator = request.form.get("separator", "\n\n")
    parallel_requests = int(request.form.get("parallel_requests", 5))
    chunk_size = int(request.form.get("chunk_size", 8000))
    max_requests_per_minute = request.form.get("max_requests_per_minute", 5)

    # Convert empty string to None for max_requests_per_minute
    if max_requests_per_minute:
        max_requests_per_minute = int(max_requests_per_minute)
    else:
        max_requests_per_minute = None

    result = generate(
        prompt, text, separator, parallel_requests, chunk_size, max_requests_per_minute
    )
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(debug=True)
