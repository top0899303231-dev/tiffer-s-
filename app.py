<div id="finderPage" class="page">
        <nav class="p-5 glass-purple flex items-center justify-between sticky top-0 z-50">
            <button onclick="switchPage('mainPage')"><i class="fas fa-arrow-left text-purple-400"></i></button>
            <span class="font-bold cyan-neon tracking-tighter">DEEP SEARCH SYSTEM</span>
            <label for="fileInput" class="bg-cyan-500/20 px-3 py-1 rounded-xl border border-cyan-500 text-[10px] font-bold cursor-pointer">
                <i class="fas fa-upload mr-1"></i> โหลดไฟล์
                <input type="file" id="fileInput" class="hidden" multiple onchange="loadFilesToMemory(this)">
            </label>
        </nav>
        
        <main class="p-4 max-w-md mx-auto w-full flex flex-col h-full space-y-4">
            <div class="glass-purple p-4 rounded-3xl border border-purple-500 shadow-lg">
                <p class="text-[10px] text-cyan-400 mb-2 font-bold uppercase"><i class="fas fa-filter mr-1"></i> ระบุชื่อหรือคำที่ต้องการค้นหา</p>
                <div class="relative">
                    <input type="text" id="wordSearch" placeholder="ตัวอย่าง: M8, สกรู, ราคา..." 
                           class="w-full p-4 pl-12 rounded-2xl outline-none search-input font-bold text-lg"
                           onkeyup="deepSearch()">
                    <i class="fas fa-search absolute left-4 top-4 text-purple-500"></i>
                </div>
                <p id="fileStatus" class="text-[9px] text-gray-500 mt-2 text-right">โหลดแล้ว 0 ไฟล์</p>
            </div>

            <div class="flex-1 overflow-y-auto space-y-3 pb-20">
                <div id="searchResultArea">
                    <div class="text-center py-20 opacity-30">
                        <i class="fas fa-microscope text-5xl mb-3 text-purple-900"></i>
                        <p class="text-xs">พิมพ์คำที่ต้องการหา ระบบจะสแกนทุกไฟล์ให้เอง</p>
                    </div>
                </div>
            </div>
        </main>
    </div>

<script>
    let loadedFilesData = []; // เก็บเนื้อหาไฟล์ทั้งหมดไว้ในเครื่อง

    // 1. โหลดไฟล์เข้าหน่วยความจำ
    async function loadFilesToMemory(input) {
        const files = Array.from(input.files);
        loadedFilesData = []; // ล้างค่าเก่า
        
        for (let file of files) {
            const content = await file.text();
            loadedFilesData.push({
                name: file.name,
                text: content
            });
        }
        
        document.getElementById('fileStatus').innerText = `โหลดแล้ว ${loadedFilesData.length} ไฟล์`;
        speak("โหลดไฟล์ " + loadedFilesData.length + " ไฟล์ พร้อมสแกนครับ");
        deepSearch(); // สั่งค้นหาทันทีที่โหลดเสร็จ
    }

    // 2. ระบบค้นหาคำในเนื้อหาไฟล์ (ระบุชื่อหาคำ)
    function deepSearch() {
        const keyword = document.getElementById('wordSearch').value.toLowerCase();
        const resultArea = document.getElementById('searchResultArea');
        resultArea.innerHTML = "";

        if (keyword === "") {
            resultArea.innerHTML = '<p class="text-center text-[10px] text-purple-900 py-10">พิมพ์คำเพื่อเริ่มค้นหา...</p>';
            return;
        }

        let foundCount = 0;

        loadedFilesData.forEach(file => {
            const lines = file.text.split('\n');
            const matchedLines = lines.filter(line => line.toLowerCase().includes(keyword));

            if (matchedLines.length > 0) {
                foundCount++;
                const fileBox = document.createElement('div');
                fileBox.className = "glass-purple p-4 rounded-2xl border-l-4 border-cyan-500 mb-3";
                
                let resultsHtml = `<p class="text-[10px] font-bold text-purple-400 mb-2 uppercase italic border-b border-purple-900 pb-1">${file.name}</p>`;
                
                matchedLines.forEach(line => {
                    // ไฮไลท์คำที่หา
                    const highlightedLine = line.replace(new RegExp(keyword, 'gi'), (match) => `<span class="bg-cyan-500 text-black px-1 rounded">${match}</span>`);
                    resultsHtml += `<p class="text-xs text-white leading-relaxed mb-2 font-mono">🔍 ...${highlightedLine}...</p>`;
                });

                fileBox.innerHTML = resultsHtml;
                resultArea.appendChild(fileBox);
            }
        });

        if (foundCount === 0 && loadedFilesData.length > 0) {
            resultArea.innerHTML = `<div class="text-center py-10 text-red-500 text-xs font-bold animate-pulse">ไม่พบคำว่า "${keyword}" ในไฟล์ทั้งหมด</div>`;
        }
    }
</script>
