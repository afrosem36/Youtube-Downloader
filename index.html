<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HD Pro Downloader</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">

    <style>
        @keyframes fadeSlideIn { from { opacity:0; transform:translateY(-14px) scale(.97); } to { opacity:1; transform:none; } }
        @keyframes thumbReveal  { from { opacity:0; transform:scale(.93); } to { opacity:1; transform:none; } }
        @keyframes toastIn      { from { opacity:0; transform:translateX(110%); } to { opacity:1; transform:none; } }
        @keyframes toastOut     { from { opacity:1; transform:none; } to { opacity:0; transform:translateX(110%); } }
        @keyframes pulseRing    { 0% { transform:scale(1); opacity:.55; } 100% { transform:scale(1.13); opacity:0; } }
        @keyframes bounceHand   { 0%,100% { transform:translateY(0); } 50% { transform:translateY(-7px); } }
        @keyframes shimmer      { 0% { background-position:-400px 0; } 100% { background-position:400px 0; } }
        @keyframes barFlow      { 0% { background-position:0 0; } 100% { background-position:40px 0; } }

        .fade-in      { animation: fadeSlideIn .38s ease both; }
        .thumb-anim   { animation: thumbReveal .45s cubic-bezier(.22,1,.36,1) both; }
        .toast-in     { animation: toastIn .3s ease both; }
        .toast-out    { animation: toastOut .3s ease forwards; }
        .pulse-ring   { animation: pulseRing 1.4s ease-out infinite; }
        .bounce-hand  { animation: bounceHand 1s ease-in-out infinite; }

        .card-glow    { box-shadow: 0 0 50px rgba(239,68,68,.1), 0 4px 40px rgba(0,0,0,.7); }
        .btn-glow-red { box-shadow: 0 4px 22px rgba(239,68,68,.4); }
        .btn-glow-grn { box-shadow: 0 4px 22px rgba(34,197,94,.4); }
        .ad-glow      { box-shadow: 0 0 0 2px rgba(251,191,36,.55), 0 0 22px rgba(251,191,36,.18); }

        /* Skeleton shimmer */
        .skeleton {
            background: linear-gradient(90deg, #1e293b 25%, #334155 50%, #1e293b 75%);
            background-size: 400px 100%;
            animation: shimmer 1.6s infinite;
        }

        /* Animated progress bar stripes */
        .progress-bar-animated {
            background: linear-gradient(
                45deg,
                rgba(255,255,255,.12) 25%,
                transparent 25%,
                transparent 50%,
                rgba(255,255,255,.12) 50%,
                rgba(255,255,255,.12) 75%,
                transparent 75%
            );
            background-size: 40px 40px;
            animation: barFlow .7s linear infinite;
        }

        select option { background:#0f172a; }

        /* Scrollbar */
        ::-webkit-scrollbar { width:6px; }
        ::-webkit-scrollbar-track { background:#0f172a; }
        ::-webkit-scrollbar-thumb { background:#334155; border-radius:99px; }
    </style>
</head>
<body class="bg-slate-950 text-white min-h-screen flex flex-col items-center justify-center p-4 font-sans">

    <!-- ═══════════════════════════════════════════════
         ONCLICK POP AD — fires on the 2nd click only
    ════════════════════════════════════════════════ -->
    <script>
        (function() {
            let _clickCount = 0;
            let _popLoaded  = false;
            document.addEventListener('click', function() {
                _clickCount++;
                if (_clickCount === 2 && !_popLoaded) {
                    _popLoaded = true;
                    var s = document.createElement('script');
                    s.src = 'https://pl28816171.effectivegatecpm.com/ae/bb/45/aebb4548ea36d292822e96b52b5dbc4f.js';
                    document.head.appendChild(s);
                }
            }, true);
        })();
    </script>

    <!-- Toast Container -->
    <div id="toastContainer" class="fixed top-4 right-4 z-50 flex flex-col gap-2 pointer-events-none"></div>

    <!-- ── Main Card ── -->
    <div class="max-w-md w-full bg-slate-900 rounded-3xl card-glow p-7 border border-slate-800 mb-4">

        <!-- Header -->
        <div class="text-center mb-6">
            <div class="inline-flex items-center gap-2 bg-red-600/10 border border-red-600/30 rounded-full px-4 py-1 mb-3">
                <i class="fa-solid fa-bolt text-red-400 text-xs"></i>
                <span class="text-red-400 text-xs font-bold tracking-widest uppercase">4K Ultra Supported</span>
            </div>
            <h1 class="text-3xl font-black text-white italic tracking-tight">HD PRO <span class="text-red-500">DOWNLOADER</span></h1>
            <p class="text-slate-500 text-xs mt-1">Fast • Free • High Quality</p>
        </div>

        <!-- URL Input -->
        <div class="space-y-3">
            <div class="relative">
                <i class="fa-brands fa-youtube absolute left-4 top-1/2 -translate-y-1/2 text-red-500 text-lg pointer-events-none"></i>
                <input type="text" id="videoUrl"
                    placeholder="Paste YouTube URL here…"
                    onkeydown="if(event.key==='Enter') fetchInfo()"
                    class="w-full pl-11 pr-4 py-4 bg-slate-800 border border-slate-700 rounded-xl outline-none focus:ring-2 focus:ring-red-500 transition placeholder:text-slate-500 text-sm">
            </div>
            <button onclick="fetchInfo()" id="fetchBtn"
                class="w-full py-4 bg-red-600 rounded-xl font-bold hover:bg-red-500 active:scale-95 transition btn-glow-red flex items-center justify-center gap-2 text-sm">
                <i id="fetchBtnIcon" class="fa-solid fa-magnifying-glass"></i>
                <span id="fetchBtnText">ANALYZE VIDEO</span>
            </button>
        </div>

        <!-- ── Loading State ── -->
        <div id="loadingState" class="hidden mt-6">

            <!-- Step label + timer -->
            <div class="flex items-center justify-between mb-2">
                <span id="loadingStepLabel" class="text-xs text-slate-400 font-semibold">
                    <i class="fa-solid fa-satellite-dish text-red-400 mr-1 animate-pulse"></i>
                    Connecting to YouTube…
                </span>
                <span id="loadingTimer" class="text-xs font-black text-red-400 tabular-nums">0s</span>
            </div>

            <!-- Progress bar track -->
            <div class="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden mb-3">
                <div id="loadingBar"
                    class="h-full bg-red-500 rounded-full progress-bar-animated transition-all duration-500"
                    style="width:0%"></div>
            </div>

            <!-- Step dots -->
            <div class="flex items-center justify-between px-1">
                <div id="ldot1" class="flex flex-col items-center gap-1">
                    <div class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></div>
                    <span class="text-slate-500 text-[10px]">Connect</span>
                </div>
                <div id="ldot2" class="flex flex-col items-center gap-1 opacity-40">
                    <div class="w-2 h-2 rounded-full bg-slate-600"></div>
                    <span class="text-slate-500 text-[10px]">Fetch</span>
                </div>
                <div id="ldot3" class="flex flex-col items-center gap-1 opacity-40">
                    <div class="w-2 h-2 rounded-full bg-slate-600"></div>
                    <span class="text-slate-500 text-[10px]">Formats</span>
                </div>
                <div id="ldot4" class="flex flex-col items-center gap-1 opacity-40">
                    <div class="w-2 h-2 rounded-full bg-slate-600"></div>
                    <span class="text-slate-500 text-[10px]">Ready</span>
                </div>
            </div>

            <!-- Skeleton preview -->
            <div class="mt-4 space-y-2">
                <div class="skeleton w-full h-32 rounded-xl"></div>
                <div class="skeleton w-3/4 h-3 rounded-full"></div>
                <div class="skeleton w-1/2 h-3 rounded-full"></div>
            </div>
        </div>

        <!-- ── Step 2 — Results ── -->
        <div id="step2" class="hidden mt-6 border-t border-slate-800 pt-5 fade-in">

            <!-- Permanent Banner Ad -->
            <div class="mb-5 flex items-center justify-center overflow-hidden rounded-xl border border-slate-700/50 bg-slate-800/40 min-h-[60px]">
                <script>
                    atOptions = {
                        'key' : 'ec7dcba92468f7d44abe2402b6b740f9',
                        'format' : 'iframe',
                        'height' : 250,
                        'width' : 300,
                        'params' : {}
                    };
                </script>
                <script src="https://www.highperformanceformat.com/ec7dcba92468f7d44abe2402b6b740f9/invoke.js"></script>
            </div>

            <!-- Thumbnail -->
            <div class="relative mb-4 rounded-2xl overflow-hidden border border-slate-700/80 shadow-2xl">
                <img id="thumb" class="w-full thumb-anim object-cover" src="" alt="Thumbnail">
                <div id="durationBadge" class="absolute bottom-2 right-2 bg-black/80 backdrop-blur-sm text-white text-xs font-bold px-2.5 py-1 rounded-lg hidden">
                    <i class="fa-regular fa-clock mr-1 text-red-400"></i><span id="durationText"></span>
                </div>
                <div class="absolute top-2 left-2 bg-red-600/90 backdrop-blur-sm text-white text-[10px] font-black px-2 py-0.5 rounded-md uppercase tracking-wider">
                    YouTube
                </div>
            </div>

            <!-- Title -->
            <h3 id="videoTitle" class="font-semibold text-sm mb-4 text-slate-200 leading-snug line-clamp-2"></h3>

            <!-- Download Form -->
            <form id="dlForm" onsubmit="handleDownload(event)">
                <input type="hidden" id="formUrl">
                <input type="hidden" id="unlockToken">

                <!-- Resolution + quality badge -->
                <div class="relative mb-1">
                    <select id="resSelect" onchange="onResChange()"
                        class="w-full p-4 pr-10 bg-slate-800 border border-slate-700 rounded-xl focus:ring-2 focus:ring-green-500 outline-none appearance-none text-sm cursor-pointer font-semibold">
                    </select>
                    <i class="fa-solid fa-chevron-down absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 pointer-events-none text-xs"></i>
                </div>

                <!-- Quality info bar -->
                <div id="qualityBar" class="flex items-center gap-2 mb-4 px-1 text-xs text-slate-500">
                    <i id="qualityIcon" class="fa-solid fa-circle-info"></i>
                    <span id="qualityLabel">Select a resolution</span>
                </div>

                <!-- Download button -->
                <button type="submit" id="dlBtn"
                    class="w-full py-4 bg-green-600 rounded-xl font-bold hover:bg-green-500 active:scale-95 transition btn-glow-grn flex items-center justify-center gap-2 text-sm">
                    <i id="dlBtnIcon" class="fa-solid fa-cloud-arrow-down"></i>
                    <span id="dlBtnText">DOWNLOAD NOW</span>
                </button>

                <!-- Download progress bar (shown while downloading) -->
                <div id="dlProgressWrap" class="hidden mt-3">
                    <div class="flex justify-between text-xs text-slate-400 mb-1">
                        <span>Preparing your file…</span>
                        <span id="dlProgressPct" class="font-bold text-green-400">0%</span>
                    </div>
                    <div class="w-full bg-slate-800 rounded-full h-2 overflow-hidden">
                        <div id="dlProgressBar" class="h-full bg-green-500 rounded-full progress-bar-animated transition-all duration-300" style="width:0%"></div>
                    </div>
                </div>

                <p id="lockNotice" class="hidden text-center text-xs text-amber-400 mt-3 font-semibold">
                    <i class="fa-solid fa-lock mr-1"></i>Click the ad to unlock 4K download
                </p>
            </form>
        </div>
    </div>

    <!-- ── Container Ad (below card) ── -->
    <div class="max-w-md w-full flex items-center justify-center mb-4">
        <div id="container-e2d939f7ebf37a8b70ec44178e001fe8" class="overflow-hidden rounded-xl border border-slate-800 bg-slate-900/60 min-h-[60px] flex items-center justify-center w-full"></div>
    </div>
    <script async data-cfasync="false" src="https://pl28816183.effectivegatecpm.com/e2d939f7ebf37a8b70ec44178e001fe8/invoke.js"></script>

    <!-- ══════════════════════════════════════════════
         4K UNLOCK MODAL
    ═══════════════════════════════════════════════ -->
    <div id="unlockModal" class="hidden fixed inset-0 bg-black/85 backdrop-blur-sm flex items-center justify-center z-40 p-4">
        <div class="bg-slate-900 border border-slate-700 rounded-3xl p-6 max-w-sm w-full text-center shadow-2xl fade-in">

            <div class="inline-flex items-center justify-center w-14 h-14 rounded-full bg-amber-500/15 border border-amber-500/30 mb-3">
                <i class="fa-solid fa-crown text-amber-400 text-2xl"></i>
            </div>
            <h2 class="text-xl font-black mb-1">Unlock 4K Download</h2>

            <!-- Step indicators -->
            <div class="flex items-center justify-center gap-2 mb-5">
                <div id="stepDot1" class="flex items-center gap-1.5 text-xs font-bold text-amber-400 transition-all duration-300">
                    <span class="w-6 h-6 rounded-full bg-amber-500 text-black flex items-center justify-center font-black text-xs">1</span>
                    Click Ad
                </div>
                <div class="flex-1 h-px bg-slate-700 max-w-[36px]"></div>
                <div id="stepDot2" class="flex items-center gap-1.5 text-xs font-bold text-slate-500 transition-all duration-300">
                    <span id="step2Circle" class="w-6 h-6 rounded-full bg-slate-700 text-slate-400 flex items-center justify-center font-black text-xs transition-all duration-300">2</span>
                    Unlock
                </div>
            </div>

            <!-- Instruction -->
            <p id="adInstruction" class="text-slate-400 text-sm mb-3">
                <i class="fa-solid fa-hand-pointer text-amber-400 mr-1"></i>
                Click the banner below to unlock 4K
            </p>

            <!-- Clickable ad banner -->
            <div id="adClickWrapper"
                class="relative mb-4 rounded-xl overflow-hidden border-2 border-amber-500/70 bg-slate-800/60 cursor-pointer ad-glow"
                onclick="onAdClicked()">
                <div class="absolute inset-0 rounded-xl border-2 border-amber-400 pulse-ring pointer-events-none"></div>
                <div id="adClickOverlay"
                    class="absolute inset-0 z-10 flex flex-col items-center justify-center bg-black/50 rounded-xl pointer-events-none">
                    <i class="fa-solid fa-hand-pointer text-amber-300 text-3xl mb-2 bounce-hand"></i>
                    <span class="text-amber-200 text-xs font-black uppercase tracking-widest bg-black/60 px-3 py-1 rounded-full">Tap to Unlock 4K</span>
                </div>
                <script>
                    atOptions = {
                        'key' : 'ec7dcba92468f7d44abe2402b6b740f9',
                        'format' : 'iframe',
                        'height' : 250,
                        'width' : 300,
                        'params' : {}
                    };
                </script>
                <script src="https://www.highperformanceformat.com/ec7dcba92468f7d44abe2402b6b740f9/invoke.js"></script>
            </div>

            <!-- Success box -->
            <div id="adStatusBox" class="hidden mb-4 p-3 rounded-xl bg-green-600/15 border border-green-500/40 fade-in">
                <p class="text-green-400 text-sm font-bold">
                    <i class="fa-solid fa-circle-check mr-1"></i>
                    Ad opened! You can now unlock 4K.
                </p>
            </div>

            <!-- Unlock button -->
            <button id="unlockBtn" disabled onclick="completeUnlock()"
                class="w-full py-3 rounded-xl font-bold transition-all flex items-center justify-center gap-2 bg-slate-700 text-slate-500 cursor-not-allowed text-sm">
                <i id="unlockBtnIcon" class="fa-solid fa-lock"></i>
                <span id="unlockBtnText">Click the Ad First</span>
            </button>

            <button onclick="cancelModal()" class="mt-3 text-slate-500 text-xs hover:text-slate-300 transition">
                Cancel
            </button>
        </div>
    </div>

    <!-- ═══════════════════════ SCRIPTS ══════════════════════ -->
    <script>
        let _isDownloading = false;
        let _adClicked     = false;
        let _timerInterval = null;
        let _loadStart     = 0;
        let _dlFakeInterval = null;

        // Loading steps config
        const LOAD_STEPS = [
            { at: 0,   pct: 8,  label: 'Connecting to YouTube…',     dot: 1 },
            { at: 1500, pct: 30, label: 'Fetching video metadata…',   dot: 2 },
            { at: 3000, pct: 58, label: 'Reading available formats…', dot: 3 },
            { at: 5500, pct: 82, label: 'Almost ready…',              dot: 4 },
        ];

        // ── Toast ─────────────────────────────────────────────
        function showToast(msg, type = "info", duration = 4000) {
            const colors = {
                success: "bg-green-600 border-green-500",
                error:   "bg-red-700 border-red-500",
                info:    "bg-slate-700 border-slate-600",
                warning: "bg-amber-600 border-amber-500",
            };
            const icons = {
                success: "fa-circle-check", error: "fa-circle-xmark",
                info: "fa-circle-info", warning: "fa-triangle-exclamation"
            };
            const el = document.createElement("div");
            el.className = `pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl border text-sm font-semibold shadow-2xl toast-in max-w-xs ${colors[type]}`;
            el.innerHTML = `<i class="fa-solid ${icons[type]}"></i><span>${msg}</span>`;
            document.getElementById("toastContainer").appendChild(el);
            setTimeout(() => {
                el.classList.replace("toast-in", "toast-out");
                setTimeout(() => el.remove(), 350);
            }, duration);
        }

        // ── Loading progress helpers ──────────────────────────
        function setDot(n, active) {
            const dot = document.getElementById(`ldot${n}`);
            if (!dot) return;
            const circle = dot.querySelector('div');
            if (active) {
                dot.classList.remove('opacity-40');
                circle.className = 'w-2 h-2 rounded-full bg-red-500 animate-pulse';
            } else {
                dot.classList.add('opacity-40');
                circle.className = 'w-2 h-2 rounded-full bg-slate-600';
            }
        }

        function startLoadingUI() {
            _loadStart = Date.now();
            document.getElementById("loadingState").classList.remove("hidden");
            document.getElementById("loadingBar").style.width = "0%";
            document.getElementById("loadingTimer").textContent = "0s";

            // Activate step dots progressively
            LOAD_STEPS.forEach(step => {
                setTimeout(() => {
                    document.getElementById("loadingBar").style.width = step.pct + "%";
                    document.getElementById("loadingStepLabel").innerHTML =
                        `<i class="fa-solid fa-satellite-dish text-red-400 mr-1 animate-pulse"></i>${step.label}`;
                    for (let i = 1; i <= 4; i++) setDot(i, i === step.dot);
                }, step.at);
            });

            // Live second counter
            _timerInterval = setInterval(() => {
                const elapsed = ((Date.now() - _loadStart) / 1000).toFixed(1);
                document.getElementById("loadingTimer").textContent = elapsed + "s";
            }, 100);
        }

        function stopLoadingUI(success) {
            clearInterval(_timerInterval);
            if (success) {
                document.getElementById("loadingBar").style.width = "100%";
                document.getElementById("loadingBar").classList.remove("bg-red-500");
                document.getElementById("loadingBar").classList.add("bg-green-500");
                document.getElementById("loadingStepLabel").innerHTML =
                    '<i class="fa-solid fa-circle-check text-green-400 mr-1"></i>Done!';
                for (let i = 1; i <= 4; i++) setDot(i, true);
                setTimeout(() => document.getElementById("loadingState").classList.add("hidden"), 600);
            } else {
                document.getElementById("loadingBar").classList.add("bg-red-700");
                document.getElementById("loadingStepLabel").innerHTML =
                    '<i class="fa-solid fa-circle-xmark text-red-400 mr-1"></i>Failed.';
                setTimeout(() => document.getElementById("loadingState").classList.add("hidden"), 1200);
            }
        }

        // ── Fetch video info ──────────────────────────────────
        async function fetchInfo() {
            const url = document.getElementById("videoUrl").value.trim();
            if (!url) { showToast("Please paste a YouTube URL first.", "warning"); return; }

            // Hide previous results
            document.getElementById("step2").classList.add("hidden");
            document.getElementById("loadingBar").classList.remove("bg-green-500", "bg-red-700");
            document.getElementById("loadingBar").classList.add("bg-red-500");

            setFetchBtnLoading(true);
            startLoadingUI();

            try {
                const res  = await fetch("/get_info", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ url })
                });
                const data = await res.json();
                if (!res.ok || data.status === "error") {
                    stopLoadingUI(false);
                    showToast(data.message || "Failed to fetch video info.", "error");
                    return;
                }
                stopLoadingUI(true);
                setTimeout(() => populateStep2(data, url), 650);
            } catch {
                stopLoadingUI(false);
                showToast("Network error. Check your connection and try again.", "error");
            } finally {
                setFetchBtnLoading(false);
            }
        }

        function setFetchBtnLoading(on) {
            document.getElementById("fetchBtn").disabled = on;
            document.getElementById("fetchBtnIcon").className = on
                ? "fa-solid fa-spinner animate-spin"
                : "fa-solid fa-magnifying-glass";
            document.getElementById("fetchBtnText").textContent = on ? "Analyzing…" : "ANALYZE VIDEO";
        }

        function populateStep2(data, url) {
            document.getElementById("step2").classList.remove("hidden");
            document.getElementById("thumb").src = data.thumbnail;
            document.getElementById("videoTitle").textContent = data.title;
            document.getElementById("formUrl").value = url;

            if (data.duration && data.duration !== "Unknown") {
                document.getElementById("durationText").textContent = data.duration;
                document.getElementById("durationBadge").classList.remove("hidden");
            }

            const select = document.getElementById("resSelect");
            select.innerHTML = "";
            (data.resolutions || []).forEach(res => {
                const label = res >= 2160 ? " [4K ULTRA 🔒]" : res >= 1080 ? " [Full HD]" : res >= 720 ? " [HD]" : res >= 480 ? " [SD]" : " [Low]";
                const opt = document.createElement("option");
                opt.value = res;
                opt.textContent = `${res}p${label}`;
                select.appendChild(opt);
            });
            onResChange();
        }

        // ── Resolution change ─────────────────────────────────
        function onResChange() {
            const res  = parseInt(document.getElementById("resSelect").value);
            const btn  = document.getElementById("dlBtn");
            const icon = document.getElementById("dlBtnIcon");
            const lock = document.getElementById("lockNotice");
            const qi   = document.getElementById("qualityIcon");
            const ql   = document.getElementById("qualityLabel");

            if (res >= 2160) {
                btn.className  = "w-full py-4 bg-amber-600 rounded-xl font-bold hover:bg-amber-500 active:scale-95 transition flex items-center justify-center gap-2 text-sm";
                icon.className = "fa-solid fa-lock";
                document.getElementById("dlBtnText").textContent = "UNLOCK & DOWNLOAD 4K";
                lock.classList.remove("hidden");
                qi.className = "fa-solid fa-star text-amber-400";
                ql.textContent = "Premium 4K Ultra HD — Ad unlock required";
                ql.className = "text-amber-400 font-semibold";
            } else {
                btn.className  = "w-full py-4 bg-green-600 rounded-xl font-bold hover:bg-green-500 active:scale-95 transition btn-glow-grn flex items-center justify-center gap-2 text-sm";
                icon.className = "fa-solid fa-cloud-arrow-down";
                document.getElementById("dlBtnText").textContent = "DOWNLOAD NOW";
                lock.classList.add("hidden");
                const tag = res >= 1080 ? "Full HD — Great quality" : res >= 720 ? "HD — Good quality" : "Standard / Low quality";
                qi.className = "fa-solid fa-circle-info text-slate-400";
                ql.textContent = tag;
                ql.className = "text-slate-500";
            }
        }

        // ── Download ──────────────────────────────────────────
        function handleDownload(e) {
            e.preventDefault();
            if (_isDownloading) return;
            const res = parseInt(document.getElementById("resSelect").value);
            res === 2160 ? openUnlockModal() : submitDownload();
        }

        async function submitDownload() {
            if (_isDownloading) return;
            _isDownloading = true;

            const dlBtn = document.getElementById("dlBtn");
            dlBtn.disabled = true;
            document.getElementById("dlBtnIcon").className = "fa-solid fa-spinner animate-spin";
            document.getElementById("dlBtnText").textContent = "PREPARING FILE…";

            // Show fake progress bar while server processes
            showDlProgress(true);
            startFakeProgress();

            const form = new FormData();
            form.append("url",          document.getElementById("formUrl").value);
            form.append("resolution",   document.getElementById("resSelect").value);
            form.append("unlock_token", document.getElementById("unlockToken").value);

            try {
                const res = await fetch("/download", { method: "POST", body: form });
                if (!res.ok) {
                    const err = await res.json().catch(() => ({ message: "Unknown server error." }));
                    stopFakeProgress(false);
                    if (res.status === 403) {
                        showToast("4K token expired. Please unlock again.", "warning");
                        document.getElementById("unlockToken").value = "";
                    } else {
                        showToast(err.message || "Download failed.", "error");
                    }
                    return;
                }

                stopFakeProgress(true);
                const blob        = await res.blob();
                const disposition = res.headers.get("Content-Disposition") || "";
                const nameMatch   = disposition.match(/filename\*?=(?:UTF-8'')?["']?([^"';\n]+)/i);
                const filename    = nameMatch ? decodeURIComponent(nameMatch[1]) : "video.mp4";
                const a = document.createElement("a");
                a.href = URL.createObjectURL(blob);
                a.download = filename;
                a.click();
                URL.revokeObjectURL(a.href);
                showToast("Download started! Check your downloads folder.", "success", 5000);

            } catch {
                stopFakeProgress(false);
                showToast("Network error during download. Please retry.", "error");
            } finally {
                _isDownloading = false;
                dlBtn.disabled = false;
                onResChange();
                setTimeout(() => showDlProgress(false), 1500);
            }
        }

        function showDlProgress(show) {
            document.getElementById("dlProgressWrap").classList.toggle("hidden", !show);
        }

        function startFakeProgress() {
            let pct = 0;
            clearInterval(_dlFakeInterval);
            _dlFakeInterval = setInterval(() => {
                // Slow down as it approaches 90%
                const step = pct < 30 ? 3 : pct < 60 ? 1.5 : pct < 85 ? 0.5 : 0;
                pct = Math.min(pct + step, 90);
                document.getElementById("dlProgressBar").style.width = pct + "%";
                document.getElementById("dlProgressPct").textContent = Math.round(pct) + "%";
            }, 200);
        }

        function stopFakeProgress(success) {
            clearInterval(_dlFakeInterval);
            const bar = document.getElementById("dlProgressBar");
            const pct = document.getElementById("dlProgressPct");
            if (success) {
                bar.style.width = "100%";
                bar.classList.remove("bg-green-500"); bar.classList.add("bg-green-400");
                pct.textContent = "100%";
            } else {
                bar.classList.remove("bg-green-500"); bar.classList.add("bg-red-500");
                pct.textContent = "Error";
                pct.className = "font-bold text-red-400 text-xs";
            }
        }

        // ── 4K Modal ──────────────────────────────────────────
        function openUnlockModal() {
            _adClicked = false;

            document.getElementById("adClickOverlay").classList.remove("hidden");
            document.getElementById("adClickWrapper").style.pointerEvents = "auto";
            document.getElementById("adStatusBox").classList.add("hidden");
            document.getElementById("adInstruction").innerHTML =
                '<i class="fa-solid fa-hand-pointer text-amber-400 mr-1"></i>Click the banner below to unlock 4K';

            document.getElementById("stepDot1").className = "flex items-center gap-1.5 text-xs font-bold text-amber-400 transition-all duration-300";
            document.getElementById("stepDot2").className = "flex items-center gap-1.5 text-xs font-bold text-slate-500 transition-all duration-300";
            document.getElementById("step2Circle").className = "w-6 h-6 rounded-full bg-slate-700 text-slate-400 flex items-center justify-center font-black text-xs transition-all duration-300";

            const btn = document.getElementById("unlockBtn");
            btn.disabled = true;
            btn.className = "w-full py-3 rounded-xl font-bold transition-all flex items-center justify-center gap-2 bg-slate-700 text-slate-500 cursor-not-allowed text-sm";
            document.getElementById("unlockBtnIcon").className = "fa-solid fa-lock";
            document.getElementById("unlockBtnText").textContent = "Click the Ad First";

            document.getElementById("unlockModal").classList.remove("hidden");
        }

        function cancelModal() {
            document.getElementById("unlockModal").classList.add("hidden");
            _adClicked = false;
        }

        function onAdClicked() {
            if (_adClicked) return;
            _adClicked = true;

            document.getElementById("adClickOverlay").classList.add("hidden");
            document.getElementById("adClickWrapper").style.pointerEvents = "none";

            document.getElementById("stepDot1").className = "flex items-center gap-1.5 text-xs font-bold text-green-400 transition-all duration-300";
            document.getElementById("stepDot2").className = "flex items-center gap-1.5 text-xs font-bold text-amber-400 transition-all duration-300";
            document.getElementById("step2Circle").className = "w-6 h-6 rounded-full bg-amber-500 text-black flex items-center justify-center font-black text-xs transition-all duration-300";

            document.getElementById("adInstruction").innerHTML =
                '<i class="fa-solid fa-circle-check text-green-400 mr-1"></i>Ad opened! Now click Unlock below.';
            document.getElementById("adStatusBox").classList.remove("hidden");

            const btn = document.getElementById("unlockBtn");
            btn.disabled = false;
            btn.className = "w-full py-3 rounded-xl font-bold transition-all flex items-center justify-center gap-2 bg-amber-500 hover:bg-amber-400 text-black cursor-pointer active:scale-95 text-sm";
            document.getElementById("unlockBtnIcon").className = "fa-solid fa-unlock";
            document.getElementById("unlockBtnText").textContent = "Unlock 4K & Download";

            showToast("Ad opened! Click Unlock to get your 4K download.", "info", 3500);
        }

        async function completeUnlock() {
            const btn = document.getElementById("unlockBtn");
            btn.disabled = true;
            document.getElementById("unlockBtnText").textContent = "Unlocking…";
            document.getElementById("unlockBtnIcon").className = "fa-solid fa-spinner animate-spin";

            try {
                const res  = await fetch("/get_token", { method: "POST" });
                const data = await res.json();
                if (data.status === "ok" && data.token) {
                    document.getElementById("unlockToken").value = data.token;
                    showToast("4K unlocked! Starting download…", "success", 5000);
                } else {
                    showToast("Token issue — proceeding anyway.", "warning");
                }
            } catch {
                showToast("Token fetch failed — proceeding anyway.", "warning");
            }

            cancelModal();
            await submitDownload();
        }
    </script>
</body>
</html>
