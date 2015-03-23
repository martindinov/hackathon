import open_bci_v3 as bci
import os
import time
import socket
import sys
import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import tornado
import atexit
import threading

STREAM_TIMEOUTLAPSE = 10 #In seconds
connections = []

def printData(sample):
  #Sample callback that can be passed into the openbci board
  global latest_string
  #print "Called!"
  #os.system('clear')
  """
  output = ""
  output += "----------------"
  output += ("%f" %(sample.id))
  output += str(sample.channel_data)
  output += str(sample.aux_data)n
  """
  output = ','.join([str(i) for i in sample.channel_data]) + '\n'
  print output
  latest_string = output

def boardDoContinueCallback():
  #The openbci board periodically checks to see if it should shut off
  global bciboard_stopsignal
  if bciboard_stopsignal:
    bciboard_stopsignal = False
    return False
  else:
    return True

def boardErrorCallback():
  #The openbci board periodically checks to see if it should shut off
  print "Sees that the board exited."


def set_boardstreaming(doStart, conn):
  global latest_string, bciboard,bciboard_thread,bciboard_stopsignal
  global sock_server, osc_server

  output = ""

  if doStart and not bciboard.streaming:
    #initialize the thread
    #,sendSocketMessage
    bciboard_thread = threading.Thread(target=bciboard.start_streaming, args=[[printData],boardDoContinueCallback,boardErrorCallback,STREAM_TIMEOUTLAPSE])
    #set daemon to true so the app.py can still be ended with a single ^C
    bciboard_thread.daemon = True
    #spawn the thread
    bciboard_thread.start()
    output = "STARTING STREAMING"

  elif not doStart:

    bciboard_stopsignal = True
    #bciboard_thread = None
    output = "STOPPING STREAMING"
  else:
    output = "DID NOTHING: Likely trying to start while aleady streaming"

  return output


class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
    	self.render("index.html")

class WSHandler(tornado.websocket.WebSocketHandler):
  def check_origin(self,origin):
    return True

  def open(self):
    print 'WSHandler opened:'
    connections.append(self)
    self.stream.set_nodelay(True)
    set_boardstreaming(True, self)

  def on_message(self, message):
    print 'received:', message
    # self.write_message("The server says: " + message + " back at you")


  def on_close(self):
    print 'WSHandler closed:'
    set_boardstreaming(False, self)
    connections.remove(self)


def cleanup():
  bciboard.disconnect()

application = tornado.web.Application([
  (r'/', IndexHandler),
  (r'/ws', WSHandler),
])

if __name__ == "__main__":
  bciboard = bci.OpenBCIBoard(is_simulator=False)
  atexit.register(cleanup)
  application.listen(51243)
  tornado.ioloop.IOLoop.instance().start()



