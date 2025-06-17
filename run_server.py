#!/usr/bin/env python3
"""
Run script for the Ancient Indian Encryption Systems REST server.
"""
import argparse
import socket
from contextlib import closing
from Source.Controller.restService import app

def find_free_port(start_port=5000, max_port=65535):
    """
    Find the next available port starting from start_port.
    Returns None if no port is available.
    """
    for port in range(start_port, max_port + 1):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
            try:
                sock.bind(('', port))
                return port
            except OSError:
                continue
    return None

def parse_args():
    parser = argparse.ArgumentParser(description='Run the Ancient Indian Encryption Systems REST server')
    parser.add_argument('--port', type=int, help='Port to run the server on')
    parser.add_argument('--auto-port', action='store_true', help='Automatically find next available port')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the server to')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    
    if args.auto_port:
        port = find_free_port()
        if port is None:
            print("Error: No available ports found")
            exit(1)
        print(f"Using automatically found port: {port}")
    else:
        port = args.port or 5000
    
    print(f"Starting server on {args.host}:{port}")
    app.run(debug=True, host=args.host, port=port)