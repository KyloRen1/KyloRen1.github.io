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
    const numberOfParticles = Math.floor((canvas.width * canvas.height) / 15000);

    const savedState = sessionStorage.getItem('particleState');
    if (savedState) {
      sessionStorage.removeItem('particleState'); // Prevent stale reads on subsequent resize events
      try {
        const state = JSON.parse(savedState);
        if (state.particles && state.particles.length > 0) {
          const timePassed = Date.now() - state.time;
          const framesPassed = Math.min(timePassed / 16.6, 60 * 2); // extrapolate up to 2 seconds max
          
          particles = [];
          for (let i = 0; i < state.particles.length; i++) {
            const p = new Particle();
            const sp = state.particles[i];
            
            p.x = sp.x;
            p.y = sp.y;
            p.vx = sp.vx;
            p.vy = sp.vy;
            p.size = sp.size;
            p.color = sp.color;
            
            p.x += p.vx * framesPassed;
            p.y += p.vy * framesPassed;
            
            // Bounds check so they do not drift outside
            if (p.x < 0) p.x = 0;
            if (p.x > canvas.width) p.x = canvas.width;
            if (p.y < 0) p.y = 0;
            if (p.y > canvas.height) p.y = canvas.height;
            
            particles.push(p);
          }
        }
      } catch (e) {
        // Ignore errors
      }
    }

    // Adjust particle count to match current window size without clearing existing ones
    if (particles.length < numberOfParticles) {
      for (let i = particles.length; i < numberOfParticles; i++) {
        particles.push(new Particle());
      }
    } else if (particles.length > numberOfParticles) {
      particles.splice(numberOfParticles);
    }
  }

  // Save state on unload
  window.addEventListener('beforeunload', () => {
    const state = {
      time: Date.now(),
      width: canvas.width,
      height: canvas.height,
      particles: particles.map(p => ({
        x: p.x,
        y: p.y,
        vx: p.vx,
        vy: p.vy,
        size: p.size,
        color: p.color
      }))
    };
    sessionStorage.setItem('particleState', JSON.stringify(state));
  });
  
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
