import uuid
from datetime import datetime
from core.rules import analyze_priority

def create_task(name, deadline=None, estimate=None):
    """Crée une tâche avec métadonnées enrichies."""
    return {
        "id": str(uuid.uuid4())[:8],
        "name": name,
        "priority": analyze_priority(name),
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "deadline": deadline if deadline else None,
        "estimate": estimate if estimate else None,
    }

def mark_done(tasks, task_name):
    for t in tasks:
        if t["name"].lower() == task_name.lower():
            t["done"] = True
            return f"Tâche '{task_name}' marquée comme terminée ✅"
    return f"Aucune tâche nommée '{task_name}' trouvée."

def remove_task(tasks, task_name):
    for t in tasks:
        if t["name"].lower() == task_name.lower():
            tasks.remove(t)
            return f"Tâche '{task_name}' supprimée 🗑️"
    return f"Aucune tâche nommée '{task_name}' trouvée."

def sort_tasks(tasks):
    """Trie par priorité puis par deadline (si présente)."""
    priority_order = {"haute": 3, "moyenne": 2, "basse": 1}
    
    def sort_key(t):
        score = priority_order.get(t["priority"], 0)
        if t.get("deadline"):
            try:
                deadline = datetime.strptime(t["deadline"], "%Y-%m-%d")
                # plus la date est proche, plus la priorité monte
                score += max(0, 10 - (deadline - datetime.now()).days)
            except ValueError:
                pass
        return score
    
    return sorted(tasks, key=sort_key, reverse=True)
