import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ส่วนตั้งค่าระบบ (ดึงค่าจาก Environment Variables ใน Render) ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

# --- 🔋 ส่วนเชื่อมต่อ "แบตสำรองข้อมูล" (Google Form ของช่าง TOP) ---
# ใช้รหัส ID จากลิงก์ที่ช่างส่งมาเพื่อยิงข้อมูลเข้า Google Sheets ถาวร
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI หน้าตาเว็บไซต์ฉบับ "หยดน้ำสำรองข้อมูล" (V.4.0) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOP AI V.4.0 - BACKUP SYSTEM 🔋</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
        body { font-family: 'Kanit', sans-serif; }
        .bg-glass { background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); }
    </style>
</head>
<body class="bg-blue-50 min-h-screen flex flex-col">

    <nav class="bg-white border-b border-blue-100 px-6 py-4 sticky top-0 z-10 shadow-sm">
        <div class="max-w-md mx-auto flex justify-between items-center">
            <span class="text-xl font-bold text-blue-600"><i class="fas fa-droplet mr-2"></i>TOP AI V.4.0</span>
            <div class="flex items-center space-x-2">
                <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
                <span class="text-[10px] text-slate-400 font-bold uppercase tracking-widest text-blue-500">Backup Active 🔋</span>
            </div>
        </div>
    </nav>

    <main class="flex-grow p-6 flex flex-col items-center justify-start pt-8">
        <div class="w-full max-w-md bg-white rounded-[2rem] shadow-2xl border border-blue-50 overflow-hidden">
            <div class="bg-gradient-to-br from-sky-500 to-blue-600 p-8 text-white text-center">
                <div class="inline-block p-3 bg-white/20 rounded-2xl mb-3">
                    <i class="fas fa-battery-full text-3xl"></i>
                </div>
                <h2 class="text-2xl font-bold">บันทึกข้อมูลถาวร</h2>
                <p class="text-sky-100 text-xs opacity-90 italic">เชื่อมต่อ Google Sheets & LINE Notify 🔋💧</p>
            </div>
            
            <div class="p-8 space-y-6">
                <div>
                    <label class="block text-[11px] font-bold text-blue-400 uppercase mb-2 ml-1 tracking-wider">ชื่อผู้ใช้งาน / เพื่อนช่าง</label>
                    <div class="relative">
                        <i class="fas fa-user absolute left-4 top-3.5 text-sky-300"></i>
                        <input type="text" id="username" placeholder="ใส่ชื่อของคุณ" 
                               class="w-full pl-11 pr-4 py-3.5 bg-blue-50/50 border border-blue-100 rounded-2xl focus:ring-2 focus:ring-sky-400 focus:bg-white outline-none transition-all placeholder:text-sky-200 text-slate-700">
                    </div>
                </div>

                <div>
                    <label class="block text-[11px] font-bold text-blue-400 uppercase mb-2 ml-1 tracking-wider">รายละเอียดข้อความ</label>
                    <textarea id="message" placeholder="พิมพ์ข้อความที่นี่..." rows="4"
                              class="w-full p-4 bg-blue-50/50 border border-blue-100 rounded-2xl focus:ring-2 focus:ring-sky-400 focus:bg-white outline-none transition-all resize-none placeholder:text-sky-200 text-slate-700"></textarea>
                </div>

                <button onclick="sendData()" id="sendBtn"
                        class="w-full bg-blue-600 text-white font-bold py-4 rounded-2xl hover:bg-blue-700 shadow-xl shadow-blue-100 transition-all flex items-center justify-center space-x-2 active:scale-95 group">
                    <i class="fas fa-cloud-upload-alt group-hover:animate-bounce"></i>
                    <span>ส่งข้อมูลเข้า Cloud Backup</span>
                </button>

                <div id="responseMsg" class="hidden text-center p-4 rounded-2xl text-sm font-medium border animate-pulse"></div>
            </div>
        </div>

        <p class="mt-8 text-blue-300 text-[10px] font-bold uppercase tracking-[0.2em]">
            Developed by ช่าง TOP | 2026 🔋💧
        </p>
    </main>

    <script>
        async function sendData() {
            const name = document.getElementById('username').value;
            const msg = document.getElementById('message').value;
            const resBox = document.getElementById('responseMsg');
            const btn = document.getElementById('sendBtn');

            if(!name || !msg) {
                alert('ช่างครับ กรุณากรอกให้ครบนะ! 💧');
                return;
            }

            // State: Loading
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner animate-spin"></i> <span>กำลังสำรองข้อมูล...</span>';
            resBox.classList.add('hidden');

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: name, message: msg })
                });
                const result = await response.json();
                
                resBox.innerText = result.message;
                resBox.classList.remove('hidden', 'bg-red-50', 'border-red-100', 'text-red-600', 'bg-green-50', 'border-green-100', 'text-green-600');
                resBox.classList.add('block');
                
                if (result.status === 'success') {
                    resBox.classList.add('bg-green-50', 'border-green-100', 'text-green-600');
                    document.getElementById('username').value = "";
                    document.getElementById('message').value = "";
                } else {
                    resBox.classList.add('bg-red-50', 'border-red-100', 'text-red-600');
                }
            } catch (error) {
                resBox.innerText = "เชื่อมต่อ Server ไม่ได้! ❌";
                resBox.classList.remove('hidden');
                resBox.classList.add('bg-red-50', 'border-red-100', 'text-red-600');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-cloud-upload-alt"></i> <span>ส่งข้อมูลเข้า Cloud Backup</span>';
            }
        }
    </script>
</body>
</html>
'''

# --- 🧠 ส่วนการประมวลผลหลังบ้าน (Backend) ---

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
        try:
            # 🔋 1. แบตสำรองข้อมูล: ยิงเข้า Google Form (เข้า Google Sheets อัตโนมัติ)
            # ใช้รหัส entry.xxxx จากฟอร์มของช่างที่ตรวจสอบแล้ว
            payload = {
                "entry.1691238515": name,
                "entry.540166297": message
            }
            requests.post(FORM_URL, data=payload)

            # 💬 2. การแจ้งเตือน: ส่งเข้า LINE Push Message
            if LINE_ACCESS_TOKEN and USER_ID:
                line_text = f"🔋 V.4.0 Backup Success!\n👤 จากคุณ: {name}\n💬: {message}\n⏰: {time_now}"
                url = 'https://api.line.me/v2/bot/message/push'
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
                }
                line_payload = {
                    'to': USER_ID,
                    'messages': [{'type': 'text', 'text': line_text}]
                }
                requests.post(url, headers=headers, json=line_payload)

            return jsonify({"status": "success", "message": "🔋 สำรองข้อมูลถาวรเรียบร้อย!"})
        except Exception as e:
            return jsonify({"status": "error", "message": f"พังครับช่าง: {str(e)}"})

    return jsonify({"status": "error", "message": "⚠️ กรอกข้อมูลไม่ครบ!"})

if __name__ == '__main__':
    # รันพอร์ตตามที่ Render กำหนด
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
