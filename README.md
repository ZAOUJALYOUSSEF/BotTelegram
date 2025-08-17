# 🤖 Telegram Background Removal Bot


Un bot Telegram intelligent pour supprimer les arrière-plans des images automatiquement.

## ✨ Fonctionnalités

- 🖼️ Suppression automatique des arrière-plans
- 📤 Prise en charge des photos et fichiers image
- 💬 Interface claire avec messages en temps réel
- 🧹 Nettoyage automatique des fichiers temporaires
- ⚡ Traitement rapide des images

## 🚀 Démarrage Rapide

```
# Cloner le dépôt
git clone https://github.com/votre-utilisateur/telegram-bg-remover.git
cd telegram-bg-remover

# Installer les dépendances
pip install -r requirements.txt

# Configurer le token Telegram
cp .env.example .env
nano .env  # Ajouter votre token

# Lancer le bot
python BotTelegram.py
```
⚙️ Configuration
Fichier .env
```
TOKEN=votre_token_telegram_ici
```
Structure des fichiers
```
telegram-bg-remover/
├── BotTelegram.py                # Code principal
├── requirements.txt      # Dépendances
├── .env.example          # Configuration
└── README.md
```
📦 Dépendances
requirements.txt :

```
python-telegram-bot==20.0
pillow==10.0.0
rembg==2.0.38
python-dotenv==1.0.0
```
💡 Utilisation
Démarrer le bot avec /start

Envoyer une image (photo ou fichier)

Recevoir la version sans arrière-plan

Commandes disponibles :

```/start``` - Démarrer le bot

```/help``` - Afficher l'aide

⚠️ Dépannage
Si rembg pose problème :

```
# Solution 1 : Versions spécifiques
pip install numba==0.56.4 llvmlite==0.39.1

# Solution 2 : Utiliser Docker
docker pull danielgatis/rembg
```
