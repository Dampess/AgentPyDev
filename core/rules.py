# core/rules.py
from typing import Dict, List

def analyze_priority(task_name: str) -> str:
    """Attribue une priorité simple selon mots-clés."""
    name = task_name.lower()
    if any(k in name for k in ("urgent", "immediat", "critique", "bug", "bloquant")):
        return "haute"
    if any(k in name for k in ("amélior", "refactor", "optim", "perf")):
        return "moyenne"
    if any(k in name for k in ("test", "doc", "documentation", "readme")):
        return "basse"
    return "moyenne"

def suggest_next_task(tasks: List[Dict]) -> str:
    """Renvoie la tâche non faite la plus prioritaire."""
    pending = [t for t in tasks if not t.get("done", False)]
    if not pending:
        return "✅ Toutes les tâches sont terminées."
    priority_order = {"haute": 3, "moyenne": 2, "basse": 1}
    # si priorité inconnue -> moyenne
    next_task = max(pending, key=lambda t: priority_order.get(t.get("priority","moyenne"), 2))
    return f"Prochaine tâche recommandée : {next_task['name']} (priorité: {next_task.get('priority','moyenne')})"
