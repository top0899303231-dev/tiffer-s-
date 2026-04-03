<div id="filePage" class="page">
        <nav class="p-5 glass-purple flex items-center justify-between sticky top-0 z-50">
            <div class="flex items-center space-x-4">
                <button onclick="switchPage('mainPage')"><i class="fas fa-arrow-left text-purple-400"></i></button>
                <span class="font-bold purple-neon">FILE FINDER</span>
            </div>
            <label for="fileInput" class="cursor-pointer text-cyan-400 bg-cyan-900/30 p-2 rounded-xl border border-cyan-500">
                <i class="fas fa-plus-circle"></i> นำเข้าไฟล์
                <input type="file" id="fileInput" class="hidden" multiple onchange="importFiles(this)">
            </label>
        </nav>
        
        <main class="p-4 max-w-md mx-auto w-full space-y-4">
            <div class="relative">
                <i class="fas fa-search absolute left-4 top-4 text-purple-500"></i>
                <input type="text" id="fileSearch" placeholder="พิมพ์ชื่อไฟล์ที่ต้องการหา..." 
                       class="w-full p-4 pl-12 rounded-2xl outline-none bg-black/60 border border-purple-900 text-cyan-400 font-bold"
                       onkeyup="filterFiles()">
            </div>

            <div id="fileList" class="space-y-2 max-h-[200px] overflow-y-auto">
                <p class="text-[10px] text-center text-purple-800">ยังไม่มีไฟล์ในระบบ (กดนำเข้าไฟล์มุมขวา)</p>
            </div>

            <div class="glass-purple p-4 rounded-3xl min-h-[300px] border border-purple-900">
                <div id="fileHeader" class="flex justify-between items-center mb-3 hidden">
                    <span id="currentFileName" class="text-xs text-cyan-400 font-bold truncate pr-4"></span>
                    <button onclick="closeFile()" class="text-red-500 text-xs font-bold uppercase">ปิด [X]</button>
                </div>
                <div id="readerEmpty" class="text-center py-20 text-purple-900 opacity-40">
                    <i class="fas fa-file-signature text-5xl mb-2"></i>
                    <p class="text-xs">เลือกไฟล์ด้านบนเพื่ออ่านเนื้อหา</p>
                </div>
                <pre id="textContent" class="text-sm text-white whitespace-pre-wrap font-mono hidden"></pre>
            </div>
        </main>
    </div>

<script>
    let allFiles = []; // เก็บข้อมูลไฟล์ทั้งหมดที่นำเข้า

    // 📥 ฟังก์ชันนำเข้าไฟล์ (รองรับหลายไฟล์พร้อมกัน)
    function importFiles(input) {
        const files = Array.from(input.files);
        files.forEach(file => {
            allFiles.push(file);
        });
        updateFileList(allFiles);
        speak("นำเข้า " + files.length + " ไฟล์สำเร็จ");
    }

    // 📋 อัปเดตรายการไฟล์ในหน้าจอ
    function updateFileList(filesToDisplay) {
        const listContainer = document.getElementById('fileList');
        listContainer.innerHTML = "";
        
        if (filesToDisplay.length === 0) {
            listContainer.innerHTML = '<p class="text-[10px] text-center text-red-900">ไม่พบไฟล์ที่ค้นหา</p>';
            return;
        }

        filesToDisplay.forEach((file, index) => {
            const row = document.createElement('div');
            row.className = "flex justify-between items-center bg-purple-900/20 p-3 rounded-xl border border-purple-900/50 active:bg-purple-600";
            row.onclick = () => viewFile(file);
            row.innerHTML = `
                <div class="flex items-center space-x-3">
                    <i class="fas fa-file-alt text-purple-400"></i>
                    <span class="text-xs text-white truncate w-40">${file.name}</span>
                </div>
                <i class="fas fa-chevron-right text-[10px] text-purple-700"></i>
            `;
            listContainer.appendChild(row);
        });
    }

    // 🔍 ฟังก์ชันค้นหา/กรองชื่อไฟล์
    function filterFiles() {
        const keyword = document.getElementById('fileSearch').value.toLowerCase();
        const filtered = allFiles.filter(f => f.name.toLowerCase().includes(keyword));
        updateFileList(filtered);
    }

    // 📖 ฟังก์ชันแสดงเนื้อหาไฟล์
    function viewFile(file) {
        const reader = new FileReader();
        document.getElementById('fileHeader').classList.remove('hidden');
        document.getElementById('currentFileName').innerText = "กำลังอ่าน: " + file.name;
        document.getElementById('readerEmpty').classList.add('hidden');
        
        reader.onload = function(e) {
            document.getElementById('textContent').innerText = e.target.result;
            document.getElementById('textContent').classList.remove('hidden');
            speak("เปิดไฟล์ " + file.name);
        };
        reader.readAsText(file);
    }

    function closeFile() {
        document.getElementById('fileHeader').classList.add('hidden');
        document.getElementById('textContent').classList.add('hidden');
        document.getElementById('readerEmpty').classList.remove('hidden');
    }
</script>
