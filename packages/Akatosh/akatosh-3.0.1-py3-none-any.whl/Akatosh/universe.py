from __future__ import annotations

import asyncio
import logging
import time
from typing import TYPE_CHECKING, List

from . import logger

if TYPE_CHECKING:
    from .event import Event


class Universe:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """The simulation universe."""
        self._time_resolution = 3
        self._time_step = round(1 / pow(10, self.time_resolution), self.time_resolution)
        self._time = 0
        self._elapsed_time = 0
        self._time_difference = 0
        self._simulation_start_time = 0
        self._simulation_end_time = 0
        self._realtime = False
        self._current_event_priority = 0
        self._max_event_priority = 0
        self._pending_events: List[Event] = list()

    def simulate(self, till: float):
        """Simulate the universe until the given time."""

        # Define the flow of time
        async def time_flow():
            """Flow of time."""
            self._simulation_start_time = time.perf_counter()
            while self.time < till:
                logger.debug(f"Simulation time:\t{self.time}")
                for event in self.pending_events:
                    asyncio.create_task(event())
                self.pending_events.clear()
                if self.realtime:
                    logger.debug(f"Iteration started at Real Time: {time.perf_counter() - self.simulation_start_time:0.6f}")
                    # iterate through all event priorities
                    self._current_event_priority = 0
                    while self.current_event_priority <= self._max_event_priority:
                        logger.debug(
                            f"Current Event Priority: {self.current_event_priority}"
                        )
                        await asyncio.sleep(0)
                        self._current_event_priority += 1
                    # wait for the time step
                    self._time += self.time_step
                    self._time = round(self.time, self.time_resolution)
                    logger.debug(f"Iteration finished at Real Time: {time.perf_counter() - self.simulation_start_time:0.6f}")
                    logger.debug(f"Waiting for next interation...")
                    while time.perf_counter() - self.simulation_start_time < self.time:
                        await asyncio.sleep(0)
                    # self._elapsed_time = (
                    #     time.perf_counter() - self.simulation_start_time
                    # )
                    # self._time_difference = self.time - self.elapsed_time
                    # logger.debug(
                    #     f"Current Real Time: {self.elapsed_time:0.3f}."
                    # )
                    # waiting_time = max(0, self.time_difference)
                    # logger.debug(
                    #     f"Waiting for {waiting_time:0.3f} seconds."
                    # )
                    # before = time.perf_counter()
                    # await asyncio.sleep(waiting_time)
                    # after = time.perf_counter()
                    # logger.debug(
                    #     f"Actual waiting time: {after - before:0.3f} seconds."
                    # )
                    
                else:
                    # iterate through all event priorities
                    self._current_event_priority = 0
                    while self.current_event_priority <= self._max_event_priority:
                        logger.debug(
                            f"Current Event Priority: {self.current_event_priority}"
                        )
                        await asyncio.sleep(0)
                        self._current_event_priority += 1
                    # wait for the time step
                    self._time += self.time_step
                    self._time = round(self.time, self.time_resolution)
                    await asyncio.sleep(0)

            self._simulation_end_time = time.perf_counter()
            if self.realtime:
                logger.info(
                    f"Simulation completed in {round(self.simulation_end_time - self.simulation_start_time, 6)} seconds, exceeding real time by {round(((self.simulation_end_time - self.simulation_start_time - till)/till)*100,2)}%."
                )

        return time_flow()

    def enable_realtime(self, time_resolution: int = 3):
        """Enable the real time simulation. Time step will be adjusted to 0.1s."""
        self.time_resolution = time_resolution
        self._time_step = round(1 / pow(10, self.time_resolution), self.time_resolution)
        self._realtime = True

    def set_logging_level(self, level: int = logging.DEBUG):
        """Set the logging level. Default is DEBUG."""
        logger.setLevel(level)

    @property
    def time(self):
        """Return the current time."""
        return self._time

    @property
    def time_resolution(self):
        """Return the time resolution. 1 for 0.1s, 2 for 0.01s, 3 for 0.001s, and so on. Default is 3."""
        if self._time_resolution < 0:
            raise ValueError("Time resolution cannot be less than 0.")
        return self._time_resolution

    @time_resolution.setter
    def time_resolution(self, value: int):
        """Set the time resolution. 1 for 0.1s, 2 for 0.01s, 3 for 0.001s, and so on. Default is 3."""
        if value < 0:
            raise ValueError("Time resolution cannot be less than 0.")
        self._time_resolution = value
        self._time_step = round(1 / pow(10, self.time_resolution), self.time_resolution)

    @property
    def time_step(self):
        """The time step of the simulation. Default is 0.001s."""
        return self._time_step

    @property
    def realtime(self):
        """Return True if the simulation is in real time mode, otherwise False. Default is False."""
        return self._realtime

    @property
    def pending_events(self):
        """The events that are pending to be executed. Please note that this is not the queue for future events. This is used for start async tasks for the events."""
        return self._pending_events

    @property
    def current_event_priority(self):
        """The current event priority."""
        return self._current_event_priority

    @property
    def max_event_priority(self):
        """The maximum event priority."""
        return self._max_event_priority

    @property
    def elapsed_time(self):
        """The real elapsed time of the simulation."""
        return self._elapsed_time

    @property
    def time_difference(self):
        """The time difference between the real time and simulation time."""
        return self._time_difference

    @property
    def simulation_start_time(self):
        """The time when the simulation started."""
        return self._simulation_start_time

    @property
    def simulation_end_time(self):
        """The time when the simulation ended."""
        return self._simulation_end_time


Mundus = Universe()
