import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN - DEVICE SELECTOR & SECURE LOGIN ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0c001a">
    <title>ทริปเฟอร์ AI - SELECT 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #000; color: white; margin: 0; padding: 0; overflow: hidden; }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; }
        .glass-purple { background: rgba(20, 0, 40, 0.95); backdrop-filter: blur(25px); border: 1px solid #5b21b6; }
        
        /* ⚡ ระบบเด้งสลับหน้า */
        .page { display: none; width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; overflow-y: auto; }
        .active-page { display: flex !important; flex-direction: column; }
        
        .select-card { background: rgba(30, 0, 60, 0.6); border: 2px solid #44178a; transition: 0.3s; cursor: pointer; }
        .select-card:hover, .select-card:active { border-color: #bf40bf; background: rgba(124, 58, 237, 0.2); transform: scale(1.02); }
        
        .option-card { background: linear-gradient(145deg, #1e1b4b, #0c001a); border: 2px solid #5b21b6; transition: 0.2s; }
        input { background: rgba(0,0,0,0.6) !important; border: 1px solid #44178a !important; color: white !important; }
    </style>
</head>
<body>

    <div id="startPage" class="page active-page items-center justify-center p-6 text-center">
        <div class="max-w-sm w-full space-y-8">
            <div class="mb-10">
                <i class="fas fa-microchip text-purple-500 text-6xl animate-pulse mb-4"></i>
                <h1 class="text-3xl font-bold purple-neon">ทริปเฟอร์ AI</h1>
                <p class="text-purple-400 text-xs uppercase tracking-widest mt-2 font-bold">กรุณาเลือกอุปกรณ์ใช้งาน</p>
            </div>
            
            <div class="grid grid-cols-1 gap-4">
                <div onclick="selectDevice('Desktop')" class="select-card p-8 rounded-[2.5rem] flex flex-col items-center shadow-lg">
                    <i class="fas fa-desktop text-4xl mb-3 text-purple-300"></i>
                    <span class="font-bold text-xl uppercase tracking-tighter">Computer</span>
                    <span class="text-[10px] text-purple-500 mt-1">PC / LAPTOP MODE</span>
                </div>
                
                <div onclick="selectDevice('Mobile')" class="select-card p-8 rounded-[2.5rem] flex flex-col items-center shadow-lg border-dashed">
                    <i class="fas fa-mobile-alt text-4xl mb-3 text-purple-300"></i>
                    <span class="font-bold text-xl uppercase tracking-tighter">Mobile</span>
                    <span class="text-[10px] text-purple-500 mt-1">SMARTPHONE MODE</span>
                </div>
            </div>
        </div>
    </div>

    <div id="loginPage" class="page items-center justify-center p-6">
        <div class="w-full max-w-md glass-purple p-8 rounded-[2.5rem] text-center border-t-4 border-purple-600 shadow-2xl">
            <h2 class="text-2xl font-bold purple-neon mb-6">เข้าสู่ระบบ (<span id="deviceTypeDisplay"></span>)</h2>
            <div class="space-y-4 text-left">
                <input type="text" id="authName" placeholder="ชื่อช่าง" class="w-full p-4 rounded-2xl outline-none">
                <input type="email" id="authEmail" placeholder="อีเมล" class="w-full p-4 rounded-2xl outline-none">
                <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full p-4 rounded-2xl outline-none text-center tracking-[0.5em]">
                <button onclick="handleLogin()" class="w-full bg-purple-600 py-5 rounded-2xl font-bold active:scale-95 transition-all mt-4 text-xl">ยืนยัน 📺</button>
                <div id="loginError" class="hidden bg-red-900/40 border border-red-500 p-3 rounded-xl mt-3 text-center text-red-200 text-xs font-bold">รหัสผ่านไม่ถูกต้อง!</div>
            </div>
        </div>
    </div>

    <div id="mainPage" class="page">
        <nav class="p-5 flex justify-between items-center glass-purple sticky top-0 z-50">
            <span class="font-bold purple-neon tracking-wider">ช่าง <span id="navNameDisplay">...</span></span>
            <button onclick="logout()" class="text-red-500 p-2"><i class="fas fa-power-off"></i></button>
        </nav>
        <main class="p-6 space-y-4 max-w-md mx-auto w-full">
            <div onclick="switchPage('workPage')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl">
                <div class="w-14 h-14 bg-purple-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-edit"></i></div>
                <div><h3 class="font-bold text-lg text-white">บันทึกหน้างาน</h3><p class="text-xs text-purple-400">Google Sheets Sync</p></div>
            </div>
            <div onclick="alert('System Online')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl opacity-80">
                <div class="w-14 h-14 bg-indigo-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-server"></i></div>
                <div><h3 class="font-bold text-lg text-white">ตรวจสอบระบบ</h3><p class="text-xs text-indigo-400">Cloud Status</p></div>
            </div>
            <div onclick="alert('Contacting Admin')" class="option-card p-6 rounded-[2rem] flex items-center space-x-5 shadow-xl opacity-80">
                <div class="w-14 h-14 bg-slate-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-headset"></i></div>
                <div><h3 class="font-bold text-lg text-white">ช่วยเหลือ</h3><p class="text-xs text-slate-400">Admin Support</p></div>
            </div>
        </main>
    </div>

    <div id="workPage" class="page">
        <nav class="p-5 flex items-center space-x-4 glass-purple sticky top-0 z-50">
            <button onclick="switchPage('mainPage')" class="text-purple-400 text-xl"><i class="fas fa-chevron-left"></i></button>
            <span class="font-bold purple-neon uppercase">Data Input</span>
        </nav>
        <main class="p-6 space-y-6 max-w-md mx-auto w-full">
            <div class="glass-purple p-6 rounded-[2.5rem] space-y-4 shadow-2xl">
                <textarea id="message" placeholder="พิมพ์รายงาน..." rows="8" class="w-full p-5 rounded-2xl outline-none resize-none text-white"></textarea>
                <div class="grid grid-cols-4 gap-2">
                    <button onclick="startVoice()" class="bg-purple-900/50 border border-purple-500 rounded-2xl text-purple-300 py-5"><i class="fas fa-microphone text-2xl"></i></button>
                    <button onclick="sendData()" class="col-span-3 bg-purple-600 py-5 rounded-2xl font-bold uppercase text-lg">บันทึกงาน 🔋</button>
                </div>
                <div id="status" class="hidden text-center p-3 rounded-xl text-xs font-bold border border-purple-500 bg-purple-950"></div>
            </div>
        </main>
    </div>

    <script>
        const REAL_PASS = "11384";
        let currentUser = "";
        let selectedDevice = "";

        // 🧠 ตรวจสอบการจำค่า (Auto-Login)
        window.onload = function() {
            const savedUser = localStorage.getItem('tripfer_user');
            if (savedUser) {
                currentUser = savedUser;
                switchPage('mainPage');
                document.getElementById('navNameDisplay').innerText = savedUser;
            }
        };

        function switchPage(pageId) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active-page'));
            document.getElementById(pageId).classList.add('active-page');
        }

        // ฟังก์ชันเลือกอุปกรณ์จากหน้าแรก
        function selectDevice(type) {
            selectedDevice = type;
            document.getElementById('deviceTypeDisplay').innerText = type;
            switchPage('loginPage');
            speak("คุณเลือกใช้ผ่าน " + type);
        }

        function handleLogin() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            const errorBox = document.getElementById('loginError');

            if(pass === REAL_PASS && user !== "") {
                localStorage.setItem('tripfer_user', user);
                currentUser = user;
                document.getElementById('navNameDisplay').innerText = user;
                switchPage('mainPage');
                speak("ยินดีต้อนรับเข้าสู่ระบบ");
            } else {
                errorBox.classList.remove('hidden');
                speak("รหัสผ่านไม่ถูกต้อง");
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
                    body: JSON.stringify({ username: currentUser, device: selectedDevice, message: msg })
                });
                if(res.ok) {
                    status.innerText = "สำเร็จ! 🔋";
                    speak("เก็บงานเรียบร้อย");
                    document.getElementById('message').value = "";
                }
            } catch (e) { status.innerText = "พัง!"; }
        }

        function logout() {
            localStorage.clear();
            location.reload();
        }
    </script>
</body>
</html>
