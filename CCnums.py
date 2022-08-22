from asyncio import threads
import threading

num_1 = 2499999999999999
num_2 = 4999999999999999
num_3 = 7499999999999999
num_4 = 9999999999999999

class myThread(threading.Thread):
    def __init__(self, name, start_num, finish_num):
        threading.Thread.__init__(self)
        self.name = name
        self.start_num = start_num
        self.finish_num = finish_num
    def run(self):
        print("Starting "+ self.name)
        listCcNums(self.name, self.start_num, self.finish_num)
        print("exiting "+ self.name)

def listCcNums(name, start_num, finish_num):
    File = open(str(start_num)+ "_" + str(finish_num) + ".dat", "a")
    for num in range(start_num, finish_num):
        File.write(str(num)+"\n")
    File.close()

thread1 = myThread("thread-1",0,num_1)
thread2 = myThread("thread-2",num_1+1,num_2)
thread3 = myThread("thread-3",num_2+1,num_3)
thread4 = myThread("thread-4",num_3+1, num_4)

#thread1.start()
#thread2.start()
#thread3.start()
#thread4.start()

print("exiting main thread")
