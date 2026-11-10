# Stratos-v2 handover

Last updated: 10 Nov 2026
Repo: `Stratos-v2` (Flask site for Stratos, replacing the FKPA Global site)
Brief: Leah Dovey's QA and design list, plus a check of the site against the Canva brand kit.

---

## 1. Status at a glance

| # | Leah's issue | Status |
|---|---|---|
| 1 | Blurry logo | Done |
| 2 | Nav in all caps | Done |
| 3 | No Playfair headings in all caps | Done, checked sitewide |
| 4 | Icon audit and list for Leah | Done, but the icon files have since been replaced (see 3.1) |
| 5 | Blue icons to white, no white background patches | Superseded. The white filter was removed on 23 Oct because Leah's new icons are two-tone (see 3.1) |
| 6 | Remove footer grid pattern | Done |
| 7 | Fonts, weights and letter-spacing vs the brand kit | Done for headings, FAQ and footer (see 3.2 and 3.3). Body size is still open (see 5) |

Nothing from the changes below is committed yet. Every edit was written straight into the working folder. Commit and push is yours to do (see section 6).

---

## 2. Files touched in the latest rounds

All paths are relative to the repo root.

- `static/style.css`: heading weights, h4 and summary rules
- `static/stratos-refresh.css`: icon rules, callout fonts, FAQ summary, footer label fix. This is the file that wins most cascade fights.
- `templates/base.html`: Google Fonts URL and the CSS cache-bust version numbers
- `templates/home.html`: "How We Work" icons switched to the new files

Current cache-bust values in `base.html`:

- `style.css?v=20260904c`
- `stratos-refresh.css?v=20261006u`

Bump the version letter every time you change either CSS file. Browsers cache them hard.

---

## 3. What changed and why

### 3.1 Icons (23 Oct)

**Symptom:** the service-panel cards (for example "Complete UAE Establishment") showed a dashed circle and a solid white blob instead of an icon.

**Cause:** Leah replaced the `*_icon_blue.svg` files with detailed two-tone designs (light blue `#6ea0ff` plus white or near-white). Earlier CSS forced every icon to white with `filter: brightness(0) invert(1)`. That filter turns every colour into one flat colour, so all the internal detail disappeared.

**Fix, in `stratos-refresh.css`:**

- Removed `brightness(0) invert(1)` from `.svc-panel__icon`, `.card-icon`, `.band--navy .card-icon` and the "How We Work" `.info-card--icon .card-icon` rule.
- Removed the temporary `.card-icon--native` exemption CSS.

**In `home.html`:** the three "How We Work" icons that used plain fallback files now use their `_blue.svg` versions: `expert-knowledge`, `transparent-pricing` and `our-vision`.

The remaining `brightness(0) invert(1)` rules are on the footer and header logos. They are intentional, so leave them.

### 3.2 Typography vs the brand kit (21 and 23 Oct)

Brand kit: Playfair Display Regular (400) for Title, Subtitle and Heading. Raleway for Subheading. Raleway italic for Quote.

- Playfair Display 400 is now loaded in the Google Fonts URL in `base.html`.
- Every h1, h2, h3 and h4 rule across both CSS files is now weight 400. About 50 rules were changed. The bare `h1/h2/h3` defaults only reach elements nobody has styled more specifically, so the scoped rules had to be edited too.
- The desktop h4 rule (`@media (min-width: 1025px)`) was shrinking Subheadings to 18px. It is now 24px.
- `body main .callout` and `body main .fit-layout__text p.fit-note` now use Raleway (italic) instead of Playfair.
- The FAQ accordion question (`.faq-list summary`) is now 24px, weight 400, Raleway. A desktop `summary { ... !important }` rule in `style.css` was overriding the nicer rule in `stratos-refresh.css`, so both were changed. On phones the question stays 16px.

### 3.3 Footer labels (10 Nov)

The 23 Oct h4 change made the footer "STRATOS" and "LEGAL" labels 24px and light. On desktop (1025px and wider) they are back to 18px bold via an override in `stratos-refresh.css`, placed right after `html body .stratos-footer__col h4 { margin-bottom: 14px !important; }`.

---

## 4. Gotchas for whoever edits next

1. **Specificity and `!important` decide everything.** Both stylesheets are very long. If an edit does nothing, find the winning rule before touching anything else. In the browser dev tools, inspect the element and look at Computed styles. Test with `getComputedStyle()`, not by eye.
2. **`style.css` loads first and `stratos-refresh.css` loads second.** On equal specificity the later file wins. An `!important` rule in `style.css` still beats a non-important one in `stratos-refresh.css`.
3. **Windows line endings.** `style.css` uses CRLF. If you script edits in Python, open files with `newline=''`. Otherwise every line changes and the diff becomes unreadable.
4. **Heading weight rules are scattered.** Search both CSS files for `font-weight` next to `h1` to `h4` selectors before assuming a heading is covered. A single `h2 { }` edit will not reach most headings.
5. **Fonts need the right weight requested.** A weight not listed in the Google Fonts URL in `base.html` will not render properly.
6. **Several pages redirect.** `/about` and `/who-we-work-with` redirect to home anchors, and `/contact` redirects to `/appointments`. Articles return 404 unless `ARTICLES_PUBLIC` is set or a preview key is used.

---

## 5. Open items and things to decide

- **FAQ question size.** 24px looks large next to the small answer text. About 20px would be softer. It is a one-line change in `.faq-list summary` in `stratos-refresh.css`, and also in the desktop `summary` rule in `style.css`.
- **Body text base size.** The brand kit says 12px and the site has no single base size. This needs a decision, not a bug fix.
- **Caption style.** The brand kit defines no font for it, so there is nothing to apply.
- **Footer on phones.** The labels are 20px bold on phones. That predates the latest work and was not changed.
- **Unused or legacy files.** `images/icons/golden-visas_icon.svg` (about 243 KB) and `our-mission_icon.svg` are not referenced by any template. `templates/index.html` is a legacy template that no route uses. It still has h4s.
- **Cali's note (10 Nov).** Cali said something "looks off". Nobody has said what. The only defect I found was the footer labels (fixed). If Cali can name a page or send a screenshot, check that exact spot.
- **Other dashboards.** The admin and client dashboards (`/admin/`, `/client/`) need login. I did not view them rendered. Their heading weights were changed in CSS only.

---

## 6. Running it and committing

Run locally from the repo root:

```
python app.py
```

Then open `http://127.0.0.1:5000/`. Useful routes: `/`, `/services`, `/faqs`, `/appointments`, `/login`, `/privacy`, `/terms`, `/cookie-policy`, and the service pages under `/services/<name>/`.

To commit and push (you do this yourself):

```
git status
git add static/style.css static/stratos-refresh.css templates/base.html templates/home.html
git commit -m "Icons: drop white filter for new two-tone set. Headings: weight 400 per brand kit. Footer labels restored."
git push
```

Run `git status` first and look at what is staged before you commit.

---

## 7. How I checked the work

- A local Flask server plus Playwright (headless Chromium).
- Computed-style checks for font size, weight and family at 1440px, 900px and 390px wide.
- Full-page screenshots of home, services, a service detail page, FAQs, appointments, login and the legal pages.
- A check for broken images and horizontal overflow. None were found.
- Not covered: the Google Maps embed on `/appointments` (blocked in my test environment), the logged-in dashboards, and Google Fonts loading (also blocked there). Check those in a real browser.
