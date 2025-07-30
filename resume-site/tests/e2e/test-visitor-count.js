const puppeteer = require('puppeteer');

const url = process.argv[2]; // URL passed in from GitHub Actions

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  try {
    console.log(`Navigating to ${url}`);
    await page.goto(url, { waitUntil: 'networkidle2' });

    await page.waitForSelector('#visitor-count', { timeout: 5000 });

    const visitorCount = await page.$eval('#visitor-count', el => el.textContent.trim());
    const asNumber = parseInt(visitorCount, 10);

    if (isNaN(asNumber)) {
      throw new Error(`Visitor count is not a number: "${visitorCount}"`);
    }

    console.log(`✅ Visitor count loaded and is a number: ${asNumber}`);
  } catch (err) {
    console.error(`❌ Test failed: ${err.message}`);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();

