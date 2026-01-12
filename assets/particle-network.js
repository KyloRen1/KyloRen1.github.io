// Particle Network Animation
(function() {
  const canvas = document.getElementById('particle-canvas');
  const ctx = canvas.getContext('2d');
  
  let particles = [];
  let mouse = { x: null, y: null, radius: 150 };
  
  // Set canvas size
  function setCanvasSize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  
  setCanvasSize();
  window.addEventListener('resize', () => {
    setCanvasSize();
    init();
  });
  
  // Track mouse position
  window.addEventListener('mousemove', (e) => {
    mouse.x = e.x;
    mouse.y = e.y;
  });
  
  window.addEventListener('mouseout', () => {
    mouse.x = null;
    mouse.y = null;
  });
  
  // Particle class
  class Particle {
    constructor() {
      this.x = Math.random() * canvas.width;
      this.y = Math.random() * canvas.height;
      this.vx = (Math.random() - 0.5) * 0.5;
      this.vy = (Math.random() - 0.5) * 0.5;
      this.size = 3 + Math.random() * 2; // Random size between 3 and 5
      this.color = this.getRandomPastelColor();
    }
    
    getRandomPastelColor() {
      const hue = Math.floor(Math.random() * 360);
      return `hsl(${hue}, 70%, 80%)`;
    }
    
    update() {
      this.x += this.vx;
      this.y += this.vy;
      
      // Bounce off edges
      if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
      if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
    
    draw() {
      ctx.fillStyle = this.color;
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
      ctx.fill();
    }
  }
  
  // Initialize particles
  function init() {
    particles = [];
    const numberOfParticles = Math.floor((canvas.width * canvas.height) / 15000);
    for (let i = 0; i < numberOfParticles; i++) {
      particles.push(new Particle());
    }
  }
  
  // Connect particles
  function connectParticles() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x;
        const dy = particles[i].y - particles[j].y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < 120) {
          // Check if mouse is near this connection
          let lineColor = 'rgba(200, 200, 200, 0.3)';
          
          if (mouse.x !== null && mouse.y !== null) {
            const midX = (particles[i].x + particles[j].x) / 2;
            const midY = (particles[i].y + particles[j].y) / 2;
            const distToMouse = Math.sqrt(
              Math.pow(mouse.x - midX, 2) + Math.pow(mouse.y - midY, 2)
            );
            
            if (distToMouse < mouse.radius) {
              lineColor = 'rgba(100, 100, 100, 0.5)';
            }
          }
          
          ctx.strokeStyle = lineColor;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.stroke();
        }
      }
    }
  }
  
  // Animation loop
  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw connections first (so they're behind particles)
    connectParticles();
    
    // Draw particles on top
    particles.forEach(particle => {
      particle.update();
      particle.draw();
    });
    
    requestAnimationFrame(animate);
  }
  
  init();
  animate();
})();
