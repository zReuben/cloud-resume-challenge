// First: Increment the visitor count
fetch('https://hoywemblq6.execute-api.us-east-1.amazonaws.com/Prod/visitor-count', {
  method: 'POST'
})
  .then(() => {
    // Then: Retrieve the updated visitor count
    return fetch('https://hoywemblq6.execute-api.us-east-1.amazonaws.com/Prod/visitor-count');
  })
  .then(response => response.json())
  .then(data => {
    document.getElementById('replaceme').innerText = data.count;
  })
  .catch(error => {
    console.error('Error incrementing or fetching visitor count:', error);
  });
