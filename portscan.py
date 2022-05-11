from threading import Thread
import socket
import random
import time


host = input('host > ')
type = int(input('1 for brute force\n2 for random\n3 for smart\n'))
counting_open = []
counting_close = []
threads = []


def scan(port):
    s = socket.socket()
    result = s.connect_ex((host, port))
    #print('working on port > ' + (str(port)))
    if result == 0:
        counting_open.append(port)
        print((str(port))+' -> open')
        s.close()
    else:
        counting_close.append(port)
        # print((str(port))+' -> close')
        s.close()

if (type == 1):
    from_port = input('start scan from port > ')
    to_port = input('finish scan to port > ')

    for i in range(int(from_port), int(to_port) + 1):
        t = Thread(target=scan, args=(i,))
        threads.append(t)
        t.start()

    with open("portscanned.txt", "w") as myfile:
        for i in range(int(from_port), int(to_port) + 1):
            if i in counting_open:
                myfile.write('port ' + str(i) + ' open\n')
            else:
                myfile.write('port ' + str(i) + ' close\n')
elif (type == 2):
    from_port = int(input('start scan from port > '))
    to_port = int(input('finish scan to port > '))
    r = list(range(from_port,to_port))
    random.shuffle(r)
    for i in r:
        t = Thread(target=scan, args=(i,))
        threads.append(t)
        t.start()
    with open("portscanned.txt", "w") as myfile:
        for i in counting_open:
            myfile.write('port ' + str(i) + ' open\n')
elif (type == 3):
    ports = [20,21,22,23,25,54,67,68,69,80,110,123,137,138,143,179,389,443,636,989,990]
    s = 'testing common ports: ' + str(ports.pop(0))
    for p in ports:
        s += ',' + str(p)
    print(s + ':')
    for p in ports:
        t = Thread(target=scan, args=(p,))
        threads.append(t)
        t.start()

    time.sleep(2)

    with open("portscanned.txt", "w") as myfile:
        for i in ports:
            if i in counting_open:
                myfile.write('port ' + str(i) + ' open\n')
            else:
                myfile.write('port ' + str(i) + ' close\n')


print('done')
[x.join() for x in threads]

