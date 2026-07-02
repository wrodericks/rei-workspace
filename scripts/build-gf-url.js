// build-gf-url.js
// Builds a Google Flights search URL from scratch by modifying the protobuf bytes
// Created: 2026-04-04

function buildTfs({ origin, destination, departDate, returnDate, cabin, adults, children }) {
  // Cabin class values: 1=Economy, 2=Premium Economy, 3=Business, 4=First
  const cabinByte = cabin;

  // Helper: encode a string field (tag + length + bytes)
  function strField(tag, str) {
    const strBytes = Buffer.from(str, 'ascii');
    return Buffer.concat([Buffer.from([tag, strBytes.length]), strBytes]);
  }

  // Helper: encode a varint (variable length integer)
  function varint(n) {
    const bytes = [];
    while (n > 127) {
      bytes.push((n & 0x7f) | 0x80);
      n >>= 7;
    }
    bytes.push(n);
    return Buffer.from(bytes);
  }

  // Helper: encode a length-delimited message field
  function msgField(tag, inner) {
    return Buffer.concat([Buffer.from([tag, inner.length]), inner]);
  }

  // Build a leg sub-message: { date, from, to }
  function buildLeg(date, from, to) {
    // Field 2 (tag 0x12): date string
    const dateField = strField(0x12, date);
    // Field 13 (tag 0x6a): origin airport sub-message
    const originInner = Buffer.concat([Buffer.from([0x08, 0x01]), strField(0x12, from)]);
    const originField = msgField(0x6a, originInner);
    // Field 14 (tag 0x72): destination airport sub-message
    const destInner = Buffer.concat([Buffer.from([0x08, 0x01]), strField(0x12, to)]);
    const destField = msgField(0x72, destInner);
    return Buffer.concat([dateField, originField, destField]);
  }

  // Outbound leg: origin -> destination, departDate
  const leg1Inner = buildLeg(departDate, origin, destination);
  const leg1 = msgField(0x1a, leg1Inner);

  // Return leg: destination -> origin, returnDate
  const leg2Inner = buildLeg(returnDate, destination, origin);
  const leg2 = msgField(0x1a, leg2Inner);

  // Field 8 (tag 0x40): trip type, 1 = round trip
  const tripType = Buffer.from([0x40, 0x01]);

  // Field 9 (tag 0x48): cabin class
  const cabinField = Buffer.from([0x48, cabinByte]);

  // Field 14 (tag 0x70): ??? (was 0x01 in original, seems to be a flag)
  const flag = Buffer.from([0x70, 0x01]);

  // Field 16 (tag 0x82 0x01): a sub-message with 0xff... bytes (filter/options)
  const optionsInner = Buffer.from([0x08, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0x01]);
  const options = Buffer.concat([Buffer.from([0x82, 0x01, optionsInner.length]), optionsInner]);

  // Field 19 (tag 0x98 0x01): number of adults
  const adultsField = Buffer.concat([Buffer.from([0x98, 0x01]), varint(adults)]);

  // Field 20 (tag 0xa0 0x01): number of children (age 2-11)
  // Only include if children > 0
  let childrenField = Buffer.alloc(0);
  if (children > 0) {
    childrenField = Buffer.concat([Buffer.from([0xa0, 0x01]), varint(children)]);
  }

  // header bytes from original: 08 1c 10 02
  const header = Buffer.from([0x08, 0x1c, 0x10, 0x02]);

  const tfsBytes = Buffer.concat([
    header, leg1, leg2, tripType, cabinField, flag, options, adultsField, childrenField
  ]);

  // Encode as base64url
  return tfsBytes.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
}

// Build for: 3 adults, 1 child, Business, YYZ->HND, Jul 2 - Aug 14 2026
const tfs = buildTfs({
  origin: 'YYZ',
  destination: 'HND',
  departDate: '2026-07-02',
  returnDate: '2026-08-14',
  cabin: 3,       // Business
  adults: 3,
  children: 1
});

const url = `https://www.google.com/travel/flights/search?tfs=${tfs}&tfu=EgYIABAAGAA&hl=en&gl=CA`;
console.log('Built URL:');
console.log(url);
