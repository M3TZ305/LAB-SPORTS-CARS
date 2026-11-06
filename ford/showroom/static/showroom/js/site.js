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
  const dialog = gallery.querySelector("[data-gallery-dialog]");
  const expand = gallery.querySelector("[data-gallery-open]");
  const fullImage = dialog.querySelector("[data-full-image]");
  const caption = dialog.querySelector("[data-full-caption]");
  let current = 0;

  function syncDialog() {
    fullImage.src = image.src;
    fullImage.alt = image.alt;
    caption.textContent = (current + 1) + " / " + photos.length + " · " + image.alt;
  }

  expand.addEventListener("click", () => {
    syncDialog();
    dialog.showModal();
  });

  dialog.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowLeft" && event.key !== "ArrowRight") return;
    event.preventDefault();
    showPhoto(current + (event.key === "ArrowLeft" ? -1 : 1));
  });

  let touchStart;
  fullImage.addEventListener("touchstart", (event) => {
    touchStart = event.changedTouches[0].clientX;
  }, {passive: true});
  fullImage.addEventListener("touchend", (event) => {
    if (touchStart === undefined) return;
    const distance = event.changedTouches[0].clientX - touchStart;
    touchStart = undefined;
    if (Math.abs(distance) > 45) showPhoto(current + (distance > 0 ? -1 : 1));
  }, {passive: true});
  fullImage.addEventListener("touchcancel", () => { touchStart = undefined; });

  function showPhoto(index) {
    current = (index + photos.length) % photos.length;
    const photo = photos[current];
    image.src = photo.dataset.galleryPhoto;
    image.alt = photo.getAttribute("aria-label");
    if (dialog.open) syncDialog();
    status.textContent = (current + 1) + " / " + photos.length + " · " + image.alt;
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
    if (label) label.textContent = saved ? document.body.dataset.wishlistSaved : document.body.dataset.wishlistSave;
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
    newsletter.parentElement.querySelector("[role=status]").textContent = newsletter.dataset.success;
    newsletter.reset();
  });
}


const installments = document.querySelector("[data-installments]");
if (installments) {
  const fields = installments.elements;
  const price = Number(installments.dataset.price);
  const output = installments.querySelector("output");
  const arabic = document.documentElement.lang === "ar";
  const currency = new Intl.NumberFormat(arabic ? "ar-SA-u-nu-latn" : "en-SA", {
    style: "currency", currency: "SAR", currencyDisplay: arabic ? "symbol" : "code",
  });

  function updateEstimate() {
    if (!installments.checkValidity()) {
      output.textContent = installments.dataset.invalid;
      return;
    }
    const financed = price - fields.down.valueAsNumber;
    const months = Number(fields.months.value);
    const monthlyRate = fields.rate.valueAsNumber / 1200;
    const payment = monthlyRate === 0
      ? financed / months
      : financed * monthlyRate / (1 - (1 + monthlyRate) ** -months);
    output.textContent = installments.dataset.monthly.replace("{amount}", currency.format(payment));
  }

  installments.addEventListener("submit", (event) => {
    event.preventDefault();
    updateEstimate();
  });
  installments.addEventListener("input", updateEstimate);
  updateEstimate();
}


const actionLinks = [...document.querySelectorAll("[data-action-link]")];
if (actionLinks.length) {
  function syncActions() {
    const selected = actionLinks.find((link) => link.hash === window.location.hash);
    if (selected) {
      const panel = document.getElementById(selected.getAttribute("aria-controls"));
      requestAnimationFrame(() => panel.scrollIntoView({block: "start"}));
    }
    actionLinks.forEach((link) => {
      const panel = document.getElementById(link.getAttribute("aria-controls"));
      if (window.location.hash) panel.classList.remove("is-active");
      link.setAttribute("aria-expanded", String(
        link.hash === window.location.hash || panel.classList.contains("is-active")
      ));
    });
  }
  syncActions();
  window.addEventListener("hashchange", syncActions);
}

document.querySelectorAll("[data-preserve-hash]").forEach((form) => {
  form.addEventListener("submit", () => {
    const next = form.elements.namedItem("next");
    next.value = next.value.split("#")[0] + window.location.hash;
  });
});

const inventoryFilters = document.querySelector("[data-inventory-filters]");
if (inventoryFilters) {
  inventoryFilters.addEventListener("change", (event) => {
    if (event.target.matches("select")) inventoryFilters.requestSubmit();
  });
}
