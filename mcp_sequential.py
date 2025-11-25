#!/usr/bin/env python3
"""
Sequential MCP Server Runner
Runs one server at a time to avoid connection limits
"""

import subprocess
import time
import os
import sys
import signal

servers = [
    ('calculator', ['python', 'calculator.py']),
    ('VnExpress', ['python', 'VnExpress.py']),
    ('dantri_news', ['python', 'dantri_news.py']),
]

current_process = None

def signal_handler(sig, frame):
    """Handle Ctrl+C"""
    print("\nShutting down...")
    if current_process:
        current_process.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def run_server(name, command, duration=300):
    """Run a server for specified duration (seconds)"""
    global current_process
    
    print(f"\n{'='*50}")
    print(f"Starting: {name}")
    print(f"Duration: {duration}s")
    print(f"{'='*50}\n")
    
    try:
        current_process = subprocess.Popen(
            command,
            env=os.environ.copy()
        )
        
        # Wait for duration or until process ends
        try:
            current_process.wait(timeout=duration)
        except subprocess.TimeoutExpired:
            print(f"\n{name} time limit reached, stopping...")
            current_process.terminate()
            current_process.wait()
        
        print(f"\n{name} stopped")
        
    except Exception as e:
        print(f"Error running {name}: {e}")
    finally:
        current_process = None

def main():
    print("Sequential MCP Server Runner")
    print("Each server runs for 5 minutes, then switches to next")
    print("Press Ctrl+C to stop\n")
    
    # Check MCP_ENDPOINT
    if not os.getenv('MCP_ENDPOINT'):
        print("Error: MCP_ENDPOINT not set")
        sys.exit(1)
    
    # Run servers in rotation
    while True:
        for name, command in servers:
            run_server(name, command, duration=300)  # 5 minutes each
            time.sleep(5)  # 5 second gap between servers

if __name__ == '__main__':
    main()
