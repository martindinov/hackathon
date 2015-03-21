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

connections = []

def set_boardstreaming(doStart, conn):
  global latest_string, bciboard,bciboard_thread,bciboard_stopsignal

  output = ""

  if doStart and not bciboard.streaming:
    #initialize the thread
    #,sendSocketMessage
    bciboard.start_streaming(conn)
    #bciboard_thread = threading.Thread(target=bciboard.start_streaming, args=[[printData,sock_server.handle_sample,osc_server.handle_sample,sendSocketMessage],boardDoContinueCallback,boardErrorCallback,STREAM_TIMEOUTLAPSE])
    #set daemon to true so the app.py can still be ended with a single ^C
    #bciboard_thread.daemon = True
    #spawn the thread
    #bciboard_thread.start()
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
  def open(self):
   connections.append(self)
   self.stream.set_nodelay(True)
   set_boardstreaming(True, self)

  def on_message(self, message):
    print 'received:', message
    # self.write_message("The server says: " + message + " back at you")


  def on_close(self):
  	connections.remove(self)


application = tornado.web.Application([
  (r'/', IndexHandler),
  (r'/ws', WSHandler),
])



if __name__ == "__main__":
	bciboard = bci.OpenBCIBoard(is_simulator=False)
	application.listen(51244)
	tornado.ioloop.IOLoop.instance().start()

STREAM_TIMEOUTLAPSE = 10 #In seconds

def printData(sample):
  #Sample callback that can be passed into the openbci board
  global latest_string
  #print "Called!"
  #os.system('clear')
  output = ""
  output += "----------------"
  output += ("%f" %(sample.id))
  output += str(sample.channel_data)
  output += str(sample.aux_data)
  output += "----------------"
  print output
  latest_string = output



