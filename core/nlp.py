import re
from datetime import datetime

# 🔹 Patterns
PROJECT_PATTERN = r"(?:projet|dans|à)\s+([A-Za-z0-9 _-]+)"
DATE_PATTERN = r"(\d{4}-\d{2}-\d{2})|(\d{1,2}\s*(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s*\d{4})"
ESTIMATE_PATTERN = r"(\d+h|\d+\s*heures|\d+\s*pts?)"

def clean_name(name):
    """Nettoie guillemets, apostrophes et espaces superflus"""
    if not name:
        return None
    return name.strip().strip('"').strip("'").strip()

def parse_command(text):
    text_lower = text.lower().strip()

    # 🔹 Projet et description
    project = None
    description = None
    proj_match = re.search(r"projet\s+([A-Za-z0-9_-]+)(?:\s+avec description\s+(.+))?", text_lower)
    if proj_match:
        project = clean_name(proj_match.group(1))
        if proj_match.group(2):
            description = clean_name(proj_match.group(2))

    # 🔹 Date
    date_match = re.search(DATE_PATTERN, text_lower)
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
    estimate_match = re.search(ESTIMATE_PATTERN, text_lower)
    estimate = estimate_match.group(1) if estimate_match else None

    # 🔹 Priorité
    if any(word in text_lower for word in ["urgent", "immédiat", "prioritaire"]):
        priority = "haute"
    elif any(word in text_lower for word in ["optionnel", "test", "doc"]):
        priority = "basse"
    else:
        priority = "moyenne"

    # 🔹 Détection de l’action
    if any(word in text_lower for word in ["ajoute", "crée", "nouveau", "nouvelle", "ajouter"]):
        action = "add_project" if "projet" in text_lower else "add_task"
    elif any(word in text_lower for word in ["termine", "fini", "complète", "faite", "terminée", "achevée"]):
        action = "complete_task"
    elif any(word in text_lower for word in ["supprime tache", "enlève tache", "efface tache"]):
        action = "delete_task"
    elif any(word in text_lower for word in ["supprime projet", "efface projet", "supprimer projet"]):
        action = "delete_project"
    elif any(word in text_lower for word in ["montre", "affiche", "voir", "donne-moi l'état", "statut"]):
        action = "show_project"
    else:
        action = "unknown"

    # 🔹 Extraction du nom de la tâche
    task_name = None
    if action not in ["show_project", "delete_project", "add_project"]:
        cleaned = re.sub(PROJECT_PATTERN, "", text_lower)
        cleaned = re.sub(DATE_PATTERN, "", cleaned)
        cleaned = re.sub(r"\b(avant|pour|dans|à|le|la|du|de|des|une|un|tâche|ajoute|crée|nouvelle|urgent|immédiat|dans le projet|j'ai|jai|est|faite|terminée|complète|fini|termine|achevée)\b", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        task_match = re.search(r"(corriger|faire|implémenter|ajouter|réparer|tester|documenter|préparer|mettre|corrigé|bug|erreur|test|documentation|version|build)\s+(.*)", cleaned)
        task_name = clean_name(task_match.group(0).capitalize()) if task_match else clean_name(cleaned.capitalize())

    return {
        "action": action,
        "project": project,
        "task_name": task_name,
        "deadline": deadline,
        "estimate": estimate,
        "priority": priority,
        "description": description,
    }


# 🔧 Tests rapides
if __name__ == "__main__":
    tests = [
        'Crée un nouveau projet AgentPyDev avec description Gestion de tâches',
        'Ajoute une tâche urgente "corriger les bugs" dans le projet AgentPyDev avant le 2025-10-31',
        'J\'ai fini la tâche "corriger les bugs" dans le projet AgentPyDev',
        'Supprime la tâche "tests unitaires" du projet AgentPyDev',
        'Supprime le projet AgentPyDev',
        'Affiche le projet "AgentPyDev"',
    ]
    for t in tests:
        print(f"\n▶️ {t}")
        print(parse_command(t))
