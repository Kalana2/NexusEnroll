
function closeModal() {
  document.body.style.display = "none";
}

// Handle login form submission and redirect based on role
document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('signinForm');
  if (form) {
    form.addEventListener('submit', async function(e) {
      e.preventDefault();
      const formData = new FormData(form);
      const response = await fetch('/login', {
        method: 'POST',
        body: formData,
        credentials: 'include'
      });
      const data = await response.json();
      if (data.success) {
        if (data.role === 'admin') {
          window.location.href = '/admin';
        } else if (data.role === 'student') {
          window.location.href = '/student';
        } else if (data.role === 'faculty') {
          window.location.href = '/faculty';
        } else {
          window.location.href = '/';
        }
      } else {
        alert(data.message || 'Login failed');
      }
    });
  }
});
