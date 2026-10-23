function initializeNavigation() {
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");

  if (!navToggle || !navMenu || navToggle.dataset.initialized) {
    return;
  }

  navToggle.dataset.initialized = "true";
  navToggle.addEventListener("click", () => {
    const isOpen = navMenu.classList.toggle("is-open");
    document.body.classList.toggle("nav-open", isOpen);
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });

  navMenu.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      navMenu.classList.remove("is-open");
      document.body.classList.remove("nav-open");
      navToggle.setAttribute("aria-expanded", "false");
    });
  });
}

function initializeProfilePicture() {
  const visual = document.querySelector(".hero-visual-profile");
  const image = visual?.querySelector(".profile-picture");

  if (!visual || !image) {
    return;
  }

  const showImage = () => {
    visual.classList.remove("is-image-error");
    visual.classList.add("is-image-loaded");
  };
  const hideImage = () => visual.classList.add("is-image-error");

  image.addEventListener("load", showImage, { once: true });
  image.addEventListener("error", hideImage, { once: true });
  if (image.complete) {
    if (image.naturalWidth > 0) {
      showImage();
    } else {
      hideImage();
    }
  }
}

async function loadHomeContent() {
  const homeContent = document.querySelector("#home-content");
  if (!homeContent) {
    return;
  }

  try {
    const response = await fetch(homeContent.dataset.contentUrl, {
      headers: { Accept: "text/html" },
    });
    if (!response.ok) {
      throw new Error(`Home content request failed with status ${response.status}`);
    }

    const html = await response.text();
    const updatedPage = new DOMParser().parseFromString(html, "text/html");
    const updatedContent = updatedPage.querySelector("#home-content");
    if (!updatedContent) {
      throw new Error("Home content response did not contain the expected content");
    }

    const currentForm = homeContent.querySelector(".contact-form");
    const formValues = currentForm
      ? Object.fromEntries(new FormData(currentForm).entries())
      : {};

    homeContent.replaceWith(updatedContent);
    document.querySelector(".brand-socials").innerHTML =
      updatedPage.querySelector(".brand-socials").innerHTML;
    document.querySelector(".nav-menu").innerHTML =
      updatedPage.querySelector(".nav-menu").innerHTML;
    document.querySelector(".footer-grid").innerHTML =
      updatedPage.querySelector(".footer-grid").innerHTML;
    document.title = updatedPage.title;

    ["description", "og:title", "og:description"].forEach((name) => {
      const attribute = name.startsWith("og:") ? "property" : "name";
      const selector = `meta[${attribute}="${name}"]`;
      const currentMeta = document.querySelector(selector);
      const updatedMeta = updatedPage.querySelector(selector);
      if (currentMeta && updatedMeta) {
        currentMeta.content = updatedMeta.content;
      }
    });

    const updatedForm = updatedContent.querySelector(".contact-form");
    if (updatedForm) {
      for (const [name, value] of Object.entries(formValues)) {
        const field = updatedForm.elements.namedItem(name);
        if (field && "value" in field && value) {
          field.value = value;
        }
      }
    }

    initializeNavigation();
    initializeProfilePicture();
  } catch (error) {
    console.error("Unable to load portfolio content.", error);
  }
}

initializeNavigation();
initializeProfilePicture();
loadHomeContent();
