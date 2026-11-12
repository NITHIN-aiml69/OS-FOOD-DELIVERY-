import os
import sys

# Ensure root directory is on the Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from platform_server import app

# Add aliases for index route to cover Vercel rewrites
app.add_url_rule('/api/index', 'index_alias_1', app.view_functions['index'])
app.add_url_rule('/api/index/', 'index_alias_2', app.view_functions['index'])
app.add_url_rule('/api', 'index_alias_3', app.view_functions['index'])
app.add_url_rule('/api/', 'index_alias_4', app.view_functions['index'])

# WSGI Middleware to normalize Vercel rewritten PATH_INFO
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        if path.startswith('/api/index'):
            stripped = path[len('/api/index'):]
            environ['PATH_INFO'] = stripped if stripped and stripped.startswith('/') else ('/' + stripped if stripped else '/')
        elif path in ['/api', '/api/']:
            environ['PATH_INFO'] = '/'
        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Vercel WSGI entry point (exports 'app')
if __name__ == "__main__":
    app.run(port=8080)
