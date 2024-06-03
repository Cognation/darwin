from typing import Optional

from core.log import get_logger
from core.ui.base import ProjectStage, UIBase, UIClosedError, UISource, UserInput

log = get_logger(__name__)

import requests
def post(data):
    url = 'http://localhost:8080/out'
    try:
        res = requests.post(url, data={"message":data})
        print(res.json())
    except requests.exceptions.RequestException as e:
        print("Error : ", str(e))

def request_project_name(url="http://localhost:8080/request_project_name"):
    try:
        res = requests.get(url)
        return res.json()["project_name"]
    except requests.exceptions.RequestException as e:
        print("Error : ", str(e))
        return "continue"
    
def request_user_query(url="http://localhost:8080/request_user_query"):
    try:
        res = requests.get(url)
        return res.json()["user_query"]
    except requests.exceptions.RequestException as e:
        print("Error : ", str(e))
        return "continue"
    
input_counter = 0
def get_input(prompt):
    global input_counter
    if input_counter == 0:
        input_counter += 1
        return request_project_name()
    
    if input_counter == 1:
        input_counter += 1
        return request_user_query()

    url = 'http://localhost:8080/in'
    try:
        res = requests.get(url, data={"prompt":prompt})
        return res.json()["input"] 
    except requests.exceptions.RequestException as e:
        print("Error : ", str(e))
        return "continue"

class PlainConsoleUI(UIBase):
    """
    UI adapter for plain (no color) console output.
    """

    async def start(self) -> bool:
        log.debug("Starting console UI")
        return True

    async def stop(self):
        log.debug("Stopping console UI")

    async def send_stream_chunk(self, chunk: Optional[str], *, source: Optional[UISource] = None):
        if chunk is None:
            # end of stream
            # print("", flush=True)
            post("")
        else:
            # print(chunk, end="", flush=True)
            post(chunk)

    async def send_message(self, message: str, *, source: Optional[UISource] = None):
        if source:
            # print(f"[{source}] {message}")
            post(f"[{source}] {message}")
        else:
            # print(message)
            post(message)

    async def send_key_expired(self, message: Optional[str]):
        if message:
            await self.send_message(message)

    async def ask_question(
        self,
        question: str,
        *,
        buttons: Optional[dict[str, str]] = None,
        default: Optional[str] = None,
        buttons_only: bool = False,
        allow_empty: bool = False,
        hint: Optional[str] = None,
        initial_text: Optional[str] = None,
        source: Optional[UISource] = None,
    ) -> UserInput:
        if source:
            # print(f"[{source}] {question}")
            post(f"[{source}] {question}")
        else:
            # print(f"{question}")
            post(f"{question}")

        if buttons:
            for k, v in buttons.items():
                default_str = " (default)" if k == default else ""
                # print(f"  [{k}]: {v}{default_str}")
                post(f"  [{k}]: {v}{default_str}")

        while True:
            try:
                #choice = input("> ").strip()
                choice = get_input("> ")
            except KeyboardInterrupt:
                raise UIClosedError()
            if not choice and default:
                choice = default
            if buttons and choice in buttons:
                return UserInput(button=choice, text=None)
            if buttons_only:
                # print("Please choose one of available options")
                post("Please choose one of available options")
                continue
            if choice or allow_empty:
                return UserInput(button=None, text=choice)
            # print("Please provide a valid input")
            post("Please provide a valid input")

    async def send_project_stage(self, stage: ProjectStage):
        pass

    async def send_task_progress(
        self,
        index: int,
        n_tasks: int,
        description: str,
        source: str,
        status: str,
        source_index: int = 1,
    ):
        pass

    async def send_step_progress(
        self,
        index: int,
        n_steps: int,
        step: dict,
        task_source: str,
    ):
        pass

    async def send_run_command(self, run_command: str):
        pass

    async def open_editor(self, file: str, line: Optional[int] = None):
        pass

    async def send_project_root(self, path: str):
        pass

    async def send_project_stats(self, stats: dict):
        pass

    async def loading_finished(self):
        pass

    async def send_project_description(self, description: str):
        pass

    async def send_features_list(self, features: list[str]):
        pass


__all__ = ["PlainConsoleUI"]
