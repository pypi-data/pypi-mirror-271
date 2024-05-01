from .input import AdvancedInput, is_input_ready, get_character_from_input
from .constants import PriorityOrder, EventType, EventWithType
from platform import system
current_input_extender: AdvancedInput = None

def get_advanced_input(encoding: str = None):
    global current_input_extender
    if encoding is None:
        encoding = "cp850" if system() == "Windows" else "utf-8"
    if current_input_extender is None:
        current_input_extender = AdvancedInput(encoding)
        current_input_extender.start()
    return current_input_extender
