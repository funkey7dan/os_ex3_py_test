import random
import re
import os
import itertools
import threading
import time
import sys
import subprocess

PRODUCT_RANGE = 100
QUEUE_RANGE = 100
PRODUCERS_RANGE = 10
QUE_SIZE_RANGE = 30
done = False


def check_producers_length():
    mylist = []
    mydict = {}
    with open("config.txt", "r") as f:
        mylist = f.read().splitlines()
        mylist = list(filter(None, mylist))
    producersN = (len(mylist)//3)
    for i in (0, producersN):
        # put id in dictionary mapped to number of products.
        key = mylist.pop(0)
        value = mylist.pop(0)
        mydict[key] = value
        # remove the queue size, unsused.
        mylist.pop(0)
    return mydict


def count_producers(N, dict):
    global done
    mylist = []
    with open("out.txt", "r") as f:
        mylist = f.read().splitlines()
    mylist.sort()
    for i in range(1, N):
        rex = re.compile('(Producer '+str(i)+')')
        if len(rex.findall(''.join(mylist))) != int(dict[str(i)]):
            sys.stdout.write("Producer " + str(i) + " Does not match!\n")
            done = True
            exit(-1)


def generate_producer(id: int):
    gen = str(id)+'\n' + str(random.randint(1, PRODUCT_RANGE)) + \
        '\n' + str(random.randint(1, QUEUE_RANGE)) + '\n'
    return gen


def generate_config():
    sys.stdout.write("Creating config file...\n")
    with open("config.txt", "w+") as f:
        for i in range(1, PRODUCERS_RANGE):
            f.write(generate_producer(i))
            f.write("\n")
        f.write(str(random.randint(1, QUE_SIZE_RANGE)))


def compare():
    print("Comparing files...")
    mydict = check_producers_length()
    count_producers(len(mydict), mydict)


def animate():
    global done
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            sys.stdout.flush()
            break
        sys.stdout.write(c+"\r")
        sys.stdout.flush()
        time.sleep(0.1)


def main():
    global done
    t = threading.Thread(target=animate)
    t.start()
    generate_config()
    subprocess.run("./ex3.out config.txt > out.txt",shell=True)
    compare()
    done = True
    sys.stdout.write("Done,files match\n")


if __name__ == "__main__":
    main()
