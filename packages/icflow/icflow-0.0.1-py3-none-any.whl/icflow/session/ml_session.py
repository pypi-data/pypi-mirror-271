import os
from pathlib import Path

from icflow.session.session import WorkflowSession
from icflow.session.settings import SessionSettings
from icflow.session.task import Task
from icflow.output import OutputHandler


class MachineLearningSession(WorkflowSession):
    def __init__(
        self,
        settings: SessionSettings,
        dataset_dir: None | Path = None,
        result_dir: None | Path = None,
    ) -> None:
        super().__init__(settings, result_dir)

        if not dataset_dir:
            self.dataset_dir = Path(os.getcwd())
        else:
            self.dataset_dir = dataset_dir
        self.model = None
        self.dataloaders = None

        self.update_data_settings_from_model()
        self.init_dataloaders()

        self.output = OutputHandler(self.result_dir, self.settings.runtime)

    def get_model_settings(self):
        return self.settings.model

    def get_data_settings(self):
        return self.settings.data

    def get_data_setting(self, key, default=None):
        return self.settings.data.get(key, default)

    def get_model_setting(self, key, default=None):
        return self.settings.model.get(key, default)

    def get_runtime_setting(self, key, default=None):
        return self.settings.runtime.get(key, default)

    def get_model_name(self):
        return self.get_model_setting("model_name", "unnamed_model")

    def update_model_setting(self, key, value):
        self.settings.update_model_setting(key, value)

    def update_data_setting(self, key, value):
        self.settings.update_data_setting(key, value)

    def init_model(self):
        pass

    def init_dataloaders(self):
        pass

    def update_data_settings_from_model(self):
        pass

    def update_model_settings_from_dataset(self):
        pass

    def init_tasks(self):
        super().init_tasks()

        self.tasks.append(Task("train", self.train))
        self.tasks.append(Task("save", self.save, ["train"]))

    def train(self):
        self.dataloaders.load()
        self.update_model_settings_from_dataset()
        self.init_model()

        self.save_initial_config()

        num_epochs = self.get_runtime_setting("num_epochs", 5)
        self.model.train(self.dataloaders, self.output, num_epochs)

    def save(self):
        dataset_name = self.dataloaders.dataset_name
        model_output_path = f"{dataset_name}_{self.model.name}.pth"
        self.model.save(self.result_dir / model_output_path)
