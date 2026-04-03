import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# ดึงรหัสจากระบบความปลอดภัยของ Render
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

# --- หน้าตาเว็บไซต์สุดเท่จาก V.2.5 ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Control Center - ช่าง TOP Cloud</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; scroll-behavior: smooth; }
        .glass { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="bg-gradient-to-br from-slate-100 to-indigo-50 text-slate-800 min-h-screen">

    <nav class="fixed w-full z-50 glass border-b border-slate-200">
        <div class="max-w-7xl mx-auto px-6 h-16 flex justify-between items-center">
            <span class="text-2xl font-bold text-indigo-600"><i class="fas fa-robot mr-2"></i>TOP AI CLOUD</span>
            <div class="space-x-4">
                <span class="text-sm text-slate-500">Status: <span class="text-green-500 font-bold">Online 24/7</span></span>
            </div>
        </div>
    </nav>

    <header class="pt-32 pb-10 px-6">
        <div class="max-w-5xl mx-auto text-center">
            <h1 class="text-4xl md:text-6xl font-bold mb-6 text-slate-900">
                ระบบจัดการข้อมูล <br><span class="text-indigo-600 italic underline">Cloud Server</span>
            </h1>
            <p class="text-lg text-slate-600 mb-10 max-w-2xl mx-auto">
                พิมพ์ข้อความทิ้งไว้ ข้อมูลจะถูกเซฟลง Database และส่งแจ้งเตือนเข้า LINE ช่าง TOP ทันที!
            </p>

            <div class="bg-white p-8 rounded-3xl shadow-2xl border border-slate-100 max-w-xl mx-auto">
                <h3 class="text-2xl font-bold mb-6 flex items-center justify-center">
                    <i class="fas fa-paper-plane mr-3 text-indigo-500"></i> ส่งข้อมูลเข้าระบบ
                </h3>
                
                <div class="space-y-4 text-left">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">ชื่อผู้ส่ง</label>
                        <input type="text" id="username" placeholder="ใส่ชื่อของคุณ" 
                               class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none transition">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">ข้อความ</label>
                        <textarea id="message" placeholder="อยากบอกอะไรช่าง TOP..." rows="3"
                                  class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 outline-none transition"></textarea>
                    </div>
                    <button onclick="sendData()" 
                            class="w-full bg-indigo-600 text-white font-bold py-4 rounded-xl hover:bg-indigo-700 shadow-lg shadow-indigo-200 transition transform active:scale-95">
                        ส่งข้อมูลและแจ้งเตือน LINE
                    </button>
                </div>

                <div id="responseMsg" class="mt-4 hidden p-4 rounded-xl text-sm font-medium animate-pulse"></div>
            </div>
        </div>
    </header>

    <script>
        async function sendData() {
            const name = document.getElementById('username').value;
            const msg = document.getElementById('message').value;
            const resBox = document.getElementById('responseMsg');

            if(!name || !msg) {
                alert('กรอกให้ครบก่อนครับช่าง!');
                return;
            }

            resBox.innerText = "กำลังประมวลผล...";
            resBox.classList.remove('hidden', 'bg-red-100', 'text-red-700', 'bg-green-100', 'text-green-700');
            resBox.classList.add('block', 'bg-blue-100', 'text-blue-700');

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: name, message: msg })
                });
                const result = await response.json();
                
                resBox.innerText = result.message;
                resBox.classList.remove('bg-blue-100', 'text-blue-700');
                
                if (result.status === 'success') {
                    resBox.classList.add('bg-green-100', 'text-green-700');
                    document.getElementById('username').value = "";
                    document.getElementById('message').value = "";
                } else {
                    resBox.classList.add('bg-red-100', 'text-red-700');
                }
            } catch (error) {
                resBox.innerText = "เชื่อมต่อ Server ไม่ได้!";
                resBox.classList.add('bg-red-100', 'text-red-700');
            }
        }
    </script>
</body>
</html>
'''

# --- ส่วนของการประมวลผล (Backend) ---

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('username')
    message = data.get('message')
    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if name and message:
        # 1. บันทึกลงไฟล์ (Database ชั่วคราว)
        try:
            with open("database.txt", "a", encoding="utf-8") as f:
                f.write(f"[{time_now}] {name}: {message}\n")
            
            # 2. ส่งแจ้งเตือนเข้า LINE
            line_text = f"🌐 มีข้อมูลใหม่จากเว็บ!\n👤 จากคุณ: {name}\n💬 ข้อความ: {message}\n⏰ เวลา: {time_now}"
            url = 'https://api.line.me/v2/bot/message/push'
            headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'}
            payload = {'to': USER_ID, 'messages': [{'type': 'text', 'text': line_text}]}
            requests.post(url, headers=headers, json=payload)

            return jsonify({"status": "success", "message": "เซฟข้อมูลและแจ้งเตือน LINE เรียบร้อย!"})
        except Exception as e:
            return jsonify({"status": "error", "message": f"พังครับช่าง: {str(e)}"})

    return jsonify({"status": "error", "message": "กรอกข้อมูลไม่ครบนะช่าง!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
