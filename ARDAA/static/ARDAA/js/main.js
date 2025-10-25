// main.js - Enhanced with new theme animations and interactions
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

  // Chat functionality
  const chatButton = document.getElementById('chat-button');
  const chatBox = document.getElementById('chat-box');
  const chatClose = document.getElementById('chat-close');
  const chatText = document.getElementById('chat-text');
  const sendBtn = document.getElementById('send-btn');
  const chatMessages = document.getElementById('chat-messages');

  if (chatButton && chatBox) {
    chatButton.addEventListener('click', () => {
      chatBox.classList.toggle('active');
      chatBox.setAttribute('aria-hidden', chatBox.classList.contains('active') ? 'false' : 'true');
    });
  }

  if (chatClose) {
    chatClose.addEventListener('click', () => {
      chatBox.classList.remove('active');
      chatBox.setAttribute('aria-hidden', 'true');
    });
  }

  // Chat message sending
  function sendMessage() {
    const message = chatText?.value.trim();
    if (message && chatMessages) {
      // Add user message
      const userMessage = document.createElement('div');
      userMessage.className = 'chat-message user';
      userMessage.innerHTML = `
        <div class="message-content">${message}</div>
        <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
      `;
      chatMessages.appendChild(userMessage);

      // Clear input
      if (chatText) chatText.value = '';

      // Simulate bot response
      setTimeout(() => {
        const botMessage = document.createElement('div');
        botMessage.className = 'chat-message bot';
        botMessage.innerHTML = `
          <div class="message-content">I'm analyzing your request. This is a demo response.</div>
          <div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
        `;
        chatMessages.appendChild(botMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
      }, 1000);

      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
  }

  if (sendBtn) {
    sendBtn.addEventListener('click', sendMessage);
  }

  if (chatText) {
    chatText.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        sendMessage();
      }
    });
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

  .chat-message {
    margin-bottom: 16px;
    display: flex;
    flex-direction: column;
    animation: messageSlide 0.3s ease-out;
  }

  @keyframes messageSlide {
    from {
      opacity: 0;
      transform: translateY(10px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .chat-message.user {
    align-items: flex-end;
  }

  .chat-message.bot {
    align-items: flex-start;
  }

  .message-content {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 14px;
    line-height: 1.4;
  }

  .chat-message.user .message-content {
    background: linear-gradient(135deg, var(--primary-500), var(--accent-500));
    color: white;
    border-bottom-right-radius: 6px;
  }

  .chat-message.bot .message-content {
    background: var(--neutral-100);
    color: var(--text-primary);
    border-bottom-left-radius: 6px;
  }

  .message-time {
    font-size: 11px;
    color: var(--text-tertiary);
    margin-top: 4px;
    padding: 0 8px;
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
// Add pulse effect to blink button every few seconds
document.addEventListener('DOMContentLoaded', () => {
  const blinkBtn = document.querySelector('.blink-btn');
  if (blinkBtn) {
    setInterval(() => {
      blinkBtn.style.transform = 'scale(1.08)';
      setTimeout(() => {
        blinkBtn.style.transform = 'scale(1)';
      }, 500);
    }, 6000);
  }
});
document.addEventListener('DOMContentLoaded', () => {
  const hero = document.querySelector('.hero-container');
  if (hero) {
    hero.style.opacity = '0';
    hero.style.transform = 'translateY(20px)';
    setTimeout(() => {
      hero.style.transition = 'opacity 1s ease, transform 1s ease';
      hero.style.opacity = '1';
      hero.style.transform = 'translateY(0)';
    }, 300);
  }
});

// Add pulse effect to blink button every few seconds
document.addEventListener('DOMContentLoaded', () => {
  const blinkBtn = document.querySelector('.blink-btn');
  if (blinkBtn) {
    setInterval(() => {
      blinkBtn.style.transform = 'scale(1.08)';
      setTimeout(() => {
        blinkBtn.style.transform = 'scale(1)';
      }, 400);
    }, 5000);
  }
});
