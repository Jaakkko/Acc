from typing import Callable
import datetime
import queue
import threading
import mysql.connector

class Saver:
  def __init__(self, continue_work: Callable[[], bool]) -> None:
    self.continue_work = continue_work
    self.q = queue.Queue()
    self.table_name = "samples_{}".format(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
    self.mydb = mysql.connector.connect(
      host="localhost",
      user="newuser",
      password="password",
      database="acc"
    )
    mycursor = self.mydb.cursor()
    mycursor.execute(f"CREATE TABLE {self.table_name} (x double, y double, z double, epoch bigint, primary key (epoch))")
    self.mydb.commit()

    self.thread = threading.Thread(target=self.__work)
    self.thread.start()
  
  # data = (x, y, z, time_stamp)
  def push(self, data):
    self.q.put(data)

  def __work(self):
    while self.continue_work():
      try:
        cols = self.q.get(timeout=1)  # get a task from the queue, timeout after 1 second
      except queue.Empty:
        continue  # if the queue is empty, continue waiting for tasks
      # process the task here
      mycursor = self.mydb.cursor()
      sql = f"INSERT INTO {self.table_name} (x, y, z, epoch) VALUES (%s, %s, %s, %s)"
      mycursor.execute(sql, cols)
      self.mydb.commit()
      self.q.task_done()  # mark the task as done