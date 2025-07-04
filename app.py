from flask import Flask, request, jsonify, send_from_directory, Response
import openai
import os

app = Flask(__name__)

# Chargement de la clé OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("La variable d'environnement OPENAI_API_KEY est manquante.")

# Route de test simple (HTML + OpenGraph)
@app.route("/", methods=["GET"])
def home():
    html = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <title>Bot Facebook GPT</title>
        <meta property="og:title" content="Bot Facebook Commentaire GPT" />
        <meta property="og:description" content="Réponses automatiques avec GPT sur Facebook" />
        <meta property="og:image" content="https://TON-URL.onrender.com/static/og-image.jpg" />
        <meta property="og:url" content="https://TON-URL.onrender.com/" />
    </head>
    <body>
        <h1>🤖 Bot Facebook Commentaire GPT</h1>
        <p>Ce bot est actif et prêt à répondre.</p>
    </body>
    </html>
    """
    return Response(html, mimetype='text/html')

# Endpoint de santé pour Render
@app.route("/healthz", methods=["GET"])
def health_check():
    return "OK", 200

# Politique de confidentialité
@app.route("/privacy", methods=["GET"])
def privacy_policy():
    return send_from_directory(directory=".", path="privacy.html")

# Webhook principal
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Invalid data"}), 400

    user_message = data["message"]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui réponds brièvement aux commentaires Facebook."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=60
        )
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancement de l'application Flask
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
