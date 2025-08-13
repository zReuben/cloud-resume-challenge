fetch('/config.json', { cache: 'no-store' })
  .then(res => res.json())
  .then(cfg => {
    const url = cfg.apiBaseUrl;

    // First: Increment the visitor count
    return fetch(url, { method: 'POST' })
      .then(() => {
        // Then: Retrieve the updated visitor count
        return fetch(url);
      })
      .then(response => response.json())
      .then(data => {
        document.getElementById('replaceme').innerText = data.count;
      });
  })
  .catch(error => {
    console.error('Error loading config or fetching visitor count:', error);
  });
