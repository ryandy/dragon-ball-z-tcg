'''Local dev server for web/. Adds cross-origin-isolation headers so
SharedArrayBuffer is available - not needed by P1a's output-only path, but
required by P1b's synchronous input bridge, and free to set up now so the
same server works for both without reconfiguring.

Usage: python web/serve.py [port]
'''
import functools
import http.server
import pathlib
import sys


class IsolatedRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'require-corp')
        # This is a local dev server - always serve fresh files (e.g.
        # worker.js, loaded dynamically via `new Worker(...)` and thus not
        # covered by a page-level hard reload) instead of letting the
        # browser's HTTP cache serve stale content after an edit.
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()


def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    web_dir = pathlib.Path(__file__).parent
    handler = functools.partial(IsolatedRequestHandler, directory=str(web_dir))

    with http.server.ThreadingHTTPServer(('localhost', port), handler) as httpd:
        print(f'Serving {web_dir} at http://localhost:{port} (cross-origin isolated)')
        httpd.serve_forever()


if __name__ == '__main__':
    main()
