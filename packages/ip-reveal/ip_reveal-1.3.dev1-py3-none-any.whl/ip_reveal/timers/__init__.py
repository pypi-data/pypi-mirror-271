"""

File: ip_reveal/tools/timers/__init__
Author: Taylor-Jayde Blackstone <t.blackstone@inspyre.tech>
Added in Version: 1.0(dev) - 10/26/2020

Description:
    This package handles the necessary time-keeping routines for "IP Reveal".

Design:
    This package lends it's opening preparation to the "start()" method (which should not be confused with the similarly
    named: "_start()"). So, if - for example - one wanted to get all parts if the timer working, and keeping time in the
    easiest way possible (with this package), they could write something out like the following example

Examples:

    from time import sleep
    from ip_reveal import timers

    timer = timers

    timer.start()

    while True:
        timer_state = timer.get_elapsed()
        print(timer_state)

    # And resetting is even easier
    timer.reset()

"""
import humanize
import datetime as dt
from time import time, sleep


class Timer:
    """
    A Timer class to handle time-keeping routines for "IP Reveal".

    Attributes:
        start_time (float): Time when the timer was started.
        last_refresh (float): Time when the timer was last refreshed.
        last_ref_f (str): Formatted string representing the time since last update.

    Methods:
        start(): Starts the timer.
        get_elapsed(): Gets the elapsed time since the timer started or was last refreshed.
        refresh(): Refreshes the timer.
        clear(): Clears the timer.
    """

    def __init__(self):
        """
        Initializes the Timer with all attributes set to None.
        """
        self.start_time = None
        self.last_refresh = None
        self.last_ref_f = None

    def _start(self):
        """
        Private method to start the timer. It sets the start time and last refresh time.

        Raises:
            TimerStartError: If the timer is already started.
        """
        if self.start_time is None:
            self.start_time = time()
            self.last_refresh = self.start_time
        else:
            raise TimerStartError("You are trying to start a timer that's already started!")

    def start(self):
        """
        Public method to start the timer. It wraps the _start method and catches TimerStartError.

        Usage:
            timer = Timer()
            timer.start()
        """
        try:
            self._start()
        except TimerStartError as e:
            print(e)

    def get_elapsed(self):
        """
        Gets the human-readable elapsed time since the timer was started or last refreshed.

        Returns:
            str: A human-readable string representing the elapsed time.

        Usage:
            elapsed_time = timer.get_elapsed()
            print(elapsed_time)
        """
        if self.last_refresh is None:
            raise TimerNotStartedError("You are trying to get the elapsed time of a timer that hasn't been started!")
        old_time = self.last_refresh
        new_time = time()
        diff = new_time - old_time
        self.last_ref_f = humanize.naturaldelta(diff)
        return self.last_ref_f

    def refresh(self):
        """
        Refreshes the timer by updating the last refresh time.

        Usage:
            timer.refresh()
        """
        self.last_refresh = time()

    def clear(self):
        """
        Clears the timer, resetting all attributes to None.

        Usage:
            timer.clear()
        """
        self.start_time = None
        self.last_refresh = None
        self.last_ref_f = None


class TimerStartError(Exception):
    """
    Custom exception class for TimerStartError.

    Attributes:
        message (str): The error message.
    """

    def __init__(self, message="There was an error with your timer!"):
        """
        Initializes the TimerStartError with a custom message.

        Args:
            message (str): The error message. Default: "There was an error with your timer!"
        """
        self.message = message
        super().__init__(self.message)
