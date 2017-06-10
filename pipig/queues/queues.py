from Queue import Queue


class BaseQueue(Queue):
    """
    Manages the Queues for Readings
    """
    def __init__(self, name=""):
        Queue.__init__(self)
        self.name = name
        self.state = False

    def __str__(self):
        result = self.list_items()
        return self.name + " Queue: " + str(result)

    def list_items(self):
        items = []

        for i in range(self.queue.__len__()):
            result = self.queue[i]
            if result is not None:
                items.append(str(result))
        return items

    def set_state(self, state):
        self.state = state
        return self.get_state()

    def get_state(self):
        return self.state



