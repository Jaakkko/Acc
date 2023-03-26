import asyncio
import websockets
import threading
import json
import queue

class Server:
	def __init__(self):
		self.client = None
		self.buffer = []
		self.thread = threading.Thread(target=lambda: asyncio.run(self.main()))
		self.thread.start()
		self.q = None

	async def handleClient(self, websocket):
		self.q = queue.Queue()
		while not self.running.done():
			try:
				await websocket.send(self.q.get())
				self.q.task_done()
			except:
				break

	async def main(self):
		print("Serving")
		async with websockets.serve(self.handleClient, "192.168.1.151", 8765):
			self.running = asyncio.Future()
			await self.running

	def push(self, val):
		self.buffer.append(val)
		if len(self.buffer) == 10:
			if self.q != None:
				try:
					self.q.put(json.dumps(self.buffer))
				except:
					print("client.send failed")
			self.buffer = []

	def quit(self):
		self.running.set_result(None)
