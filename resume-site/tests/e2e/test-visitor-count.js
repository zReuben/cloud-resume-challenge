const puppeteer = require('puppeteer');

(async () => {
  const url = process.argv[2]; // Accepts URL from CLI
  const browser = await puppeteer.launch({ args: ['--no-sandbox'] });
  const page = await browser.newPage();

  try {
    console.log(`Visiting ${url}...`);
    await page.goto(url, { waitUntil: 'networkidle2' });

    // Wait for the #visitor-count element to be available
    await page.waitForSelector('#visitor-count', { timeout: 5000 });

    // Extract the text content
    const countText = await page.$eval('#visitor-count', el => el.textContent.trim());

    if (countText && /^\d+$/.test(countText)) {
      console.log(`Visitor count: ${countText}`);
    } else {
      throw new Error(`Unexpected text in visitor count: "${countText}"`);
    }

  } catch (err) {
    console.error("Error in E2E test:", err.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
