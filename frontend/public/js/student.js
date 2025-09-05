function showSchedule(tab) {
  document.getElementById('current').style.display = (tab === 'current') ? 'block' : 'none';
  document.getElementById('past').style.display = (tab === 'past') ? 'block' : 'none';
  document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
  event.target.classList.add('active');
}
