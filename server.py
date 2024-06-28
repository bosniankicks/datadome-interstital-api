from flask import Flask, request, jsonify
import subprocess
import json
import sys

app = Flask(__name__)

@app.route('/get_dd', methods=['POST'])
def get_dd():
    data = request.json
    url = data.get('url')
    proxy = data.get('proxy')

    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        print(f"Received request for URL: {url}")
        print(f"Flask server is using Python executable: {sys.executable}")
        
        cmd = [sys.executable, 'get_dd.py', url]
        if proxy:
            cmd.append(proxy)
        
        # Call the Playwright script using the current Python executable
        result = subprocess.run(
            cmd,
            capture_output=True, text=True
        )
        
        print(f"Subprocess stdout: {result.stdout}")
        print(f"Subprocess stderr: {result.stderr}")
        try:
            output = json.loads(result.stdout)
        except json.JSONDecodeError as e:
            print("JSON decode error:", e, file=sys.stderr)
            print(f"Subprocess stdout: {result.stdout}", file=sys.stderr)
            return jsonify({'error': 'Failed to parse Playwright script output'}), 500

        response_data = {
            'code': output.get('code', 200),
            'cookie': output.get('cookie'),
            'useragent': output.get('agent'),
            'url': output.get('url'),
            'proxy': proxy
        }

        formatted_response = json.dumps(response_data, indent=4)
        with open('response.txt', 'w') as file:
            file.write(formatted_response)
        return app.response_class(formatted_response, content_type='application/json')
    except subprocess.CalledProcessError as e:
        print(f"Subprocess error: {e}", file=sys.stderr)
        print(f"Standard Output: {e.stdout}")
        print(f"Standard Error: {e.stderr}")
        return jsonify({'error': 'Failed to execute Playwright script', 'stdout': e.stdout, 'stderr': e.stderr}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)  # Make sure to use a free port
