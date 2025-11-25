

document.addEventListener("DOMContentLoaded", function() {
    const modal = document.getElementById("attendanceModal");
    const openModalBtn = document.getElementById("side-bar-import-form");
    const openModalBtn2 = document.getElementById("side-bar-import-form2");
    const closeModalBtn = document.getElementById("closeModalBtn");

    openModalBtn2.addEventListener("click", function() {
      modal.style.display = "flex";
      document.body.classList.add("no-scroll");
    });
    
    openModalBtn.addEventListener("click", function() {
      modal.style.display = "flex";
      document.body.classList.add("no-scroll");
    });

    closeModalBtn.addEventListener("click", function() {
      modal.style.display = "none";
      document.body.classList.remove("no-scroll");
    });

    window.addEventListener("click", function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
        document.body.classList.remove("no-scroll");
      }
    });

  });

