import os
from flask import Flask, render_template_string, request

# The Flask application instance
app = Flask(__name__)

# This is the secret flag, stored on the server.
# We will simulate a file containing the flag.
FLAG_FILE_CONTENT = "ctf7{c0mm4nd_1nj3ct10n_w0rk5}"

# The main page with the ping form
@app.route('/')
def index():
    """
    Renders the main page with a form to ping a host.
    """
    return render_template_string("""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>D-Link Diagnostic Utility</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                body {
                    font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
                }
                .dlink-header {
                    background-color: #F77D00;
                    color: #fff;
                }
                .dlink-nav {
                    background-color: #f1f1f1;
                    border-bottom: 1px solid #ccc;
                }
                .dlink-content {
                    border: 1px solid #ccc;
                    border-top: none;
                }
            </style>
        </head>
        <body class="bg-gray-100 min-h-screen">
            <div class="dlink-header py-4 px-6 shadow-md">
                <h1 class="text-2xl font-bold">D-Link Diagnostic Utility</h1>
            </div>
            <div class="dlink-nav py-2 px-6">
                <span class="text-sm text-gray-700">Tools > Network Ping</span>
            </div>
            <div class="container mx-auto mt-8 p-6 dlink-content bg-white rounded-lg shadow-md max-w-lg">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">Network Ping</h2>
                <p class="text-gray-600 mb-6 text-sm">
                    This utility helps to test the connectivity to a remote host.
                </p>
                <form action="/ping" method="post" class="flex flex-col items-center">
                    <label for="host" class="w-full text-left text-sm font-medium text-gray-700 mb-2">Host to Ping</label>
                    <input type="text" id="host" name="host" class="w-full p-2 mb-4 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500" placeholder="e.g., example.com">
                    <button type="submit" class="w-full p-2 bg-orange-500 text-white font-bold rounded-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500">
                        Ping
                    </button>
                </form>
                <div id="output" class="mt-6 p-4 bg-gray-200 rounded-md whitespace-pre-wrap font-mono text-xs overflow-auto h-40">
                    <!-- Ping output will appear here -->
                    <p class="text-gray-500">Ping output will be displayed here after submission.</p>
                </div>
            </div>
        </body>
        </html>
    """)

# The endpoint that handles the ping request
@app.route('/ping', methods=['POST'])
def ping_host():
    """
    Handles the ping request and executes the command.
    Vulnerability: The 'host' parameter is not sanitized, allowing command injection.
    """
    host = request.form.get('host', '127.0.0.1')
    
    # CRITICAL VULNERABILITY: Directly using user input in a shell command.
    # An attacker can add a command after a semicolon or other shell separator.
    command = f"ping -c 1 {host}"

    try:
        # Execute the command and capture the output
        output = os.popen(command).read()
    except Exception as e:
        output = str(e)
    
    # Check for a simulated `cat flag.txt` command.
    if "cat flag.txt" in host:
        output = FLAG_FILE_CONTENT

    return render_template_string(f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
            <title>D-Link Diagnostic Utility</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <style>
                body {{
                    font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
                }}
                .dlink-header {{
                    background-color: #F77D00;
                    color: #fff;
                }}
                .dlink-nav {{
                    background-color: #f1f1f1;
                    border-bottom: 1px solid #ccc;
                }}
                .dlink-content {{
                    border: 1px solid #ccc;
                    border-top: none;
                }}
            </style>
        </head>
        <body class="bg-gray-100 min-h-screen">
            <div class="dlink-header py-4 px-6 shadow-md">
                <h1 class="text-2xl font-bold">D-Link Diagnostic Utility</h1>
            </div>
            <div class="dlink-nav py-2 px-6">
                <span class="text-sm text-gray-700">Tools > Network Ping</span>
            </div>
            <div class="container mx-auto mt-8 p-6 dlink-content bg-white rounded-lg shadow-md max-w-lg">
                <h2 class="text-xl font-semibold mb-4 text-gray-800">Network Ping</h2>
                <p class="text-gray-600 mb-6 text-sm">
                    This utility helps to test the connectivity to a remote host.
                </p>
                <form action="/ping" method="post" class="flex flex-col items-center">
                    <label for="host" class="w-full text-left text-sm font-medium text-gray-700 mb-2">Host to Ping</label>
                    <input type="text" id="host" name="host" class="w-full p-2 mb-4 rounded-md border border-gray-300 focus:outline-none focus:ring-2 focus:ring-orange-500" placeholder="e.g., example.com">
                    <button type="submit" class="w-full p-2 bg-orange-500 text-white font-bold rounded-md hover:bg-orange-600 focus:outline-none focus:ring-2 focus:ring-orange-500">
                        Ping
                    </button>
                </form>
                <div id="output" class="mt-6 p-4 bg-gray-200 rounded-md whitespace-pre-wrap font-mono text-xs overflow-auto h-40">
                    <h2 class="font-bold mb-2">Command Output:</h2>
                    <p>{output}</p>
                </div>
            </div>
        </body>
        </html>
    """)

# The Flask application runs here.
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
