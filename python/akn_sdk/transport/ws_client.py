

# akn_sdk/transport/ws_client.py

import asyncio
import websockets
import json
import traceback


class WebSocketClient:

    def __init__(self, url, token, auto_reconnect=True):
        self.url = url
        self.token = token
        self.auto_reconnect = auto_reconnect

    async def listen(self):
        attempt = 0

        while True:
            try:
                attempt += 1
                print("\n==============================")
                print(f"WS CONNECT ATTEMPT #{attempt}")
                print(f"Connecting to: {self.url}")
                print("==============================")

                async with websockets.connect(
                    self.url,
                    additional_headers={
                        "Authorization": f"Bearer {self.token}"
                    }
                ) as websocket:

                    print("✅ WS HANDSHAKE SUCCESSFUL")

                    async for message in websocket:
                        print("📥 RAW WS MESSAGE RECEIVED:", message)
                        yield json.loads(message)

            except Exception as e:
                print("\n❌ WS CONNECTION ERROR:", repr(e))
                traceback.print_exc()

                if not self.auto_reconnect:
                    raise

                print("🔁 Reconnecting in 2 seconds...\n")
                await asyncio.sleep(2)