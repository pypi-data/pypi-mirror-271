# Advanced Input

Advanced input for python, where you can read in just one character or have inputs priority ordered.

## Usage

```py
from advanced-input import get_advanced_input, PriorityOrder
from threading import Thread
from time import sleep

input_handler = get_advanced_input()

def thread_one():
    user_input = input_handler.input(priority=PriorityOrder.High)
    print(user_input)

def main():
    backgroundThread = Thread(target=thread_one)
    backgroundThread.start()
    sleep(.1)
    input_handler.read("Press any character to exit...", PriorityOrder.Low)
    input_handler.stop()
```

This will result in a user input for `thread_one` being created before the `main` function's exit will be available. Normally, this would result in the program exiting, before accepting the user input of `thread_one`. With this, thread one will be in a higher priority than `main`, and that will be the first to be served the user's input. Additionally, `Read()` returns when one character is pressed.

If there are multiple inputs with the same priority, it will return them in a first come last serve method.
