from os import system
from time import sleep

while True:
    execFile = open("execution.txt").read()
    print(execFile)
    sleep(0.05)
    system("clear")
