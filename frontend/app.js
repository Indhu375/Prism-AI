/* ═══════════════════════════════════════════════════════════════════════
   Prism AI — Frontend Logic
   Tab switching, API calls, result rendering, copy/download
   ═══════════════════════════════════════════════════════════════════════ */

const API_BASE = window.location.origin;

// ─── DOM References ─────────────────────────────────────────────────────
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const overlay = $("#loading-overlay");
const toastBox = $("#toast-container");
const statusDot = $("#status-dot");
const statusTxt = $("#status-text");

// ─── Utilities ──────────────────────────────────────────────────────────
function showLoading() { overlay.classList.remove("hidden"); }
function hideLoading() { overlay.classList.add("hidden"); }

function toast(message, type = "info") {
    const el = document.createElement("div");
    el.className = `toast ${type}`;
    el.textContent = message;
    toastBox.appendChild(el);
    setTimeout(() => el.remove(), 3200);
}

function downloadText(content, filename) {
    const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = filename;
    a.click();
    URL.revokeObjectURL(a.href);
}

function downloadImage(url, filename) {
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
}

async function copyText(text) {
    try {
        await navigator.clipboard.writeText(text);
        toast("Copied to clipboard!", "success");
    } catch {
        toast("Copy failed — try manually.", "error");
    }
}

// ─── Health Check ───────────────────────────────────────────────────────
async function checkHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(4000) });
        if (res.ok) {
            statusDot.className = "status-dot online";
            statusTxt.textContent = "API Online";
        } else {
            throw new Error();
        }
    } catch {
        statusDot.className = "status-dot offline";
        statusTxt.textContent = "API Offline";
    }
}

// Check immediately and every 30 seconds
checkHealth();
setInterval(checkHealth, 30000);

// ─── Tab Switching ──────────────────────────────────────────────────────
$$(".tab-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
        // Deactivate all
        $$(".tab-btn").forEach((b) => b.classList.remove("active"));
        $$(".tab-panel").forEach((p) => p.classList.remove("active"));

        // Activate selected
        btn.classList.add("active");
        $(`#panel-${btn.dataset.tab}`).classList.add("active");
    });
});

// ─── Range Sliders ──────────────────────────────────────────────────────
$("#blog-words").addEventListener("input", (e) => {
    $("#blog-words-val").textContent = e.target.value;
});

$("#video-duration").addEventListener("input", (e) => {
    $("#video-duration-val").textContent = `${e.target.value} min`;
});

$("#image-count").addEventListener("input", (e) => {
    $("#image-count-val").textContent = e.target.value;
});

// ─── API Call Helper ────────────────────────────────────────────────────
async function apiPost(endpoint, body) {
    const res = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: res.statusText }));
        throw new Error(err.detail || `Request failed (${res.status})`);
    }

    return res.json();
}

// ─── Blog Generation ────────────────────────────────────────────────────
let lastBlogContent = "";

$("#blog-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const product_name = $("#blog-product").value.trim();
    const tone = $("#blog-tone").value;
    const word_count = parseInt($("#blog-words").value);

    if (!product_name) return toast("Please enter a product name.", "error");

    showLoading();
    try {
        const data = await apiPost("/generate-blog", { product_name, tone, word_count });
        lastBlogContent = data.generated_blog;

        // Render the blog content
        const resultEl = $("#blog-result");
        resultEl.innerHTML = "";
        resultEl.style.whiteSpace = "pre-wrap";
        resultEl.textContent = data.generated_blog;

        toast("Blog generated successfully! ✨", "success");
    } catch (err) {
        toast(`Error: ${err.message}`, "error");
    } finally {
        hideLoading();
    }
});

// Copy & Download blog
$("#blog-copy").addEventListener("click", () => {
    if (lastBlogContent) copyText(lastBlogContent);
    else toast("Generate a blog first.", "info");
});

$("#blog-download").addEventListener("click", () => {
    if (lastBlogContent) downloadText(lastBlogContent, "prism-blog.txt");
    else toast("Generate a blog first.", "info");
});

// ─── Video Script Generation ────────────────────────────────────────────
let lastVideoContent = "";

$("#video-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const product_name = $("#video-product").value.trim();
    const tone = $("#video-tone").value;
    const duration = parseInt($("#video-duration").value);

    if (!product_name) return toast("Please enter a product name.", "error");

    showLoading();
    try {
        const data = await apiPost("/generate-video-script", { product_name, tone, duration });
        lastVideoContent = data.generated_script;

        const resultEl = $("#video-result");
        resultEl.innerHTML = "";
        resultEl.style.whiteSpace = "pre-wrap";
        resultEl.textContent = data.generated_script;

        toast("Video script generated! 🎬", "success");
    } catch (err) {
        toast(`Error: ${err.message}`, "error");
    } finally {
        hideLoading();
    }
});

// Copy & Download video script
$("#video-copy").addEventListener("click", () => {
    if (lastVideoContent) copyText(lastVideoContent);
    else toast("Generate a script first.", "info");
});

$("#video-download").addEventListener("click", () => {
    if (lastVideoContent) downloadText(lastVideoContent, "prism-video-script.txt");
    else toast("Generate a script first.", "info");
});

// ─── Image Generation ───────────────────────────────────────────────────
let lastImageUrls = [];

$("#image-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const product_name = $("#image-product").value.trim();
    const style = $("#image-style").value;
    const platform = $("#image-platform").value;
    const n = parseInt($("#image-count").value);

    if (!product_name) return toast("Please enter a product name.", "error");

    showLoading();
    try {
        const data = await apiPost("/generate-image", { product_name, style, platform, n });

        // Store URLs for download
        lastImageUrls = data.images.map((img) => ({
            url: `${API_BASE}${img.image_url}`,
            filename: img.filename,
        }));

        // Render images
        const resultEl = $("#image-result");
        resultEl.innerHTML = "";

        const grid = document.createElement("div");
        grid.className = "image-grid";

        data.images.forEach((img) => {
            const imgEl = document.createElement("img");
            imgEl.src = `${API_BASE}${img.image_url}`;
            imgEl.alt = `Generated image for ${product_name}`;
            imgEl.loading = "lazy";
            // Click to open full-size in new tab
            imgEl.addEventListener("click", () => window.open(imgEl.src, "_blank"));
            grid.appendChild(imgEl);
        });

        resultEl.appendChild(grid);

        // Show prompt
        const promptBox = $("#image-prompt-box");
        promptBox.classList.remove("hidden");
        $("#image-prompt-text").textContent = data.image_prompt;

        toast("Image generated! 🖼️", "success");
    } catch (err) {
        toast(`Error: ${err.message}`, "error");
    } finally {
        hideLoading();
    }
});

// Download image(s)
$("#image-download-btn").addEventListener("click", () => {
    if (lastImageUrls.length === 0) {
        toast("Generate an image first.", "info");
        return;
    }
    lastImageUrls.forEach((img) => downloadImage(img.url, img.filename));
});
