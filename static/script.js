document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('themeToggle');
    themeToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
        themeToggle.textContent = document.body.classList.contains('dark-mode') ? '☀️ Light Mode' : '🌙 Dark Mode';
    });

    // Note: Tab navigation is now done via server-side routing (<a> tags)

    // Downloader Logic
    const df = document.getElementById('downloadForm');
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            document.getElementById('urlInput').placeholder = 'Paste your link here...';
        });
    });
    df.addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = document.getElementById('urlInput').value.trim();
        if (!url) return;
        resetBox(document.getElementById('error'), document.getElementById('results'), document.getElementById('loading'));
        try {
            const res = await fetch('/api/download', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url }) });
            const data = await res.json();
            if (!res.ok) throw new Error(data.error || 'Invalid URL.');
            renderDownloaderResults(data, url);
        } catch (err) { showError(document.getElementById('error'), err.message, document.getElementById('loading')); }
    });

    function renderDownloaderResults(data, originalUrl) {
        const rc = document.getElementById('results');
        rc.innerHTML = `<h3 class="video-title">${data.title}</h3>`;
        const grid = document.createElement('div');
        grid.className = 'format-grid';
        if (!data.formats || !data.formats.length) grid.innerHTML = '<p>No formats.</p>';
        else {
            const seen = new Set();
            data.formats.forEach(f => {
                const id = `${f.type}-${f.quality}-${f.ext}`;
                if (!seen.has(id)) {
                    seen.add(id);
                    const card = document.createElement('div'); card.className = 'format-card';
                    card.innerHTML = `<span class="format-quality">${f.quality}</span><span class="format-type">${f.type} • ${f.ext}</span>`;
                    const btn = document.createElement('a'); btn.className = 'btn-download';
                    if (f.type === 'video' && !f.has_audio) {
                        btn.href = `/api/download_file?url=${encodeURIComponent(originalUrl)}&format_id=${f.format_id}`;
                        btn.textContent = 'Mux Audio & DL';
                    } else { btn.href = f.url; btn.target = '_blank'; btn.textContent = 'Download'; }
                    card.appendChild(btn); grid.appendChild(card);
                }
            });
        }
        rc.appendChild(grid); rc.classList.remove('hidden'); document.getElementById('loading').classList.add('hidden');
        document.getElementById('ad-results').classList.remove('hidden');
    }

    // Helper functions
    function resetBox(eBox, rBox, lBox) { eBox.classList.add('hidden'); rBox.classList.add('hidden'); rBox.innerHTML = ''; lBox.classList.remove('hidden'); }
    function showError(eBox, msg, lBox) { eBox.textContent = msg; eBox.classList.remove('hidden'); lBox.classList.add('hidden'); }
    function handleAPIResult(res, data, rBox, lBox) {
        lBox.classList.add('hidden');
        if (!res.ok) { throw new Error(data.error || 'Failed'); }
        rBox.innerHTML = `<h3>Ready: ${data.title || data.message || 'File'}</h3><br><a href="${data.download_url}" class="btn-download" target="_blank">Download File</a>`;
        rBox.classList.remove('hidden');
    }

    // MP3 Converter
    document.getElementById('convertForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const url = document.getElementById('mp3Url').value.trim();
        const bitrate = document.getElementById('mp3Bitrate').value;
        const eBox = document.getElementById('errorMp3'), rBox = document.getElementById('resMp3'), lBox = document.getElementById('loadingMp3');
        resetBox(eBox, rBox, lBox);
        try {
            const res = await fetch('/api/convert-mp3', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ url, bitrate }) });
            handleAPIResult(res, await res.json(), rBox, lBox);
        } catch (err) { showError(eBox, err.message, lBox); }
    });

    // Audio Trimmer
    document.getElementById('trimForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData();
        fd.append('file', document.getElementById('trimFile').files[0]);
        fd.append('start', document.getElementById('trimStart').value.trim());
        fd.append('end', document.getElementById('trimEnd').value.trim());
        const eBox = document.getElementById('errorTrim'), rBox = document.getElementById('resTrim'), lBox = document.getElementById('loadingTrim');
        resetBox(eBox, rBox, lBox);
        try {
            const res = await fetch('/api/trim-audio', { method: 'POST', body: fd });
            handleAPIResult(res, await res.json(), rBox, lBox);
        } catch (err) { showError(eBox, err.message, lBox); }
    });

    // Audio Merge
    document.getElementById('audioMergeForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData();
        Array.from(document.getElementById('audioMergeFiles').files).forEach(f => fd.append('files', f));
        const eBox = document.getElementById('errorAudioMerge'), rBox = document.getElementById('resAudioMerge'), lBox = document.getElementById('loadingAudioMerge');
        resetBox(eBox, rBox, lBox);
        try {
            const res = await fetch('/api/merge-audio', { method: 'POST', body: fd });
            handleAPIResult(res, await res.json(), rBox, lBox);
        } catch (err) { showError(eBox, err.message, lBox); }
    });

    // Video Merge
    document.getElementById('videoMergeForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData();
        Array.from(document.getElementById('videoMergeFiles').files).forEach(f => fd.append('files', f));
        const eBox = document.getElementById('errorVideoMerge'), rBox = document.getElementById('resVideoMerge'), lBox = document.getElementById('loadingVideoMerge');
        resetBox(eBox, rBox, lBox);
        try {
            const res = await fetch('/api/merge-video', { method: 'POST', body: fd });
            handleAPIResult(res, await res.json(), rBox, lBox);
        } catch (err) { showError(eBox, err.message, lBox); }
    });

    // Torrent
    document.getElementById('torrentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const magnet = document.getElementById('torrentMagnet').value.trim();
        const eBox = document.getElementById('errorTorrent'), rBox = document.getElementById('resTorrent'), lBox = document.getElementById('loadingTorrent');
        resetBox(eBox, rBox, lBox);
        try {
            const res = await fetch('/api/torrent', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ magnet }) });
            const data = await res.json();
            lBox.classList.add('hidden');
            if(!res.ok) throw new Error(data.error || 'Failed');
            rBox.innerHTML = `<h3>Success: ${data.message}</h3>`;
            rBox.classList.remove('hidden');
        } catch (err) { showError(eBox, err.message, lBox); }
    });
});
