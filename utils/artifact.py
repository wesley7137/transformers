# utils/artifact.py

class Artifact:
    def __init__(self, name: str):
        self.name = name
        self.paths = []

    def __str__(self):
        return self.name

    def add_path(self, path: str):
        self.paths.append({"name": self.name, "path": path})
