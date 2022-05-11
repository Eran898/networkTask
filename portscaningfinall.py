import os
import threading
from queue import Queue
import time
import socket
import logging


# a print_lock is what is used to prevent "double" modification of shared variables.
# this is used so while one thread is using a variable, others cannot access
# it. Once done, the thread releases the print_lock.
# to use it, you want to specify a print_lock per thing you wish to print_lock.
print_lock = threading.Lock()

target = input('enter ip to scan :')
stop = input('enter the delay time in sec :')
file_name = 'PortScaning.txt'
f = open(file_name, 'w+')
f.write("The scan result on ip:")
f.write(str(target))
f.write(' :\n')
f.close()




def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
            con = s.connect((target,port))
            with print_lock:
                print('port :',port,' open!\n')
                file_name = 'PortScaning.txt'
                f = open(file_name, 'a+')  # open file in append mode=add text and not run it over, +=creat the file
                f.write('port :')
                f.write(str(port))
                f.write(' open!\n')
                f.close()
            s.close()
    except:
        print('port :',port,' close!\n')
        file_name = 'PortScaning.txt'
        f = open(file_name, 'a+')  # open file in append mode=add text and not run it over, +=creat the file
        f.write('port :')
        f.write(str(port))
        f.write(' close!\n')
        f.close()
        pass


# The threader thread pulls an worker from the queue and processes it
def threader():
    while True:
        # gets an worker from the queue
        worker = q.get()

        # Run the example job with the avail worker in queue (thread)
        portscan(worker)

        # completed with the job
        q.task_done()



        

# Create the queue and threader 
q = Queue()

# how many threads are we going to allow for
for x in range(300):
     t = threading.Thread(target=threader)

     # classifying as a daemon, so they will die when the main dies
     t.daemon = True

     # begins, must come after daemon definition
     t.start()


start = time.time()

# 100 jobs assigned,first 1000 ports
for worker in range(1,100):
    if worker/10==0:
        time.sleep(stop)
    q.put(worker)

# wait until the thread terminates.
q.join()

