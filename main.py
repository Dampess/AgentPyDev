from core.agent import ProjectAgent

def main():
    agent = ProjectAgent()
    print("🤖 AgentPyDev — version 1.1 (Gestion avancée des tâches)")
    print("Commandes : nouveau / tâche / avancé / voir / fini / parle / supprimer / quit")
    
    while True:
        cmd = input("\nCommande > ").strip().lower()

        if cmd == "nouveau":
            name = input("Nom du projet : ")
            desc = input("Description : ")
            print(agent.add_project(name, desc))

        elif cmd == "tâche":
            proj = input("Projet : ")
            name = input("Nom de la tâche : ")
            print(agent.add_task(proj, name))

        elif cmd == "avancé":
            proj = input("Projet : ")
            name = input("Nom de la tâche : ")
            deadline = input("Deadline (AAAA-MM-JJ ou vide) : ") or None
            estimate = input("Estimation (ex: 2h ou 5pts) : ") or None
            print(agent.add_task(proj, name, deadline, estimate))

        elif cmd == "voir":
            proj = input("Projet : ")
            print(agent.show_status(proj))

        elif cmd == "fini":
            proj = input("Projet : ")
            name = input("Nom de la tâche terminée : ")
            print(agent.complete_task(proj, name))

        elif cmd == "parle":
            phrase = input("🗣️ Que veux-tu dire à AgentPyDev ?\n> ")
            print(agent.interpret(phrase))

        elif cmd == "supprimer":
            proj = input("Projet : ")
            name = input("Nom de la tâche à supprimer : ")
            print(agent.delete_task(proj, name))

        elif cmd in {"quit", "exit"}:
            print("👋 À bientôt, développeur !")
            break
        else:
            print("Commande inconnue.")

if __name__ == "__main__":
    main()
