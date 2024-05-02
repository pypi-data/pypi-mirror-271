import os
import json
from pathlib import Path
import logging

import icflow.utils
from icflow.session.settings import SessionSettings


class WorkflowSession:
    def __init__(
        self, settings: SessionSettings, result_dir: None | Path = None
    ) -> None:

        if result_dir is None:
            self.result_dir = Path(os.getcwd())
        else:
            self.result_dir = result_dir

        self.settings = settings
        self.tasks: list = []
        self.tasks_initialized = False

    @staticmethod
    def setup_result_dir(result_dir: Path):
        current_time = icflow.utils.get_timestamp_for_paths()
        result_dir = result_dir / Path(current_time)
        os.makedirs(result_dir, exist_ok=True)
        return result_dir

    def save_initial_config(self):
        config_output_path = self.result_dir / "initial_config.json"
        output_content = self.settings.serialize()
        with open(config_output_path, "w") as f:
            json.dump(output_content, f)

    def init_tasks(self):
        self.tasks_initialized = True

    def run_tasks(self):

        if not self.tasks_initialized:
            self.init_tasks()

        if not self.tasks:
            logging.info("No tasks available to launch")
            return

        logging.info(f"Launching {len(self.tasks)} tasks")

        for idx, task in enumerate(self.tasks):
            logging.info(f"Launching {idx} of {len(self.tasks)} tasks: {task.name}")
            task.launch()

        logging.info("Finished launching tasks")
