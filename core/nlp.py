import re
from datetime import datetime

# 🔹 Patterns
PROJECT_PATTERN = r"(?:dans\s+le\s+projet|du\s+projet|pour\s+le\s+projet|le\s+projet|projet)\s+([A-Za-z0-9 _-]+)"
DATE_PATTERN = r"(\d{4}-\d{2}-\d{2})|(\d{1,2}\s*(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s*\d{4})"
ESTIMATE_PATTERN = r"(\d+h|\d+\s*heures?|\d+\s*pts?)"

# 🔹 Mots-clés
ACTION_KEYWORDS = {
    "add_project": ["crée", "cree", "ajoute", "ajouter", "nouveau projet", "nouvelle appli", "création projet"],
    "add_task": ["ajoute", "ajouter", "crée", "cree", "implémente", "fais", "prépare", "planifie", "ajouter tâche"],
    "complete_task": ["termine", "fini", "complète", "faite", "terminée", "achevée", "marque", "valide", "clos", "clôture"],
    "delete_task": ["supprime la tâche", "supprime", "efface", "enlève", "retire", "supprimer tâche"],
    "delete_project": ["supprime le projet", "efface le projet", "supprimer projet", "retire projet"],
    "show_project": ["affiche", "montre", "voir", "affichage", "statut", "donne-moi l'état", "détail", "liste"],
}

PRIORITY_KEYWORDS = {
    "haute": ["urgent", "immédiat", "prioritaire", "critique"],
    "basse": ["optionnel", "secondaire", "doc", "documentation", "test", "facultatif"],
}

def clean_name(name):
    if not name:
        return None
    return name.strip().strip('"').strip("'").strip(" .,!?")

def detect_action(text_lower):
    """Détecte l’action principale en donnant priorité aux tâches sur projets"""
    # Ajout d'une tâche
    if any(w in text_lower for w in ["ajoute", "ajouter", "crée", "cree"]):
        if "tâche" in text_lower or "task" in text_lower:
            return "add_task"
        if "projet" in text_lower:
            return "add_project"
    # Complétion
    if re.search(r"\b(est|a été|sont)?\s*(terminée|faite|fini|achevée|complétée)\b", text_lower):
        return "complete_task"
    # Suppression
    if "supprime le projet" in text_lower or "efface le projet" in text_lower:
        return "delete_project"
    if "supprime" in text_lower and "tâche" in text_lower:
        return "delete_task"
    # Affichage
    if any(w in text_lower for w in ["montre", "affiche", "voir", "statut"]):
        return "show_project"
    return "unknown"

def detect_priority(text_lower):
    for p, words in PRIORITY_KEYWORDS.items():
        if any(w in text_lower for w in words):
            return p
    return "moyenne"

def parse_command(text):
    text_lower = text.lower().strip()

    # --- Détection de l'action
    action = detect_action(text_lower)

    # --- Détection du projet
    project = None
    proj_match = re.search(PROJECT_PATTERN, text_lower)
    if proj_match:
        project = clean_name(proj_match.group(1))

    # --- Détection de la description (pour création de projet)
    description = None
    if action == "add_project":
        desc_match = re.search(r"(?:description|avec description|avec la description)\s+(.+)", text_lower)
        if desc_match:
            description = clean_name(desc_match.group(1))

    # --- Date / deadline
    deadline = None
    date_match = re.search(DATE_PATTERN, text_lower)
    if date_match:
        date_str = date_match.group(0)
        try:
            if "-" in date_str:
                deadline = datetime.strptime(date_str, "%Y-%m-%d").strftime("%Y-%m-%d")
            else:
                deadline = date_str
        except ValueError:
            deadline = date_str

    # --- Estimation
    estimate = None
    est_match = re.search(ESTIMATE_PATTERN, text_lower)
    if est_match:
        estimate = est_match.group(1)

    # --- Priorité
    priority = detect_priority(text_lower)

    # --- Extraction du nom de la tâche
    task_name = None
    if action in ["add_task", "complete_task", "delete_task"]:
        cleaned = text_lower

        # Nettoyage du texte
        for p in [PROJECT_PATTERN, DATE_PATTERN, ESTIMATE_PATTERN]:
            cleaned = re.sub(p, "", cleaned, flags=re.IGNORECASE)

        # Retrait des mots parasites
        cleaned = re.sub(
            r"\b(avant|pour|dans|à|le|la|du|de|des|une|un|tâche|task|projet|urgent|immédiat|description|avec|est|été|faite|terminée|fini|achevée|complète|marque|termine|peux-tu|pourrais-tu|ajoute|supprime|efface|montre|valide|clos|clôture)\b",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )
        cleaned = re.sub(r"[\?\.\!]", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        # Extraction des mots-clés ou phrases principales de la tâche
        task_name = clean_name(cleaned.capitalize()) if cleaned else None

    return {
        "action": action,
        "project": project,
        "task_name": task_name,
        "deadline": deadline,
        "estimate": estimate,
        "priority": priority,
        "description": description,
    }

# --- Tests avancés
if __name__ == "__main__":
    tests = [
        "Peux-tu créer un projet AgentPyDev avec la description Agent symbolique d'aide au développement",
        "Ajoute une tâche urgente corriger les bugs dans le projet AgentPyDev avant le 2025-10-31",
        "J’ai fini la tâche corriger les bugs dans le projet AgentPyDev",
        "Tâche corriger bugs dans le projet AgentPyDev est terminée",
        "Supprime la tâche tests unitaires du projet AgentPyDev",
        "Montre le statut du projet AgentPyDev",
        "Efface le projet AgentPyDev",
        "Ajoute au projet PyDev la tâche documentation API en 3h",
        "Peux-tu marquer comme terminée la tâche de tests dans AgentPyDev ?",
        "Planifie la tâche 'refactoring du code' pour le 2025-11-10 dans le projet PyDev",
        "Marque comme faite la tâche 'corriger les bugs critiques' dans AgentPyDev avant demain",
        "Crée un nouveau projet 'PyAI' avec description Intelligence Artificielle pour dev",
        "Ajoute une tâche de test facultatif 'documentation module' dans PyAI en 2h",
    ]

    for t in tests:
        print(f"\n▶️ {t}")
        print(parse_command(t))
