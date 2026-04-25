const widgetPreloader = document.getElementById("widget_preloader");
if (widgetPreloader) {
  window.addEventListener("load", () => {
    widgetPreloader.remove();
  });
}
