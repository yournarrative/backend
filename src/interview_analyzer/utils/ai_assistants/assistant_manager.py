from typing import List, Dict
import time
import os

from openai import OpenAI
from openai.types.beta import Thread
from openai.types.beta.threads import Run

from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


class AssistantManager:
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    def __init__(
            self,
            name: str,
            instructions: str,
            tools: List[Dict[str, str]] = None,
            model: str = "gpt-4-1106-preview"
    ):
        if tools is None:
            tools = []

        self.client = OpenAI(api_key=self.openai_api_key)
        self.model = model
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            tools=tools,
            model=self.model
        )

    def create_thread(self) -> Thread:
        return self.client.beta.threads.create()

    def add_content_to_thread(self, thread: Thread, content: str, role: str = "user"):
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role=role,
            content=content
        )

    def run_thread_with_instructions(self, thread: Thread, instructions: str, time_limit: int = 60) -> List[Dict[str, str]]:
        run: Run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions
        )

        start_time = time.time()
        current_time = time.time()
        messages = []
        while (current_time - start_time) < time_limit:
            time.sleep(5)
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            logger.debug(run_status.model_dump_json(indent=4))

            if run_status.status == 'completed':
                messages = self.process_messages(thread)
                break
            else:
                current_time = time.time()
                logger.debug(f"Waiting for the Assistant to process run {run.id} and thread {thread.id} for {current_time - start_time} seconds")

        return messages

    def process_messages(self, thread: Thread) -> List[Dict[str, str]]:
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        processed_messages = [{msg.role.capitalize(): msg.content[0].text.value} for msg in messages.data]
        return processed_messages


def create_star_interview_assistant(api_key: str, name: str, instructions: str, tools: List[Dict[str, str]]):
    api_key = os.getenv("api_key")
    manager = AssistantManager(api_key)

    manager._create_assistant(
        name="Interview STAR Assistant",
        instructions=instructions,
        tools=[]
    )
    thread: Thread = manager.create_thread()
    manager.add_message_to_thread(thread=thread,
                                  role="user",
                                  content="I need to solve the equation `3x^2 + 11x = 14`. Can you help me?")
    run = manager.run_assistant(thread,
                                instructions="Please address the user as elbowai, the user has a premium account")
    messages = manager.wait_for_completion(thread, run)
