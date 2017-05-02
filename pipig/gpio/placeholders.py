# coding=utf-8
BCM = 11
BOARD = 10
BOTH = 33
FALLING = 32
HARD_PWM = 43
HIGH = 1
I2C = 42
IN = 1
LOW = 0
OUT = 0
PUD_DOWN = 21
PUD_OFF = 20
PUD_UP = 22
RISING = 31
RPI_REVISION = 3
SERIAL = 40
SPI = 41
UNKNOWN = -1
VERSION = '0.6.1'
RPI_INFO = {'MANUFACTURER': 'Embest', 'P1_REVISION': 3}


MOCK_NUMBERING_MODE = None
MOCK_GPIO_STATES = [
                    {'button1_pin': 3, 'bcm': 2, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 5, 'bcm': 3, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 7, 'bcm': 4, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 8, 'bcm': 14, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 10, 'bcm': 15, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 11, 'bcm': 17, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 12, 'bcm': 18, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 13, 'bcm': 27, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 15, 'bcm': 22, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 16, 'bcm': 23, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 18, 'bcm': 24, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 19, 'bcm': 10, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 21, 'bcm': 9, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 22, 'bcm': 25, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 23, 'bcm': 11, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 24, 'bcm': 8, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 26, 'bcm': 7, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 27, 'bcm': 0, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 28, 'bcm': 1, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 29, 'bcm': 5, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 31, 'bcm': 6, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 32, 'bcm': 12, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 33, 'bcm': 13, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 35, 'bcm': 19, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 36, 'bcm': 16, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 37, 'bcm': 26, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 38, 'bcm': 20, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW},
                    {'button1_pin': 40, 'bcm': 21, 'state': IN, 'PUPD': None, 'event_detection': None, 'value': LOW}
                    ]


def getmode():
    """
    Get numbering mode used for channel numbers.
        Returns BOARD, BCM or None
    """
    global MOCK_NUMBERING_MODE
    return MOCK_NUMBERING_MODE


def setmode(numbering_mode):
    """
    Set up numbering mode to use for channels.
    BOARD - Use Raspberry Pi board numbers
    BCM   - Use Broadcom Gpio 00..nn numbers

    :param numbering_mode: BOARD or BCM
    :return:
    """
    global MOCK_NUMBERING_MODE
    MOCK_NUMBERING_MODE = numbering_mode
    return MOCK_NUMBERING_MODE


def cleanup(gpio_pin=None):
    """
    Clean up by resetting all Gpio channels that have been used by this program to
        INPUT with no pullup/pulldown and no event detection
    :param gpio_pin: individual channel or list/tuple of channels to clean up.  Default - clean every channel that has been used.
    """
    global MOCK_GPIO_STATES
    global MOCK_NUMBERING_MODE
    update = False

    for pin in range(0, len(MOCK_GPIO_STATES)):
        if gpio_pin is None:
            update = True
        else:
            if MOCK_NUMBERING_MODE == BCM:
                if MOCK_GPIO_STATES[pin]['bcm'] == gpio_pin:
                    update = True
            elif MOCK_NUMBERING_MODE == BOARD:
                if MOCK_GPIO_STATES[pin]['button1_pin'] == gpio_pin:
                    update = True
            else:
                update = False

        if update:
            MOCK_GPIO_STATES[pin]['state'] = IN
            MOCK_GPIO_STATES[pin]['PUPD'] = None
            MOCK_GPIO_STATES[pin]['event_detection'] = None
            MOCK_GPIO_STATES[pin]['value'] = LOW
        update = False
    return


def gpio_function(gpio_pin):
    """
    Return the current Gpio function (IN, OUT, PWM, SERIAL, I2C, SPI)
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return:
    """
    global MOCK_NUMBERING_MODE
    global MOCK_GPIO_STATES
    for pin in range(0, len(MOCK_GPIO_STATES)):
        if MOCK_NUMBERING_MODE == BCM & MOCK_GPIO_STATES[pin]['bcm'] == gpio_pin:
            return MOCK_GPIO_STATES[pin]['state']
        elif MOCK_NUMBERING_MODE == BOARD & MOCK_GPIO_STATES[pin]['button1_pin'] == gpio_pin:
            return MOCK_GPIO_STATES[pin]['state']
        else:
            pass
    return None


def input(gpio_pin):
    """
    Input from a Gpio channel.  Returns HIGH=1=True or LOW=0=False
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return:
    """
    global MOCK_NUMBERING_MODE
    global MOCK_GPIO_STATES

    for pin in range(0, len(MOCK_GPIO_STATES)):
        if MOCK_NUMBERING_MODE == BCM & MOCK_GPIO_STATES[pin]['bcm'] == gpio_pin:
            return MOCK_GPIO_STATES[pin]['value']
        elif MOCK_NUMBERING_MODE == BOARD & MOCK_GPIO_STATES[pin]['button1_pin'] == gpio_pin:
            return MOCK_GPIO_STATES[pin]['value']
        else:
            pass
    return None


def output(gpio_pin, value):
    """
    Output to a Gpio channel or list of channels
    :param value: 0/1 or False/True or LOW/HIGH
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return:
    """

    global MOCK_NUMBERING_MODE
    global MOCK_GPIO_STATES

    for pin in range(0, len(MOCK_GPIO_STATES)):
        if MOCK_NUMBERING_MODE == BCM & MOCK_GPIO_STATES[pin]['bcm'] == gpio_pin:
            MOCK_GPIO_STATES[pin]['value'] = value
            return  MOCK_GPIO_STATES[pin]['value']
        elif MOCK_NUMBERING_MODE == BOARD & MOCK_GPIO_STATES[pin]['button1_pin'] == gpio_pin:
            MOCK_GPIO_STATES[pin]['value'] = value
            return MOCK_GPIO_STATES[pin]['value']
        else:
            pass
    return None


