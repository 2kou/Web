from telethon import TelegramClient, events
import json
import os
from config import API_ID, API_HASH
from user_manager import is_authorized

sessions_path = "sessions"
redirects_file = "telefeed_redirections.json"
clients = {}

def restore_redirections():
    if not os.path.exists(redirects_file):
        return []

    with open(redirects_file, "r") as f:
        return json.load(f)

def start_all_clients():
    redirections = restore_redirections()
    for redir in redirections:
        user_id = redir["user_id"]
        src = redir["source"]
        dst = redir["dest"]
        session_file = os.path.join(sessions_path, f"{user_id}.session")

        if not os.path.exists(session_file):
            print(f"⚠️ Pas de session pour l'utilisateur {user_id}")
            continue

        client = TelegramClient(session_file, API_ID, API_HASH)
        client.start()
        clients[user_id] = client

        if not is_authorized(user_id):
            print(f"⛔ L'utilisateur {user_id} n'est pas autorisé.")
            continue

        @client.on(events.NewMessage(chats=src))
        async def forward(ev):
            await client.forward_messages(dst, ev.message)

        print(f"🔁 Redirection restaurée pour {user_id} : {src} ➤ {dst}")

    for client in clients.values():
        client.run_until_disconnected()

if __name__ == "__main__":
    print("🚀 Démarrage de toutes les redirections enregistrées...")
    start_all_clients()
