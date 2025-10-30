from core.agent import ProjectAgent

def main():
    agent = ProjectAgent()
    print("🤖 AgentPyDev — version 1.1 (Gestion avancée des tâches)")
    print("Je suis là pour t'aider a organiser tes projets de dev ")
    print("🗣️ Mode Parle automatique activé ! Tape 'quit' pour quitter.")

    while True:
        # 🔹 Entrée directe du texte à l'agent
        phrase = input("\n> ").strip()
        if phrase.lower() in {"quit", "exit"}:
            print("👋 À bientôt, développeur !")
            break

        # 🔹 Interprète automatiquement toutes les phrases
        print(agent.interpret(phrase))

if __name__ == "__main__":
    main()