# --- 🎨 UI ส่วนที่เพิ่ม: เครื่องมืออ่านไฟล์ ---
# ก๊อปปี้ส่วนนี้ไปวางเพิ่มในไฟล์เดิมได้เลยครับ

HTML_TEMPLATE = '''
<div id="filePage" class="page">
        <nav class="p-5 glass-purple flex items-center justify-between sticky top-0 z-50">
            <div class="flex items-center space-x-4">
                <button onclick="switchPage('mainPage')"><i class="fas fa-arrow-left"></i></button>
                <span class="font-bold uppercase tracking-widest">File Reader</span>
            </div>
            <label for="fileInput" class="cursor-pointer text-cyan-400">
                <i class="fas fa-file-upload text-xl"></i>
                <input type="file" id="fileInput" class="hidden" onchange="readFile(this)">
            </label>
        </nav>
        
        <main class="p-6 max-w-md mx-auto w-full">
            <div id="fileInfo" class="mb-4 text-[10px] text-purple-400 font-bold uppercase hidden">
                ชื่อไฟล์: <span id="fileName" class="text-white"></span>
            </div>
            
            <div id="fileContentViewer" class="glass-purple p-5 rounded-3xl min-h-[300px] overflow-y-auto border border-purple-900 shadow-inner">
                <div id="emptyState" class="flex flex-col items-center justify-center h-full text-purple-800 opacity-50 mt-20">
                    <i class="fas fa-file-alt text-6xl mb-4"></i>
                    <p class="text-xs">กดไอคอนมุมขวาบนเพื่อเลือกไฟล์</p>
                </div>
                <pre id="textContent" class="text-sm text-cyan-100 whitespace-pre-wrap break-words font-mono hidden"></pre>
                <iframe id="pdfContent" class="w-full h-[500px] rounded-xl hidden" frameborder="0"></iframe>
            </div>
        </main>
    </div>

<script>
    // --- ฟังก์ชันอ่านไฟล์ ---
    function readFile(input) {
        const file = input.files[0];
        if (!file) return;

        document.getElementById('fileInfo').classList.remove('hidden');
        document.getElementById('fileName').innerText = file.name;
        document.getElementById('emptyState').classList.add('hidden');
        
        const reader = new FileReader();

        // ตรวจสอบประเภทไฟล์
        if (file.type === "application/pdf") {
            // อ่านไฟล์ PDF
            const fileURL = URL.createObjectURL(file);
            document.getElementById('pdfContent').src = fileURL;
            document.getElementById('pdfContent').classList.remove('hidden');
            document.getElementById('textContent').classList.add('hidden');
            speak("เปิดไฟล์ พี ดี เอฟ");
        } else {
            // อ่านไฟล์ Text / Code
            reader.onload = function(e) {
                document.getElementById('textContent').innerText = e.target.result;
                document.getElementById('textContent').classList.remove('hidden');
                document.getElementById('pdfContent').classList.add('hidden');
                speak("อ่านไฟล์ข้อความสำเร็จ");
            };
            reader.readAsText(file);
        }
    }
</script>
'''
