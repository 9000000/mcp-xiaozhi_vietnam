#!/usr/bin/env python3
"""
MCP Connection Multiplexer
Shares one WebSocket connection among multiple MCP servers
"""

import asyncio
import json
import logging
from typing import Dict
import websockets

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('MCP_Multiplexer')


class MCPMultiplexer:
    """Multiplexes multiple MCP servers over a single WebSocket connection"""
    
    def __init__(self, endpoint: str):
        self.endpoint = endpoint
        self.ws = None
        self.servers: Dict[str, asyncio.subprocess.Process] = {}
        self.running = False
    
    async def connect(self):
        """Connect to WebSocket server"""
        logger.info(f"Connecting to {self.endpoint}")
        self.ws = await websockets.connect(self.endpoint)
        logger.info("Connected successfully")
    
    async def start_server(self, name: str, command: list):
        """Start an MCP server process"""
        logger.info(f"Starting server: {name}")
        process = await asyncio.create_subprocess_exec(
            *command,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        self.servers[name] = process
        
        # Start tasks to handle I/O
        asyncio.create_task(self._read_server_output(name, process))
        asyncio.create_task(self._read_server_errors(name, process))
    
    async def _read_server_output(self, name: str, process):
        """Read output from server and send to WebSocket"""
        while self.running:
            try:
                line = await process.stdout.readline()
                if not line:
                    break
                
                # Parse and forward to WebSocket
                data = json.loads(line.decode())
                data['_server'] = name  # Tag with server name
                await self.ws.send(json.dumps(data))
                
            except Exception as e:
                logger.error(f"Error reading from {name}: {e}")
                break
    
    async def _read_server_errors(self, name: str, process):
        """Read errors from server"""
        while self.running:
            try:
                line = await process.stderr.readline()
                if not line:
                    break
                logger.warning(f"[{name}] {line.decode().strip()}")
            except Exception as e:
                logger.error(f"Error reading stderr from {name}: {e}")
                break
    
    async def _handle_websocket_messages(self):
        """Handle messages from WebSocket and route to appropriate server"""
        while self.running:
            try:
                message = await self.ws.recv()
                data = json.loads(message)
                
                # Route to appropriate server based on tag
                server_name = data.get('_server')
                if server_name and server_name in self.servers:
                    process = self.servers[server_name]
                    process.stdin.write(message.encode() + b'\n')
                    await process.stdin.drain()
                else:
                    # Broadcast to all servers
                    for process in self.servers.values():
                        process.stdin.write(message.encode() + b'\n')
                        await process.stdin.drain()
                        
            except Exception as e:
                logger.error(f"Error handling WebSocket message: {e}")
                break
    
    async def run(self):
        """Main run loop"""
        self.running = True
        
        try:
            await self.connect()
            
            # Start WebSocket message handler
            asyncio.create_task(self._handle_websocket_messages())
            
            # Keep running
            while self.running:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("Shutting down...")
        finally:
            self.running = False
            await self.cleanup()
    
    async def cleanup(self):
        """Cleanup resources"""
        logger.info("Cleaning up...")
        
        # Stop all servers
        for name, process in self.servers.items():
            logger.info(f"Stopping {name}")
            process.terminate()
            await process.wait()
        
        # Close WebSocket
        if self.ws:
            await self.ws.close()


async def main():
    import os
    
    endpoint = os.getenv('MCP_ENDPOINT')
    if not endpoint:
        logger.error("MCP_ENDPOINT not set")
        return
    
    multiplexer = MCPMultiplexer(endpoint)
    
    # Start servers
    await multiplexer.start_server('calculator', ['python', 'calculator.py'])
    await multiplexer.start_server('VnExpress', ['python', 'VnExpress.py'])
    await multiplexer.start_server('dantri_news', ['python', 'dantri_news.py'])
    
    # Run
    await multiplexer.run()


if __name__ == '__main__':
    asyncio.run(main())
