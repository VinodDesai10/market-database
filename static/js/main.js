document.addEventListener("DOMContentLoaded", () => {

  /* =============================
     🎯 SIDEBAR ACTIVE LINK LOGIC
     ============================= */
  const links = document.querySelectorAll(".sidebar .nav-link");
  const currentPath = window.location.pathname;

  links.forEach(link => {
    const linkPath = link.getAttribute("href");

    // ✅ Match only the correct current section
    if (currentPath === linkPath || currentPath.startsWith(linkPath + "/")) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }

    // Active highlight on click
    link.addEventListener("click", () => {
      links.forEach(l => l.classList.remove("active"));
      link.classList.add("active");

      // Glow effect for click
      link.classList.add("glow");
      setTimeout(() => link.classList.remove("glow"), 500);
    });
  });

  /* =============================
     🌊 BUTTON RIPPLE EFFECT
     ============================= */
  document.querySelectorAll("button, .btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
      const circle = document.createElement("span");
      circle.classList.add("ripple");
      const rect = this.getBoundingClientRect();
      circle.style.left = `${e.clientX - rect.left}px`;
      circle.style.top = `${e.clientY - rect.top}px`;
      this.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    });
  });

  /* =============================
     🌫️ PAGE FADE-OUT TRANSITION
     ============================= */
  const pageLinks = document.querySelectorAll("a[href]");
  pageLinks.forEach(link => {
    if (link.hostname === window.location.hostname) {
      link.addEventListener("click", e => {
        const target = e.currentTarget.getAttribute("href");
        if (!target || target.startsWith("#") || target.startsWith("javascript")) return;
        e.preventDefault();
        document.body.classList.add("fade-out");
        setTimeout(() => { window.location = target; }, 200);
      });
    }
  });

  /* =============================
     🪄 SMOOTH SCROLL ON LOAD
     ============================= */
  window.scrollTo({ top: 0, behavior: "smooth" });
});

/* =============================
   ✨ DYNAMIC STYLE INJECTION
   ============================= */
(function injectCSS() {
  const css = `
  /* Ripple */
  .ripple {
    position: absolute;
    width: 12px;
    height: 12px;
    background: rgba(255,255,255,0.45);
    border-radius: 50%;
    transform: translate(-50%, -50%) scale(0.8);
    animation: rippleAni .6s ease forwards;
    pointer-events: none;
  }

  @keyframes rippleAni {
    to { transform: translate(-50%, -50%) scale(10); opacity: 0; }
  }

  /* Active link click glow */
  .sidebar .nav-link.glow {
    box-shadow: 0 0 12px rgba(124,58,237,0.6);
    transition: box-shadow 0.3s ease;
  }

  /* Page fade-out transition */
  body.fade-out {
    opacity: 0;
    transform: scale(0.98);
    transition: all 0.25s ease;
  }

  /* Buttons setup */
  .btn, button {
    position: relative;
    overflow: hidden;
  }
  `;
  const s = document.createElement("style");
  s.appendChild(document.createTextNode(css));
  document.head.appendChild(s);
})();