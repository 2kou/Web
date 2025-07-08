from telethon import TelegramClient, events, sync
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError
import os, json, random, string, datetime

from config import API_ID, API_HASH, BOT_TOKEN, ADMIN_ID
from user_manager import save_user, generate_license, validate_license, is_authorized

bot = TelegramClient("bot_session", API_ID, API_HASH).start(bot_token=BOT_TOKEN)
sessions_path = "sessions"
os.makedirs(sessions_path, exist_ok=True)

clients = {}  # stocke les sessions utilisateurs connectées

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.respond("👋 Bienvenue sur TeleFeed.
Commandes disponibles : /connect, /redirection, /payer, /valide")

@bot.on(events.NewMessage(pattern="/connect"))
async def connect(event):
    user_id = str(event.sender_id)
    await event.respond("📱 Envoie ton numéro de téléphone (format international ex: +22900000000) :")
    response = await bot.wait_for(events.NewMessage(from_users=event.sender_id))
    phone = response.text.strip()
    session_file = os.path.join(sessions_path, f"{user_id}.session")

    client = TelegramClient(session_file, API_ID, API_HASH)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone)
        await event.respond("✉️ Code envoyé. Envoie-le avec `aa` devant. Ex: aa12345")
        code_msg = await bot.wait_for(events.NewMessage(from_users=event.sender_id))
        code = code_msg.text.replace("aa", "")
        try:
            await client.sign_in(phone, code)
        except SessionPasswordNeededError:
            await event.respond("🔐 Envoie ton mot de passe Telegram :")
            pwd = await bot.wait_for(events.NewMessage(from_users=event.sender_id))
            await client.sign_in(password=pwd.text.strip())

    clients[user_id] = client
    await event.respond("✅ Connexion réussie. Tu peux maintenant utiliser /redirection")

@bot.on(events.NewMessage(pattern="/redirection"))
async def redirection(event):
    user_id = str(event.sender_id)
    if not is_authorized(user_id):
        return await event.respond("⛔ Tu n'es pas autorisé. Utilise /payer et /valide d'abord.")

    if user_id not in clients:
        return await event.respond("❗ Connecte ton compte avec /connect d'abord.")

    await event.respond("📤 ID du chat source :")
    src_msg = await bot.wait_for(events.NewMessage(from_users=event.sender_id))
    src_id = int(src_msg.text.strip())

    await event.respond("📥 ID du chat destination :")
    dst_msg = await bot.wait_for(events.NewMessage(from_users=event.sender_id))
    dst_id = int(dst_msg.text.strip())

    if not os.path.exists("telefeed_redirections.json"):
        with open("telefeed_redirections.json", "w") as f:
            json.dump([], f)

    with open("telefeed_redirections.json", "r") as f:
        redirects = json.load(f)

    redirects.append({"user_id": user_id, "source": src_id, "dest": dst_id})
    with open("telefeed_redirections.json", "w") as f:
        json.dump(redirects, f)

    @clients[user_id].on(events.NewMessage(chats=src_id))
    async def forwarder(ev):
        await clients[user_id].forward_messages(dst_id, ev.message)

    await event.respond("🔁 Redirection activée.")

@bot.on(events.NewMessage(pattern="/payer"))
async def payer(event):
    user_id = str(event.sender_id)
    await event.respond("💳 Choisis un plan :
1️⃣ 1 semaine (1000F)
2️⃣ 1 mois (3000F)")

    response = await bot.wait_for(events.NewMessage(from_users=event.sender_id))
    choice = response.text.strip()
    plan = "week" if choice == "1" else "month"
    msg = f"📬 Demande de paiement
ID: {user_id}
Plan: {plan}"
    await bot.send_message(ADMIN_ID, msg)
    await event.respond("⏳ Demande envoyée à l’admin. Attends la licence.")

@bot.on(events.NewMessage(pattern="/valide"))
async def valide(event):
    user_id = str(event.sender_id)
    await event.respond("🔑 Envoie ta licence :")
    response = await bot.wait_for(events.NewMessage(from_users=event.sender_id))
    licence = response.text.strip()

    valid = validate_license(user_id, licence)
    if valid:
        save_user(user_id, licence)
        await event.respond("✅ Licence activée. Accès débloqué.")
    else:
        await event.respond("❌ Licence invalide ou volée.")

def start_bot_sync():
    print("🤖 Bot TeleFeed lancé.")
    bot.run_until_disconnected()
