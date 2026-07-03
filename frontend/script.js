const API_BASE = "https://ai-research-agent-6ka8.onrender.com";

const MAX_QUESTIONS = 3;

const pdfInput      = document.getElementById("pdf-input");
const uploadStatus  = document.getElementById("upload-status");
const docList       = document.getElementById("doc-list");
const chatMessages  = document.getElementById("chat-messages");
const questionInput = document.getElementById("question-input");
const sendBtn       = document.getElementById("send-btn");
const summarizeBtn  = document.getElementById("summarize-btn");
const compareBtn    = document.getElementById("compare-btn");

// ── QUESTION LIMIT ─────────────────────────────
function getQuestionsUsed() {
  return parseInt(localStorage.getItem("questionsUsed") || "0");
}

function incrementQuestionsUsed() {
  localStorage.setItem("questionsUsed", getQuestionsUsed() + 1);
}

function isLimitReached() {
  return getQuestionsUsed() >= MAX_QUESTIONS;
}

function updateInputState() {
  const used = getQuestionsUsed();
  const remaining = MAX_QUESTIONS - used;
  if (isLimitReached()) {
    questionInput.disabled = true;
    sendBtn.disabled = true;
    questionInput.placeholder = "Demo limit reached — see below.";
    showLimitMessage();
  } else {
    questionInput.placeholder = `Ask a question... (${remaining} question${remaining === 1 ? "" : "s"} remaining)`;
  }
}

function showLimitMessage() {
  const existing = document.getElementById("limit-message");
  if (existing) return;
  const msg = document.createElement("div");
  msg.id = "limit-message";
  msg.style.cssText = `
    text-align: center;
    padding: 16px 24px;
    background: #eff6ff;
    border: 1px solid #bfdbfe;
    border-radius: 12px;
    font-size: 13px;
    color: #1e3a5f;
    margin: 0 28px 16px;
  `;
  msg.innerHTML = `
    <strong>Demo limit reached.</strong><br/>
    This demo allows 3 questions per visitor to manage API costs.<br/>
    Interested in the full project? 
    <a href="https://github.com/maheen02mujahid-tech/AI-Research-Agent-" target="_blank" style="color:#2563eb;">View on GitHub</a>
    or connect with me on LinkedIn.
  `;
  const inputBar = document.querySelector(".input-bar");
  inputBar.parentNode.insertBefore(msg, inputBar);
}

// ── UPLOAD PDF ─────────────────────────────────
pdfInput.addEventListener("change", async () => {
  const file = pdfInput.files[0];
  if (!file) return;
  uploadStatus.textContent = "Uploading...";
  uploadStatus.className = "";
  const formData = new FormData();
  formData.append("file", file);
  try {
    const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: formData });
    if (!res.ok) throw new Error("Upload failed");
    uploadStatus.textContent = "Uploaded successfully";
    uploadStatus.className = "success";
    const li = document.createElement("li");
    li.textContent = file.name;
    docList.appendChild(li);
    addMessage("bot", `${file.name} has been uploaded and indexed. You can now ask questions about it.`);
  } catch (err) {
    uploadStatus.textContent = "Upload failed. Is your backend running?";
    uploadStatus.className = "error";
  }
  pdfInput.value = "";
});

// ── SEND QUESTION ──────────────────────────────
sendBtn.addEventListener("click", sendQuestion);
questionInput.addEventListener("keydown", (e) => { if (e.key === "Enter") sendQuestion(); });

async function sendQuestion() {
  if (isLimitReached()) return;
  const question = questionInput.value.trim();
  if (!question) return;
  addMessage("user", question);
  questionInput.value = "";
  sendBtn.disabled = true;
  const loadingId = addLoadingBubble();
  try {
    const res = await fetch(`${API_BASE}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: question }),
    });
    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();
    removeLoadingBubble(loadingId);
    const answer = data.answer || data.response || data.message || "No response received.";
    const sources = data.sources || [];
    incrementQuestionsUsed();
    addMessage("bot", answer, sources);
  } catch (err) {
    removeLoadingBubble(loadingId);
    addMessage("bot", "Could not reach the backend. The server may be starting up — please try again in 30 seconds.");
  }
  updateInputState();
  if (!isLimitReached()) sendBtn.disabled = false;
  questionInput.focus();
}

// ── SUMMARIZE ──────────────────────────────────
summarizeBtn.addEventListener("click", async () => {
  if (isLimitReached()) { showLimitMessage(); return; }
  addMessage("user", "Summarize the uploaded documents.");
  summarizeBtn.disabled = true;
  const loadingId = addLoadingBubble();
  try {
    const res = await fetch(`${API_BASE}/summarize`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();
    removeLoadingBubble(loadingId);
    incrementQuestionsUsed();
    addMessage("bot", data.answer || data.response || "No summary received.");
  } catch (err) {
    removeLoadingBubble(loadingId);
    addMessage("bot", "Could not reach the backend.");
  }
  summarizeBtn.disabled = false;
  updateInputState();
});

// ── COMPARE ────────────────────────────────────
compareBtn.addEventListener("click", () => {
  if (isLimitReached()) { showLimitMessage(); return; }
  questionInput.value = "Compare: ";
  questionInput.focus();
});

// ── HELPERS ────────────────────────────────────
function addMessage(role, text, sources = []) {
  const message = document.createElement("div");
  message.classList.add("message", role === "user" ? "user-message" : "bot-message");
  const avatar = document.createElement("div");
  avatar.classList.add("avatar");
  avatar.textContent = role === "user" ? "You" : "AI";
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerHTML = formatText(text);
  if (sources.length > 0) {
    const sourcesDiv = document.createElement("div");
    sourcesDiv.classList.add("sources");
    sourcesDiv.innerHTML = `<strong>Sources</strong><ul>${sources.map(s => `<li>${s.file || s.source || s} — Page ${s.page || "?"}</li>`).join("")}</ul>`;
    bubble.appendChild(sourcesDiv);
  }
  message.appendChild(avatar);
  message.appendChild(bubble);
  chatMessages.appendChild(message);
  scrollToBottom();
}

function formatText(text) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.*?)\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br/>");
}

function addLoadingBubble() {
  const id = "loading-" + Date.now();
  const message = document.createElement("div");
  message.classList.add("message", "bot-message", "loading-bubble");
  message.id = id;
  const avatar = document.createElement("div");
  avatar.classList.add("avatar");
  avatar.textContent = "AI";
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  bubble.innerHTML = `<div class="dot"></div><div class="dot"></div><div class="dot"></div>`;
  message.appendChild(avatar);
  message.appendChild(bubble);
  chatMessages.appendChild(message);
  scrollToBottom();
  return id;
}

function removeLoadingBubble(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function scrollToBottom() {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// ── INIT ───────────────────────────────────────
updateInputState();