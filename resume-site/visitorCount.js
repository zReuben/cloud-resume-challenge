fetch('https://79tbi3g6al.execute-api.us-east-1.amazonaws.com/Stage/hello')
  .then(response => response.json())
  .then(data => {
    document.getElementById('replaceme').innerText = data.count;
  })
  .catch(error => {
    console.error('Error fetching visitor count:', error);
  });

