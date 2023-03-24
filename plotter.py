import multiprocessing
import collections
import functools
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import os

def _plotting_process(q):
  global _ys, _line, _anim
  xs = np.linspace(0, 1000, 1000, False)
  _ys = collections.deque(maxlen=1000)
  _ys.extend(np.zeros(1000))
  fig = plt.figure()
  axis = plt.axes(xlim =(0, 1000), ylim =(-5, -2.5))
  _line, = axis.plot([], [], lw = 1)
  _line.set_data(xs, [])
  _anim = FuncAnimation(
    fig,
    functools.partial(_animate, q=q),
    interval = 20,
    blit = True
  )
  
  plt.show()

def _animate(i, q: multiprocessing.Queue):
  a = []
  try:
    while True:
      a.append(q.get_nowait())
  except:
    pass

  _ys.extend(np.log(np.abs(np.array(a) - 1)))
  _line.set_ydata(_ys)
  return _line,

class Plotter:
  def __init__(self) -> None:
    self.q = multiprocessing.Queue()
    self.p = multiprocessing.Process(target=_plotting_process, args=(self.q,))
    self.p.start()

  def new(self, val):
    self.q.put_nowait(val)

  def quit(self):
    self.p.terminate()