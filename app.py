import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🎨 UI TOTAL SMART TOOLBOX ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0c001a">
    <title>TRIPFER SMART TOOLBOX 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #000; color: white; margin: 0; padding: 0; overflow: hidden; }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; color: #ff00ff; }
        .cyan-neon { text-shadow: 0 0 10px #00ffff, 0 0 20px #00ffff; color: #00ffff; }
        .glass-purple { background: rgba(20, 0, 40, 0.95); backdrop-filter: blur(25px); border: 1px solid #5b21b6; }
        
        .page { display: none; width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; overflow-y: auto; }
        .active-page { display: flex !important; flex-direction: column; }
        
        .tool-card { background: linear-gradient(145deg, #1e1b4b, #0c001a); border: 1px solid #44178a; transition: 0.2s; cursor: pointer; }
        .tool-card:active { border-color: #00ffff; transform: scale(0.95); }
        
        /* สไตล์ช่องค้นหาและรายการไฟล์ */
        .search-input { background: rgba(0,0,0,0.8) !important; border: 1px solid #5b21b6 !important; color: #00ffff !important; }
        .file-item { background: rgba(191, 64, 191, 0.1); border: 1px solid #44178a; transition: 0.2s; }
        .file-item:active { background: rgba(191, 64, 191, 0.3); border-color: #ff00ff; }
        
        pre { font-family: 'Courier New', Courier, monospace; line-height: 1.4; }
    </style>
</head>
<body>

    <div id="loginPage" class="page active-page items-center justify-center p-6">
        <div class="w-full max-w-md glass-purple p-8 rounded-[2.5rem] text-center border-t-4 border-purple-600 shadow-2xl">
            <i class="fas fa-user-cog text-5xl text-purple-500 mb-4"></i>
            <h2 class="text-2xl font-bold purple-neon mb-6">ยืนยันตัวตนช่าง</h2>
            <input type="text" id="authName" placeholder="ชื่อของคุณ" class="w-full p-4 rounded-2xl mb-4 outline-none search-input text-center font-bold">
            <input type="password" id="authPass" placeholder="รหัสผ่าน (11384)" class="w-full p-4 rounded-2xl mb-6 outline-none search-input text-center tracking-[0.5em]">
            <button onclick="handleLogin()" class="w-full bg-purple-600 py-4 rounded-2xl font-bold active:scale-95 text-xl">เข้าสู่ระบบ 🔋</button>
        </div>
    </div>

    <div id="mainPage" class="page">
        <nav class="p-5 glass-purple flex justify-between items-center sticky top-0 z-50">
            <div>
                <p class="text-[10px] text-purple-400 font-bold uppercase tracking-widest">Technician</p>
                <span id="navUserName" class="font-bold purple-neon">...</span>
            </div>
            <button onclick="logout()" class="text-red-500"><i class="fas fa-power-off"></i></button>
        </nav>
        <main class="p-6 grid grid-cols-2 gap-4 max-w-md mx-auto w-full">
            <div onclick="switchPage('finderPage')" class="tool-card p-6 rounded-3xl text-center shadow-lg">
                <i class="fas fa-search-location text-3xl mb-2 text-cyan-400"></i>
                <p class="text-[10px] font-bold uppercase">ค้นหาไฟล์</p>
            </div>
            <div onclick="switchPage('calcPage')" class="tool-card p-6 rounded-3xl text-center shadow-lg">
                <i class="fas fa-calculator text-3xl mb-2 text-purple-400"></i>
                <p class="text-[10px] font-bold uppercase">คำนวณงาน</p>
            </div>
            <div onclick="switchPage('galleryPage')" class="tool-card p-6 rounded-3xl text-center shadow-lg">
                <i class="fas fa-images text-3xl mb-2 text-yellow-400"></i>
                <p class="text-[10px] font-bold uppercase">คลังรูปภาพ</p>
            </div>
            <div onclick="alert('ระบบกำลังพัฒนา')" class="tool-card p-6 rounded-3xl text-center shadow-lg opacity-50">
                <i class="fas fa-cog text-3xl mb-2 text-gray-400"></i>
                <p class="text-[10px] font-bold uppercase">ตั้งค่า</p>
            </div>
        </main>
    </div>

    <div id="finderPage" class="page">
        <nav class="p-5 glass-purple flex items-center justify-between sticky top-0 z-50">
            <button onclick="switchPage('mainPage')"><i class="fas fa-arrow-left text-purple-400"></i></button>
            <span class="font-bold cyan-neon">SMART FINDER</span>
            <label for="fileInput" class="text-cyan-400"><i class="fas fa-file-import text-xl"></i><input type="file" id="fileInput" class="hidden" multiple onchange="importFiles(this)"></label>
        </nav>
        
        <main class="p-4 max-w-md mx-auto w-full flex flex-col h-full">
            <div class="relative mb-4">
                <input type="text" id="fileSearch" placeholder="พิมพ์ชื่อไฟล์ที่ต้องการหา..." 
                       class="w-full p-4 pl-12 rounded-2xl outline-none search-input font-bold"
                       onkeyup="runFilter()">
                <i class="fas fa-search absolute left-4 top-4 text-purple-500"></i>
            </div>

            <div id="fileResults" class="space-y-2 mb-4 max-h-[150px] overflow-y-auto pr-1">
                <p class="text-center text-[10px] text-purple-900 py-4 italic">นำเข้าไฟล์เพื่อเริ่มค้นหา...</p>
            </div>

            <div class="glass-purple flex-1 rounded-3xl p-4 border border-purple-900 overflow-hidden flex flex-col shadow-inner">
                <div id="readerHeader" class="flex justify-between items-center mb-2 hidden">
                    <span id="currentName" class="text-[10px] font-bold text-cyan-400 truncate w-40"></span>
                    <button onclick="clearReader()" class="text-red-500 text-[10px] font-bold">ปิด [X]</button>
                </div>
                <div id="readerBody" class="flex-1 overflow-y-auto">
                    <pre id="textContent" class="text-xs text-white hidden"></pre>
                    <div id="readerEmpty" class="h-full flex flex-col items-center justify-center opacity-30">
                        <i class="fas fa-file-alt text-4xl mb-2"></i>
                        <p class="text-[10px]">เลือกไฟล์ด้านบนเพื่ออ่าน</p>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <div id="calcPage" class="page">
        <nav class="p-5 glass-purple flex items-center space-x-4"><button onclick="switchPage('mainPage')"><i class="fas fa-arrow-left"></i></button><span class="font-bold">CALCULATOR</span></nav>
        <main class="p-6 max-w-md mx-auto w-full text-center">
            <div class="glass-purple p-6 rounded-3xl space-y-4">
                <input type="number" id="val1" value="5" class="w-full p-4 rounded-xl search-input text-xl font-bold">
                <i class="fas fa-times text-purple-500"></i>
                <input type="number" id="val2" value="10" class="w-full p-4 rounded-xl search-input text-xl font-bold">
                <p class="text-4xl font-bold cyan-neon pt-4" id="res">50.-</p>
                <button onclick="doCalc()" class="w-full bg-cyan-600 py-4 rounded-xl font-bold">คำนวณเงิน ⚡</button>
            </div>
        </main>
    </div>

    <script>
        const MASTER_PASS = "11384";
        let filesStorage = [];

        // --- ระบบล็อคอิน ---
        function handleLogin() {
            const u = document.getElementById('authName').value;
            const p = document.getElementById('authPass').value;
            if(p === MASTER_PASS && u !== "") {
                localStorage.setItem('worker_name', u);
                document.getElementById('navUserName').innerText = u;
                switchPage('mainPage');
                speak("ยินดีต้อนรับช่าง " + u);
            } else { alert("รหัสผิด!"); }
        }

        function switchPage(p) {
            document.querySelectorAll('.page').forEach(pg => pg.classList.remove('active-page'));
            document.getElementById(p).classList.add('active-page');
        }

        // --- ระบบค้นหาและอ่านไฟล์ (แก้ให้ระบุชื่อหาได้) ---
        function importFiles(input) {
            const news = Array.from(input.files);
            news.forEach(f => filesStorage.push(f));
            runFilter();
            speak("นำเข้าไฟล์สำเร็จ");
        }

        function runFilter() {
            const key = document.getElementById('fileSearch').value.toLowerCase();
            const container = document.getElementById('fileResults');
            container.innerHTML = "";

            const matched = filesStorage.filter(f => f.name.toLowerCase().includes(key));
            
            if(matched.length === 0 && filesStorage.length > 0) {
                container.innerHTML = '<p class="text-center text-red-500 text-[10px]">ไม่พบไฟล์ที่ระบุชื่อ</p>';
                return;
            }

            matched.forEach(file => {
                const div = document.createElement('div');
                div.className = "file-item p-3 rounded-xl flex justify-between items-center cursor-pointer";
                div.onclick = () => openFile(file);
                div.innerHTML = `<span class="text-xs truncate">${file.name}</span><i class="fas fa-eye text-[10px] text-cyan-400"></i>`;
                container.appendChild(div);
            });
        }

        function openFile(file) {
            const reader = new FileReader();
            document.getElementById('readerHeader').classList.remove('hidden');
            document.getElementById('readerEmpty').classList.add('hidden');
            document.getElementById('currentName').innerText = file.name;
            
            reader.onload = (e) => {
                document.getElementById('textContent').innerText = e.target.result;
                document.getElementById('textContent').classList.remove('hidden');
                speak("กำลังอ่านไฟล์ " + file.name);
            };
            reader.readAsText(file);
        }

        function clearReader() {
            document.getElementById('readerHeader').classList.add('hidden');
            document.getElementById('textContent').classList.add('hidden');
            document.getElementById('readerEmpty').classList.remove('hidden');
        }

        function doCalc() {
            const total = document.getElementById('val1').value * document.getElementById('val2').value;
            document.getElementById('res').innerText = total + ".-";
            speak("ยอดรวม " + total);
        }

        function speak(t) {
            const utter = new SpeechSynthesisUtterance(t);
            utter.lang = 'th-TH';
            window.speechSynthesis.speak(utter);
        }

        function logout() { localStorage.clear(); location.reload(); }

        window.onload = () => {
            const saved = localStorage.getItem('worker_name');
            if(saved) {
                document.getElementById('navUserName').innerText = saved;
                switchPage('mainPage');
            }
        }
    </script>
</body>
</html>
