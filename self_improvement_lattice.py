import json
import os

LATTICE_FILE = "lattice.json"

DEFAULT_LATTICE = {
    "Code Quality": ["Refactor duplicate logic", "Add error handling"],
    "Documentation": ["Update README", "Add docstrings"],
    "Testing": ["Increase unit test coverage"]
}


def _default_structure():
    return {
        cat: [{"task": t, "done": False} for t in tasks]
        for cat, tasks in DEFAULT_LATTICE.items()
    }


class SelfImprovementLattice:
    def __init__(self, path: str = LATTICE_FILE):
        self.path = path
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return _default_structure()

    def save(self):
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2)

    def list_tasks(self) -> str:
        lines = []
        for cat, tasks in self.data.items():
            lines.append(f"{cat}:")
            for i, task in enumerate(tasks, 1):
                status = "✓" if task.get("done") else " "
                lines.append(f"  {i}. [{status}] {task['task']}")
        return "\n".join(lines)

    def add_task(self, category: str, task: str):
        tasks = self.data.setdefault(category, [])
        tasks.append({"task": task, "done": False})
        self.save()

    def complete_task(self, category: str, index: int) -> bool:
        tasks = self.data.get(category)
        if tasks and 0 <= index < len(tasks):
            tasks[index]["done"] = True
            self.save()
            return True
        return False

    def reset(self):
        self.data = _default_structure()
        self.save()
