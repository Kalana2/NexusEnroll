const overlay = document.getElementById("overlay");
const openBtn = document.getElementById("openOverlay");
const closeBtn = document.getElementById("closeOverlay");

openBtn.onclick = () => (overlay.style.display = "flex");
closeBtn.onclick = () => (overlay.style.display = "none");

function confirmDelete() {
  document.getElementById("deleteModal").style.display = "block";
}
function cancelDelete() {
  currentItemToDelete = null;
  document.getElementById("deleteModal").style.display = "none";
}
window.onclick = function (event) {
  const modal = document.getElementById("deleteModal");
  if (event.target === modal) {
    cancelDelete();
  }
};
