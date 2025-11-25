
(function() {
  function $(sel, ctx) { return (ctx || document).querySelector(sel); }
  const modal = $('#attendanceModal');
  const closeBtn = $('#closeModalBtn');

  if (!modal) {
    console.warn('modal.js: #attendanceModal not found on page.');
    return;
  }

  function openModal() {
    modal.style.display = 'flex';
    document.body.classList.add('no-scroll');
  }
  function closeModal() {
    modal.style.display = 'none';
    document.body.classList.remove('no-scroll');
  }

  
  document.addEventListener('click', function (e) {
    
    if (e.target.closest('#side-bar-import-form') || e.target.closest('#side-bar-import-form2')) {
      e.preventDefault();
      openModal();
      return;
    }

    
    if (e.target.closest('#closeModalBtn') || e.target.closest('.modal .close')) {
      e.preventDefault();
      closeModal();
      return;
    }

    
    if (e.target === modal) {
      closeModal();
      return;
    }
  });

  
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.style.display === 'flex') closeModal();
  });

  
  console.log('modal.js loaded — modal element found:', !!modal);
})();
