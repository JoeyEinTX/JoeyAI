
// JoeyAI single chat system
let currentProjectId = null;
let currentTitle = '';
let hasMessages = false;

const chatArea = document.getElementById('chatArea');
const messagesDiv = document.getElementById('messages');
const composerForm = document.getElementById('composer');
const promptInput = document.getElementById('promptInput');
const sendBtn = document.getElementById('sendBtn');
const wordmark = document.getElementById('wordmark');
const logoHero = document.getElementById('logoHero');
const memoryBtn = document.getElementById('memoryBtn');
const memoryModal = document.getElementById('memoryModal');
const memorySearch = document.getElementById('memorySearch');
const memoryResults = document.getElementById('memoryResults');

// API helpers
async function api(url, opts={}) {
	const res = await fetch(url, opts);
	if (!res.ok) throw new Error(await res.text());
	return await res.json();
}

async function getProjects() {
	return await api('/projects');
}
async function createProject(title='') {
	return await api('/projects', {
		method: 'POST',
		headers: {'Content-Type':'application/json'},
		body: JSON.stringify({title})
	});
}
async function patchProject(id, title) {
	return await api(`/projects/${id}`, {
		method: 'PATCH',
		headers: {'Content-Type':'application/json'},
		body: JSON.stringify({title})
	});
}
async function getMessages(id) {
	return await api(`/projects/${id}/messages`);
}
async function postMessage(id, text) {
	return await api(`/projects/${id}/message`, {
		method: 'POST',
		headers: {'Content-Type':'application/json'},
		body: JSON.stringify({role:'user',content:text})
	});
}
async function searchMemory(q) {
	return await api(`/search?q=${encodeURIComponent(q)}`);
}

// UI helpers
function renderMessages(list) {
	messagesDiv.innerHTML = '';
	list.forEach(m => {
		const div = document.createElement('div');
		div.className = `bubble ${m.role}`;
		div.textContent = m.content;
		messagesDiv.appendChild(div);
	});
}

function setChatState(msgCount) {
	hasMessages = msgCount > 0;
	if (hasMessages) {
		chatArea.classList.remove('start');
		chatArea.classList.add('active');
		chatArea.classList.remove('grid-rows-[0fr_auto]');
		chatArea.classList.add('grid-rows-[1fr_auto]');
		messagesDiv.classList.remove('hidden');
		logoHero.style.display = 'none';
		wordmark.classList.remove('hidden');
	} else {
		chatArea.classList.add('start');
		chatArea.classList.remove('active');
		chatArea.classList.add('grid-rows-[0fr_auto]');
		chatArea.classList.remove('grid-rows-[1fr_auto]');
		messagesDiv.classList.add('hidden');
		logoHero.style.display = '';
		wordmark.classList.add('hidden');
	}
}

// Chat flow
async function loadChat() {
	let projects = await getProjects();
	if (!projects.length) {
		const p = await createProject('');
		currentProjectId = p.id;
		currentTitle = p.title;
	} else {
		const p = projects[0];
		currentProjectId = p.id;
		currentTitle = p.title;
	}
	let msgs = await getMessages(currentProjectId);
	setChatState(msgs.length);
	if (hasMessages) renderMessages(msgs);
}

composerForm.addEventListener('submit', async (e) => {
	e.preventDefault();
	const text = promptInput.value.trim();
	if (!text) return;
	// Append user bubble
	const userDiv = document.createElement('div');
	userDiv.className = 'bubble user';
	userDiv.textContent = text;
	messagesDiv.appendChild(userDiv);
	promptInput.value = '';
	// Send to backend
	try {
		const res = await postMessage(currentProjectId, text);
		// Append assistant bubble
		const aiDiv = document.createElement('div');
		aiDiv.className = 'bubble assistant';
		aiDiv.textContent = res.reply;
		messagesDiv.appendChild(aiDiv);
		setChatState(messagesDiv.children.length);
		// Auto-title if needed
		if (!currentTitle || currentTitle === 'Untitled') {
			const autoTitle = text.split(' ').slice(0, 10).join(' ');
			await patchProject(currentProjectId, autoTitle);
			currentTitle = autoTitle;
		}
	} catch (err) {
		const errDiv = document.createElement('div');
		errDiv.className = 'bubble error';
		errDiv.textContent = 'Error: ' + err.message;
		messagesDiv.appendChild(errDiv);
	}
});

// Enter/Shift+Enter behavior
promptInput.addEventListener('keydown', (e) => {
	if (e.key === 'Enter' && !e.shiftKey) {
		e.preventDefault();
		sendBtn.click();
	}
});

// Memory modal
function openMemoryModal() {
	memoryModal.classList.remove('hidden');
	memorySearch.focus();
}
function closeMemoryModal() {
	memoryModal.classList.add('hidden');
}
memoryBtn.addEventListener('click', openMemoryModal);
memorySearch.addEventListener('keydown', async (e) => {
	if (e.key === 'Escape') closeMemoryModal();
	if (e.key === 'Enter') {
		const q = memorySearch.value.trim();
		if (!q) return;
		const results = await searchMemory(q);
		memoryResults.innerHTML = '';
		results.forEach(r => {
			const li = document.createElement('li');
			li.innerHTML = `<b>${r.snippet}</b> <span class='text-xs text-cyan-400'>${r.ts}</span>`;
			memoryResults.appendChild(li);
		});
	}
});
document.addEventListener('keydown', (e) => {
	if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
		e.preventDefault();
		openMemoryModal();
	}
});
memoryModal.addEventListener('click', (e) => {
	if (e.target === memoryModal) closeMemoryModal();
});

window.addEventListener('DOMContentLoaded', loadChat);
