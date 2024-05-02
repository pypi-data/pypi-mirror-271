class Task:
    def __init__(self, name, func, depends=None) -> None:
        self.name = name
        self.func = func

        if not depends:
            self.depends = []
        else:
            self.depends = depends

    def launch(self):
        self.func()
