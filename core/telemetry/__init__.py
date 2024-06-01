import sys
import time
import traceback
from copy import deepcopy
from pathlib import Path
from typing import Any

import httpx

from core.config import get_config
from core.config.user_settings import settings
from core.config.version import get_version
from core.log import get_logger

log = get_logger(__name__)

LARGE_REQUEST_THRESHOLD = 50000  # tokens
SLOW_REQUEST_THRESHOLD = 300  # seconds


class Telemetry:
    """
    Pythagora telemetry data collection.

    This class is a singleton, use the `telemetry` global variable to access it:

    >>> from core.telemetry import telemetry

    To record start of application creation process:

    >>> telemetry.start()

    To record data or increase counters:

    >>> telemetry.set("model", "gpt-4")
    >>> telemetry.inc("num_llm_requests", 5)

    To stop recording and send the data:

    >>> telemetry.stop()
    >>> await telemetry.send()

    Note: all methods are no-ops if telemetry is not enabled.
    """

    MAX_CRASH_FRAMES = 3

    def __init__(self):
        self.enabled = False
        self.telemetry_id = None
        self.endpoint = None
        self.clear_data()

        if settings.telemetry is not None:
            self.enabled = settings.telemetry.enabled
            self.telemetry_id = settings.telemetry.id
            self.endpoint = settings.telemetry.endpoint

        if self.enabled:
            log.debug(f"Telemetry enabled (id={self.telemetry_id}), configure or disable it in {settings.config_path}")

    def clear_data(self):
        """
        Reset all telemetry data to default values.
        """
        config = get_config()

        self.data = {
            # System platform
            "platform": sys.platform,
            # Python version used for GPT Pilot
            "python_version": sys.version,
            # GPT Pilot version
            "pilot_version": get_version(),
            # GPT Pilot Extension version
            "extension_version": None,
            # Is extension used
            "is_extension": False,
            # The default LLM provider and model
            "provider": config.agent["default"].provider.value,
            "model": config.agent["default"].model,
            # Initial prompt
            "initial_prompt": None,
            # Optional template used for the project
            "template": None,
            # Optional user contact email
            "user_contact": None,
            # Unique project ID (app_id)
            "app_id": None,
            # Project architecture
            "architecture": None,
        }
        if sys.platform == "linux":
            try:
                import distro

                self.data["linux_distro"] = distro.name(pretty=True)
            except Exception as err:
                log.debug(f"Error getting Linux distribution info: {err}", exc_info=True)
        self.clear_counters()

    def clear_counters(self):
        """
        Reset telemetry counters while keeping the base data.
        """
        self.data.update(
            {
                # Number of LLM requests made
                "num_llm_requests": 0,
                # Number of LLM requests that resulted in an error
                "num_llm_errors": 0,
                # Number of tokens used for LLM requests
                "num_llm_tokens": 0,
                # Number of development steps
                "num_steps": 0,
                # Number of commands run during development
                "num_commands": 0,
                # Number of times a human input was required during development
                "num_inputs": 0,
                # Number of files in the project
                "num_files": 0,
                # Total number of lines in the project
                "num_lines": 0,
                # Number of tasks started during development
                "num_tasks": 0,
                # Number of seconds elapsed during development
                "elapsed_time": 0,
                # Total number of lines created by GPT Pilot
                "created_lines": 0,
                # End result of development:
                # - success:initial-project
                # - success:feature
                # - success:exit
                # - failure
                # - failure:api-error
                # - interrupt
                "end_result": None,
                # Whether the project is continuation of a previous session
                "is_continuation": False,
                # Optional user feedback
                "user_feedback": None,
                # If GPT Pilot crashes, record diagnostics
                "crash_diagnostics": None,
                # Statistics for large requests
                "large_requests": None,
                # Statistics for slow requests
                "slow_requests": None,
            }
        )
        self.start_time = None
        self.end_time = None
        self.large_requests = []
        self.slow_requests = []

    def set(self, name: str, value: Any):
        """
        Set a telemetry data field to a value.

        :param name: name of the telemetry data field
        :param value: value to set the field to

        Note: only known data fields may be set, see `Telemetry.clear_data()` for a list.
        """
        if name not in self.data:
            log.error(f"Telemetry.record(): ignoring unknown telemetry data field: {name}")
            return

        self.data[name] = value

    def inc(self, name: str, value: int = 1):
        """
        Increase a telemetry data field by a value.

        :param name: name of the telemetry data field
        :param value: value to increase the field by (default: 1)

        Note: only known data fields may be increased, see `Telemetry.clear_data()` for a list.
        """
        if name not in self.data:
            log.error(f"Telemetry.increase(): ignoring unknown telemetry data field: {name}")
            return

        self.data[name] += value

    def start(self):
        """
        Record start of application creation process.
        """
        self.start_time = time.time()
        self.end_time = None

    def stop(self):
        """
        Record end of application creation process.
        """
        if self.start_time is None:
            log.error("Telemetry.stop(): cannot stop telemetry, it was never started")
            return

        self.end_time = time.time()
        self.data["elapsed_time"] = int(self.end_time - self.start_time)

    def record_crash(
        self,
        exception: Exception,
        end_result: str = "failure",
    ) -> str:
        """
        Record crash diagnostics.

        The formatted stack trace only contains frames from the `core` package
        of gpt-pilot.

        :param exception: exception that caused the crash
        :param end_result: end result of the application (default: "failure")
        :return: formatted stack trace of the exception

        Records the following crash diagnostics data:
        * formatted stack trace
        * exception (class name and message)
        * file:line for the last (innermost) 3 frames of the stack trace, only counting
            the frames from the `core` package.
        """
        self.set("end_result", end_result)

        root_dir = Path(__file__).parent.parent.parent
        exception_class_name = exception.__class__.__name__
        exception_message = str(exception)

        frames = []
        info = []

        for frame in traceback.extract_tb(exception.__traceback__):
            try:
                file_path = Path(frame.filename).absolute().relative_to(root_dir).as_posix()
            except ValueError:
                # outside of root_dir
                continue

            if not file_path.startswith("core/"):
                continue

            frames.append(
                {
                    "file": file_path,
                    "line": frame.lineno,
                    "name": frame.name,
                    "code": frame.line,
                }
            )
            info.append(f"File `{file_path}`, line {frame.lineno}, in {frame.name}\n    {frame.line}")

        frames.reverse()
        stack_trace = "\n".join(info) + f"\n{exception.__class__.__name__}: {str(exception)}"

        self.data["crash_diagnostics"] = {
            "stack_trace": stack_trace,
            "exception_class": exception_class_name,
            "exception_message": exception_message,
            "frames": frames[: self.MAX_CRASH_FRAMES],
        }
        return stack_trace

    def record_llm_request(
        self,
        tokens: int,
        elapsed_time: int,
        is_error: bool,
    ):
        """
        Record an LLM request.

        :param tokens: number of tokens in the request
        :param elapsed_time: time elapsed for the request
        :param is_error: whether the request resulted in an error
        """
        self.inc("num_llm_requests")

        if is_error:
            self.inc("num_llm_errors")
        else:
            self.inc("num_llm_tokens", tokens)

        if tokens > LARGE_REQUEST_THRESHOLD:
            self.large_requests.append(tokens)
        if elapsed_time > SLOW_REQUEST_THRESHOLD:
            self.slow_requests.append(elapsed_time)

    def calculate_statistics(self):
        """
        Calculate statistics for large and slow requests.
        """
        n_large = len(self.large_requests)
        n_slow = len(self.slow_requests)

        self.data["large_requests"] = {
            "num_requests": n_large,
            "min_tokens": min(self.large_requests) if n_large > 0 else None,
            "max_tokens": max(self.large_requests) if n_large > 0 else None,
            "avg_tokens": sum(self.large_requests) // n_large if n_large > 0 else None,
            "median_tokens": sorted(self.large_requests)[n_large // 2] if n_large > 0 else None,
        }
        self.data["slow_requests"] = {
            "num_requests": n_slow,
            "min_time": min(self.slow_requests) if n_slow > 0 else None,
            "max_time": max(self.slow_requests) if n_slow > 0 else None,
            "avg_time": sum(self.slow_requests) // n_slow if n_slow > 0 else None,
            "median_time": sorted(self.slow_requests)[n_slow // 2] if n_slow > 0 else None,
        }

    async def send(self, event: str = "pilot-telemetry"):
        """
        Send telemetry data to the phone-home endpoint.

        Note: this method clears all telemetry data after sending it.
        """
        if not self.enabled:
            return

        if self.endpoint is None:
            log.error("Telemetry.send(): cannot send telemetry, no endpoint configured")
            return

        if self.start_time is not None and self.end_time is None:
            self.stop()

        self.calculate_statistics()
        payload = {
            "pathId": self.telemetry_id,
            "event": event,
            "data": self.data,
        }

        log.debug(f"Telemetry.send(): sending telemetry data to {self.endpoint}")
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.endpoint, json=payload)
                response.raise_for_status()
            self.clear_counters()
            self.set("is_continuation", True)
        except httpx.RequestError as e:
            log.error(f"Telemetry.send(): failed to send telemetry data: {e}", exc_info=True)

    def get_project_stats(self) -> dict:
        return {
            "num_lines": self.data["num_lines"],
            "num_files": self.data["num_files"],
            "num_tokens": self.data["num_llm_tokens"],
        }

    async def trace_code_event(self, name: str, data: dict):
        """
        Record a code event to trace potential logic bugs.

        :param name: name of the event
        :param data: data to send with the event
        """
        if not self.enabled:
            return

        payload = {
            "pathId": self.telemetry_id,
            "event": f"trace-{name}",
            "data": data,
        }

        log.debug(f"Sending trace event {name} to {self.endpoint}")

        try:
            async with httpx.AsyncClient() as client:
                await client.post(self.endpoint, json=payload)
        except httpx.RequestError:
            pass

    async def trace_loop(self, name: str, task_with_loop: dict):
        payload = deepcopy(self.data)
        payload["task_with_loop"] = task_with_loop
        await self.trace_code_event(name, payload)


telemetry = Telemetry()


__all__ = ["telemetry"]
