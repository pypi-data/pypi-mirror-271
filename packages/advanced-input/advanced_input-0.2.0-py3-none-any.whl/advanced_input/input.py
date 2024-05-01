from sys import stdin, stdout
from threading import Event, Thread
from typing import Dict, List
from .constants import PriorityOrder, EventWithType, EventType
from time import sleep
from os import path
from platform import system
import ctypes

modul_name = "inputExtention" if system() == "Windows" else "inputExtention.so"
inputExtention = ctypes.CDLL(path.join(path.dirname(__file__), modul_name))
inputExtentionInit = inputExtention.init
inputExtentionStop = inputExtention.stop
is_input_ready = inputExtention.isInputReady
is_input_ready.restype = ctypes.c_bool
get_character_from_input = inputExtention.getCharacter
get_character_from_input.restype = ctypes.c_uint

class AdvancedInput():
    def __init__(self, encoding: str) -> None:
        self.last_input: str = ""
        self.order: Dict[PriorityOrder, List[EventWithType]] = {PriorityOrder.Low: [], PriorityOrder.Normal: [], PriorityOrder.High: []}
        self.stop_event = Event()
        self.main_thread: Thread = None
        self.encoding = encoding
        inputExtentionInit()

    def __loop(self) -> None:
        while not self.stop_event.is_set():
            counter = 0
            while not is_input_ready() and not self.stop_event.is_set():
                counter += 1
                if counter >= 5:
                    stdout.flush()
                    counter = 0
                self.stop_event.wait(.1)
            if self.stop_event.is_set(): break
            tmp: int = get_character_from_input()
            self.last_input: str = tmp.to_bytes(4, "little").decode(self.encoding).strip("\x00")
            for priority in reversed(PriorityOrder):
                if (len(self.order[priority]) > 0):
                    currentEvent = self.order[priority].pop()
                    if currentEvent.type == EventType.LINE and self.last_input not in ["\n"]:
                        self.last_input += stdin.readline().rstrip()
                    currentEvent.set()
                    break

    def start(self) -> None:
        self.stop_event.clear()
        self.main_thread = Thread(target=self.__loop)
        self.main_thread.name = "Advanced Input Reader Thread"
        self.main_thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.main_thread.join()
        self.main_thread = None
        inputExtentionStop()

    def input(self, prompt: str = None, priority: PriorityOrder = PriorityOrder.Normal) -> str:
        input_event = EventWithType(EventType.LINE)
        return self.__get_data(prompt, priority, input_event)

    def read(self, prompt: str = None, priority: PriorityOrder = PriorityOrder.Normal) -> str:
        input_event = EventWithType(EventType.CHAR)
        return self.__get_data(prompt, priority, input_event)
        
    def __get_data(self, prompt: str, priority: PriorityOrder, event: EventWithType) -> str:
        if prompt is not None:
            print(prompt, end="")
        self.order[priority].append(event)
        event.wait()
        ret = self.last_input
        self.last_input = ""
        sleep(.1)
        return ret
