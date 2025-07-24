let currentPage = 0;

function updateBook() {
  const pages = document.querySelectorAll(".page");

  pages.forEach((page, index) => {
    if (index <= currentPage) {
      page.style.transform = "rotateY(-180deg)";
      page.style.zIndex = index + 1;
    } else {
      page.style.transform = "rotateY(0deg)";
      page.style.zIndex = pages.length - index;
    }
  });

  console.log(`📖 Viewing Page ${currentPage + 1} of ${pages.length}`);
}

document.addEventListener("DOMContentLoaded", () => {
  const nextBtn = document.getElementById("nextPage");
  const prevBtn = document.getElementById("prevPage");
  const pages = document.querySelectorAll(".page");

  if (!nextBtn || !prevBtn || pages.length === 0) {
    console.warn("Missing buttons or pages.");
    return;
  }

  nextBtn.addEventListener("click", () => {
    if (currentPage < pages.length - 1) {
      currentPage++;
      updateBook();
    }
  });

  prevBtn.addEventListener("click", () => {
    if (currentPage > 0) {
      currentPage--;
      updateBook();
    }
  });

  updateBook(); // Initial render
});
