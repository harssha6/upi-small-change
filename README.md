# UPI is now mostly small payments

A live, interactive report built from NPCI's public UPI statistics, April 2016 to October 2026.

**Live:** https://now.harssha.design/upi-small-payments/

UPI does 25 billion payments a month and the average one is ₹1,238, smaller every year. The report shows where the growth came from: groceries, cigarettes, a few cities and two apps. Seven charts, one claim each.

1. UPI adds the same four billion payments every year.
2. Only one month in ten years went backwards: April 2020.
3. The average payment is shrinking. Shop payments are the reason.
4. Shops get many tiny payments. Finance gets a few big ones.
5. Every app, bank and state, ranked by the size of one payment.
6. PhonePe and Google Pay own 79%. The rest is growing anyway.
7. In most states, one city does most of the paying.

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
