import requests
from flask import Flask, render_template_string, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# --- 🛠️ ตั้งค่าระบบ ---
LINE_ACCESS_TOKEN = os.environ.get('LINE_TOKEN')
USER_ID = os.environ.get('LINE_USER_ID')
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSeuSJ5qyiHYO8_atM412MZkqlGDbOY0lk0PY5L2M1CjNh7A3A/formResponse"

# --- 🎨 UI TV MAN PURPLE + PERSONAL PAGE ---
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ทริปเฟอร์ AI - TV MAN 📺</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600&display=swap');
        body { font-family: 'Kanit', sans-serif; background: #0c001a; color: white; }
        .purple-neon { text-shadow: 0 0 10px #bf40bf, 0 0 20px #bf40bf; }
        .glass-purple { background: rgba(30, 0, 60, 0.8); backdrop-filter: blur(15px); border: 2px solid #bf40bf; }
        .hidden-page { display: none; }
        .tv-screen { background: #000; border: 4px solid #5b21b6; position: relative; overflow: hidden; }
        .crt-line { width: 100%; height: 2px; background: rgba(191, 64, 191, 0.2); position: absolute; animation: scan 3s linear infinite; }
        @keyframes scan { from { top: 0; } to { top: 100%; } }
    </style>
</head>
<body class="min-h-screen">

    <div id="loginPage" class="flex items-center justify-center min-h-screen p-6">
        <div class="w-full max-w-md glass-purple p-10 rounded-[2.5rem] shadow-[0_0_50px_rgba(191,64,191,0.3)]">
            <div class="flex flex-col items-center mb-8">
                <div class="w-24 h-20 tv-screen rounded-lg mb-4 flex items-center justify-center shadow-[0_0_20px_#bf40bf]">
                    <div class="crt-line"></div>
                    <i class="fas fa-smile text-purple-500 text-4xl"></i>
                </div>
                <h2 class="text-2xl font-bold purple-neon">ทริปเฟอร์ AI</h2>
                <p class="text-purple-300 text-xs mt-2 uppercase tracking-widest">Login to Access</p>
            </div>
            
            <div class="space-y-4">
                <div class="relative">
                    <i class="fas fa-user absolute left-4 top-4 text-purple-400"></i>
                    <input type="text" id="authName" placeholder="ชื่อผู้ใช้งาน" class="w-full pl-12 pr-4 py-4 bg-purple-900/50 border border-purple-500 rounded-2xl outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder:text-purple-700">
                </div>
                <div class="relative">
                    <i class="fas fa-key absolute left-4 top-4 text-purple-400"></i>
                    <input type="password" id="authPass" placeholder="รหัสผ่าน" class="w-full pl-12 pr-4 py-4 bg-purple-900/50 border border-purple-500 rounded-2xl outline-none focus:ring-2 focus:ring-purple-400 text-white placeholder:text-purple-700">
                </div>
                
                <button onclick="handleLogin()" class="w-full bg-purple-600 hover:bg-purple-500 text-white font-bold py-5 rounded-2xl shadow-[0_10px_20px_rgba(0,0,0,0.3)] active:scale-95 transition-all text-xl">
                    เข้าสู่ระบบ 📺
                </button>
            </div>
        </div>
    </div>

    <div id="mainPage" class="hidden-page flex flex-col min-h-screen">
        <nav class="bg-purple-950/80 border-b border-purple-500 px-6 py-4 sticky top-0 z-10 backdrop-blur-md">
            <div class="max-w-md mx-auto flex justify-between items-center">
                <span class="text-xl font-bold purple-neon"><i class="fas fa-tv mr-2"></i>ทริปเฟอร์ AI</span>
                <button onclick="logout()" class="text-purple-300 text-sm font-bold border border-purple-500 px-3 py-1 rounded-lg">ออกระบบ</button>
            </div>
        </nav>

        <main class="p-6 flex flex-col items-center pt-8">
            <div class="w-full max-w-md glass-purple rounded-[2rem] overflow-hidden shadow-2xl">
                <div class="bg-gradient-to-br from-purple-800 to-indigo-900 p-10 text-center relative">
                    <div class="absolute top-4 right-4 animate-pulse">
                        <i class="fas fa-signal text-green-400"></i>
                    </div>
                    <h2 class="text-3xl font-bold italic mb-2" id="welcomeMsg">สวัสดี ช่าง!</h2>
                    <p class="text-purple-300 text-xs font-bold uppercase tracking-widest bg-black/30 inline-block px-3 py-1 rounded-full">Personal Page 🟣</p>
                </div>
                
                <div class="p-8 space-y-6">
                    <div class="bg-black/20 p-4 rounded-2xl border border-purple-900">
                        <label class="block text-[10px] font-bold text-purple-400 uppercase mb-2 tracking-widest">สถานะปัจจุบัน</label>
                        <p class="text-white text-sm" id="userStatus">กำลังรอข้อมูลใหม่จาก... </p>
                    </div>

                    <textarea id="message" placeholder="พิมพ์ข้อความที่ต้องการบันทึก..." rows="4"
                              class="w-full p-5 bg-purple-950/50 border border-purple-800 rounded-2xl outline-none focus:ring-2 focus:ring-purple-500 resize-none text-white placeholder:text-purple-800"></textarea>

                    <div class="flex space-x-3">
                        <button onclick="startVoice()" class="flex-1 bg-purple-900/50 text-purple-300 py-4 rounded-2xl border border-purple-500 hover:bg-purple-800 transition-all">
                            <i class="fas fa-microphone text-xl"></i>
                        </button>
                        <button onclick="sendData()" class="flex-[3] bg-purple-600 text-white font-bold py-4 rounded-2xl shadow-lg shadow-purple-900/50 hover:bg-purple-500 transition-all active:scale-95 uppercase tracking-widest">
                            บันทึกลงคลาวด์ 🔋
                        </button>
                    </div>
                    <div id="status" class="hidden text-center p-4 rounded-2xl text-sm font-bold border border-purple-500 bg-purple-950 shadow-inner"></div>
                </div>
            </div>
        </main>
    </div>

    <script>
        let currentUser = "";

        function speak(text) {
            const synth = window.speechSynthesis;
            const utter = new SpeechSynthesisUtterance(text);
            utter.lang = 'th-TH';
            synth.speak(utter);
        }

        function startVoice() {
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.lang = 'th-TH';
            speak("ฟังอยู่ บอกมาเลย");
            recognition.start();
            recognition.onresult = (event) => {
                document.getElementById('message').value = event.results[0][0].transcript;
                speak("รับทราบ");
            };
        }

        function handleLogin() {
            const user = document.getElementById('authName').value;
            const pass = document.getElementById('authPass').value;
            
            if(!user || !pass) { alert("ใส่ชื่อกับรหัสด้วย!"); return; }
            
            // ล็อคอินปุ๊บ เปลี่ยนหน้าทันที
            currentUser = user;
            document.getElementById('loginPage').classList.add('hidden-page');
            document.getElementById('mainPage').classList.remove('hidden-page');
            
            // หน้าเฉพาะคน: โชว์ชื่อคนล็อคอิน
            document.getElementById('welcomeMsg').innerText = "สวัสดี " + currentUser;
            document.getElementById('userStatus').innerText = "หน้าส่วนตัวของ: " + currentUser;
            
            speak("เข้าสู่ระบบแล้ว ยินดีต้อนรับ " + currentUser);
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
                const data = await res.json();
                if(data.status === 'success') {
                    status.innerText = "🔋 บันทึกเรียบร้อย!";
                    speak("เก็บข้อมูลให้แล้ว");
                    document.getElementById('message').value = "";
                }
            } catch (e) {
                status.innerText = "พัง! เชื่อมต่อไม่ได้";
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
            # บันทึกลง Google Sheets
            payload = {"entry.1691238515": name, "entry.540166297": message}
            requests.post(FORM_URL, data=payload)

            # แจ้งเตือน LINE
            if LINE_ACCESS_TOKEN and USER_ID:
                text = f"🟣 [ทริปเฟอร์ AI]\n👤 ช่าง: {name}\n💬: {message}\n⏰: {time_now}"
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
