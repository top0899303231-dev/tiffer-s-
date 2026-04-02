import requests
from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

# ดึงค่าจาก Environment Variables ใน Render
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

@app.route('/')
def home():
    # หน้าจอ Dashboard แบบสวยๆ ที่ช่างคุ้นเคย
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>TOP AI - CLOUD CONTROL</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <script src="https://cdn.tailwindcss.com"></script>
    </head>
    <body class="bg-slate-900 text-white flex items-center justify-center min-h-screen">
        <div class="p-8 bg-slate-800 rounded-3xl shadow-2xl border border-slate-700 w-full max-w-md text-center">
            <h1 class="text-2xl font-bold text-sky-400 mb-6">TOP AI SYSTEM ☁️</h1>
            <input id="msg" type="text" placeholder="พิมพ์ข้อความ..." class="w-full p-4 bg-slate-700 rounded-xl mb-4 outline-none border border-transparent focus:border-sky-500">
            <button onclick="send()" class="w-full bg-sky-500 hover:bg-sky-600 py-4 rounded-xl font-bold transition-all">PUSH TO LINE</button>
            <p id="status" class="mt-4 text-sm text-slate-400"></p>
        </div>
        <script>
            async function send() {
                const msg = document.getElementById('msg').value;
                if(!msg) return;
                const status = document.getElementById('status');
                status.innerText = "กำลังส่ง...";
                const res = await fetch('/api/push', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ message: msg })
                });
                const data = await res.json();
                status.innerText = data.status === 'success' ? "✅ ส่งสำเร็จ!" : "❌ ส่งไม่สำเร็จ!";
                document.getElementById('msg').value = "";
            }
        </script>
    </body>
    </html>
    """

@app.route('/api/push', methods=['POST'])
def api_push():
    content = request.json.get('message')
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    payload = {
        'to': USER_ID,
        'messages': [{'type': 'text', 'text': f"📢 แจ้งเตือนจาก Cloud:\n{content}"}]
    }
    res = requests.post(url, headers=headers, json=payload)
    return jsonify({"status": "success" if res.status_code == 200 else "error"})

if __name__ == '__main__':
    # 🔴 จุดตายที่ต้องแก้: Render จะสุ่ม Port ให้เรา เราต้องดึงค่าจากระบบมาใช้
    port = int(os.environ.get("PORT", 5000))
    # 🔴 ต้องใช้ host='0.0.0.0' เพื่อให้คนข้างนอกเข้าเว็บเราได้
    app.run(host='0.0.0.0', port=port)
