from flask import Flask, request, render_template_string, jsonify
from generate import generate
import subprocess

app = Flask(__name__)

HTML_TEMPLATE = '''
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
    </script>
  </head>
  <body>
    <h1>Generate Content with LLM</h1>
    <form onsubmit="submitForm(event)">
      <label for="prompt">Prompt for LLM:</label><br>
      <textarea id="prompt" name="prompt" rows="10" cols="80">{{ prompt }}</textarea><br>
      
      <label for="text">Text:</label><br>
      <textarea id="text" name="text" rows="10" cols="80">{{ text }}</textarea><br>
      
      <label for="separator">Separator:</label><br>
      <textarea id="separator" name="separator" rows="3" cols="80">{{ separator }}</textarea><br>
      
      <label for="parallel_requests">Amount of Parallel Requests:</label><br>
      <input type="number" id="parallel_requests" name="parallel_requests" value="{{ parallel_requests or 1 }}"><br>
      
      <label for="chunk_size">Size of a Chunk in Symbols:</label><br>
      <input type="number" id="chunk_size" name="chunk_size" value="{{ chunk_size or 1000 }}"><br>
      
      <input type="submit" value="Generate">
    </form>
    <div id="result"></div>
  </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE,
                                prompt=request.args.get('prompt', ''),
                                text=request.args.get('text', ''),
                                separator=request.args.get('separator', ''),
                                parallel_requests=request.args.get('parallel_requests', 1),
                                chunk_size=request.args.get('chunk_size', 1000))

@app.route('/generate', methods=['POST'])
def generate_content():
    prompt = request.form.get('prompt')
    text = request.form.get('text')
    separator = request.form.get('separator')
    parallel_requests = request.form.get('parallel_requests')
    chunk_size = request.form.get('chunk_size')
    
    # Call the generate function with the provided parameters
    result = generate(prompt, text, separator, int(parallel_requests), int(chunk_size))
    
    # Return JSON response
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
