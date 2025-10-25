// main.js - Enhanced with new theme animations and your advanced chat functionality
document.addEventListener('DOMContentLoaded', function () {
  // NAVBAR hamburger
  const hamburger = document.getElementById('hamburger');
  const navLinks = document.getElementById('navLinks');
  if (hamburger && navLinks) {
    hamburger.addEventListener('click', function () {
      const active = navLinks.classList.toggle('active');
      hamburger.setAttribute('aria-expanded', active ? 'true' : 'false');
    });
  }

  // Drag and drop + file input
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('resume');
  const fileName = document.getElementById('file-name');

  function setFileName(name) {
    fileName.textContent = name || 'No file selected';
  }

  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      const f = e.target.files && e.target.files[0];
      setFileName(f ? f.name : '');
    });
  }

  if (dropzone) {
    dropzone.addEventListener('click', () => fileInput && fileInput.click());
    dropzone.addEventListener('keydown', (e) => { 
      if (e.key === 'Enter' || e.key === ' ') { 
        e.preventDefault(); 
        fileInput && fileInput.click(); 
      } 
    });

    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.classList.add('is-dragover');
    });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('is-dragover'));
    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('is-dragover');
      const dt = e.dataTransfer;
      if (dt && dt.files && dt.files.length) {
        fileInput.files = dt.files;
        setFileName(dt.files[0].name);
      }
    });
  }

  // Intersection Observer for entrance animations
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-in');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  // Observe elements for animation
  document.querySelectorAll('.feature, .upload-card, .hero-title, .hero-sub').forEach(el => {
    el.classList.add('animate-on-scroll');
    observer.observe(el);
  });

  // Stagger animation for features
  document.querySelectorAll('.feature').forEach((el, index) => {
    el.style.transitionDelay = `${index * 0.1}s`;
  });

  // Form submission handling
  const analyzeForm = document.getElementById('analyzeForm');
  const analyzeBtn = document.getElementById('analyzeBtn');
  if (analyzeForm && analyzeBtn) {
    analyzeForm.addEventListener('submit', (e) => {
      analyzeBtn.disabled = true;
      analyzeBtn.classList.add('loading');
      analyzeBtn.querySelector('.btn-text').textContent = 'Analyzing...';
      
      // Add loading animation
      const btnIcon = analyzeBtn.querySelector('.btn-icon');
      if (btnIcon) {
        btnIcon.style.animation = 'spin 1s linear infinite';
      }
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });

  // Enhanced resume widget animations
  const resumeWidget = document.getElementById('resume-widget');
  if (resumeWidget) {
    // Periodic attention grabber
    setInterval(() => {
      resumeWidget.style.animation = 'none';
      setTimeout(() => {
        resumeWidget.style.animation = 'widget-float 4s ease-in-out infinite, widget-entrance 1s ease-out, widget-shake 0.6s ease-in-out';
      }, 10);
    }, 12000);
    
    // Enhanced hover effects
    resumeWidget.addEventListener('mouseenter', () => {
      resumeWidget.style.transform = 'scale(1.03) translateY(-5px)';
      resumeWidget.style.transition = 'transform 0.3s ease';
    });
    
    resumeWidget.addEventListener('mouseleave', () => {
      resumeWidget.style.transform = 'scale(1)';
    });

    // Create floating particles
    function createWidgetParticle() {
      const particle = document.createElement('div');
      particle.style.position = 'absolute';
      particle.style.width = '4px';
      particle.style.height = '4px';
      particle.style.background = 'rgba(255, 255, 255, 0.8)';
      particle.style.borderRadius = '50%';
      particle.style.pointerEvents = 'none';
      particle.style.zIndex = '1';
      
      const rect = resumeWidget.getBoundingClientRect();
      particle.style.left = Math.random() * rect.width + 'px';
      particle.style.bottom = '0px';
      
      resumeWidget.appendChild(particle);
      
      let position = 0;
      const floatAnimation = setInterval(() => {
        position += 2;
        particle.style.bottom = position + 'px';
        particle.style.opacity = 1 - (position / 200);
        
        if (position >= 200) {
          clearInterval(floatAnimation);
          particle.remove();
        }
      }, 20);
    }
    
    // Create particles periodically
    setInterval(createWidgetParticle, 3000);
  }

  // Add dynamic background shapes animation
  function animateBackgroundShapes() {
    const shapes = document.querySelectorAll('.shape');
    shapes.forEach((shape, index) => {
      const duration = 15 + (index * 5);
      const delay = index * 2;
      shape.style.animationDuration = `${duration}s`;
      shape.style.animationDelay = `${delay}s`;
    });
  }

  animateBackgroundShapes();

  // Add parallax effect to hero section
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const heroBackground = document.querySelector('.hero-background');
    if (heroBackground) {
      heroBackground.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
  });

  // Chat functionality - Using your existing chat.js implementation
  const chatButton = document.getElementById('chat-button');
  const chatBox = document.getElementById('chat-box');
  const sendBtn = document.getElementById('send-btn');
  const chatText = document.getElementById('chat-text');
  const chatMessages = document.getElementById('chat-messages');

  // Toggle chat box
  chatButton && chatButton.addEventListener('click', () => {
    if (!chatBox) return;
    const visible = chatBox.style.display === 'flex';
    chatBox.style.display = visible ? 'none' : 'flex';
    chatBox.setAttribute('aria-hidden', visible ? 'true' : 'false');
  });

  // Append message
  function appendMessage(cls, text = '') {
    const div = document.createElement('div');
    div.className = `chat-message ${cls}`;
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
  }

  // Typing effect
  function typeMessage(element, text, speed = 35) {
    element.textContent = '';
    let i = 0;
    const interval = setInterval(() => {
      if (i < text.length) {
        element.textContent += text.charAt(i);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        i++;
      } else {
        clearInterval(interval);
      }
    }, speed);
  }

  // CSRF token helper
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Send message
  function sendMessage() {
    const txt = chatText.value.trim();
    if (!txt) return;

    appendMessage('user', txt);
    chatText.value = '';

    const botDiv = appendMessage('bot', ' ARDAA is typing...');
    botDiv.innerHTML = `<div class="typing"><span></span><span></span><span></span></div>`;

    fetch("/chat/send/", {   // ✅ must match chat/urls.py
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({ message: txt })
    })
      .then(res => res.json())
      .then(data => {
        const reply = data.reply || "🤖 Sorry, I couldn't respond.";
        typeMessage(botDiv, reply, 35);
      })
      .catch(err => {
        console.error(err);
        botDiv.textContent = "⚠️ Error: Could not connect to ARDAA.";
      });
  }

  // Events
  sendBtn && sendBtn.addEventListener('click', sendMessage);
  chatText && chatText.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
  });

  // --- Make chat box draggable ---
  function makeDraggable(element, handle) {
    let offsetX = 0, offsetY = 0, isDown = false;

    handle.addEventListener('mousedown', (e) => {
      isDown = true;
      offsetX = e.clientX - element.getBoundingClientRect().left;
      offsetY = e.clientY - element.getBoundingClientRect().top;
      document.body.style.userSelect = "none"; // prevent text highlight
    });

    document.addEventListener('mouseup', () => {
      isDown = false;
      document.body.style.userSelect = "";
    });

    document.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      element.style.top = (e.clientY - offsetY) + "px";
      element.style.left = (e.clientX - offsetX) + "px";
      element.style.bottom = "auto"; 
      element.style.right = "auto";
    });
  }

  const header = document.querySelector('.chat-header');
  if (chatBox && header) {
    makeDraggable(chatBox, header);
  }
});

// Add custom animations
const style = document.createElement('style');
style.textContent = `
  @keyframes widget-shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-8px) rotate(-2deg); }
    75% { transform: translateX(8px) rotate(2deg); }
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }

  .animate-on-scroll {
    opacity: 0;
    transform: translateY(30px);
    transition: opacity 0.6s ease, transform 0.6s ease;
  }

  .animate-in {
    opacity: 1;
    transform: translateY(0);
  }
`;
document.head.appendChild(style);