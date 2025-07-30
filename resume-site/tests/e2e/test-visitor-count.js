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
  await page.goto(url, { waitUntil: 'networkidle0' });

  const visitorCount = await page.$eval('#visitor-count', el => el.textContent);
  console.log(`Visitor count displayed: ${visitorCount}`);

  if (!/^\d+$/.test(visitorCount.trim())) {
    console.error('Visitor count is not a number!');
    process.exit(1);
  }

  await browser.close();
})();
