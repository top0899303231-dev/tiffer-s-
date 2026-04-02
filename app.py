import requests
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# ดึงรหัสจากระบบความปลอดภัย (เดี๋ยวเราไปกรอกใน Render)
TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

@app.route('/')
def home():
    return "<h1>TOP AI SYSTEM ONLINE!</h1>"

@app.route('/send/<msg>')
def send_msg(msg):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {TOKEN}'}
    payload = {'to': USER_ID, 'messages': [{'type': 'text', 'text': f"📢 แจ้งเตือน: {msg}"}]}
    res = requests.post(url, headers=headers, json=payload)
    return f"ส่งข้อความ '{msg}' เรียบร้อย!" if res.status_code == 200 else "ส่งไม่สำเร็จ เช็ครหัส Token ครับ"

if __name__ == '__main__':
    app.run()
