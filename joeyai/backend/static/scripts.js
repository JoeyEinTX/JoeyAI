// JoeyAI Neon Theme & Chat Logic
// Assumes DOM structure from updated index.html


document.addEventListener('DOMContentLoaded', () => {
  const chatArea = document.getElementById('chatArea');
  const logoHero = document.getElementById('logoHero');
  const messages = document.getElementById('messages');
  const composer = document.getElementById('composer');
  const promptInput = document.getElementById('promptInput');
  const sendBtn = document.getElementById('sendBtn');
  const memoryBtn = document.getElementById('memoryBtn');
  const chatList = document.getElementById('chatList');

  // Initial state: show logoHero, hide messages
  function toStartLayout() {
    chatArea.classList.remove('active');
    chatArea.classList.add('start');
    logoHero.style.opacity = '1';
    logoHero.style.transform = 'translateY(0)';
    logoHero.style.display = 'flex';
    messages.style.display = 'none';
  }

  // Transition to active chat: hide logoHero, show messages
  function toActiveLayout() {
    chatArea.classList.remove('start');
    chatArea.classList.add('active');
    logoHero.style.opacity = '0';
    logoHero.style.transform = 'translateY(-32px)';
    setTimeout(() => {
      logoHero.style.display = 'none';
      messages.style.display = 'block';
    }, 250);
  }

  // Add message to chat
  function addMessage(role, text) {
    const msg = document.createElement('div');
    msg.className = `msg ${role}`;
    msg.innerHTML = `<span>${text}</span>`;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
  }


  // Send message on Ctrl+Enter, allow Enter for newlines
  composer.addEventListener('submit', (e) => {
    e.preventDefault();
    const text = promptInput.value.trim();
    if (!text) return;
    if (chatArea.classList.contains('start')) toActiveLayout();
    addMessage('user', text);
    promptInput.value = '';
    // TODO: Call backend API, show loading, then add assistant message
  });

  promptInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.ctrlKey) {
      e.preventDefault();
      composer.requestSubmit();
    }
  });

  // Chat selection (simulate)
  chatList?.addEventListener('click', (e) => {
    if (e.target.tagName === 'LI') {
      toActiveLayout();
      // TODO: Load selected chat messages
    }
  });

  // Neon focus effect
  promptInput.addEventListener('focus', () => {
    promptInput.style.boxShadow = '0 0 12px var(--glow)';
  });
  promptInput.addEventListener('blur', () => {
    promptInput.style.boxShadow = '';
  });

  // Responsive: hide sidebar on mobile
  function handleResize() {
    const sidebar = document.querySelector('.sidebar');
    if (window.innerWidth < 980) sidebar.style.display = 'none';
    else sidebar.style.display = '';
  }
  window.addEventListener('resize', handleResize);
  handleResize();

  // On first load, always start in start layout
  toStartLayout();
});
