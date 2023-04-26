from PySide6.QtCore import QObject, Signal, Slot

class EventManager(QObject):

    event_sent = Signal(str, object)

    def __init__(self):
        self.__observers_for_events = {}

    def subscribe(self, listener, event_type):
        if event_type not in self.__observers_for_events:
            self.__observers_for_events[event_type] = []
        self.__observers_for_events[event_type].append(listener)

    def unsubscribe(self, listener, event_type):
        if event_type in self.__observers_for_events:
            if listener in self.__observers_for_events[event_type]:
                self.__observers_for_events[event_type].remove(listener)

    @Slot
    def notify(self, event_type, data):
        pass
