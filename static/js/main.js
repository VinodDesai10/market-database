/* ===================================================
   🎯 MARKET DB - ADVANCED INTERACTIONS & ANIMATIONS
   =================================================== */

document.addEventListener("DOMContentLoaded", () => {
  console.log("[v0] Initializing dashboard animations and interactions")

  /* =============================
     🔗 SIDEBAR ACTIVE LINK LOGIC
     ============================= */
  const sidebarLinks = document.querySelectorAll(".sidebar-link")
  const currentPath = window.location.pathname

  sidebarLinks.forEach((link) => {
    const linkPath = link.getAttribute("href")
    if (currentPath === linkPath || currentPath.startsWith(linkPath + "/")) {
      link.classList.add("active")
    } else {
      link.classList.remove("active")
    }

    link.addEventListener("click", () => {
      sidebarLinks.forEach((l) => l.classList.remove("active"))
      link.classList.add("active")
    })
  })

  /* =============================
     ✨ RIPPLE EFFECT ON BUTTONS
     ============================= */
  function addRippleEffect(element) {
    element.addEventListener("click", function (e) {
      const ripple = document.createElement("span")
      ripple.classList.add("ripple")

      const rect = this.getBoundingClientRect()
      const x = e.clientX - rect.left
      const y = e.clientY - rect.top

      ripple.style.left = x + "px"
      ripple.style.top = y + "px"
      ripple.style.width = ripple.style.height = "12px"

      this.appendChild(ripple)

      setTimeout(() => ripple.remove(), 800)
    })
  }

  document.querySelectorAll(".btn, .nav-btn, .nav-link").forEach(addRippleEffect)

  /* =============================
     🌊 PAGE TRANSITION ANIMATION
     ============================= */
  const internalLinks = document.querySelectorAll("a[href]")
  internalLinks.forEach((link) => {
    if (link.hostname === window.location.hostname && !link.href.includes("#")) {
      link.addEventListener("click", (e) => {
        if (!link.hasAttribute("data-bs-toggle")) {
          e.preventDefault()
          document.body.classList.add("fade-out")
          setTimeout(() => {
            window.location = link.href
          }, 300)
        }
      })
    }
  })

  /* =============================
     📊 TABLE ROW INTERSECTION ANIMATION
     ============================= */
  const tableRows = document.querySelectorAll(".table tbody tr")
  if (tableRows.length > 0 && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            entry.target.style.animation = `fadeInUp 0.5s ease-out ${index * 0.08}s both`
            observer.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.1 },
    )

    tableRows.forEach((row) => observer.observe(row))
  }

  /* =============================
     🎨 CARD ENTRANCE ANIMATIONS
     ============================= */
  const cards = document.querySelectorAll(".card")
  if (cards.length > 0 && "IntersectionObserver" in window) {
    const cardObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            entry.target.style.animation = `slideInUp 0.6s ease-out ${index * 0.1}s both`
            cardObserver.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.1 },
    )

    cards.forEach((card) => cardObserver.observe(card))
  }

  /* =============================
     🔔 TOAST AUTO-DISMISS
     ============================= */
  const toasts = document.querySelectorAll(".toast-notification")
  toasts.forEach((toast) => {
    setTimeout(() => {
      toast.style.animation = "fadeOut 0.5s ease-out forwards"
      setTimeout(() => toast.remove(), 500)
    }, 5000)
  })

  /* =============================
     🎯 FORM FIELD FOCUS EFFECTS
     ============================= */
  const formControls = document.querySelectorAll(".form-control, .form-select, .form-check-input")
  formControls.forEach((control) => {
    control.addEventListener("focus", function () {
      const parent = this.closest(".form-group") || this.closest(".mb-3") || this.parentElement
      if (parent) {
        parent.classList.add("focused")
      }
      // Ensure focus styling is maintained
      this.style.boxShadow = "0 0 0 3px rgba(6, 182, 212, 0.25), inset 0 0 0 1px rgba(6, 182, 212, 0.4)"
    })

    control.addEventListener("blur", function () {
      const parent = this.closest(".form-group") || this.closest(".mb-3") || this.parentElement
      if (parent) {
        parent.classList.remove("focused")
      }
    })

    control.addEventListener("input", function () {
      if (document.activeElement === this) {
        this.style.boxShadow = "0 0 0 3px rgba(6, 182, 212, 0.25), inset 0 0 0 1px rgba(6, 182, 212, 0.4)"
      }
    })
  })

  /* =============================
     💫 SCROLL-TO-TOP SMOOTH BEHAVIOR
     ============================= */
  window.addEventListener("load", () => {
    window.scrollTo({ top: 0, behavior: "smooth" })
  })

  /* =============================
     🔽 DROPDOWN CLOSE ON OUTSIDE CLICK
     ============================= */
  document.addEventListener("click", (e) => {
    const dropdowns = document.querySelectorAll(".dropdown-glass")
    dropdowns.forEach((dropdown) => {
      if (!dropdown.parentElement.contains(e.target)) {
        // Close dropdown - Bootstrap handles this automatically
      }
    })
  })

  /* =============================
     ✨ SMOOTH DROPDOWN TRANSITIONS
     ============================= */
  const dropdownButtons = document.querySelectorAll("[data-bs-toggle='dropdown']")
  dropdownButtons.forEach((button) => {
    button.addEventListener("shown.bs.dropdown", function () {
      const dropdown = this.nextElementSibling
      if (dropdown && dropdown.classList.contains("dropdown-glass")) {
        dropdown.style.animation = "slideDownDropdown 0.3s cubic-bezier(0.34, 1.56, 0.64, 1)"
      }
    })
  })

  /* =============================
     🎯 RIGHT SIDEBAR MENU TOGGLE FUNCTIONALITY
     ============================= */
  const sidebarToggle = document.getElementById("sidebarToggle")
  const rightSidebar = document.getElementById("rightSidebar")
  const closeSidebarBtn = document.getElementById("closeSidebar")
  let sidebarOverlay = document.querySelector(".sidebar-overlay")

  // Create overlay if it doesn't exist
  if (!sidebarOverlay) {
    sidebarOverlay = document.createElement("div")
    sidebarOverlay.className = "sidebar-overlay"
    document.body.appendChild(sidebarOverlay)
  }

  // Toggle sidebar
  if (sidebarToggle) {
    sidebarToggle.addEventListener("click", () => {
      rightSidebar.classList.toggle("active")
      sidebarOverlay.classList.toggle("active")
    })
  }

  // Close sidebar
  if (closeSidebarBtn) {
    closeSidebarBtn.addEventListener("click", () => {
      rightSidebar.classList.remove("active")
      sidebarOverlay.classList.remove("active")
    })
  }

  // Close sidebar when clicking overlay
  sidebarOverlay.addEventListener("click", () => {
    rightSidebar.classList.remove("active")
    sidebarOverlay.classList.remove("active")
  })

  // Close sidebar when clicking a link
  const rightNavItems = document.querySelectorAll(".right-nav-item")
  rightNavItems.forEach((item) => {
    item.addEventListener("click", () => {
      rightSidebar.classList.remove("active")
      sidebarOverlay.classList.remove("active")
    })
  })

  console.log("[v0] Dashboard initialized successfully")
})

/* =============================
   🌐 INJECT ADVANCED CSS ANIMATIONS
   ============================= */
;(function injectAdvancedCSS() {
  const css = `
    @keyframes slideInUp {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    @keyframes fadeOut {
      from {
        opacity: 1;
      }
      to {
        opacity: 0;
      }
    }

    @keyframes shimmer {
      0% {
        background-position: -1000px 0;
      }
      100% {
        background-position: 1000px 0;
      }
    }

    .loader {
      background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0.1),
        rgba(255, 255, 255, 0.3),
        rgba(255, 255, 255, 0.1)
      );
      background-size: 1000px 100%;
      animation: shimmer 2s infinite;
    }

    /* Smooth scrolling */
    html {
      scroll-behavior: smooth;
    }

    /* Disable animations for users who prefer reduced motion */
    @media (prefers-reduced-motion: reduce) {
      * {
        animation: none !important;
        transition: none !important;
      }
    }
  `

  const style = document.createElement("style")
  style.appendChild(document.createTextNode(css))
  document.head.appendChild(style)
})()
