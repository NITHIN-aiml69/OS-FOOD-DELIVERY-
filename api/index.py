import os
import sys
from urllib.parse import parse_qs

# Ensure root directory is on the Python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from platform_server import app

# Normalization middleware
class VercelPathMiddleware:
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        qs = parse_qs(environ.get('QUERY_STRING', ''))
        if '__subpath__' in qs and qs['__subpath__']:
            sub = qs['__subpath__'][0]
            environ['PATH_INFO'] = sub if sub else '/'
            return self.wsgi_app(environ, start_response)

        # Fallback to header inspection if rewrite didn't append query param
        for h in ['HTTP_X_FORWARDED_URI', 'HTTP_X_ORIGINAL_URL', 'HTTP_X_NOW_ROUTE_MATCHES', 'HTTP_X_MATCHED_PATH', 'RAW_URI']:
            val = environ.get(h)
            if val and not val.startswith('/api/index'):
                clean = val.split('?')[0]
                environ['PATH_INFO'] = clean
                return self.wsgi_app(environ, start_response)

        path = environ.get('PATH_INFO', '')
        if path in ['/api/index', '/api/index/', '/api', '/api/']:
            environ['PATH_INFO'] = '/'
        elif path.startswith('/api/index/'):
            sub = path[len('/api/index'):]
            environ['PATH_INFO'] = sub if sub else '/'

        return self.wsgi_app(environ, start_response)

app.wsgi_app = VercelPathMiddleware(app.wsgi_app)

# Vercel WSGI entry point (exports 'app')
if __name__ == "__main__":
    app.run(port=8080)
