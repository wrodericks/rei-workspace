// flight-search.js
// Search Google Flights from the command line — no browser required.
//
// Usage:
//   node flight-search.js --from YYZ --to HND --depart 2026-07-02 --return 2026-08-14 --cabin business --adults 3 --children 1
//
// Cabin options: economy, premium, business, first
// Defaults: 1 adult, 0 children, economy
//
// Created: 2026-04-04

const { chromium } = require('playwright-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');

chromium.use(StealthPlugin());

// ---- Parse command line arguments ----
const args = process.argv.slice(2);
const get = (flag) => { const i = args.indexOf(flag); return i !== -1 ? args[i + 1] : null; };

const config = {
  from:     get('--from')     || 'YYZ',
  to:       get('--to')       || 'HND',
  depart:   get('--depart'),
  ret:      get('--return'),
  cabin:    get('--cabin')    || 'economy',
  adults:   parseInt(get('--adults')   || '1'),
  children: parseInt(get('--children') || '0'),
};

if (!config.depart || !config.ret) {
  console.error('Error: --depart and --return dates are required (format: YYYY-MM-DD)');
  process.exit(1);
}

// ---- Cabin class encoding ----
const cabinCodes = { economy: 1, premium: 2, business: 3, first: 4 };
const cabinCode = cabinCodes[config.cabin.toLowerCase()] || 1;
const cabinLabel = Object.keys(cabinCodes).find(k => cabinCodes[k] === cabinCode);

// ---- Build the Google Flights tfs protobuf URL parameter ----
function buildTfs({ origin, destination, departDate, returnDate, cabin, adults, children }) {

  function strField(tag, str) {
    const b = Buffer.from(str, 'ascii');
    return Buffer.concat([Buffer.from([tag, b.length]), b]);
  }

  function varint(n) {
    const bytes = [];
    while (n > 127) { bytes.push((n & 0x7f) | 0x80); n >>= 7; }
    bytes.push(n);
    return Buffer.from(bytes);
  }

  function msgField(tag, inner) {
    return Buffer.concat([Buffer.from([tag, inner.length]), inner]);
  }

  function buildLeg(date, from, to) {
    const dateField   = strField(0x12, date);
    const originInner = Buffer.concat([Buffer.from([0x08, 0x01]), strField(0x12, from)]);
    const destInner   = Buffer.concat([Buffer.from([0x08, 0x01]), strField(0x12, to)]);
    return Buffer.concat([dateField, msgField(0x6a, originInner), msgField(0x72, destInner)]);
  }

  const leg1    = msgField(0x1a, buildLeg(departDate, origin, destination));
  const leg2    = msgField(0x1a, buildLeg(returnDate, destination, origin));
  const options = Buffer.concat([
    Buffer.from([0x82, 0x01, 0x0b]),
    Buffer.from([0x08, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x01])
  ]);
  const adultsField   = Buffer.concat([Buffer.from([0x98, 0x01]), varint(adults)]);
  const childrenField = children > 0
    ? Buffer.concat([Buffer.from([0xa0, 0x01]), varint(children)])
    : Buffer.alloc(0);

  const tfsBytes = Buffer.concat([
    Buffer.from([0x08, 0x1c, 0x10, 0x02]),  // header
    leg1, leg2,
    Buffer.from([0x40, 0x01]),               // round trip
    Buffer.from([0x48, cabin]),              // cabin class
    Buffer.from([0x70, 0x01]),               // flag
    options,
    adultsField,
    childrenField
  ]);

  return tfsBytes.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

// ---- Main ----
async function search() {
  const tfs = buildTfs({
    origin:      config.from,
    destination: config.to,
    departDate:  config.depart,
    returnDate:  config.ret,
    cabin:       cabinCode,
    adults:      config.adults,
    children:    config.children,
  });

  const url = `https://www.google.com/travel/flights/search?tfs=${tfs}&tfu=EgYIABAAGAA&hl=en&gl=CA`;

  console.log(`\nSearching: ${config.from} → ${config.to}`);
  console.log(`Dates:     ${config.depart} → ${config.ret}`);
  console.log(`Cabin:     ${cabinLabel}`);
  console.log(`Passengers: ${config.adults} adult(s), ${config.children} child(ren)\n`);

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
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });

  // Retry on error
  for (let i = 1; i <= 3; i++) {
    const err = await page.locator('text=something went wrong').isVisible().catch(() => false);
    if (err) { await page.reload({ waitUntil: 'domcontentloaded' }); await page.waitForTimeout(6000); }
    else break;
  }
  await page.waitForTimeout(5000);

  // Extract flight results from page text
  const pageText = await page.evaluate(() => document.body.innerText);
  await browser.close();

  // Parse results: find lines with prices and nearby context
  const lines = pageText.split('\n').map(l => l.trim()).filter(l => l);
  const results = [];
  let current = {};

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    if (line.match(/^CA\$[\d,]+$/)) {
      current.price = line;
      if (current.airline) results.push({ ...current });
      current = {};
    } else if (line.match(/Nonstop|1 stop|2 stops|3 stops/)) {
      current.stops = line;
    } else if (line.match(/\d{1,2}:\d{2}/) && !current.times) {
      current.times = line;
    } else if (line.match(/hr \d{1,2} min|hr$/) && !current.duration) {
      current.duration = line;
    } else if (line.match(/Air Canada|United|ANA|Japan Airlines|All Nippon|American|Delta|JAL/i) && !current.airline) {
      current.airline = line;
    }
  }

  if (results.length === 0) {
    console.log('No results parsed — raw price lines:');
    lines.filter(l => l.includes('CA$')).slice(0, 10).forEach(l => console.log(' ', l));
    return;
  }

  console.log('='.repeat(55));
  console.log(`Results (per adult, taxes included):`);
  console.log('='.repeat(55));
  results.slice(0, 8).forEach((r, i) => {
    console.log(`\n${i + 1}. ${r.airline || 'Unknown airline'}`);
    if (r.stops)    console.log(`   Stops:    ${r.stops}`);
    if (r.times)    console.log(`   Times:    ${r.times}`);
    if (r.duration) console.log(`   Duration: ${r.duration}`);
    if (r.price)    console.log(`   Price:    ${r.price} per adult`);
  });

  const totalAdults = config.adults;
  const cheapest = results[0];
  if (cheapest?.price) {
    const perAdult = parseInt(cheapest.price.replace(/[^0-9]/g, ''));
    const totalEst = perAdult * totalAdults;
    console.log(`\n${'='.repeat(55)}`);
    console.log(`Cheapest option: ${cheapest.price} per adult`);
    console.log(`Estimated total for ${totalAdults} adults: CA$${totalEst.toLocaleString()}`);
    console.log(`(Child pricing varies by airline — not included above)`);
  }
}

search().catch(console.error);
