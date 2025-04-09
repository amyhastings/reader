document.addEventListener('DOMContentLoaded', function () {
    const pageSearchForm = document.getElementById('page_search_form');
    const progressBarContainer = document.getElementById('progress-bar-container');
    const progressBar = document.getElementById('progress-bar');
  
    if (pageSearchForm) {
      pageSearchForm.addEventListener('submit', function (event) {
        // Show the progress bar
        progressBarContainer.classList.remove('d-none');
  
        // Reset the progress bar
        progressBar.style.width = '0%';
        progressBar.setAttribute('aria-valuenow', '0');
  
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
          progress += 10; // Increment progress by 10%
          progressBar.style.width = `${progress}%`;
          progressBar.setAttribute('aria-valuenow', progress);
  
          // Stop the progress bar at 100%
          if (progress >= 100) {
            clearInterval(interval);
          }
        }, 200); // Update every 200ms
      });
    }
});

window.addEventListener('load', function () {
    const progressBarContainer = document.getElementById('progress-bar-container');
    if (progressBarContainer) {
      progressBarContainer.classList.add('d-none');
    }
  });

  document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('search_form');
    const progressBarContainer = document.getElementById('progress-bar-container');
    const progressBar = document.getElementById('progress-bar');
  
    if (searchForm) {
      searchForm.addEventListener('submit', function (event) {
        // Show the progress bar
        progressBarContainer.classList.remove('d-none');
  
        // Reset the progress bar
        progressBar.style.width = '0%';
        progressBar.setAttribute('aria-valuenow', '0');
  
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
          progress += 10; // Increment progress by 10%
          progressBar.style.width = `${progress}%`;
          progressBar.setAttribute('aria-valuenow', progress);
  
          // Stop the progress bar at 100%
          if (progress >= 100) {
            clearInterval(interval);
          }
        }, 200); // Update every 200ms
      });
    }
});