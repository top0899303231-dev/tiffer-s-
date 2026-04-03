HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TOP AI - CONTROL PANEL (💧 Water Drop)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500&display=swap');
        body { font-family: 'Kanit', sans-serif; }
    </style>
</head>
<body class="bg-blue-50/50 min-h-screen flex flex-col">

    <nav class="bg-gradient-to-r from-sky-100 to-blue-50 border-b border-blue-100 px-6 py-4 sticky top-0 z-10 shadow-sm">
        <div class="max-w-md mx-auto flex justify-between items-center">
            <span class="text-xl font-bold text-blue-700"><i class="fas fa-droplet mr-2"></i>TOP AI V.3.5 💧</span>
            <div class="flex items-center space-x-2">
                <div class="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
                <span class="text-xs text-blue-600 font-medium uppercase tracking-wider">Cloud Active</span>
            </div>
        </div>
    </nav>

    <main class="flex-grow p-6 flex flex-col items-center justify-start pt-10">
        <div class="w-full max-w-md bg-white rounded-3xl shadow-xl border border-blue-50 overflow-hidden">
            <div class="bg-sky-500 p-6 text-white text-center">
                <h2 class="text-xl font-bold">บันทึกข้อมูล & แจ้งเตือน</h2>
                <p class="text-sky-100 text-sm opacity-90 italic">ระบบช่าง TOP ออนไลน์ 24 ชม. (💧)</p>
            </div>
            
            <div class="p-6 space-y-5">
                <div>
                    <label class="block text-xs font-semibold text-blue-500 uppercase mb-2 ml-1">ชื่อผู้ใช้งาน</label>
                    <div class="relative">
                        <i class="fas fa-user absolute left-4 top-3.5 text-sky-400"></i>
                        <input type="text" id="username" placeholder="ระบุชื่อของคุณ" 
                               class="w-full pl-11 pr-4 py-3 bg-sky-50/50 border border-sky-100 rounded-2xl focus:ring-2 focus:ring-sky-500 focus:bg-white outline-none transition-all placeholder:text-sky-300">
                    </div>
                </div>

                <div>
                    <label class="block text-xs font-semibold text-blue-500 uppercase mb-2 ml-1">ข้อความแจ้งซ่อม/ฝากไว้</label>
                    <textarea id="message" placeholder="พิมพ์ข้อความที่นี่..." rows="4"
                              class="w-full p-4 bg-sky-50/50 border border-sky-100 rounded-2xl focus:ring-2 focus:ring-sky-500 focus:bg-white outline-none transition-all resize-none placeholder:text-sky-300"></textarea>
                </div>

                <button onclick="sendData()" id="sendBtn"
                        class="w-full bg-sky-600 text-white font-bold py-4 rounded-2xl hover:bg-blue-700 shadow-lg shadow-sky-100 transition-all flex items-center justify-center space-x-2 active:scale-95">
                    <i class="fas fa-paper-plane"></i>
                    <span>ส่งข้อมูลเข้าระบบ</span>
                </button>

                <div id="responseMsg" class="hidden text-center p-4 rounded-2xl text-sm font-medium border animate-bounce"></div>
            </div>
        </div>

        <p class="mt-8 text-blue-400 text-xs font-medium uppercase tracking-widest">
            Developed by ช่าง TOP | 2026 💧
        </p>
    </main>

    <script>
        async function sendData() {
            const name = document.getElementById('username').value;
            const msg = document.getElementById('message').value;
            const resBox = document.getElementById('responseMsg');
            const btn = document.getElementById('sendBtn');

            if(!name || !msg) {
                alert('ช่างครับ กรุณากรอกให้ครบนะ! 💧');
                return;
            }

            // แสดงสถานะกำลังส่ง (เปลี่ยนสี Loading ให้เข้าโทน 💧)
            btn.disabled = true;
            btn.innerHTML = '<i class="fas fa-spinner animate-spin"></i> <span class="text-sky-100">กำลังประมวลผล...</span>';
            resBox.classList.add('hidden');

            try {
                const response = await fetch('/submit', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ username: name, message: msg })
                });
                const result = await response.json();
                
                resBox.innerText = result.message;
                // ปรับสีแจ้งเตือนให้เข้าโทน 💧 (สีเขียวอ่อน/แดงอ่อน)
                resBox.classList.remove('hidden', 'bg-red-50', 'border-red-100', 'text-red-600', 'bg-green-50', 'border-green-100', 'text-green-600');
                resBox.classList.add('block');
                
                if (result.status === 'success') {
                    resBox.classList.add('bg-green-50', 'border-green-100', 'text-green-600');
                    document.getElementById('username').value = "";
                    document.getElementById('message').value = "";
                } else {
                    resBox.classList.add('bg-red-50', 'border-red-100', 'text-red-600');
                }
            } catch (error) {
                resBox.innerText = "เชื่อมต่อ Server ไม่ได้! 💧";
                resBox.classList.remove('hidden');
                resBox.classList.add('bg-red-50', 'border-red-100', 'text-red-600');
            } finally {
                btn.disabled = false;
                // เปลี่ยนไอคอนปุ่มส่งให้เข้าโทน 💧
                btn.innerHTML = '<i class="fas fa-paper-plane"></i> <span>ส่งข้อมูลเข้าระบบ</span>';
            }
        }
    </script>
</body>
</html>
'''