def setup(gpio_pin, direction, pupd=None):
    """
    Set up a Gpio channel or list of channels with a direction and (optional) pull/up down control
    :param pupd: Pull Up, Pull Down Control
    :param direction: IN or OUT
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return:
    """
    global MOCK_NUMBERING_MODE
    global MOCK_GPIO_STATES

    for pin in range(0, len(MOCK_GPIO_STATES)):
        if MOCK_NUMBERING_MODE == BCM & MOCK_GPIO_STATES[pin]['bcm'] == gpio_pin:
            MOCK_GPIO_STATES[pin]['state'] = direction
            MOCK_GPIO_STATES[pin]['PUPD'] = pupd
            return  MOCK_GPIO_STATES[pin]['state']
        elif MOCK_NUMBERING_MODE == BOARD & MOCK_GPIO_STATES[pin]['button1_pin'] == gpio_pin:
            MOCK_GPIO_STATES[pin]['state'] = direction
            MOCK_GPIO_STATES[pin]['PUPD'] = pupd
            return MOCK_GPIO_STATES[pin]['state']
        else:
            pass
    return None


def event_detected(gpio_pin):
    """
    Returns True if an edge has occured on a given Gpio.  You need to enable edge detection using add_event_detect() first.
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return:
    """


def remove_event_detect(gpio_pin):
    """
    Remove edge detection for a particular Gpio channel
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return:
    """


def wait_for_edge(gpio_pin, edge, bouncetime=0, timeout=None):
    """
    Wait for an edge.  Returns the channel number or None on timeout.
    :param timeout: timeout in ms
    :param bouncetime: time allowed between calls to allow for switchbounce
    :param edge: RISING, FALLING or BOTH
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return: Returns the channel number or None on timeout.
    """
    pass


def wait_for_interrupts(threaded=False, epoll_timeout=1):
    """
    This is the main blocking loop which, while active, will listen for interrupts and start your custom callbacks.
    At some point in your script you need to start this to receive interrupt callbacks.
    This blocking method is perfectly suited as “the endless loop that keeps your script running”.
    (RPIO will automatically shut down the thread when your script exits):

    :param threaded: With the argument threaded=True, this method starts in the background while your script continues in the main thread
    :param epoll_timeout:
    :return:
    """
    pass

def stop_waiting_for_interrupts():
    """
    Stop waiting for interupts
    """

def add_interrupt_callback(gpio_id, callback,
                           edge='both',
                           pull_up_down=PUD_OFF,
                           threaded_callback=False,
                           debounce_timeout_ms=None):
    """
    Adds a callback to receive notifications when a Gpio changes it’s state from 0 to 1 or vice versa.

    A callback typically looks like this:
    def gpio_callback(gpio_id, value):

    :param gpio_id: The callback receives two arguments: the gpio number and the value (an integer, either 0 (Low) or 1 (High)).
    :param callback: Function to call when interupt
    :param edge: Possible edges are rising, falling and both (default).
    :param pull_up_down: Possible pull_up_down values are RPIO.PUD_UP, RPIO.PUD_DOWN and RPIO.PUD_OFF (default).
    :param threaded_callback: If threaded_callback is True, the callback will be started inside a thread.
    Else the callback will block RPIO from waiting for interrupts until it has finished (in the meantime no further callbacks are dispatched).
    :param debounce_timeout_ms: If debounce_timeout_ms is set, interrupt callbacks will not be started until the specified milliseconds have passed since the last interrupt.
    Adjust this to your needs (typically between 10ms and 100ms).
    :return:
    """
    pass

def del_interrupt_callback(gpio_id):
    """
    Removes all callbacks for this particular Gpio.
    :param gpio_id: Gpio Pin to remove interupt callbacks from
    :return:
    """
    pass

def add_tcp_callback(port, callback, threaded_callback=False):
    """
    Adds a socket server callback, which will be started when a connected socket client sends something.
    This is implemented by RPIO creating a TCP server socket at the specified port.
    Incoming connections will be accepted when RPIO.wait_for_interrupts() runs.
    The callback must accept exactly two parameters: socket and message (eg. def callback(socket, msg)).

    The callback can use the socket parameter to send values back to the client (eg. socket.send("hi there\n")).
    To close the connection to a client, use RPIO.close_tcp_client(..).
    A client can close the connection the same way or by sending an empty message to the server.

    You can use socket.getpeername() to get the IP address of the client. Socket object documentation.

    You can test the TCP socket interrupts with $ telnet <your-ip> <your-port> (eg. $ telnet localhost 8080).
    An empty string tells the server to close the client connection
    (for instance if you just press enter in telnet, you’ll get disconnected).
        :param port:
        :param callback:
        :param threaded_callback:
        :return:
        """
    pass


def close_tcp_client(self, fileno):
    """
    Closes the client socket connection and removes it from epoll.
    You can use this from the callback with RPIO.close_tcp_client(socket.fileno()).
    :param self:
    :param fileno:
    :return:
    """
    pass


def add_event_callback(gpio_pin, callback):
    """
    Add a callback for an event already defined using add_event_detect()
    :param callback: a callback function
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    """
    pass

def add_event_detect(gpio_pin, edge, callback=None, bouncetime=None):
    """
    Enable edge detection events for a particular Gpio channel.
    :param bouncetime: Switch bounce timeout in ms for callback
    :param callback: A callback function for the event (optional)
    :param edge: RISING, FALLING or BOTH
    :param gpio_pin: either board button1_pin number or BCM number depending on which mode is set.
    :return:
    """
    pass

