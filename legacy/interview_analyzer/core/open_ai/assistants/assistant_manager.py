import os
import time
from typing import List

from openai import OpenAI
from openai.types.beta import Thread
from openai.types.beta.threads import Run

from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


class AssistantManager:
    openai_api_key = os.environ.get("OPENAI_API_KEY")

    def __init__(
        self,
        name: str,
        instructions: str,
        model: str = "gpt-4-1106-preview",
        tools=None,
    ):
        if tools is None:
            tools = []
        self.client = OpenAI(api_key=self.openai_api_key)
        self.assistant = self.client.beta.assistants.create(
            name=name,
            instructions=instructions,
            model=model,
            tools=tools,
        )

    def create_thread(self) -> Thread:
        return self.client.beta.threads.create()

    def add_message_to_thread(self, thread: Thread, content: str):
        self.client.beta.threads.messages.create(thread_id=thread.id, role="user", content=content)

    def run_thread(self, thread: Thread, instructions: str, time_limit: int = 60) -> List[str]:
        run: Run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            instructions=instructions,
        )

        start_time = time.time()
        current_time = time.time()
        messages = []
        while (current_time - start_time) < time_limit:
            time.sleep(5)  # big async speedup boost by refactoring this
            run_status = self.client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

            logger.debug(f"Run status: {run_status.status}")

            if run_status.status == "completed":
                messages = self.process_messages(thread)
                break
            else:
                current_time = time.time()

        return messages

    def process_messages(self, thread: Thread) -> List[str]:
        messages = self.client.beta.threads.messages.list(thread_id=thread.id)
        processed_messages = [msg.content[0].text.value for msg in messages.data]
        return processed_messages
