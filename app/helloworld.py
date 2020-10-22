#Write a program in Python or Nodejs that can be used in load testing
#○ The program takes in a parameter of a URL
#○ The program will fire request to the URL as fast as possible for a period of time
#○ The program will report on:
#   -Count and percentage of successful requests
#   -Count and percentage of failed requests
#   -Count and percentage of different responses you got
#   -Avg time of the success response
#○ Document the design rationale of the program
#
#
#To take a parameter of a URL I used a command line argument
#"firing requests to the URL as fast possible for a period of time"
#       -requirement break down:
#           -continual firing of requests for a period of time
#               -time in which threads are active
#               -worker threads
#           -as fast as possible
#               -many threads
#           -threading
#               -need to avoid race conditions
#                   -mutex locks
#
#to store and report the many types of response I used the python equivalent of hashmaps
#       -using status code as the key and count as the value
#
#potential improvements:
#       -using concurrent.futures.executor


import threading
import time
import sys
import requests

isDone = False
lockData = False
timeTotal = 0
requestCount = 0
successCount = 0
failureCount = 0
data = dict()

def threadJob(URL):
    global isDone, lockData
    global data
    global timeTotal
    global requestCount, successCount, failureCount
    while(not isDone):
        startTime = time.thread_time_ns()
        r = requests.get(URL,) #assumption is any request so get request for simplicity
        endTime = time.thread_time_ns()
        status = r.status_code
        while(lockData): #wait for lock so the thread working on it can finish 
            pass
        lockData = True #lock global variables
        if(int(status / 100) == 2):
            timeTotal += (endTime - startTime)
            successCount += 1
        if int(status / 100)  == 4 or int(status / 100)  == 5:
            failureCount += 1
        requestCount += 1
        if(status in data):
            data[status] += 1
        else:
            data[status] = 1
        lockData = False #unlock global variables

if(len(sys.argv) == 2):
    URL = sys.argv[1]
    threads = []
    for _ in range(300): #arbitrary number of threads
        thread = threading.Thread(target=threadJob,args=(URL,))
        thread.start()
        threads.append(thread)
    time.sleep(5)        #arbitrary time period
    isDone = True
    for t in threads:
        t.join()
    print('success count: ',successCount,' percentage: ',successCount/requestCount * 100.0)
    print('failure count: ',failureCount,' percentage: ',failureCount/requestCount * 100.0)
    for d in data:
        print('status code: ',d,' count: ',data[d],' percentage: ',data[d]/requestCount * 100.0)
    print('average time for success in ms: ',timeTotal/requestCount/1000000)