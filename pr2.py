# Capital Gain Calculator using Queues
#
from timeit import default_timer as timer
from queue import Empty
import sys
import re
# ---- Class ArrayQueue (mostly from textbook, code fragments 6.6 and 6.7) ---- #
# ---- You do not need to modify this class. ---- #
class ArrayQueue:
    """FIFO queue implementation using a Python list as underlying storage."""
    DEFAULT_CAPACITY = 10 # moderate capacity for all new queues

    def __init__(self):
        """Create an empty queue."""
        self.data = [None] * ArrayQueue.DEFAULT_CAPACITY
        self.size = 0
        self.front = 0
    
    def len(self):
        """Return the number of elements in the queue."""
        return self.size

    def is_empty(self):
        """Return True if the queue is empty."""
        return self.size == 0

    def first(self):
        """Return (but do not remove) the element at the front of the queue. Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('Queue is empty')
        return self.data[self.front]

    def dequeue(self):
        """Remove and return the first element of the queue (i.e., FIFO). Raise Empty exception if the queue is empty."""
        if self.is_empty():
            raise Empty('Queue is empty')
        answer = self.data[self.front]
        self.data[self.front] = None # help garbage collection
        self.front = (self.front + 1) % len(self.data)
        self.size -= 1
        return answer

    def enqueue(self, e):
        """Add an element to the back of queue."""
        if self.size == len(self.data): # if queue is full
            self.resize(2 *len(self.data)) # double the array size
        avail = (self.front + self.size) % len(self.data)
        self.data[avail] = e
        self.size += 1

    def resize(self, cap):
        """Resize to a new list of capacity >= len(self)."""
        old = self.data # keep track of existing list
        self.data = [None] * cap # allocate list with new capacity
        walk = self.front
        for k in range(self.size): # only consider existing elements
            self.data[k] = old[walk] # intentionally shift indices
            walk = (1 + walk) %len(old) # use old size as modulus
        self.front = 0 # front has been realigned

    def replace_first(self, e):
        """Update the element at the front of the queue. """
        if self.is_empty():
            raise Empty('Queue is empty')
        self.data[self.front] = e


# -------- Main Program -------- #
# ----- Add your code here ----- #

# TO DO: start timer.
start = timer()


# TO DO: Parse the command line arguments.
if len(sys.argv) != 2:
    raise ValueError('Please provide one file name.')
inputFileName = sys.argv[1]


# DONE: Initialize a queue named q. Use this queue to store the "buy" transactions.
q = ArrayQueue()


# DONE: Initialize a variable to keep track of the overall capital gain.
totalGain = 0


# TO DO: Read text file. Each line is a "transaction".
# For each transaction, update the queue (add, update, or remove elements).
# For transactions of type "sell", print the capital gain for that transaction.
myList = []
f = open(inputFileName, "r")
myList = f.readlines()
f.close()


print("\n************************")
print("The file that will be used for input is", inputFileName)
print("************************")


for i in range(len(myList)):
    txt = myList[i]

#if we run into a sold transaction we use this process to find capital gains/update q
    if "sell" in txt:
        sell = re.findall('\d+', txt) #singles out digits in the string being sold
        print("sell: {0} at ${1}".format(sell[0], sell[1])) #prints the sell statement
        quantity = int(sell[0])
        sold = int(sell[1]) #price the shares sold at
        capitalGains = 0


        #implementation of given formula to calculate cG while sold shares remain
        while (quantity > 0):
            bought = q.dequeue()
            if (quantity > bought[0]):
                banked = bought[0] * (sold - bought[1])
            else:
                banked = quantity * (sold - bought[1])
            #adds/subtracks capital gains and decreases quantity by the shares
            capitalGains += banked
            quantity -= bought[0]

        print("This transaction's capital gain is: ", capitalGains)

        #adds this transaction's capital gains to total
        totalGain += capitalGains

        #if sold shares do not equal out with bought from queue this reformats q
        storage = []
        if (quantity != 0):
            storage.append((-1 * quantity, bought[1]))

            while not q.is_empty():
                storage.append(q.dequeue())

            for item in storage:
                q.enqueue(item)

        print("\n")

    else:
        picks = re.findall('\d+', txt) #singles out digits in the string being bought
        picks[0] = int(picks[0])
        picks[1] = int(picks[1]) #turns string digits into ints
        print("buy: {0} at ${1}".format(picks[0], picks[1])) #prints buy statement
        picks = tuple(picks) #turns list into tuple
        q.enqueue(picks) #places tuple into queue

# DONE: After processing the file, print the total capital gain for the entire sequence.
print("**********************")
print("The total capital gain is:", totalGain)

# TO DO: Print remaining elements in the queue.
print("\n**********************")
print("Shares remaining in the queue:")
while not q.is_empty():
    draw = q.dequeue()
    print("{0} shares bought at ${1} per share.".format(draw[0], draw[1]))

# TO DO: end timer.
end = timer()

# TO DO: Print program's runtime.
print("\n**********************")
print("Time of Program: {:.8f} milliseconds".format(end - start))
