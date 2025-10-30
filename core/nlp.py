import re
from datetime import datetime

PROJECT_PATTERN = r"(?:projet|dans|à)\s+([A-Za-z0-9_-]+)"
DATE_PATTERN = r"(\d{4}-\d{2}-\d{2})|(\d{1,2}\s*(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s*\d{4})"
ESTIMATE_PATTERN = r"(\d+h|\d+\s*heures|\d+\s*pts?)"

def clean_name(name):
    """Nettoie les guillemets, apostrophes et espaces superflus"""
    if not name:
        return None
    return name.strip().strip('"').strip("'").strip()

def parse_command(text):
    text = text.lower().strip()

    # 🔹 Projet
    project_match = re.search(PROJECT_PATTERN, text)
    project = clean_name(project_match.group(1)) if project_match else None

    # 🔹 Date
    date_match = re.search(DATE_PATTERN, text)
    deadline = None
    if date_match:
        date_str = date_match.group(0)
        try:
            if "-" in date_str:
                deadline = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            else:
                deadline = date_str
        except ValueError:
            deadline = date_str

    # 🔹 Estimation
    estimate_match = re.search(ESTIMATE_PATTERN, text)
    estimate = estimate_match.group(1) if estimate_match else None

    # 🔹 Priorité
    if any(word in text for word in ["urgent", "immédiat", "prioritaire"]):
        priority = "haute"
    elif any(word in text for word in ["optionnel", "test", "doc"]):
        priority = "basse"
    else:
        priority = "moyenne"

    # 🔹 Détection de l’action
    if any(word in text for word in ["ajoute", "crée", "nouvelle", "ajouter"]):
        action = "add_task"
    elif any(word in text for word in ["termine", "fini", "complète", "faite", "terminée", "achevée"]):
        action = "complete_task"
    elif any(word in text for word in ["supprime", "enlève", "efface"]):
        action = "delete_task"
    elif any(word in text for word in ["montre", "affiche", "voir", "donne-moi l'état", "statut"]):
        action = "show_project"
    else:
        action = "unknown"

    # 🔹 Extraction du nom de la tâche
    task_name = None
    if action not in ["show_project"]:
        cleaned = re.sub(PROJECT_PATTERN, "", text)
        cleaned = re.sub(DATE_PATTERN, "", cleaned)
        cleaned = re.sub(r"\b(avant|pour|dans|à|le|la|du|de|des|une|un|tâche|ajoute|crée|nouvelle|urgent|immédiat|dans le projet|j'ai|jai|est|faite|terminée|complète|fini|termine|achevée)\b", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        # Exemples : "corriger les bugs", "tests unitaires"
        task_match = re.search(r"(corriger|faire|implémenter|ajouter|réparer|tester|documenter|préparer|mettre|corrigé|bug|erreur|test|documentation|version|build)\s+(.*)", cleaned)
        if task_match:
            task_name = task_match.group(0).capitalize()
        else:
            task_name = cleaned.capitalize()
        task_name = clean_name(task_name)

    return {
        "action": action,
        "project": project,
        "task_name": task_name,
        "deadline": deadline,
        "estimate": estimate,
        "priority": priority,
    }

# 🔧 Test rapide
if __name__ == "__main__":
    tests = [
        'J\'ai fini la tâche "corriger les bugs"',
        "Termine la tâche tests unitaires",
        "La documentation est faite",
        'Affiche le projet "AgentPyDev"',
        'Ajoute une tâche urgente "corriger les bugs" avant le 2025-10-31',
    ]
    for t in tests:
        print(f"\n▶️ {t}")
        print(parse_command(t))
