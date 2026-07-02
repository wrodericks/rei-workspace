// google-flights-final.js
// Searches Google Flights: YYZ -> HND, Business, Jul 2 - Aug 14 2026
// Fixed: destination selection + correct search button
// Created: 2026-04-04

const { chromium } = require('playwright-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');

chromium.use(StealthPlugin());

async function searchFlights() {

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

  console.log('Loading Google Flights...');
  await page.goto('https://www.google.com/travel/flights?hl=en-CA&gl=CA&curr=CAD', {
    waitUntil: 'domcontentloaded', timeout: 30000
  });
  await page.waitForTimeout(3000);

  // ---- Business class ----
  console.log('Selecting Business class...');
  await page.locator('div[role="combobox"]:has-text("Economy")').click();
  await page.waitForTimeout(800);
  await page.locator('ul[aria-label="Select your preferred seating class."] li:has-text("Business")').click();
  await page.waitForTimeout(800);

  // ---- Destination ----
  console.log('Setting destination...');
  const destField = page.locator('input[placeholder="Where to?"]').first();
  await destField.click();
  await page.waitForTimeout(500);
  await destField.fill('HND');  // Use airport code for unambiguous match
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'final-step1-dest-typed.png' });

  // Look for the HND suggestion and click it directly
  const hndOption = page.locator('[role="option"]').filter({ hasText: 'HND' }).first();
  if (await hndOption.isVisible({ timeout: 5000 })) {
    await hndOption.click();
    console.log('Selected HND from dropdown');
  } else {
    // Fallback: try pressing Enter on first option
    await page.keyboard.press('ArrowDown');
    await page.waitForTimeout(300);
    await page.keyboard.press('Enter');
    console.log('Selected first dropdown option');
  }
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'final-step2-dest-selected.png' });

  // ---- Dates ----
  console.log('Opening date picker...');
  await page.locator('input[placeholder="Departure"]').first().click();
  await page.waitForTimeout(2000);

  // Navigate to July
  const nextBtn = page.locator('button[aria-label="Next"]').first();
  for (let i = 0; i < 3; i++) { await nextBtn.click(); await page.waitForTimeout(600); }

  // Select July 2
  await page.locator('[aria-label="Thursday, July 2, 2026"]').click();
  await page.waitForTimeout(800);
  console.log('Departure date: July 2 selected');

  // Select August 14
  await page.locator('[aria-label="Friday, August 14, 2026"]').click();
  await page.waitForTimeout(800);
  console.log('Return date: August 14 selected');
  await page.screenshot({ path: 'final-step3-dates-selected.png' });

  // Close calendar
  await page.locator('button:has-text("Done")').last().click();
  await page.waitForTimeout(1500);
  await page.screenshot({ path: 'final-step4-ready.png' });

  // ---- Click the search button ----
  // After a specific destination is selected the button should say "Search"
  // Try multiple possible selectors
  console.log('Clicking Search...');
  try {
    // Try the search button that appears when a specific destination is set
    const searchBtn = page.locator('button:has(svg)').filter({ hasText: /search/i }).first();
    await searchBtn.click({ timeout: 5000 });
  } catch {
    try {
      // Try button with magnifying glass icon that contains "Search" text
      await page.locator('button[jsname="vLv7Lb"]').click({ timeout: 3000 });
    } catch {
      // Last resort: press Enter in the destination field
      await destField.press('Enter');
    }
  }

  console.log('Waiting for results...');
  await page.waitForTimeout(12000);
  await page.screenshot({ path: 'final-step5-results.png', fullPage: false });

  // Extract prices
  const pageText = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync('final-results-text.txt', pageText);

  const prices = pageText.match(/\$[\d,]+/g) || [];
  if (prices.length > 0) {
    console.log('\n--- Prices found ---');
    console.log([...new Set(prices)].slice(0, 20).join(', '));
  } else {
    console.log('No prices found — check final-results-text.txt');
  }

  await browser.close();
}

searchFlights();
