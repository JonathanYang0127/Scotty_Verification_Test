class Stack:
    "a container with a last-in-first-out (lifo) queuing policy."
    def __init__(self):
        self.list = []

    def push(self,item):
        "push 'item' onto the stack"
        self.list.append(item)

    def pop(self):
        "pop the most recently pushed item from the stack"
        return self.list.pop()

    def isEmpty(self):
        "returns true if the stack is empty"
        return len(self.list) == 0
