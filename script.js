const API_BASE = "https://ai-research-agent-6ka8.onrender.com";

const pdfInput       = document.getElementById("pdf-input");
const uploadStatus   = document.getElementById("upload-status");
const docList        = document.getElementById("doc-list");
const chatMessages   = document.getElementById("chat-messages");
const questionInput  = document.getElementById("question-input");
const sendBtn        = document.getElementById("send-btn");
const summarizeBtn   = document.getElementById("summarize-btn");
const compareBtn     = document.getElementById("compare-btn");

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

sendBtn.addEventListener("click", sendQuestion);
questionInput.addEventListener("keydown", (e) => { if (e.key === "Enter") sendQuestion(); });

async function sendQuestion() {
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
    addMessage("bot", answer, sources);
  } catch (err) {
    removeLoadingBubble(loadingId);
    addMessage("bot", "Could not reach the backend. Make sure your FastAPI server is running.");
  }
  sendBtn.disabled = false;
  questionInput.focus();
}

summarizeBtn.addEventListener("click", async () => {
  addMessage("user", "Summarize the uploaded documents.");
  summarizeBtn.disabled = true;
  const loadingId = addLoadingBubble();
  try {
    const res = await fetch(`${API_BASE}/summarize`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({}) });
    if (!res.ok) throw new Error("Request failed");
    const data = await res.json();
    removeLoadingBubble(loadingId);
    addMessage("bot", data.answer || data.response || "No summary received.");
  } catch (err) {
    removeLoadingBubble(loadingId);
    addMessage("bot", "Could not reach the backend.");
  }
  summarizeBtn.disabled = false;
});

compareBtn.addEventListener("click", () => {
  questionInput.value = "Compare: ";
  questionInput.focus();
});

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