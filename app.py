import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN ANDROID - SECURITY LOCK ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0c001a">
    <title>ทริปเฟ84 AI - SECURE 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #000; color: white; -webkit-tap-highlight-color: transparent; }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; }
        .glass-purple { background: rgba(20, 0, 40, 0.85); backdrop-filter: blur(20px); border: 1px solid #5b21b6; }
        .hidden-page { display: none; }
        .option-card { background: linear-gradient(145deg, #1e1b4b, #0c001a); border: 2px solid #5b21b6; transition: all 0.3s; }
        .option-card:active { transform: scale(0.95); }
    </style>
</head>
<body class="min-h-screen">

    <div id="loginPage" class="flex items-center justify-center min-h-screen p-6">
        <div class="w-full max-w-md glass-purple p-10 rounded-[2.5rem] shadow-2xl text-center border-t-4 border-purple-600">
            <div class="mb-8">
                <i class="fas fa-shield-halved text-purple-500 text-5xl mb-4 animate-pulse"></i>
                <h1 class="text-3xl font-bold purple-neon">ทริปเฟอร์ AI</h1>
                <p class="text-purple-400 text-[10px] uppercase tracking-widest mt-2">Security Verification</p>
            </div>
            
            <div class="space-y-4 text-left">
                <div class="space-y-1">
                    <label class="text-[10px] text-purple-400 font-bold ml-2 uppercase">ชื่อผู้ใช้งาน</label>
                    <input type="text" id="authName" placeholder="ระบุชื่อช่าง" class="w-full p-4 bg-black/60 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white">
                </div>
                <div class="space-y-1">
                    <label class="text-[10px] text-purple-400 font-bold ml-2 uppercase">รหัสผ่านลับ</label>
                    <input type="password" id="authPass" placeholder="•••••" class="w-full p-4 bg-black/60 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white text-center tracking-[1em]">
                </div>
                <button onclick="handleLogin()" class="w-full bg-purple-600 hover:bg-purple-500 py-5 rounded-2xl font-bold shadow-lg active:scale-95 transition-all uppercase tracking-widest mt-4">ปลดล็อคระบบ 📺</button>
                <p id="loginError" class="hidden text-red-500 text-center text-xs font-bold mt-2 animate-bounce">❌ รหัสผิด! ลองใหม่นะช่าง</p>
            </div>
        </div>
    </div>

    <div id="mainPage" class="hidden-page flex flex-col min-h-screen">
        <nav class="p-5 flex justify-between items-center glass-purple sticky top-0 z-50">
            <div class="flex items-center space-x-3">
                <div class="w-8 h-8 rounded-lg bg-purple-600 flex items-center justify-center"><i class="fas fa-check-shield text-white text-xs"></i></div>
                <span class="font-bold purple-neon" id="navName">ONLINE</span>
            </div>
            <button onclick="logout()" class="text-purple-400 p-2"><i class="fas fa-power-off"></i></button>
        </nav>

        <main class="p-6 space-y-4 max-w-md mx-auto w-full">
            <div onclick="openWorkPage()" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl">
                <div class="w-14 h-14 bg-purple-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-pen-nib text-white"></i></div>
                <div><h3 class="font-bold text-lg">บันทึกหน้างาน</h3><p class="text-xs text-purple-400">ส่งข้อมูลเข้า Sheets</p></div>
            </div>
            <div onclick="alert('ระบบคลาวด์ปกติ 🔋')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl opacity-80">
                <div class="w-14 h-14 bg-indigo-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-database text-white"></i></div>
                <div><h3 class="font-bold text-lg">สถานะเซิร์ฟเวอร์</h3><p class="text-xs text-indigo-400">Cloud Online</p></div>
            </div>
            <div onclick="alert('โทร 191... ล้อเล่นครับ 📞')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl opacity-80">
                <div class="w-14 h-14 bg-slate-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-headset text-white"></i></div>
                <div><h3 class="font-bold text-lg">ติดต่อแอดมิน</h3><p class="text-xs text-slate-400">Support 24h</p></div>
            </div>
        </main>
    </div>

    <div id="workPage" class="hidden-page flex flex-col min-h-screen">
        <nav class="p-5 flex items-center space-x-4 glass-purple sticky top-0 z-50">
            <button onclick="backToMain()" class="text-purple-400 text-xl"><i class="fas fa-chevron-left"></i></button>
            <span class="font-bold purple-neon uppercase tracking-widest">บันทึกข้อมูล</span>
        </nav>
        <main class="p-6 space-y-6 max-w-md mx-auto w-full">
            <div class="glass-purple p-6 rounded-[2.5rem] space-y-4 shadow-2xl">
                <textarea id="message" placeholder="พิมพ์รายงาน..." rows="6" class="w-full p-5 bg-black/50 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white resize-none"></textarea>
                <div class="grid grid-cols-4 gap-2">
                    <button onclick="startVoice()" class="bg-purple-900/50 border border-purple-500 rounded-2xl text-purple-300 py-4"><i class="fas fa-microphone text-xl"></i></button>
                    <button onclick="sendData()" class="col-span-3 bg-purple-600 py-4 rounded-2xl font-bold active:scale-95 transition-all">ส่งข้อมูล 🔋</button>
                </div>
                <div id="status" class="hidden text-center p-3 rounded-xl text-[10px] font-bold border border-purple-500 bg-purple-950"></div>
            </div>
        </main>
    </div>

    <script>
        // 🔑 ตั้งรหัสผ่านที่นี่!
        const REAL_PASS = "11384"; 
        let currentUser = "";

        document.addEventListener('DOMContentLoaded', () => {
            const savedUser = localStorage.getItem('tripfer_user');
            if (savedUser) showMainPage(savedUser);
        });

        function handleLogin() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            const errorMsg = document.getElementById('loginError');

            // 🛡️ ตรวจสอบรหัสผ่านจริง
            if(pass === REAL_PASS) {
                localStorage.setItem('tripfer_user', user);
                showMainPage(user);
                speak("ยินดีต้อนรับกลับมา");
                errorMsg.classList.add('hidden');
            } else {
                errorMsg.classList.remove('hidden');
                speak("รหัสผิดนะ");
            }
        }

        function showMainPage(user) {
            currentUser = user;
            document.getElementById('loginPage').classList.add('hidden-page');
            document.getElementById('workPage').classList.add('hidden-page');
            document.getElementById('mainPage').classList.remove('hidden-page');
            document.getElementById('navName').innerText = "ช่าง " + user;
        }

        function openWorkPage() {
            document.getElementById('mainPage').classList.add('hidden-page');
            document.getElementById('workPage').classList.remove('hidden-page');
        }

        function backToMain() {
            document.getElementById('workPage').classList.add('hidden-page');
            document.getElementById('mainPage').classList.remove('hidden-page');
        }

        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'th-TH';
            synth.speak(utter);
        }

        function startVoice() {
            const recognition = new (window.webkitRecognition || window.SpeechRecognition)();
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
            status.innerText = "กำลังยิงข้อมูล...";
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
            } catch (e) { status.innerText = "พัง!"; }
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
