import open_bci_v3 as bci
import os
import time
import socket
import sys

#global variables:
#bciboard -> the link to the openbci board over UART
#bciboard_thread -> the secondary thread that runs the board
#bciboard_stopsignal -> Set True if the board should be stopped next second
#sock_server -> udp_ser
#latest_string -> Temporary string to pass data



OUTPUT_OPTIONS = {"csv":False, "udp":False,"osc":True}
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



HOST = ''
PORT = 51244
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
  s.bind((HOST, PORT))
except socket.error as msg:
	print msg [1]
	sys.exit();


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

bciboard = bci.OpenBCIBoard(is_simulator=False)
#s.setblocking(0)
s.listen(1)


while 1:
	conn, addr = s.accept()
	print 'connected with ' + addr[0]
	if(conn.recv(6) == "<data>"):
	  print '<Data> recd, start streaming'
	  conn.send("<dataOK>")
	  conn.send("<dataOK2>")
	  set_boardstreaming(True, conn)

