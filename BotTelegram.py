import os
import asyncio
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram import Update
from PIL import Image
from rembg import remove

TOKEN = "8073022902:AAFhPyqMQFXc_JoNsS9a8PECNRk2aM8UIuc" 

# Créer les dossiers nécessaires
os.makedirs("./temp", exist_ok=True)
os.makedirs("./processed", exist_ok=True)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envoie un message d'aide"""
    help_text = """
🤖 *Background Removal Bot* 🤖

Envoyez-moi une photo et je supprimerai l'arrière-plan pour vous!

Commandes disponibles:
/start - Démarrer le bot
/help - Afficher ce message
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Démarre l'interaction avec le bot"""
    welcome_text = """
✨ *Bienvenue!* ✨

Envoyez-moi une image et je supprimerai son arrière-plan pour vous.

Pour plus d'infos, tapez /help
"""
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def process_image(photo_name: str):
    """Traite l'image pour supprimer l'arrière-plan"""
    try:
        name, _ = os.path.splitext(photo_name)
        output_name = f"./processed/{name}.png"
        
        with Image.open(f"./temp/{photo_name}") as input_img:
            output = remove(input_img)
            output.save(output_name)
        
        os.remove(f"./temp/{photo_name}")
        return output_name
    except Exception as e:
        print(f"Erreur lors du traitement: {e}")
        raise

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages entrants avec des images"""
    try:
        # Vérifier si c'est une photo ou un document image
        if update.message.photo:
            file_id = update.message.photo[-1].file_id
            unique_file_id = update.message.photo[-1].file_unique_id
            photo_name = f"{unique_file_id}.jpg"
        elif update.message.document and update.message.document.mime_type.startswith('image/'):
            file_id = update.message.document.file_id
            unique_file_id = update.message.document.file_unique_id
            ext = os.path.splitext(update.message.document.file_name)[1]
            photo_name = f"{unique_file_id}{ext or '.jpg'}"
        else:
            await update.message.reply_text("Veuillez envoyer une image valide.")
            return

        # Télécharger l'image
        photo_file = await context.bot.get_file(file_id)
        temp_path = f"./temp/{photo_name}"
        await photo_file.download_to_drive(custom_path=temp_path)
        
        # Traitement
        await update.message.reply_text("🔄 Traitement de l'image...")
        processed_image = await process_image(photo_name)
        
        # Envoyer le résultat
        with open(processed_image, 'rb') as photo:
            await update.message.reply_photo(photo=photo, caption="Voici votre image sans arrière-plan!")
        
        # Nettoyage
        os.remove(processed_image)
        
    except Exception as e:
        print(f"Erreur: {e}")
        await update.message.reply_text("❌ Une erreur s'est produite lors du traitement. Veuillez réessayer.")

def main():
    """Configure et lance le bot"""
    application = ApplicationBuilder().token(TOKEN).build()

    # Gestionnaires de commandes
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Gestionnaire de messages
    application.add_handler(MessageHandler(
        filters.PHOTO | (filters.Document.IMAGE & ~filters.COMMAND), 
        handle_message
    ))

    print("🤖 Bot en écoute...")
    application.run_polling()

if __name__ == "__main__":
    main()