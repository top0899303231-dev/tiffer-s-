import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN SHOPPING - ANDROID STYLE ---
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
        .product-card { background: rgba(30, 0, 60, 0.6); border: 1px solid #44178a; transition: 0.2s; }
        .product-card:active { border-color: #bf40bf; transform: scale(0.98); }
        .cart-badge { background: #ff00ff; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px; position: absolute; top: -5px; right: -5px; }
    </style>
</head>
<body>

    <div id="startPage" class="page active-page items-center justify-center p-6 text-center">
        <div class="max-w-sm w-full space-y-8">
            <i class="fas fa-shopping-cart text-purple-500 text-6xl animate-bounce mb-4"></i>
            <h1 class="text-3xl font-bold purple-neon">TRIPFER SHOP</h1>
            <div class="grid grid-cols-1 gap-4">
                <div onclick="selectDevice('Computer')" class="glass-purple p-6 rounded-2xl border-2 border-purple-900">COMPUTER</div>
                <div onclick="selectDevice('Mobile')" class="glass-purple p-6 rounded-2xl border-2 border-purple-900 border-dashed">MOBILE</div>
            </div>
        </div>
    </div>

    <div id="loginPage" class="page items-center justify-center p-6">
        <div class="w-full max-w-md glass-purple p-8 rounded-[2.5rem] text-center border-t-4 border-purple-600 shadow-2xl">
            <h2 class="text-2xl font-bold purple-neon mb-6">เข้าสู่ระบบการซื้อขาย</h2>
            <div class="space-y-4 text-left">
                <input type="text" id="authName" placeholder="ชื่อลูกค้า/ช่าง" class="w-full p-4 bg-black/60 border border-purple-900 rounded-2xl outline-none text-white">
                <input type="email" id="authEmail" placeholder="อีเมล" class="w-full p-4 bg-black/60 border border-purple-900 rounded-2xl outline-none text-white">
                <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full p-4 bg-black/60 border border-purple-900 rounded-2xl outline-none text-white text-center tracking-[0.5em]">
                <button onclick="handleLogin()" class="w-full bg-purple-600 py-5 rounded-2xl font-bold active:scale-95 text-xl">เข้าสู่ร้านค้า 🛒</button>
                <div id="loginError" class="hidden bg-red-900/40 border border-red-500 p-3 rounded-xl mt-3 text-center text-red-200 text-xs font-bold">รหัสผ่านไม่ถูกต้อง!</div>
            </div>
        </div>
    </div>

    <div id="mainPage" class="page">
        <nav class="p-5 flex justify-between items-center glass-purple sticky top-0 z-50">
            <span class="font-bold purple-neon">TRIPFER STORE</span>
            <div class="flex space-x-4">
                <div class="relative"><i class="fas fa-shopping-basket text-xl"></i><span id="cartCount" class="cart-badge">0</span></div>
                <button onclick="logout()" class="text-red-500"><i class="fas fa-power-off"></i></button>
            </div>
        </nav>
        <main class="p-6 space-y-4 max-w-md mx-auto w-full">
            <div onclick="switchPage('shopPage')" class="glass-purple p-6 rounded-[2rem] flex items-center space-x-5 border-2 border-purple-500">
                <div class="w-14 h-14 bg-purple-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-box-open"></i></div>
                <div><h3 class="font-bold text-lg">เลือกซื้อสินค้า</h3><p class="text-xs text-purple-400">น็อต สกรู และอุปกรณ์</p></div>
            </div>
            <div onclick="switchPage('orderPage')" class="glass-purple p-6 rounded-[2rem] flex items-center space-x-5 opacity-80 border border-purple-900">
                <div class="w-14 h-14 bg-indigo-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-history"></i></div>
                <div><h3 class="font-bold text-lg">ประวัติสั่งซื้อ</h3><p class="text-xs text-indigo-400">ตรวจสอบรายการล่าสุด</p></div>
            </div>
            <div onclick="alert('แอดมินกำลังรอสาย...')" class="glass-purple p-6 rounded-[2rem] flex items-center space-x-5 opacity-80 border border-purple-900">
                <div class="w-14 h-14 bg-slate-800 rounded-2xl flex items-center justify-center text-2xl"><i class="fas fa-comments"></i></div>
                <div><h3 class="font-bold text-lg">คุยกับผู้ขาย</h3><p class="text-xs text-slate-400">สอบถามราคาโรงงาน</p></div>
            </div>
        </main>
    </div>

    <div id="shopPage" class="page">
        <nav class="p-5 flex items-center justify-between glass-purple sticky top-0 z-50">
            <button onclick="switchPage('mainPage')"><i class="fas fa-chevron-left text-purple-400 text-xl"></i></button>
            <span class="font-bold">รายการสินค้า</span>
            <button onclick="checkout()" class="bg-green-600 px-4 py-1 rounded-full text-xs font-bold">ชำระเงิน</button>
        </nav>
        <main class="p-4 grid grid-cols-2 gap-4">
            <div class="product-card p-4 rounded-3xl text-center" onclick="addToCart('น็อตตัวผู้ M8', 5)">
                <div class="bg-purple-900/30 h-24 rounded-2xl mb-2 flex items-center justify-center text-3xl"><i class="fas fa-nut"></i></div>
                <h4 class="text-sm font-bold">น็อตตัวผู้ M8</h4>
                <p class="text-purple-400 text-xs">5 บาท / ชิ้น</p>
                <button class="mt-2 bg-purple-600 text-[10px] px-3 py-1 rounded-full">+ ลงตะกร้า</button>
            </div>
            <div class="product-card p-4 rounded-3xl text-center" onclick="addToCart('สกรูเกลียวเหล็ก', 3)">
                <div class="bg-purple-900/30 h-24 rounded-2xl mb-2 flex items-center justify-center text-3xl"><i class="fas fa-bolt"></i></div>
                <h4 class="text-sm font-bold">สกรูเกลียวเหล็ก</h4>
                <p class="text-purple-400 text-xs">3 บาท / ชิ้น</p>
                <button class="mt-2 bg-purple-600 text-[10px] px-3 py-1 rounded-full">+ ลงตะกร้า</button>
            </div>
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

        function switchPage(pageId) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active-page'));
            document.getElementById(pageId).classList.add('active-page');
        }

        function selectDevice(t) { switchPage('loginPage'); speak("เลือกโหมด " + t); }

        function handleLogin() {
            const pass = document.getElementById('authPass').value;
            const user = document.getElementById('authName').value;
            if(pass === REAL_PASS && user !== "") {
                localStorage.setItem('tripfer_user', user);
                currentUser = user;
                switchPage('mainPage');
                speak("ยินดีต้อนรับสู่ร้านค้า");
            } else {
                document.getElementById('loginError').classList.remove('hidden');
                speak("รหัสผ่านไม่ถูกต้อง");
            }
        }

        function addToCart(name, price) {
            cart.push({name, price});
            document.getElementById('cartCount').innerText = cart.length;
            speak("เพิ่ม " + name + " แล้ว");
        }

        async function checkout() {
            if(cart.length === 0) return alert("ตะกร้าว่างเปล่า!");
            let total = cart.reduce((sum, item) => sum + item.price, 0);
            let itemsText = cart.map(i => i.name).join(', ');
            
            speak("กำลังสรุปยอด " + total + " บาท");
            
            try {
                await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ 
                        username: currentUser, 
                        message: "🛒 สั่งซื้อ: " + itemsText + " | รวม: " + total + " บาท"
                    })
                });
                alert("สั่งซื้อสำเร็จ! ยอดรวม " + total + " บาท");
                cart = [];
                document.getElementById('cartCount').innerText = "0";
                switchPage('mainPage');
            } catch (e) { alert("พัง!"); }
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
                text = f"💰 [ออเดอร์ใหม่]\n👤 ลูกค้า: {name}\n📦 รายการ: {message}\n⏰: {datetime.now().strftime('%H:%M')}"
                requests.post('https://api.line.me/v2/bot/message/push', headers={'Authorization': f'Bearer {LINE_ACCESS_TOKEN}', 'Content-Type': 'application/json'}, json={'to': USER_ID, 'messages': [{'type': 'text', 'text': text}]})
            return jsonify({"status": "success"})
        except: pass
    return jsonify({"status": "error"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
