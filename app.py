import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ (ดึงค่าจาก Environment Variables) ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')

# --- 🔋 เชื่อมต่อ Google Sheets (ใช้เลข Entry จากฟอร์มช่าง) ---
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI ทริปเฟอร์ AI Pro (3-in-1: Login, Register, Dashboard) ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ทริปเฟอร์ AI - PRO SYSTEM 🔋</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #f0f7ff; }
        .glass { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); }
        .hidden-page { display: none; }
    </style>
</head>
<body class="min-h-screen">

    <div id="loginPage" class="flex items-center justify-center min-h-screen p-6">
        <div class="w-full max-w-md glass p-8 rounded-[2.5rem] shadow-2xl border border-blue-100">
            <div class="text-center mb-8">
                <div class="inline-block p-4 bg-blue-600 rounded-2xl shadow-lg mb-4">
                    <i class="fas fa-lock text-3xl text-white"></i>
                </div>
                <h2 id="formTitle" class="text-2xl font-bold text-slate-800 text-blue-700">เข้าสู่ระบบ ทริปเฟอร์ AI</h2>
            </div>
            
            <div class="space-y-4">
                <input type="text" id="authName" placeholder="ชื่อผู้ใช้งาน" class="w-full p-4 bg-blue-50 border border-blue-100 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all">
                <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full p-4 bg-blue-50 border border-blue-100 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 transition-all">
                
                <button onclick="handleAuth()" class="w-full bg-blue-600 text-white font-bold py-4 rounded-2xl shadow-lg hover:bg-blue-700 active:scale-95 transition-all">
                    ตกลง
                </button>
                <p class="text-center text-sm text-slate-500 mt-4 cursor-pointer hover:text-blue-600" onclick="toggleAuthMode()">
                    ยังไม่มีบัญชี? <span id="toggleText">ลงทะเบียนที่นี่</span>
                </p>
            </div>
        </div>
    </div>

    <div id="mainPage" class="hidden-page flex flex-col min-h-screen">
        <nav class="bg-white border-b border-blue-100 px-6 py-4 sticky top-0 z-10 shadow-sm">
            <div class="max-w-md mx-auto flex justify-between items-center">
                <span class="text-xl font-bold text-blue-700"><i class="fas fa-droplet mr-2"></i>ทริปเฟอร์ AI 🔋</span>
                <button onclick="logout()" class="text-red-500 text-sm font-bold"><i class="fas fa-sign-out-alt"></i></button>
            </div>
        </nav>

        <main class="p-6 flex flex-col items-center pt-8">
            <div class="w-full max-w-md bg-white rounded-[2rem] shadow-xl border border-blue-50 overflow-hidden">
                <div class="bg-gradient-to-r from-blue-600 to-sky-500 p-8 text-white text-center">
                    <h2 class="text-xl font-bold italic" id="welcomeMsg">สวัสดีครับช่าง!</h2>
                    <p class="text-xs opacity-80 mt-1 uppercase tracking-widest">Voice Control Active 🎙️</p>
                </div>
                
                <div class="p-8 space-y-6">
                    <div>
                        <label class="block text-[11px] font-bold text-blue-400 uppercase mb-2">รายละเอียดข้อความ</label>
                        <textarea id="message" placeholder="พิมพ์ข้อความ หรือ กดไมค์..." rows="4"
                                  class="w-full p-4 bg-blue-50 border border-blue-100 rounded-2xl outline-none focus:ring-2 focus:ring-blue-500 resize-none"></textarea>
                    </div>

                    <div class="flex space-x-3">
                        <button onclick="startVoice()" class="flex-1 bg-slate-100 text-slate-600 py-4 rounded-2xl hover:bg-slate-200 transition-all active:scale-95">
                            <i class="fas fa-microphone text-xl"></i>
                        </button>
                        <button onclick="sendData()" class="flex-[3] bg-blue-600 text-white font-bold py-4 rounded-2xl shadow-lg hover:bg-blue-700 transition-all active:scale-95">
                            <i class="fas fa-paper-plane mr-2"></i> บันทึกข้อมูล
                        </button>
                    </div>
                    <div id="status" class="hidden text-center p-3 rounded-xl text-sm font-medium border animate-pulse"></div>
                </div>
            </div>
        </main>
    </div>

    <script>
        let isRegister = false;
        let currentUser = "";

        // 🗣️ ระบบพูด (Speech Synthesis)
        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'th-TH';
            synth.speak(utter);
        }

        // 🎙️ ระบบฟังเสียง (Speech Recognition)
        function startVoice() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'th-TH';
            speak("กำลังฟังครับช่าง...");
            recognition.start();
            recognition.onresult = (event) => {
                document.getElementById('message').value = event.results[0][0].transcript;
                speak("รับทราบครับ");
            };
        }

        function toggleAuthMode() {
            isRegister = !isRegister;
            document.getElementById('formTitle').innerText = isRegister ? "ลงทะเบียน ทริปเฟอร์ AI" : "เข้าสู่ระบบ ทริปเฟอร์ AI";
            document.getElementById('toggleText').innerText = isRegister ? "กลับไปหน้า Login" : "ลงทะเบียนที่นี่";
        }

        function handleAuth() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            if(!user || !pass) { alert("กรอกข้อมูลให้ครบครับ"); return; }
            
            // ระบบง่ายๆ (สามารถเปลี่ยนเป็นเช็ค DB จริงได้)
            currentUser = user;
            document.getElementById('loginPage').classList.add('hidden-page');
            document.getElementById('mainPage').classList.remove('hidden-page');
            document.getElementById('welcomeMsg').innerText = "สวัสดีครับ " + currentUser;
            speak("ยินดีต้อนรับเข้าสู่ระบบ ทริปเฟอร์ AI ครับคุณ " + currentUser);
        }

        async function sendData() {
            const msg = document.getElementById('message').value;
            const status = document.getElementById('status');
            if(!msg) return;

            status.innerText = "กำลังบันทึก...";
            status.classList.remove('hidden');

            try {
                const res = await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: currentUser, message: msg })
                });
                const data = await res.json();
                if(data.status === 'success') {
                    status.innerText = "🔋 บันทึกถาวรเรียบร้อย!";
                    speak("บันทึกข้อมูลเรียบร้อยแล้วครับ");
                    document.getElementById('message').value = "";
                }
            } catch (e) {
                status.innerText = "เกิดข้อผิดพลาด!";
            }
        }

        function logout() { location.reload(); }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    name = data.get('username')
    message = data.get('message')
    time_now = datetime.now().strftime("%H:%M")

    if name and message:
        try:
            # 1. บันทึกลง Google Sheets (Backup)
            payload = {"entry.1691238515": name, "entry.540166297": message}
            requests.post(FORM_URL, data=payload)

            # 2. แจ้งเตือน LINE
            if LINE_ACCESS_TOKEN and USER_ID:
                text = f"🔋 [ทริปเฟอร์ AI]\n👤 ผู้ใช้งาน: {name}\n💬: {message}\n⏰: {time_now}"
                requests.post('https://api.line.me/v2/bot/message/push', 
                             headers={'Authorization': f'Bearer {LINE_ACCESS_TOKEN}', 'Content-Type': 'application/json'},
                             json={'to': USER_ID, 'messages': [{'type': 'text', 'text': text}]})

            return jsonify({"status": "success", "message": "Done"})
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
    return jsonify({"status": "error", "message": "No data"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
