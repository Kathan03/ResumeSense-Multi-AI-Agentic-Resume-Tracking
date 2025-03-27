document.addEventListener('DOMContentLoaded', () => {
  // DOM Elements
  const themeToggle = document.getElementById('themeToggle');
  const chatToggle = document.getElementById('chatToggle');
  const chatSidebar = document.getElementById('chatSidebar');
  const closeChatBtn = document.getElementById('closeChat');
  const form = document.getElementById('uploadForm');
  const loading = document.getElementById('loading');
  const resultsSection = document.querySelector('.results-section');
  const resultsGrid = document.getElementById('results');
  const chatMessages = document.getElementById('chatMessages');
  const userInput = document.getElementById('userInput');
  const sendMessageBtn = document.getElementById('sendMessage');
  const fileInputs = document.querySelectorAll('.file-input input[type="file"]');
  const container = document.querySelector('main.container');
  const baseUrl = window.location.origin;

  // State
  let currentFilenames = null;
  let isProcessing = false;
  let isChatOpen = false;

  // Initialize Theme
  function initializeTheme() {
    const savedTheme = localStorage.getItem('theme') || 'dark';
    document.documentElement.setAttribute('data-theme', savedTheme);
  }
  initializeTheme();

  // File Input Handlers
  fileInputs.forEach(input => {
    input.addEventListener('change', (event) => {
      const fileName = event.target.files[0]?.name || "Upload File";
      const label = input.parentElement.querySelector('.file-label');
      if (label) label.textContent = fileName;
    });
  });

  // Theme Toggle
  themeToggle.addEventListener('click', () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
  });

  // Chat Toggle
  function toggleChat() {
    isChatOpen = !isChatOpen;
    chatSidebar.classList.toggle('active', isChatOpen);
    container.classList.toggle('with-chat', isChatOpen);
    updateChatToggleIcon();
    if (!currentFilenames) {
      chatMessages.innerHTML = '<div class="default-chat-message">Please upload and submit the resume and job description first to chat.</div>';
      userInput.disabled = true;
      sendMessageBtn.disabled = true;
    }
  }

  function updateChatToggleIcon() {
    const icon = chatToggle.querySelector('i');
    icon.className = isChatOpen ? 'bx bx-x' : 'bx bx-message-dots';
  }

  chatToggle.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleChat();
  });
  closeChatBtn.addEventListener('click', toggleChat);
  document.addEventListener('click', (e) => {
    if (isChatOpen && !chatSidebar.contains(e.target) && !chatToggle.contains(e.target)) {
      toggleChat();
    }
  });

  // Form Submission
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    if (isProcessing) return;
    try {
      isProcessing = true;
      // Show loading overlay and blur container
      loading.style.display = 'flex';
      container.style.filter = 'blur(5px)';
      resultsSection.classList.remove('visible');

      const formData = new FormData(form);
      const uploadResponse = await fetch('/upload', { method: 'POST', body: formData });
      if (!uploadResponse.ok) throw new Error('File upload failed');
      const uploadData = await uploadResponse.json();
      // Map keys from backend correctly
      const { resume_filename, job_desc_filename } = uploadData;
      const processResponse = await fetch('/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_filename, job_desc_filename })
      });
      if (!processResponse.ok) throw new Error('Document processing failed');
      const results = await processResponse.json();
      console.log("Results received:", results);
      displayResults(results);
      currentFilenames = { resumeFilename: resume_filename, jobDescFilename: job_desc_filename };
      // Enable chat
      userInput.disabled = false;
      sendMessageBtn.disabled = false;
      if (chatMessages.querySelector('.default-chat-message')) {
        chatMessages.innerHTML = '';
      }
      if (!isChatOpen) toggleChat();
      // Add welcome chat bubble
      addChatMessage("Hi! I am here to ease your recruitment process. Ask me anything about the candidate.", "bot");
      // Remove blur and loading overlay
      setTimeout(() => {
        container.style.filter = 'none';
      }, 500);
    } catch (error) {
      showError(error.message);
      console.error('Processing Error:', error);
    } finally {
      isProcessing = false;
      loading.style.display = 'none';
    }
  });

  // Display Results
  function displayResults(data) {
    console.log("displayResults data:", data);
    resultsGrid.innerHTML = '';
    const questions = Array.isArray(data.questions)
      ? data.questions
      : typeof data.questions === 'string'
      ? data.questions.split('\n').filter(line => line.trim().length > 0)
      : [];
    const cards = [
      {
        title: 'Key Skills',
        icon: 'fa-key',
        content: data.keywords && data.keywords.skills && data.keywords.skills.length
          ? `<ul class="skills-list">${data.keywords.skills.map(k => `<li>${k}</li>`).join('')}</ul>`
          : '<p>No skills detected</p>'
      },
      {
        title: 'Summary',
        icon: 'fa-file-alt',
        content: data.summary || 'No summary available'
      },
      {
        title: 'Match Score',
        icon: 'fa-percentage',
        content: `<div class="score-display">${Math.round((data.score || 0) * 100)}%</div>`
      },
      {
        title: 'Interview Questions',
        icon: 'fa-question-circle',
        content: questions.length
           ? `<p>${questions.join('<br>')}</p>`
            : '<p>No questions generated</p>'
      }
    ];
    cards.forEach(card => {
      const cardEl = document.createElement('div');
      cardEl.className = 'result-card';
      cardEl.innerHTML = `<h3><i class="fas ${card.icon}"></i> ${card.title}</h3>${card.content}`;
      resultsGrid.appendChild(cardEl);
    });
    setTimeout(() => {
      resultsSection.classList.add('visible');
      resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  // Chat Handling
  sendMessageBtn.addEventListener('click', handleChatMessage);
  userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleChatMessage();
  });

  async function handleChatMessage() {
    const query = userInput.value.trim();
    if (!query || !currentFilenames || isProcessing) return;
    try {
      isProcessing = true;
      addChatMessage(query, 'user');
      userInput.value = '';
      const loadingMsg = addChatMessage('...', 'bot', true);
      const response = await fetch('/ask', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          resume_filename: currentFilenames.resumeFilename,
          job_desc_filename: currentFilenames.jobDescFilename,
          query
        })
      });
      if (!response.ok) throw new Error(await response.text());
      const { answer } = await response.json();
      updateChatMessage(loadingMsg.id, answer, 'bot');
    } catch (error) {
      updateChatMessage(loadingMsg.id, error.message, 'error');
      console.error('Chat Error:', error);
    } finally {
      isProcessing = false;
    }
  }

  // Chat UI Functions
  function addChatMessage(content, type, isLoading = false) {
    const messageId = Date.now().toString();
    const messageEl = document.createElement('div');
    messageEl.className = `chat-message ${type}${isLoading ? ' loading' : ''}`;
    messageEl.id = messageId;
    messageEl.innerHTML = isLoading
      ? '<div class="typing-indicator"><span></span><span></span><span></span></div>'
      : `<p>${content}</p>`;
    chatMessages.appendChild(messageEl);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return { id: messageId, element: messageEl };
  }

  function updateChatMessage(id, content, type) {
    const messageEl = document.getElementById(id);
    if (messageEl) {
      messageEl.className = `chat-message ${type}`;
      messageEl.innerHTML = `<p>${content}</p>`;
    }
  }

  // Error Display
  function showError(message) {
    const errorEl = document.createElement('div');
    errorEl.className = 'error-message';
    errorEl.textContent = message;
    document.body.appendChild(errorEl);
    setTimeout(() => errorEl.remove(), 3000);
  }

  // Particles Initialization
  function initializeParticles() {
    const container = document.getElementById('particles-container');
    for (let i = 0; i < 50; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.cssText = `
        left: ${Math.random() * 100}%;
        top: ${Math.random() * 100}%;
        animation-duration: ${15 + Math.random() * 15}s;
        width: ${4 + Math.random() * 4}px;
        height: ${4 + Math.random() * 4}px;
      `;
      container.appendChild(particle);
    }
  }
  initializeParticles();
});
