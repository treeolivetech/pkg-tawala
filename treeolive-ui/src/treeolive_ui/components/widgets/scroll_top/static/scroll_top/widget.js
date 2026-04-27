const widgetScrollTop = document.getElementById("widget_scroll_top");

function toggleScrollTop() {
  if (!widgetScrollTop) return;

  const shouldShow = window.scrollY > 100;
  widgetScrollTop.classList.toggle("opacity-0", !shouldShow);
  widgetScrollTop.classList.toggle("invisible", !shouldShow);
  widgetScrollTop.classList.toggle("opacity-100", shouldShow);
  widgetScrollTop.classList.toggle("visible", shouldShow);
}

if (widgetScrollTop) {
  widgetScrollTop.addEventListener("click", (e) => {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
}

window.addEventListener("load", toggleScrollTop);
document.addEventListener("scroll", toggleScrollTop);
