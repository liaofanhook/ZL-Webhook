from flask import Flask, request, jsonify
from notion_client import Client
import os
from datetime import datetime

app = Flask(__name__)

# 初始化 Notion 客户端
notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

@app.route('/')
def index():
    return "ZL Webhook Handler Ready"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()

    # 字段映射（字段名请严格匹配 Notion 中的列名）
    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Client Name": {"title": [{"text": {"content": data.get("client_name", "")}}]},
                "Birthday": {"date": {"start": data.get("birthday", None)}},
                "Nationality": {"rich_text": [{"text": {"content": data.get("nationality", "")}}]},
                "Phone": {"rich_text": [{"text": {"content": data.get("phone", "")}}]},
                "Quotation Time": {"date": {"start": data.get("quotation_time", datetime.utcnow().isoformat())}},
                "Quotation Round": {"number": data.get("quotation_round", 1)},
                "Quote Detail": {"rich_text": [{"text": {"content": data.get("quote_detail", "")}}]},
                "Benefits": {"rich_text": [{"text": {"content": data.get("benefits", "")}}]},
                "Exchange Rate": {"number": data.get("exchange_rate", 0)},
            }
        )
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500