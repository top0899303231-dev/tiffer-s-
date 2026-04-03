import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# ดึงรหัสจาก Environment Variables (ใส่ใน Render เหมือนเดิมนะครับ)
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

# --- UI V.2.0 แบบสีฟ้า 💧 (สะอาดตา เรียบง่าย) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOP AI V.2.0 - CLOUD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
        body { font-family: 'Kanit', sans-serif; }
    </style>
</head>
<body class="bg-blue-50 min-h-screen flex items-center justify-center p-6">

    <div class="w-full max-w-md bg-white rounded-3xl shadow-2xl border border-blue-100 overflow-hidden">
        <div class="bg-sky-500 p-8 text-white text-center">
            <div class="inline-block p-4 bg-white/20 rounded-full mb-4">
                <i class="fas fa-database text-3xl"></i>
            </div>
            <h1 class="text-2xl font-bold">TOP SERVER V.2.0</h1>
            <p class="text-sky-100 text-sm opacity-90">ระบบบันทึกข้อมูลลงฐานข้อมูล Cloud 💧</p>
        </div>

        <div class="p-8 space-y-6">
            <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">ชื่อผู้ลงทะเบียน</label>
                <input type="text" id="username" placeholder="กรุณาใส่ชื่อของคุณ" 
                       class="w-full px-4 py-3 rounded-xl border border-blue-100 bg-blue-50/30 focus:ring-2 focus:ring-sky-500 outline-none transition-all">
            </div>

            <div>
                <label class="block text-sm font-medium text-slate-600 mb-2">ข้อความที่ต้องการบันทึก</label>
                <textarea id="message" placeholder="พิมพ์ข้อความที่นี่..." rows="3"
                          class="w-full px-4 py-3 rounded-xl border border-blue-100 bg-blue-50/30 focus:ring-2 focus:ring-sky-500 outline-none transition-all"></textarea>
            </div>

            <button onclick="saveToV2()" id="btn"
                    class="w-full bg-sky-600 text-white font-bold py-4 rounded-xl hover:bg-blue-700 shadow-lg shadow-sky-200 transition-all active:scale-95 flex items-center justify-center space-x-2">
                <i class="fas fa-save"></i>
                <span>บันทึกลง V.2.0 DATABASE</span>
            </button>

            <div id="status" class="hidden text-center p-4 rounded-xl text-sm font-medium border"></div>
        </div>
        
        <div class="bg-slate-50 p-4 text-center border-t border-slate-100">
            <p class="text-slate-400 text-xs uppercase tracking-widest">Powered by ช่าง TOP 💧 2026</p>
        </div>
    </div>

    <script>
        async function saveToV2() {
            const user = document.getElementById('username').value;
            const msg = document.getElementById('message').value;
            const status = document.getElementById('status');
            const btn = document.getElementById('btn');

            if(!user || !msg) { alert('กรอกข้อมูลให้ครบก่อนครับช่าง!'); return; }

            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner animate-spin"></i> <span>กำลังบันทึก...</span>';

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: user, message: msg })
                });
                const result = await response.json();
                
                status.innerText = result.message;
                status.classList.remove('hidden', 'bg-green-50', 'text-green-600', 'bg-red-50', 'text-red-600');
                status.classList.add('block', result.status === 'success' ? 'bg-green-50' : 'bg-red-50');
                status.classList.add(result.status === 'success' ? 'text-green-600' : 'text-red-600');

                if(result.status === 'success') {
                    document.getElementById('username').value = "";
                    document.getElementById('message').value = "";
                }
            } catch (e) {
                status.innerText = "เชื่อมต่อ Server ไม่ได้!";
                status.classList.remove('hidden');
            } finally {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-save"></i> <span>บันทึกลง V.2.0 DATABASE</span>';
            }
        }
    </script>
</body>
</html>
'''

# --- ส่วนของ Backend (ระบบบันทึกไฟล์แบบ V.2.0) ---

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
        # จุดเด่นของ V.2.0: บันทึกลงไฟล์ database.txt
        try:
            with open("database.txt", "a", encoding="utf-8") as f:
                f.write(f"--- ข้อมูลใหม่ V.2.0 ---\n")
                f.write(f"เวลา: {time_now}\n")
                f.write(f"ชื่อ: {name}\n")
                f.write(f"ข้อความ: {message}\n")
                f.write("-" * 20 + "\n")
            
            # แถมระบบส่งแจ้งเตือน LINE ให้ด้วย (เพราะมันคือ V.2.0 บน Cloud!)
            if LINE_ACCESS_TOKEN and USER_ID:
                line_msg = f"💧 V.2.0 บันทึกข้อมูลใหม่!\n👤 ชื่อ: {name}\n💬: {message}"
                url = 'https://api.line.me/v2/bot/message/push'
                headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'}
                payload = {'to': USER_ID, 'messages': [{'type': 'text', 'text': line_msg}]}
                requests.post(url, headers=headers, json=payload)

            return jsonify({"status": "success", "message": f"สำเร็จ! บันทึกชื่อ {name} ลงไฟล์เรียบร้อย"})
        except Exception as e:
            return jsonify({"status": "error", "message": f"เกิดข้อผิดพลาด: {str(e)}"})

    return jsonify({"status": "error", "message": "กรอกข้อมูลไม่ครบครับช่าง!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
