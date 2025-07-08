# 🚀 Guide de déploiement Render pour TeleFeed Bot

## ✅ Étapes à suivre

### 1. Prépare ton dépôt GitHub

- Place tous les fichiers du bot à la racine :
  - bot_handlers.py
  - user_manager.py
  - render_deploy.py
  - config.py
  - users.json
  - requirements_render.txt
  - Procfile
  - README.md

- N'oublie pas le dossier `sessions/` (vide) et `telefeed_redirections.json`

---

### 2. Crée un service sur Render.com

- Va sur [Render.com](https://render.com)
- Clique sur **New > Web Service** *(mais choisis Worker ensuite)*
- Connecte ton dépôt GitHub
- Nomme ton projet : `telefeed-bot` (ou ce que tu veux)

---

### 3. Paramètres Render

- Type de service : **Background Worker**
- Start Command :  
```
python3 render_deploy.py
```

- Ajouter les variables d’environnement :
  - `API_ID`
  - `API_HASH`
  - `BOT_TOKEN`
  - `ADMIN_ID`

---

### 4. Déploiement

- Clique sur **Create Web Service**
- Le bot va démarrer et logguer dans Render :
  ```
  🚀 Démarrage de toutes les redirections enregistrées...
  ```

---

### 📌 Conseils

- Ne pas utiliser de Web Service (sinon page blanche)
- Ajouter un webhook de redémarrage si tu modifies `users.json`
- Vérifie que tes sessions sont bien stockées dans `sessions/`

---

🎉 Ton bot est maintenant prêt à fonctionner avec Render.
