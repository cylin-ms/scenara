#!/usr/bin/env python3
"""
Simple web server to view MyGraph locally
"""

import http.server
import socketserver
import webbrowser
import os
import threading
import time

def start_server():
    """Start a simple HTTP server"""
    # Change to the docs directory
    os.chdir('/Users/cyl/projects/Scenara/docs')
    
    # Use a random available port
    port = 8000
    max_attempts = 10
    
    for attempt in range(max_attempts):
        try:
            with socketserver.TCPServer(("", port), http.server.SimpleHTTPRequestHandler) as httpd:
                print(f"🌐 MyGraph Server starting on http://localhost:{port}")
                print(f"📊 View your graph at: http://localhost:{port}/mygraph_explorer.html")
                print()
                print("🎯 Your MyGraph has:")
                print("   📊 1,207 nodes (people, docs, meetings, etc.)")
                print("   🔗 1,097 links (relationships)")
                print("   📅 Data from October 15 (9 days ago)")
                print()
                print("💡 Tips:")
                print("   • Drag nodes to explore relationships")
                print("   • Use search to find specific people/items")
                print("   • Zoom in/out with mouse wheel")
                print("   • Different colors represent different types")
                print()
                print("🛑 Press Ctrl+C to stop the server")
                print()
                
                # Auto-open browser after a short delay
                def open_browser():
                    time.sleep(1)
                    webbrowser.open(f'http://localhost:{port}/mygraph_explorer.html')
                
                browser_thread = threading.Thread(target=open_browser)
                browser_thread.daemon = True
                browser_thread.start()
                
                httpd.serve_forever()
                
        except OSError:
            port += 1
            if attempt == max_attempts - 1:
                print(f"❌ Could not start server on any port from 8000 to {8000 + max_attempts}")
                return
            continue

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Thanks for using MyGraph!")