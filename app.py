import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN PURPLE - ANDROID & PWA SUPPORT ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="theme-color" content="#0c001a"> <title>ทริปเฟอร์ AI - MOBILE 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { 
            font-family: 'Kanit', sans-serif; 
            background: #0c001a; 
            color: white; 
            overflow-x: hidden;
            -webkit-tap-highlight-color: transparent; /* ลบสีฟ้าเวลาแตะบน Android */
        }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; }
        .glass-purple { background: rgba(30, 0, 60, 0.75); backdrop-filter: blur(15px); border: 1px solid rgba(191, 64, 191, 0.4); }
        .hidden-page { display: none; }
        .tv-screen { background: #000; border: 3px solid #7c3aed; position: relative; overflow: hidden; box-shadow: 0 0 15px #7c3aed; }
        .scanline { width: 100%; height: 100%; background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%); background-size: 100% 2px; pointer-events: none; position: absolute; animation: move 10s linear infinite; }
        @keyframes move { from { background-position: 0 0; } to { background-position: 0 100%; } }
    </style>
</head>
<body>

    <div id="loginPage" class="flex items-center justify-center min-h-screen p-6">
        <div class="w-full max-w-md glass-purple p-8 rounded-[2.5rem] shadow-2xl border-t-2 border-purple-500">
            <div class="text-center mb-8">
                <div class="w-24 h-20 tv-screen rounded-xl mx-auto mb-4 flex items-center justify-center">
                    <div class="scanline"></div>
                    <i class="fas fa-satellite-dish text-purple-400 text-3xl animate-pulse"></i>
                </div>
                <h1 class="text-3xl font-bold purple-neon tracking-tighter">ทริปเฟอร์ AI</h1>
                <p class="text-purple-400 text-[10px] uppercase tracking-[0.3em] mt-2">Android Workspace V.1</p>
            </div>
            
            <div class="space-y-4">
                <input type="text" id="authName" placeholder="ชื่อช่าง" class="w-full p-4 bg-black/50 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white">
                <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full p-4 bg-black/50 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white">
                <button onclick="handleLogin()" class="w-full bg-purple-600 hover:bg-purple-500 py-5 rounded-2xl font-bold shadow-lg active:scale-95 transition-all uppercase">เปิดหน้างาน 📺</button>
            </div>
        </div>
    </div>

    <div id="mainPage" class="hidden-page flex flex-col min-h-screen">
        <nav class="p-5 flex justify-between items-center glass-purple sticky top-0 z-50">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-8 tv-screen rounded flex items-center justify-center"><i class="fas fa-bolt text-purple-500 text-xs"></i></div>
                <span class="font-bold purple-neon tracking-wider">WORKSPACE</span>
            </div>
            <button onclick="logout()" class="p-2 text-red-400"><i class="fas fa-power-off"></i></button>
        </nav>

        <main class="p-6 space-y-6 max-w-md mx-auto w-full">
            <div class="glass-purple p-8 rounded-[2.5rem] text-center border-b-4 border-purple-500 shadow-2xl">
                <div class="w-20 h-20 rounded-full bg-purple-900 mx-auto mb-4 border-4 border-purple-500 flex items-center justify-center text-3xl font-bold" id="userInitial">?</div>
                <h2 class="text-2xl font-bold" id="welcomeMsg">สวัสดี ช่าง</h2>
                <p class="text-[10px] text-purple-400 mt-2 font-bold uppercase tracking-widest">ยินดีต้อนรับกลับเข้าสู่ระบบ</p>
            </div>

            <div class="glass-purple p-6 rounded-[2.5rem] space-y-4">
                <textarea id="message" placeholder="พิมพ์รายงานหน้างาน..." rows="4" class="w-full p-5 bg-black/40 border border-purple-900 rounded-2xl outline-none focus:border-purple-500 text-white resize-none"></textarea>
                
                <div class="grid grid-cols-4 gap-2">
                    <button onclick="startVoice()" class="col-span-1 bg-purple-900/50 border border-purple-500 rounded-2xl text-purple-300 py-4">
                        <i class="fas fa-microphone text-xl"></i>
                    </button>
                    <button onclick="sendData()" class="col-span-3 bg-purple-600 py-4 rounded-2xl font-bold uppercase tracking-widest active:scale-95 transition-all">บันทึก 🔋</button>
                </div>
                <div id="status" class="hidden text-center p-3 rounded-xl text-[10px] font-bold border border-purple-500 bg-purple-950/80"></div>
            </div>
        </main>
    </div>

    <script>
        let currentUser = "";

        // 🧠 ระบบเช็คสถานะ Android (เด้งเข้าหน้าอัตโนมัติ)
        document.addEventListener('DOMContentLoaded', () => {
            const savedUser = localStorage.getItem('tripfer_user');
            if (savedUser) {
                showDashboard(savedUser);
                // ไม่ต้องพูดซ้ำทุกครั้งที่เปิดบน Android จะได้ไม่น่ารำคาญ
            }
        });

        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'th-TH';
            synth.speak(utter);
        }

        function handleLogin() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            if(!user || !pass) return;
            
            localStorage.setItem('tripfer_user', user);
            showDashboard(user);
            speak("เข้างานแล้ว " + user);
        }

        function showDashboard(user) {
            currentUser = user;
            document.getElementById('loginPage').classList.add('hidden-page');
            document.getElementById('mainPage').classList.remove('hidden-page');
            document.getElementById('welcomeMsg').innerText = "สวัสดี " + user;
            document.getElementById('userInitial').innerText = user.charAt(0).toUpperCase();
        }

        function startVoice() {
            const recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
            recognition.lang = 'th-TH';
            speak("ว่ามา");
            recognition.start();
            recognition.onresult = (e) => {
                document.getElementById('message').value = e.results[0][0].transcript;
                speak("รับทราบ");
            };
        }

        async function sendData() {
            const msg = document.getElementById('message').value;
            const status = document.getElementById('status');
            if(!msg) return;

            status.innerText = "กำลังส่งข้อมูล...";
            status.classList.remove('hidden');

            try {
                const res = await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: currentUser, message: msg })
                });
                if(res.ok) {
                    status.innerText = "บันทึกเรียบร้อย! 🔋";
                    speak("เรียบร้อย");
                    document.getElementById('message').value = "";
                }
            } catch (e) {
                status.innerText = "ข้อผิดพลาด!";
            }
        }

        function logout() {
            localStorage.removeItem('tripfer_user');
            location.reload();
        }
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
    name, message = data.get('username'), data.get('message')
    if name and message:
        try:
            requests.post(FORM_URL, data={"entry.1691238515": name, "entry.540166297": message})
            if LINE_ACCESS_TOKEN and USER_ID:
                text = f"🟣 [ทริปเฟอร์ AI]\n👤 ช่าง: {name}\n💬: {message}\n⏰: {datetime.now().strftime('%H:%M')}"
                requests.post('https://api.line.me/v2/bot/message/push', headers={'Authorization': f'Bearer {LINE_ACCESS_TOKEN}', 'Content-Type': 'application/json'}, json={'to': USER_ID, 'messages': [{'type': 'text', 'text': text}]})
            return jsonify({"status": "success"})
        except: pass
    return jsonify({"status": "error"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
