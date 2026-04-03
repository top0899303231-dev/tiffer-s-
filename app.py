import requests
from Flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ส่วนตั้งค่า ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN ANDROID - INSTANT SWITCH EDITION ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0c001a">
    <title>ทริปเฟอร์ AI 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #000; color: white; margin: 0; padding: 0; overflow: hidden; }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; }
        .glass-purple { background: rgba(20, 0, 40, 0.9); backdrop-filter: blur(20px); border: 1px solid #5b21b6; }
        
        /* ⚡ ระบบเด้งสลับหน้า (Instant Switch) */
        .page { display: none; width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; overflow-y: auto; }
        .active-page { display: flex !important; flex-direction: column; }
        
        .option-card { background: linear-gradient(145deg, #1e1b4b, #0c001a); border: 2px solid #5b21b6; transition: 0.2s; }
        .option-card:active { background: #4c1d95; transform: scale(0.98); }
    </style>
</head>
<body>

    <div id="loginPage" class="page active-page items-center justify-center p-6">
        <div class="w-full max-w-md glass-purple p-10 rounded-[2.5rem] text-center border-t-4 border-purple-600 shadow-[0_0_50px_rgba(191,64,191,0.2)]">
            <i class="fas fa-tv text-purple-500 text-6xl mb-6"></i>
            <h1 class="text-3xl font-bold purple-neon mb-8">ทริปเฟอร์ AI</h1>
            <div class="space-y-4 text-left">
                <input type="text" id="authName" placeholder="ชื่อช่าง" class="w-full p-4 bg-black/60 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white">
                <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full p-4 bg-black/60 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white text-center tracking-[0.5em]">
                <button onclick="handleLogin()" class="w-full bg-purple-600 py-5 rounded-2xl font-bold active:scale-95 transition-all mt-4">ปลดล็อค 📺</button>
                <p id="loginError" class="hidden text-red-500 text-center text-xs font-bold mt-2">รหัสผิด!</p>
            </div>
        </div>
    </div>

    <div id="mainPage" class="page">
        <nav class="p-5 flex justify-between items-center glass-purple sticky top-0">
            <span class="font-bold purple-neon uppercase">TRIPFER WORKSPACE</span>
            <button onclick="logout()" class="text-purple-400 p-2"><i class="fas fa-power-off"></i></button>
        </nav>
        <main class="p-6 space-y-4 max-w-md mx-auto w-full">
            <h2 class="text-xs font-bold text-purple-400 uppercase tracking-widest ml-1 mt-4">เลือกโหมด</h2>
            
            <div onclick="switchPage('workPage')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl">
                <div class="w-14 h-14 bg-purple-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-pen-nib text-white"></i></div>
                <div><h3 class="font-bold text-lg text-white">บันทึกหน้างาน</h3><p class="text-xs text-purple-400">ส่งข้อมูลเข้า Google Sheets</p></div>
            </div>

            <div onclick="alert('คลาวด์ปกติ 🔋')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl opacity-80">
                <div class="w-14 h-14 bg-indigo-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-database text-white"></i></div>
                <div><h3 class="font-bold text-lg text-white">สถานะระบบ</h3><p class="text-xs text-indigo-400">Server Status Online</p></div>
            </div>

            <div onclick="alert('กำลังเรียกแอดมิน...')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl opacity-80">
                <div class="w-14 h-14 bg-slate-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-headset text-white"></i></div>
                <div><h3 class="font-bold text-lg text-white">ช่วยเหลือ</h3><p class="text-xs text-slate-400">Contact Admin</p></div>
            </div>
        </main>
    </div>

    <div id="workPage" class="page">
        <nav class="p-5 flex items-center space-x-4 glass-purple sticky top-0">
            <button onclick="switchPage('mainPage')" class="text-purple-400 text-xl"><i class="fas fa-chevron-left"></i></button>
            <span class="font-bold purple-neon uppercase">บันทึกข้อมูล</span>
        </nav>
        <main class="p-6 space-y-6 max-w-md mx-auto w-full">
            <div class="glass-purple p-6 rounded-[2.5rem] space-y-4 shadow-2xl">
                <textarea id="message" placeholder="พิมพ์รายงาน..." rows="8" class="w-full p-5 bg-black/50 border border-purple-900 rounded-2xl outline-none focus:border-purple-400 text-white resize-none"></textarea>
                <div class="grid grid-cols-4 gap-2">
                    <button onclick="startVoice()" class="bg-purple-900/50 border border-purple-500 rounded-2xl text-purple-300 py-5"><i class="fas fa-microphone text-2xl"></i></button>
                    <button onclick="sendData()" class="col-span-3 bg-purple-600 py-5 rounded-2xl font-bold uppercase tracking-widest text-lg">ส่งข้อมูล 🔋</button>
                </div>
                <div id="status" class="hidden text-center p-3 rounded-xl text-xs font-bold border border-purple-500 bg-purple-950"></div>
            </div>
        </main>
    </div>

    <script>
        const REAL_PASS = "11384"; 
        let currentUser = "";

        // 🧠 ฟังก์ชันสลับหน้า (Instant Switch)
        function switchPage(pageId) {
            // ซ่อนทุกหน้า
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active-page'));
            // โชว์หน้าที่ต้องการ
            document.getElementById(pageId).classList.add('active-page');
        }

        document.addEventListener('DOMContentLoaded', () => {
            const savedUser = localStorage.getItem('tripfer_user');
            if (savedUser) {
                currentUser = savedUser;
                switchPage('mainPage');
            }
        });

        function handleLogin() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            if(pass === REAL_PASS) {
                localStorage.setItem('tripfer_user', user);
                currentUser = user;
                switchPage('mainPage');
                speak("เข้าสู่ระบบเรียบร้อย");
            } else {
                document.getElementById('loginError').classList.remove('hidden');
                speak("รหัสผิด");
            }
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
            status.innerText = "กำลังส่ง...";
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
            } catch (e) { status.innerText = "Error!"; }
        }

        function logout() {
            localStorage.removeItem('tripfer_user');
            location.reload();
        }
    </script>
</body>
</html>
