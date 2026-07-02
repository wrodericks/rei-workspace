# Scripts

Useful scripts built with Playwright. All run via Node.js.

---

## flight-search.js

Search Google Flights and get results without opening a browser.

**Usage:**
```
node flight-search.js --from YYZ --to HND --depart 2026-07-02 --return 2026-08-14 --cabin business --adults 3 --children 1
```

**Options:**
| Flag | Description | Default |
|------|-------------|---------|
| `--from` | Origin airport code | YYZ |
| `--to` | Destination airport code | HND |
| `--depart` | Departure date (YYYY-MM-DD) | required |
| `--return` | Return date (YYYY-MM-DD) | required |
| `--cabin` | economy / premium / business / first | economy |
| `--adults` | Number of adults | 1 |
| `--children` | Number of children (age 2-11) | 0 |

**Notes:**
- Prices shown are per adult, taxes included
- Google Flights always shows per-adult prices regardless of passenger count
- Child pricing varies by airline and is not included in the total estimate
- Results are sorted by price + convenience (Google's default ranking)

**Created:** 2026-04-04
