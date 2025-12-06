"""
WebUI Server for Ventilairsec2HA
Provides HTTP API and web dashboard
"""

import asyncio
import logging
import json
from typing import Optional
from datetime import datetime

try:
    from aiohttp import web
    from aiohttp.web_runner import AppRunner
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

logger = logging.getLogger(__name__)


class WebUIServer:
    """HTTP server for WebUI and API"""

    def __init__(self, config, communicator, ventilairsec_manager):
        self.config = config
        self.communicator = communicator
        self.ventilairsec_manager = ventilairsec_manager

        self.app: Optional[web.Application] = None
        self.runner: Optional[AppRunner] = None
        self.running = False

    async def start(self) -> bool:
        """Start the WebUI server"""
        try:
            if not AIOHTTP_AVAILABLE:
                logger.warning("⚠️  aiohttp not available, WebUI disabled")
                return False

            logger.info(f"🌐 Starting WebUI server on port {self.config.webui_port}")

            # Create application
            self.app = web.Application()

            # Add routes
            self.app.router.add_get('/', self.handle_index)
            self.app.router.add_get('/api/status', self.handle_api_status)
            self.app.router.add_get('/api/devices', self.handle_api_devices)
            self.app.router.add_post('/api/command', self.handle_api_command)
            self.app.router.add_get('/api/logs', self.handle_api_logs)
            self.app.router.add_static('/static', '/app/static', name='static')

            # Create runner
            self.runner = AppRunner(self.app)
            await self.runner.setup()

            # Start server
            site = web.TCPSite(self.runner, '0.0.0.0', self.config.webui_port)
            await site.start()

            logger.info(f"✅ WebUI server started: http://0.0.0.0:{self.config.webui_port}")
            return True

        except Exception as e:
            logger.error(f"❌ WebUI startup error: {e}")
            return False

    async def server_loop(self):
        """Server loop - keeps server running"""
        self.running = True

        while self.running:
            try:
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"❌ Server loop error: {e}")

    async def handle_index(self, request: web.Request) -> web.Response:
        """Handle index request"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Ventilairsec2HA</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
                .container { max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 5px; }
                h1 { color: #333; }
                .status { background: #e8f5e9; padding: 10px; border-radius: 3px; margin: 10px 0; }
                .device { border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 3px; }
                .api-section { background: #f9f9f9; padding: 10px; margin: 10px 0; border-left: 3px solid #2196F3; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🌬️ Ventilairsec2HA</h1>
                <p>Home Assistant addon pour VMI Purevent Ventilairsec via EnOcean</p>

                <div class="api-section">
                    <h2>API Endpoints</h2>
                    <ul>
                        <li><code>GET /api/status</code> - État du système</li>
                        <li><code>GET /api/devices</code> - Liste des appareils</li>
                        <li><code>POST /api/command</code> - Envoyer une commande</li>
                        <li><code>GET /api/logs</code> - Logs</li>
                    </ul>
                </div>

                <div id="status"></div>
                <div id="devices"></div>

                <script>
                    async function updateStatus() {
                        const response = await fetch('/api/status');
                        const data = await response.json();
                        document.getElementById('status').innerHTML =
                            '<div class="status">' +
                            '<strong>Status:</strong> ' + JSON.stringify(data, null, 2) +
                            '</div>';
                    }

                    async function updateDevices() {
                        const response = await fetch('/api/devices');
                        const data = await response.json();
                        let html = '<h2>Appareils</h2>';
                        for (const [addr, device] of Object.entries(data)) {
                            html += '<div class="device">' +
                                '<strong>' + device.name + '</strong> (' + addr + ')<br>' +
                                '<pre>' + JSON.stringify(device.data, null, 2) + '</pre>' +
                                '</div>';
                        }
                        document.getElementById('devices').innerHTML = html;
                    }

                    setInterval(updateStatus, 5000);
                    setInterval(updateDevices, 5000);
                    updateStatus();
                    updateDevices();
                </script>
            </div>
        </body>
        </html>
        """
        return web.Response(text=html, content_type='text/html')

    async def handle_api_status(self, request: web.Request) -> web.Response:
        """Handle API status request"""
        status = {
            'connected': self.communicator.serial is not None,
            'base_id': self.communicator.base_id.hex() if self.communicator.base_id else None,
            'timestamp': datetime.now().isoformat()
        }
        return web.json_response(status)

    async def handle_api_devices(self, request: web.Request) -> web.Response:
        """Handle API devices request"""
        devices = self.ventilairsec_manager.get_device_states()
        return web.json_response(devices)

    async def handle_api_command(self, request: web.Request) -> web.Response:
        """Handle API command request"""
        try:
            data = await request.json()

            command = data.get('command')
            if command == 'set_speed':
                speed = data.get('speed', 50)
                result = await self.ventilairsec_manager.set_vmi_speed(speed)
                return web.json_response({'success': result})

            return web.json_response({'error': 'Unknown command'}, status=400)

        except Exception as e:
            logger.error(f"❌ Command error: {e}")
            return web.json_response({'error': str(e)}, status=500)

    async def handle_api_logs(self, request: web.Request) -> web.Response:
        """Handle API logs request"""
        logs = {
            'message': 'Log retrieval not implemented yet'
        }
        return web.json_response(logs)

    async def stop(self):
        """Stop the server"""
        logger.info("🛑 Stopping WebUI server")
        self.running = False

        if self.runner:
            await self.runner.cleanup()
