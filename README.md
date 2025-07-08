# 🤖 TeleFeed Bot – Version Professionnelle

TeleFeed est un bot Telegram professionnel qui permet :

- 🔐 Connexion sécurisée via numéro
- 🔁 Redirection automatique de messages entre chats
- 💳 Paiement avec validation de licence
- 🔑 Gestion d’abonnement (1 semaine / 1 mois)
- 📁 Hébergement facile sur Render ou Replit

## ⚙️ Commandes principales

- /connect → Connecte ton compte Telegram avec code aa12345
- /redirection → Configure une source et une destination pour rediriger les messages
- /payer → Demande un abonnement
- /valide → Valide ta licence
- /start → Menu d’accueil

## 📁 Fichiers importants

- bot_handlers.py : toutes les commandes
- user_manager.py : gestion des utilisateurs et licences
- telefeed_redirections.json : redirections enregistrées
- users.json : base des utilisateurs
- sessions/ : stockage des connexions actives
- render_deploy.py : relance les redirections à chaque démarrage

## 🚀 Déploiement Render

- Type : Background Worker
- Procfile : `worker: python3 render_deploy.py`
- Variables d’environnement : API_ID, API_HASH, BOT_TOKEN, ADMIN_ID
