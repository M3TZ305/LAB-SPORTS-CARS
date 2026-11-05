document.querySelectorAll("[data-toggle]").forEach((button) => {
  const target = document.getElementById(button.dataset.toggle);
  button.addEventListener("click", () => {
    const open = button.getAttribute("aria-expanded") === "true";
    button.setAttribute("aria-expanded", String(!open));
    if (target.id === "primary-nav") {
      target.classList.toggle("is-open", !open);
    } else {
      target.hidden = open;
      if (!open) target.querySelector("input").focus();
    }
  });
});

const hero = document.querySelector("[data-hero]");
if (hero) {
  const photos = [...hero.querySelectorAll(".hero-image")];
  const dots = [...hero.querySelectorAll(".hero-dots button")];
  dots.forEach((dot, index) => {
    dot.addEventListener("click", () => {
      photos.forEach((photo, number) => photo.classList.toggle("is-active", index === number));
      dots.forEach((item, number) => item.setAttribute("aria-pressed", String(index === number)));
    });
  });
}

const gallery = document.querySelector("[data-gallery]");
if (gallery) {
  const image = gallery.querySelector("[data-gallery-image]");
  const photos = [...gallery.querySelectorAll("[data-gallery-photo]")];
  const status = gallery.querySelector("[data-gallery-status]");
  let current = 0;

  function showPhoto(index) {
    current = (index + photos.length) % photos.length;
    const photo = photos[current];
    image.src = photo.dataset.galleryPhoto;
    image.alt = photo.getAttribute("aria-label");
    status.textContent = "Image " + (current + 1) + " of " + photos.length + ". " + image.alt;
    photos.forEach((item, number) => item.setAttribute("aria-pressed", String(current === number)));
  }

  photos.forEach((photo, index) => photo.addEventListener("click", () => showPhoto(index)));
  gallery.querySelectorAll("[data-gallery-step]").forEach((button) => {
    button.addEventListener("click", () => showPhoto(current + Number(button.dataset.galleryStep)));
  });
}

const detailLinks = [...document.querySelectorAll("[data-detail-nav] a")];
function highlightDetailLink() {
  const target = window.location.hash || "#overview";
  detailLinks.forEach((link) => {
    if (link.hash === target) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  });
}
if (detailLinks.length) {
  highlightDetailLink();
  window.addEventListener("hashchange", highlightDetailLink);
}

const wishlistKey = "ford-wishlist";
let savedCars = new Set();
try {
  const saved = JSON.parse(window.localStorage.getItem(wishlistKey) || "[]");
  if (Array.isArray(saved)) savedCars = new Set(saved);
} catch {
  // Keep the wishlist usable for this visit if browser storage is unavailable.
}

document.querySelectorAll("[data-wishlist]").forEach((button) => {
  const slug = button.dataset.wishlist;
  const label = button.querySelector("[data-wishlist-label]");

  function updateButton() {
    const saved = savedCars.has(slug);
    button.setAttribute("aria-pressed", String(saved));
    if (label) label.textContent = saved ? "Saved to Wishlist" : "Save to Wishlist";
  }

  updateButton();
  button.addEventListener("click", () => {
    if (savedCars.has(slug)) savedCars.delete(slug);
    else savedCars.add(slug);
    updateButton();
    try {
      window.localStorage.setItem(wishlistKey, JSON.stringify([...savedCars]));
    } catch {
      // The selection remains available on this page.
    }
  });
});

const newsletter = document.querySelector("[data-demo-newsletter]");
if (newsletter) {
  newsletter.addEventListener("submit", (event) => {
    event.preventDefault();
    newsletter.parentElement.querySelector("[role=status]").textContent = "Demo signup complete.";
    newsletter.reset();
  });
}
