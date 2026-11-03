# UPI became small change

A live, interactive report built from NPCI's public UPI statistics, April 2016 to October 2026.

**Live:** https://now.harssha.design/upi-six-charts/

The thesis: UPI did not grow by moving more money per payment. It grew by swallowing the ₹65 cigarette, the ₹120 vada pav and the ₹214 grocery run. Seven claims, each with the chart that proves it.

1. It stopped compounding. It now adds the same four billion a year.
2. Ten years, one crash, and a February problem.
3. The average payment halved. Nobody started paying less.
4. Merchants are wide and short. Finance is thin and tall.
5. The rupee ladder: everything in UPI, placed by what one payment is worth.
6. The duopoly is not cracking from the top. It is being nibbled from the bottom.
7. A state's UPI is mostly its one metro.

## Layout

```
data/        CSVs scraped from NPCI's JSON endpoints (Nov 2026)
src/page.html  the page: HTML, CSS and D3 charts, with a /*__DATA__*/ slot
src/page-v1.html  the first, table-like version, kept for comparison
build.py     embeds the CSVs into src/page.html and writes index.html
shoot.py     Playwright pass: renders every chapter, both themes, checks tooltips
assets/      photos (Unsplash) and the UPI mark
index.html   the built page
```

Rebuild after editing the template or data:

```sh
python3 build.py
python3 shoot.py 1280   # optional: screenshots into shots/
```

## Data

NPCI's site blocks plain HTTP clients, so the tables were fetched from inside a browser session against the same JSON API the site uses. Headline volume and value run to October 2026. App, merchant and state tables run to September 2026. Average ticket is value divided by volume. Merchant categories use NPCI's MCC grouping. 44% of state-wise volume is unclassified in the source.

## Credits

Photos by Rudra Gupta, Urip Dunker, rupixen and David De Gendt on Unsplash. Type is Fraunces and Inter. Charts are D3.
