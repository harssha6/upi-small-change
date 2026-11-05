# UPI became small change

A live, interactive report built from NPCI's public UPI statistics, April 2016 to October 2026.

**Live:** https://now.harssha.design/upi-six-charts/

The thesis: UPI did not grow by moving more money per payment. It grew by swallowing the ₹65 cigarette, the ₹120 vada pav and the ₹214 grocery run. Seven claims, each with the chart that proves it.

1. Growth fell from 56% to 23%. Nothing slowed down.
2. UPI lost a fifth of its payments in April 2020. Once.
3. People still get ₹2,400 a payment. Shops get ₹603.
4. Brokers take 0.6% of merchant taps and 8.4% of the money.
5. FamApp averages ₹132 a payment. Cred averages ₹3,881.
6. PhonePe and Google Pay peaked at 87%. They hold 79% now.
7. Bengaluru is 57% of Karnataka's UPI.

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
