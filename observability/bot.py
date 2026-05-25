import os
import logging
from flask import Flask, request, jsonify
import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")


def send_telegram(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        logger.warning("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        logger.info("Telegram response: %s %s", resp.status_code, resp.text)
    except Exception as e:
        logger.error("Failed to send Telegram message: %s", e)


@app.route("/alert", methods=["POST"])
def alert_webhook():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "no payload"}), 400

    alerts = data.get("alerts", [])
    for alert in alerts:
        status = alert.get("status", "firing")
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})

        emoji = "🔴" if status == "firing" else "✅"
        title = annotations.get("summary", "Unknown")
        desc = annotations.get("description", "")
        severity = labels.get("severity", "info")

        message = (
            f"{emoji} <b>{title}</b>\n"
            f"Status: {status}\n"
            f"Severity: {severity}\n"
            f"{desc}"
        )
        send_telegram(message)

    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
