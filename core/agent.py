from core.memory import load_projects, save_projects
from core.planner import create_task, mark_done, remove_task, sort_tasks
from core.rules import suggest_next_task
from core.nlp import parse_command


class ProjectAgent:
    def __init__(self):
        self.projects = load_projects()
        self.active_project = None  # 🧠 Mémoire du dernier projet utilisé

    # 🔍 Recherche insensible à la casse
    def _get_project_key(self, project_name):
        """Retourne la clé exacte du projet dans self.projects, insensible à la casse."""
        if not project_name:
            return None
        for key in self.projects:
            if key.lower() == project_name.lower():
                return key
        return None

    def add_project(self, name, description):
        """Ajoute un projet en évitant les doublons insensibles à la casse."""
        key = self._get_project_key(name)
        if key:
            return f"⚠️ Le projet '{key}' existe déjà."
        self.projects[name] = {"description": description, "tasks": []}
        save_projects(self.projects)
        self.active_project = name  # 💾 Défini comme projet actif
        return f"✅ Projet '{name}' ajouté et défini comme projet actif."

    def add_task(self, project, task_name, deadline=None, estimate=None):
        """Ajoute une tâche à un projet existant (insensible à la casse)."""
        key = self._get_project_key(project or self.active_project)
        if not key:
            return f"❌ Aucun projet trouvé ou actif."
        task = create_task(task_name, deadline, estimate)
        self.projects[key]["tasks"].append(task)
        save_projects(self.projects)
        self.active_project = key  # 💾 Mise à jour du projet actif
        return f"Tâche '{task_name}' ajoutée à {key} (priorité: {task['priority']})."

    def show_status(self, project=None):
        """Affiche l’état d’un projet (ou du projet actif si aucun précisé)."""
        key = self._get_project_key(project or self.active_project)
        if not key:
            return "❌ Aucun projet actif ou trouvé."
        p = self.projects[key]
        tasks = sort_tasks(p["tasks"])

        lines = [f"\n📁 {key} — {p['description']}"]
        for t in tasks:
            status = "✅" if t["done"] else "🕓"
            dl = f" ⏰ {t['deadline']}" if t["deadline"] else ""
            est = f" ⏱️ {t['estimate']}" if t["estimate"] else ""
            lines.append(f" - {t['name']} ({t['priority']}){dl}{est} {status}")
        lines.append("\n" + suggest_next_task(tasks))
        return "\n".join(lines)

    def complete_task(self, project, task_name):
        """Marque une tâche comme terminée."""
        key = self._get_project_key(project or self.active_project)
        if not key:
            return "❌ Aucun projet actif ou trouvé."
        msg = mark_done(self.projects[key]["tasks"], task_name)
        save_projects(self.projects)
        self.active_project = key
        return msg
    def delete_project(self, project):
         """Supprime un projet complet de la base de données."""
         key = self._get_project_key(project)
         if not key:
           return f"❌ Projet inconnu : {project}"
    
         # Supprime le projet
         del self.projects[key]
         save_projects(self.projects)
    
        # Si c'était le projet actif, on le désactive
         if self.active_project == key:
          self.active_project = None
    
          return f"🗑️ Projet '{key}' supprimé avec succès."

    def delete_task(self, project, task_name):
        """Supprime une tâche d’un projet."""
        key = self._get_project_key(project or self.active_project)
        if not key:
            return "❌ Aucun projet actif ou trouvé."
        msg = remove_task(self.projects[key]["tasks"], task_name)
        save_projects(self.projects)
        self.active_project = key
        return msg

    def interpret(self, text):
        """Interprète une commande textuelle naturelle."""
        parsed = parse_command(text)
        print("\n[DEBUG] Analyse NLP :", parsed) #temporaire


        action = parsed.get("action")
        project = parsed.get("project")
        task_name = parsed.get("task_name")
        deadline = parsed.get("deadline")
        estimate = parsed.get("estimate")
        priority = parsed.get("priority")
        description = parsed.get("description")

        if action == "unknown":
            return "🤔 Je n'ai pas compris la commande."

        elif action == "add_project":
            if not project:
                return "❌ Il manque le nom du projet."
            return self.add_project(project, description or "")

        elif action == "add_task":
            if not project or not task_name:
                return "❌ Il manque le nom du projet ou de la tâche."
            return self.add_task(project, task_name, deadline, estimate)

        elif action == "complete_task":
            if not project or not task_name:
                return "❌ Il manque le nom du projet ou de la tâche."
            return self.complete_task(project, task_name)

        elif action == "delete_task":
            if not project or not task_name:
                return "❌ Il manque le nom du projet ou de la tâche."
            return self.delete_task(project, task_name)

        elif action == "delete_project":
            if not project:
                return "❌ Il faut préciser le projet à supprimer."
            # On supprime le projet de la base
            key = self._get_project_key(project)
            if not key:
                return f"❌ Projet inconnu : {project}"
            del self.projects[key]
            save_projects(self.projects)
            return f"🗑️ Projet '{key}' supprimé."

        elif action == "show_project":
            if not project:
                return "❌ Il faut préciser quel projet tu veux voir."
            return self.show_status(project)

        else:
            return "❓ Commande non reconnue."

