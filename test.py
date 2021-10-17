import pyttsx3
from multiprocessing import Process, Queue

engine = pyttsx3.init()

def say(q,text):
    q.put(text)
    engine.say(text)
    engine.runAndWait()

def background(t):
    q = Queue()
    p = Process(target=say, args=(q,t))
    p.start()

if __name__ == '__main__':
    text = "test"
    i = 0
    while True:
        if(i % 1000):
            background("test")
        i = i + 1
        print(i)