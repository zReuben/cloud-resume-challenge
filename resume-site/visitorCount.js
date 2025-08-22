const spinner = document.getElementById("spinner");
const countSpan = document.getElementById("replaceme");

if (spinner) {
  spinner.style.display = "inline-block";
}

const url = "/visitor-count";

fetch(url, { method: "POST" })        // First: increment
  .then(() => fetch(url, { cache: "no-store" }))  // Then: read updated count
  .then(response => response.json())
  .then(data => {
    countSpan.innerText = data.count;
  })
  .catch(error => {
    console.error("Error fetching visitor count:", error);
    countSpan.innerText = "N/A";
  })
  .finally(() => {
    if (spinner) {
      spinner.style.display = "none";
    }
  });
