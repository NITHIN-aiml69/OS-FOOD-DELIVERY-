import os
import sys

# Ensure root directory is on the Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from platform_server import app

# WSGI Middleware to normalize Vercel rewritten PATH_INFO
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        # 1. Check if Vercel passed original requested URI in headers
        for h in ['HTTP_X_FORWARDED_URI', 'HTTP_X_ORIGINAL_URL', 'HTTP_X_NOW_ROUTE_MATCHES']:
            val = environ.get(h)
            if val and not val.startswith('/api/index'):
                clean_path = val.split('?')[0]
                environ['PATH_INFO'] = clean_path
                return self.wsgi_app(environ, start_response)
        
        path = environ.get('PATH_INFO', '')
        # If the path is exactly /api/index, /api, or /api/, it's the root dashboard
        if path in ['/api/index', '/api/index/', '/api', '/api/']:
            environ['PATH_INFO'] = '/'
        # If the path is prefixed with /api/index/, strip it so subroutes match cleanly
        elif path.startswith('/api/index/'):
            sub = path[len('/api/index'):]
            environ['PATH_INFO'] = sub if sub else '/'

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Vercel WSGI entry point (exports 'app')
if __name__ == "__main__":
    app.run(port=8080)
