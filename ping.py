from bottle import run, route, request
import subprocess
import shlex

@route('/', method=['GET'])
def index():
    return '''
        <html>
        <head>
            <title>Ping Web App</title>
        </head>
        <body>
            <h1>Ping Web App</h1>
            <p>Enter a host to ping:</p>
            <form action="/ping" method="post">
                <input type="text" name="host" placeholder="example.com or 8.8.8.8" required>
                <button type="submit">Ping</button>
            </form>
        </body>
        </html>
    '''

@route('/ping', method=['POST'])
def do_ping():
    host = request.forms.get('host', '').strip()

    if not host:
        return '<p>No host provided.</p>'

    # Very simple validation: avoid spaces etc.
    if any(c.isspace() for c in host):
        return '<p>Invalid host.</p>'

    try:
        # Use subprocess instead of os.popen for safety
        result = subprocess.run(
            ['ping', '-c', '1', host],
            capture_output=True,
            text=True,
            timeout=5
        )
        output = result.stdout or result.stderr
    except Exception as e:
        output = f'Error running ping: {e}'

    page = f'''
        <html>
        <head>
            <title>Ping result for {host}</title>
        </head>
        <body>
            <h1>Ping result for {host}</h1>
            <pre>{output}</pre>
            <p><a href="/">Ping another host</a></p>
        </body>
        </html>
    '''
    return page

run(host='127.0.0.1', port=8080, debug=True, reloader=True)
