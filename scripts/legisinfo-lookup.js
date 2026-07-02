// legisinfo-lookup.js
// Looks up a Canadian bill on LEGISinfo and extracts its summary and full text
// Created: 2026-04-04

const { chromium } = require('playwright-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

chromium.use(StealthPlugin());

async function lookup() {

  const browser = await chromium.launch({
    headless: true,
    args: ['--lang=en-CA', '--disable-blink-features=AutomationControlled']
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    locale: 'en-CA',
    timezoneId: 'America/Toronto',
    viewport: { width: 1280, height: 900 }
  });

  const page = await context.newPage();

  // Search LEGISinfo for Bill C-15
  console.log('Searching LEGISinfo for Bill C-15...');
  await page.goto('https://www.parl.ca/legisinfo/en/bill/44-1/c-15', {
    waitUntil: 'domcontentloaded', timeout: 30000
  });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: 'legisinfo-c15.png' });

  const pageText = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync('legisinfo-c15.txt', pageText);
  console.log('LEGISinfo page saved');

  // Also try to get the full bill text from laws-lois.justice.gc.ca
  console.log('\nFetching full bill text...');
  await page.goto('https://www.parl.ca/DocumentViewer/en/44-1/bill/C-15/royal-assent', {
    waitUntil: 'domcontentloaded', timeout: 30000
  });
  await page.waitForTimeout(3000);

  const billText = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync('bill-c15-text.txt', billText);
  console.log('Bill text saved');

  // Search for Insurance Companies Act references
  const icaLines = billText.split('\n')
    .map(l => l.trim())
    .filter(l => l.toLowerCase().includes('insurance companies act') || l.toLowerCase().includes('insurance companies'));

  console.log('\n--- Insurance Companies Act references ---');
  icaLines.slice(0, 20).forEach(l => console.log(l));

  await browser.close();
}

lookup().catch(console.error);
