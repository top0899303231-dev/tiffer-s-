import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN SHOPPING - HISTORY EDITION ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta name="theme-color" content="#0c001a">
    <title>ทริปเฟอร์ SHOP 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #000; color: white; margin: 0; padding: 0; overflow: hidden; }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; }
        .glass-purple { background: rgba(20, 0, 40, 0.95); backdrop-filter: blur(25px); border: 1px solid #5b21b6; }
        .page { display: none; width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; overflow-y: auto; }
        .active-page { display: flex !important; flex-direction: column; }
        .product-card, .history-card { background: rgba(30, 0, 60, 0.6); border: 1px solid #44178a; transition: 0.2s; }
        .product-card:active { border-color: #bf40bf; transform: scale(0.98); }
        .cart-badge { background: #ff00ff; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px; position: absolute; top: -5px; right: -5px; font-weight: bold; }
    </style>
</head>
<body>

    <div id="startPage" class="page active-page items-center justify-center p-6 text-center">
        <div class="max-w-sm w-full space-y-8">
            <i class="fas fa-shopping-basket text-purple-500 text-6xl animate-pulse mb-4"></i>
            <h1 class="text-3xl font-bold purple-neon">TRIPFER SHOP</h1>
            <div class="grid grid-cols-1 gap-4">
                <div onclick="selectDevice('Computer')" class="glass-purple p-6 rounded-2xl border-2 border-purple-900 shadow-lg text-lg font-bold">COMPUTER</div>
                <div onclick="selectDevice('Mobile')" class="glass-purple p-6 rounded-2xl border-2 border-purple-900 border-dashed shadow-lg text-lg font-bold">MOBILE</div>
            </div>
        </div>
    </div>

    <div id="loginPage" class="page items-center justify-center p-6">
        <div class="w-full max-w-md glass-purple p-8 rounded-[2.5rem] text-center border-t-4 border-purple-600 shadow-2xl">
            <h2 class="text-2xl font-bold purple-neon mb-6">เข้าสู่ระบบร้านค้า</h2>
            <div class="space-y-4 text-left">
                <input type="text" id="authName" placeholder="ชื่อลูกค้า" class="w-full p-4 rounded-2xl outline-none bg-black/60 border border-purple-900 text-white">
                <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full p-4 rounded-2xl outline-none bg-black/60 border border-purple-900 text-white text-center tracking-[0.5em]">
                <button onclick="handleLogin()" class="w-full bg-purple-600 py-5 rounded-2xl font-bold active:scale-95 text-xl mt-2">เปิดร้านค้า 🛒</button>
                <div id="loginError" class="hidden text-red-500 text-xs font-bold mt-2 text-center">รหัสผ่านไม่ถูกต้อง!</div>
            </div>
        </div>
    </div>

    <div id="mainPage" class="page">
        <nav class="p-5 flex justify-between items-center glass-purple sticky top-0 z-50">
            <span class="font-bold purple-neon">TRIPFER STORE</span>
            <button onclick="logout()" class="text-red-500 p-2"><i class="fas fa-power-off"></i></button>
        </nav>
        <main class="p-6 space-y-4 max-w-md mx-auto w-full">
            <div onclick="switchPage('shopPage')" class="glass-purple p-6 rounded-[2rem] flex items-center space-x-5 border-2 border-purple-500 shadow-lg">
                <div class="w-14 h-14 bg-purple-800 rounded-2xl flex items-center justify-center text-2xl shadow-lg"><i class="fas fa-box-open"></i></div>
                <div><h3 class="font-bold text-lg text-white">เลือกซื้อสินค้า</h3><p class="text-xs text-purple-400">น็อต สกรู และเครื่องมือ</p></div>
            </div>

            <div onclick="showHistory()" class="glass-purple p-6 rounded-[2rem] flex items-center space-x-5 border border-purple-900 opacity-90 shadow-lg">
                <div class="w-14 h-14 bg-indigo-800 rounded-2xl flex items-center justify-center text-2xl shadow-lg"><i class="fas fa-history"></i></div>
                <div><h3 class="font-bold text-lg text-white">ประวัติสั่งซื้อ</h3><p class="text-xs text-indigo-400">รายการที่สั่งไปแล้ว</p></div>
            </div>

            <div onclick="alert('กำลังเรียกแอดมิน...')" class="glass-purple p-6 rounded-[2rem] flex items-center space-x-5 border border-purple-900 opacity-90 shadow-lg">
                <div class="w-14 h-14 bg-slate-800 rounded-2xl flex items-center justify-center text-2xl shadow-lg"><i class="fas fa-headset"></i></div>
                <div><h3 class="font-bold text-lg text-white">ช่วยเหลือ</h3><p class="text-xs text-slate-400">คุยกับแอดมิน</p></div>
            </div>
        </main>
    </div>

    <div id="shopPage" class="page">
        <nav class="p-5 flex items-center justify-between glass-purple sticky top-0 z-50">
            <button onclick="switchPage('mainPage')"><i class="fas fa-chevron-left text-purple-400 text-xl"></i></button>
            <span class="font-bold">รายการสินค้า</span>
            <div class="relative"><i class="fas fa-shopping-basket text-purple-400 text-2xl"></i><span id="cartCount" class="cart-badge">0</span></div>
        </nav>
        <main class="p-4 grid grid-cols-2 gap-4 max-w-md mx-auto w-full">
            <div class="product-card p-4 rounded-3xl text-center" onclick="addToCart('น็อต M8', 5)">
                <div class="w-full h-20 bg-purple-900/20 rounded-xl mb-2 flex items-center justify-center text-3xl"><i class="fas fa-nut"></i></div>
                <h4 class="text-xs font-bold">น็อต M8</h4>
                <p class="text-purple-400 text-[10px]">5.- / ชิ้น</p>
                <button class="mt-2 bg-purple-600 text-[9px] px-3 py-1 rounded-full font-bold">+ ลงตะกร้า</button>
            </div>
            <div class="product-card p-4 rounded-3xl text-center" onclick="addToCart('ประแจเลื่อน', 250)">
                <div class="w-full h-20 bg-purple-900/20 rounded-xl mb-2 flex items-center justify-center text-3xl"><i class="fas fa-wrench"></i></div>
                <h4 class="text-xs font-bold">ประแจเลื่อน</h4>
                <p class="text-purple-400 text-[10px]">250.- / ชิ้น</p>
                <button class="mt-2 bg-purple-600 text-[9px] px-3 py-1 rounded-full font-bold">+ ลงตะกร้า</button>
            </div>
        </main>
        <div class="p-4 glass-purple border-t-2 border-purple-500 mt-auto sticky bottom-0 z-50">
            <div class="flex justify-between items-center max-w-md mx-auto w-full">
                <div><span class="text-xs text-purple-400 font-bold uppercase">TOTAL</span><p class="text-2xl font-bold purple-neon"><span id="cartTotal">0</span>.-</p></div>
                <button onclick="checkout()" class="bg-green-600 px-10 py-4 rounded-2xl font-bold uppercase tracking-widest shadow-lg">สั่งซื้อ 🔋</button>
            </div>
        </div>
    </div>

    <div id="historyPage" class="page">
        <nav class="p-5 flex items-center space-x-4 glass-purple sticky top-0 z-50">
            <button onclick="switchPage('mainPage')" class="text-purple-400 text-xl"><i class="fas fa-chevron-left"></i></button>
            <span class="font-bold purple-neon uppercase tracking-widest">Order History</span>
        </nav>
        <main id="historyList" class="p-6 space-y-4 max-w-md mx-auto w-full">
            </main>
    </div>

    <script>
        const REAL_PASS = "11384";
        let currentUser = "";
        let cart = [];

        window.onload = function() {
            const savedUser = localStorage.getItem('tripfer_user');
            if (savedUser) { currentUser = savedUser; switchPage('mainPage'); }
        };

        function switchPage(p) {
            document.querySelectorAll('.page').forEach(page => page.classList.remove('active-page'));
            document.getElementById(p).classList.add('active-page');
        }

        function selectDevice(t) { switchPage('loginPage'); speak("โหมด " + t); }

        function handleLogin() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            if(pass === REAL_PASS && user !== "") {
                localStorage.setItem('tripfer_user', user);
                currentUser = user;
                switchPage('mainPage');
                speak("เข้าสู่ระบบสำเร็จ");
            } else {
                document.getElementById('loginError').classList.remove('hidden');
                speak("รหัสผิด");
            }
        }

        function addToCart(name, price) {
            cart.push({name, price});
            document.getElementById('cartCount').innerText = cart.length;
            document.getElementById('cartTotal').innerText = cart.reduce((s, i) => s + i.price, 0);
            speak("เพิ่ม " + name);
        }

        async function checkout() {
            if(cart.length === 0) return;
            const total = cart.reduce((s, i) => s + i.price, 0);
            const items = cart.map(i => i.name).join(', ');
            const date = new datetime().toLocaleString('th-TH');

            const order = { items, total, date };
            
            // 💾 บันทึกลงเครื่อง (History)
            let history = JSON.parse(localStorage.getItem('tripfer_history') || '[]');
            history.unshift(order);
            localStorage.setItem('tripfer_history', JSON.stringify(history));

            speak("สั่งซื้อเรียบร้อย ยอดรวม " + total + " บาท");

            try {
                await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: currentUser, message: "🛒 ออเดอร์: " + items + " | ยอด: " + total + ".-" })
                });
                alert("สั่งซื้อสำเร็จ!");
                cart = [];
                document.getElementById('cartCount').innerText = "0";
                document.getElementById('cartTotal').innerText = "0";
                switchPage('mainPage');
            } catch (e) { alert("Error!"); }
        }

        function showHistory() {
            const list = document.getElementById('historyList');
            const history = JSON.parse(localStorage.getItem('tripfer_history') || '[]');
            
            list.innerHTML = history.length ? "" : '<p class="text-center text-purple-900 mt-10">ยังไม่มีประวัติการสั่งซื้อ</p>';
            
            history.forEach(order => {
                list.innerHTML += `
                    <div class="history-card p-5 rounded-[2rem] border-l-4 border-purple-500 shadow-xl">
                        <div class="flex justify-between items-start mb-2">
                            <span class="text-[10px] text-purple-400 font-bold uppercase">${order.date}</span>
                            <span class="text-green-400 font-bold">${order.total}.-</span>
                        </div>
                        <p class="text-sm text-white font-bold">${order.items}</p>
                        <div class="mt-3 flex items-center text-[10px] text-purple-300">
                            <i class="fas fa-check-circle mr-1"></i> สำเร็จ
                        </div>
                    </div>
                `;
            });
            switchPage('historyPage');
            speak("เปิดประวัติการสั่งซื้อ");
        }

        function speak(t) {
            const utter = new SpeechSynthesisUtterance(t);
            utter.lang = 'th-TH';
            window.speechSynthesis.speak(utter);
        }

        function logout() { localStorage.clear(); location.reload(); }
    </script>
</body>
</html>
