const puppeteer = require('puppeteer');

(async () => {
  const url = process.argv[2];
  if (!url) {
    console.error('Usage: node test-visitor-count.js <url>');
    process.exit(1);
  }

  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  await page.goto(url, { waitUntil: 'networkidle2' });

  try {
    // Wait for the #visitor-count element to show up in the DOM
    await page.waitForSelector('#visitor-count', { timeout: 5000 });

    const visitorCount = await page.$eval('#visitor-count', el => el.textContent);
    console.log(`Visitor count displayed: ${visitorCount}`);

    // Check if it's actually a number
    if (!/^\d+$/.test(visitorCount.trim())) {
      console.error('Visitor count is not a valid number');
      process.exit(1);
    }
  } catch (err) {
    console.error('Error in E2E test:', err.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
