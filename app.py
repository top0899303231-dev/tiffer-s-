import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TOTAL TOOLBOX - THE ULTIMATE EDITION ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0c001a">
    <title>ทริปเฟอร์ AI - SYSTEM 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #000; color: white; margin: 0; padding: 0; overflow: hidden; }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; }
        .cyan-neon { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; }
        .glass-purple { background: rgba(20, 0, 40, 0.95); backdrop-filter: blur(25px); border: 1px solid #5b21b6; }
        
        .page { display: none; width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; overflow-y: auto; }
        .active-page { display: flex !important; flex-direction: column; }
        
        .tool-card { background: linear-gradient(145deg, #1e1b4b, #0c001a); border: 1px solid #44178a; transition: 0.2s; cursor: pointer; }
        .tool-card:active { border-color: #00ffff; transform: scale(0.95); }
        
        input { background: rgba(0,0,0,0.6) !important; border: 1px solid #44178a !important; color: #00ffff !important; text-align: center; }
        .img-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; }
    </style>
</head>
<body>

    <div id="startPage" class="page active-page items-center justify-center p-6 text-center">
        <div class="max-w-sm w-full space-y-8">
            <i class="fas fa-microchip text-purple-500 text-6xl animate-pulse"></i>
            <h1 class="text-3xl font-bold purple-neon">TRIPFER AI</h1>
            <div class="grid grid-cols-1 gap-4">
                <div onclick="selectDevice('Computer')" class="glass-purple p-6 rounded-2xl border-2 border-purple-900 shadow-lg text-lg font-bold">COMPUTER</div>
                <div onclick="selectDevice('Mobile')" class="glass-purple p-6 rounded-2xl border-2 border-purple-900 border-dashed shadow-lg text-lg font-bold">MOBILE</div>
            </div>
        </div>
    </div>

    <div id="loginPage" class="page items-center justify-center p-6">
        <div class="w-full max-w-md glass-purple p-8 rounded-[2.5rem] text-center border-t-4 border-purple-600 shadow-2xl">
            <h2 class="text-2xl font-bold purple-neon mb-6">ระบุชื่อเข้าใช้งาน</h2>
            <input type="text" id="authName" placeholder="ชื่อช่าง" class="w-full p-4 rounded-2xl mb-4 outline-none bg-black/60 border border-purple-900 text-white font-bold">
            <input type="password" id="authPass" placeholder="รหัสผ่าน (11384)" class="w-full p-4 rounded-2xl mb-4 outline-none tracking-[0.5em]">
            <button onclick="handleLogin()" class="w-full bg-purple-600 py-4 rounded-2xl font-bold">START TOOLS ⚡</button>
        </div>
    </div>

    <div id="mainPage" class="page">
        <nav class="p-5 glass-purple flex justify-between items-center sticky top-0 z-50">
            <div>
                <p class="text-[10px] text-purple-400 font-bold uppercase">System Active</p>
                <span id="navName" class="font-bold purple-neon">...</span>
            </div>
            <button onclick="logout()" class="text-red-500 p-2"><i class="fas fa-power-off"></i></button>
        </nav>
        <main class="p-6 grid grid-cols-2 gap-4 max-w-md mx-auto w-full">
            <div onclick="switchPage('calcPage')" class="tool-card p-6 rounded-3xl text-center">
                <i class="fas fa-calculator text-3xl mb-2 text-cyan-400"></i>
                <p class="text-[10px] font-bold">คำนวณราคา</p>
            </div>
            <div onclick="switchPage('galleryPage')" class="tool-card p-6 rounded-3xl text-center">
                <i class="fas fa-images text-3xl mb-2 text-purple-400"></i>
                <p class="text-[10px] font-bold">ดูรูปสินค้า</p>
            </div>
            <div onclick="switchPage('stockPage')" class="tool-card p-6 rounded-3xl text-center opacity-80">
                <i class="fas fa-boxes text-3xl mb-2 text-yellow-400"></i>
                <p class="text-[10px] font-bold">สต็อกสินค้า</p>
            </div>
            <div onclick="alert('กำลังเรียกแอดมิน...')" class="tool-card p-6 rounded-3xl text-center opacity-80">
                <i class="fas fa-headset text-3xl mb-2 text-green-400"></i>
                <p class="text-[10px] font-bold">ช่วยเหลือ</p>
            </div>
        </main>
    </div>

    <div id="calcPage" class="page">
        <nav class="p-5 glass-purple flex items-center space-x-4">
            <button onclick="switchPage('mainPage')"><i class="fas fa-chevron-left"></i></button>
            <span class="font-bold">PRICE CALCULATOR</span>
        </nav>
        <main class="p-6 space-y-4 max-w-md mx-auto w-full text-center">
            <div class="glass-purple p-6 rounded-3xl">
                <input type="number" id="price" value="5" class="w-full p-4 rounded-xl mb-4 text-2xl font-bold">
                <p class="text-xs text-purple-400 mb-4">คูณด้วยจำนวน</p>
                <input type="number" id="qty" value="10" class="w-full p-4 rounded-xl mb-6 text-2xl font-bold">
                <p class="text-4xl font-bold cyan-neon mb-6" id="res">50.-</p>
                <button onclick="calc()" class="w-full bg-cyan-600 py-4 rounded-xl font-bold">คำนวณเงิน 🔋</button>
            </div>
        </main>
    </div>

    <div id="galleryPage" class="page">
        <nav class="p-5 glass-purple flex items-center space-x-4">
            <button onclick="switchPage('mainPage')"><i class="fas fa-chevron-left"></i></button>
            <span class="font-bold">IMAGE GALLERY</span>
        </nav>
        <main class="p-4 img-grid max-w-md mx-auto w-full">
            <img onclick="zoom('https://i.ibb.co/vzYpXfN/bolt.jpg')" src="https://i.ibb.co/vzYpXfN/bolt.jpg" class="rounded-xl border border-purple-900 h-32 object-cover">
            <img onclick="zoom('https://i.ibb.co/PZ0y67M/wrench.jpg')" src="https://i.ibb.co/PZ0y67M/wrench.jpg" class="rounded-xl border border-purple-900 h-32 object-cover">
            <img onclick="zoom('https://i.ibb.co/F8zP6p7/stock.jpg')" src="https://i.ibb.co/F8zP6p7/stock.jpg" class="rounded-xl border border-purple-900 h-32 object-cover">
            <div class="flex items-center justify-center bg-purple-900/20 rounded-xl border-2 border-dashed border-purple-900 h-32">
                <i class="fas fa-plus text-purple-900 text-2xl"></i>
            </div>
        </main>
    </div>

    <div id="modal" class="hidden fixed inset-0 z-[100] bg-black/95 flex items-center justify-center p-6" onclick="this.classList.add('hidden')">
        <img id="zImg" src="" class="max-w-full max-h-[80vh] rounded-2xl border-2 border-cyan-500 shadow-lg">
    </div>

    <script>
        const PASS = "11384";
        function switchPage(p) {
            document.querySelectorAll('.page').forEach(page => page.classList.remove('active-page'));
            document.getElementById(p).classList.add('active-page');
        }
        function selectDevice(t) { switchPage('loginPage'); speak("เลือกโหมด " + t); }
        function handleLogin() {
            const name = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            if(pass === PASS && name !== "") {
                localStorage.setItem('tripfer_user', name);
                document.getElementById('navName').innerText = name;
                switchPage('mainPage');
                speak("สวัสดีช่าง " + name);
            } else { alert("ข้อมูลไม่ถูกต้อง"); }
        }
        function calc() {
            const total = document.getElementById('price').value * document.getElementById('qty').value;
            document.getElementById('res').innerText = total + ".-";
            speak("ยอดรวมคือ " + total + " บาท");
        }
        function zoom(url) {
            document.getElementById('zImg').src = url;
            document.getElementById('modal').classList.remove('hidden');
        }
        function speak(t) {
            const utter = new SpeechSynthesisUtterance(t);
            utter.lang = 'th-TH';
            window.speechSynthesis.speak(utter);
        }
        function logout() { localStorage.clear(); location.reload(); }
        
        window.onload = function() {
            const saved = localStorage.getItem('tripfer_user');
            if(saved) {
                document.getElementById('navName').innerText = saved;
                switchPage('mainPage');
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

# ... ส่วน /submit เหมือนเดิม ...
