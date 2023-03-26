import webpage
from server import Server
from saver import Saver
from acc_data_provider import AccelerationDataProvider
from test_data_provider import TestDataProvider
# from plotter import Plotter
import signal

# plotter = Plotter()
server = Server()

run=True
def signal_handler(sig, frame):
	global run
	# plotter.quit()
	server.quit()
	run=False

signal.signal(signal.SIGINT, signal_handler)

# saver = Saver(lambda: run)
data_provider = AccelerationDataProvider()
while run:
	acceleration = data_provider.get()
	# saver.push((acceleration["x"], acceleration["y"], acceleration["z"], time.time_ns() // 1_000_000))
	# plotter.new(acceleration["z"])
	server.push(acceleration["z"])