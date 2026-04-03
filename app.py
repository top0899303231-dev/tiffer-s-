import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN SHOPPING - MOBILE UI EDITION ---
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
        
        /* ⚡ ระบบสลับหน้าแบบรวดเร็ว */
        .page { display: none; width: 100vw; height: 100vh; position: absolute; top: 0; left: 0; overflow-y: auto; }
        .active-page { display: flex !important; flex-direction: column; }
        
        .product-card { background: rgba(30, 0, 60, 0.6); border: 1px solid #44178a; transition: 0.2s; cursor: pointer; }
        .product-card:active { border-color: #bf40bf; transform: scale(0.98); background: rgba(124, 58, 237, 0.1); }
        .cart-badge { background: #ff00ff; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px; position: absolute; top: -5px; right: -5px; font-weight: bold; }
        
        input, textarea { background: rgba(0,0,0,0.6) !important; border: 1px solid #44178a !important; color: white !important; }
        input:focus { border-color: #bf40bf !important; }
    </style>
</head>
<body>

    <div id="startPage" class="page active-page items-center justify-center p-6 text-center">
        <div class="max-w-sm w-full space-y-8">
            <i class="fas fa-shopping-basket text-purple-500 text-6xl animate-pulse mb-4"></i>
            <h1 class="text-3xl font-bold purple-neon tracking-tighter">TRIPFER SHOP</h1>
            <p class="text-purple-400 text-xs uppercase tracking-widest mt-2 font-bold">เลือกโหมดการใช้งาน</p>
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
                <input type="text" id="authName" placeholder="ชื่อลูกค้า" class="w-full p-4 rounded-2xl outline-none">
                <input type="email" id="authEmail" placeholder="อีเมล" class="w-full p-4 rounded-2xl outline-none">
                <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full p-4 rounded-2xl outline-none text-center tracking-[0.5em]">
                <button onclick="handleLogin()" class="w-full bg-purple-600 hover:bg-purple-500 py-5 rounded-2xl font-bold active:scale-95 text-xl mt-2">เปิดตะกร้าซื้อของ 🛒</button>
                <div id="loginError" class="hidden bg-red-900/40 border border-red-500 p-3 rounded-xl mt-3 text-center text-red-200 text-xs font-bold animate-pulse">รหัสผ่านไม่ถูกต้อง!</div>
            </div>
        </div>
    </div>

    <div id="mainPage" class="page">
        <nav class="p-5 flex justify-between items-center glass-purple sticky top-0 z-50">
            <span class="font-bold purple-neon tracking-wider">TRIPFER SHOP</span>
            <div class="flex space-x-4 items-center">
                <div class="relative"><i class="fas fa-shopping-basket text-purple-400 text-2xl"></i><span id="cartCount" class="cart-badge">0</span></div>
                <button onclick="logout()" class="text-red-500 p-2"><i class="fas fa-power-off"></i></button>
            </div>
        </nav>
        
        <main class="p-4 grid grid-cols-2 gap-4 max-w-md mx-auto w-full">
            <h2 class="col-span-2 text-xs font-bold text-purple-400 uppercase tracking-[0.3em] ml-2 mt-4">รายการสินค้า</h2>
            
            <div class="product-card p-4 rounded-3xl text-center shadow-lg" onclick="addToCart('น็อตตัวผู้ M8', 5)">
                <div class="w-full h-24 bg-purple-900/30 rounded-2xl mb-3 flex items-center justify-center text-4xl border border-purple-900"><i class="fas fa-nut"></i></div>
                <h4 class="text-sm font-bold text-white truncate">น็อตตัวผู้ M8</h4>
                <p class="text-purple-400 text-xs mt-1">5 บาท / ชิ้น</p>
                <button class="mt-3 bg-purple-600 text-[10px] px-4 py-1.5 rounded-full font-bold uppercase tracking-wider">+ ลงตะกร้า</button>
            </div>
            
            <div class="product-card p-4 rounded-3xl text-center shadow-lg" onclick="addToCart('สกรูเกลียวเหล็ก', 3)">
                <div class="w-full h-24 bg-purple-900/30 rounded-2xl mb-3 flex items-center justify-center text-4xl border border-purple-900"><i class="fas fa-bolt"></i></div>
                <h4 class="text-sm font-bold text-white truncate">สกรูเกลียวเหล็ก</h4>
                <p class="text-purple-400 text-xs mt-1">3 บาท / ชิ้น</p>
                <button class="mt-3 bg-purple-600 text-[10px] px-4 py-1.5 rounded-full font-bold uppercase tracking-wider">+ ลงตะกร้า</button>
            </div>
            
            <div class="product-card p-4 rounded-3xl text-center shadow-lg" onclick="addToCart('ประแจแหวน M10', 120)">
                <div class="w-full h-24 bg-purple-900/30 rounded-2xl mb-3 flex items-center justify-center text-4xl border border-purple-900"><i class="fas fa-wrench"></i></div>
                <h4 class="text-sm font-bold text-white truncate">ประแจแหวน M10</h4>
                <p class="text-purple-400 text-xs mt-1">120 บาท / ชิ้น</p>
                <button class="mt-3 bg-purple-600 text-[10px] px-4 py-1.5 rounded-full font-bold uppercase tracking-wider">+ ลงตะกร้า</button>
            </div>
            
            <div class="product-card p-4 rounded-3xl text-center shadow-lg" onclick="addToCart('สปริง 4 นิ้ว', 45)">
                <div class="w-full h-24 bg-purple-900/30 rounded-2xl mb-3 flex items-center justify-center text-4xl border border-purple-900"><i class="fas fa-stream"></i></div>
                <h4 class="text-sm font-bold text-white truncate">สปริง 4 นิ้ว</h4>
                <p class="text-purple-400 text-xs mt-1">45 บาท / ชิ้น</p>
                <button class="mt-3 bg-purple-600 text-[10px] px-4 py-1.5 rounded-full font-bold uppercase tracking-wider">+ ลงตะกร้า</button>
            </div>
        </main>
        
        <div class="p-4 glass-purple border-t-2 border-purple-500 mt-auto sticky bottom-0 z-50">
            <div class="flex justify-between items-center max-w-md mx-auto w-full">
                <div>
                    <span class="text-xs text-purple-400">รวมทั้งหมด:</span>
                    <p class="text-2xl font-bold purple-neon"><span id="cartTotal">0</span> บาท</p>
                </div>
                <button onclick="checkout()" class="bg-green-600 px-8 py-4 rounded-2xl font-bold uppercase tracking-widest text-lg shadow-lg active:bg-green-500">สั่งซื้อ 🔋</button>
            </div>
        </div>
    </div>

    <script>
        const REAL_PASS = "11384"; // 🔑 รหัสผ่านช่าง
        let currentUser = "";
        let cart = [];

        // 🧠 ตรวจสอบการจำค่า (Auto-Login)
        window.onload = function() {
            const savedUser = localStorage.getItem('tripfer_user');
            if (savedUser) { currentUser = savedUser; switchPage('mainPage'); speak("ยินดีต้อนรับกลับมา"); }
        };

        function switchPage(pageId) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active-page'));
            document.getElementById(pageId).classList.add('active-page');
        }

        function selectDevice(t) { switchPage('loginPage'); speak("คุณเลือกใช้ผ่าน " + t); }

        function handleLogin() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            if(pass === REAL_PASS && user !== "") {
                localStorage.setItem('tripfer_user', user);
                currentUser = user;
                switchPage('mainPage');
                speak("ยินดีต้อนรับ เข้าสู่ระบบสำเร็จ");
                document.getElementById('loginError').classList.add('hidden');
            } else {
                document.getElementById('loginError').classList.remove('hidden');
                speak("รหัสผิดนะ");
            }
        }

        function addToCart(name, price) {
            cart.push({name, price});
            updateCartUI();
            speak("เพิ่ม " + name + " แล้ว");
        }

        function updateCartUI() {
            document.getElementById('cartCount').innerText = cart.length;
            let total = cart.reduce((sum, item) => sum + item.price, 0);
            document.getElementById('cartTotal').innerText = total;
        }

        async function checkout() {
            if(cart.length === 0) return alert("ตะกร้าว่างเปล่า!");
            let total = cart.reduce((sum, item) => sum + item.price, 0);
            let itemsText = cart.map(i => i.name).join(', ');
            
            speak("กำลังสรุปยอด " + total + " บาท");
            
            try {
                // ส่งข้อมูลออเดอร์
                await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ 
                        username: currentUser, 
                        message: "🛒 สั่งซื้อสินค้า: " + itemsText + " | ยอดรวม: " + total + " บาท"
                    })
                });
                alert("สั่งซื้อสำเร็จ! ยอดรวม " + total + " บาท ออเดอร์ส่งถึงช่างแล้ว");
                cart = [];
                updateCartUI();
                switchPage('mainPage');
            } catch (e) { alert("ล้มเหลว!"); }
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
