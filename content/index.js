document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("root");
  if (!root) {
    console.error("No #root element found in HTML!");
    return;
  }

  root.innerHTML = `
    <div>
      <h1>Welcome to My Quartz Site</h1>
      <p>This site is built using Quartz and Vanilla JS.</p>
    </div>
  `;
});
