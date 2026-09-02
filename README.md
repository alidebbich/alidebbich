<div align="center">

<h3><code>alidebbich@github ~ $ ./contributions.sh</code></h3>
<img src="./contrib-heatmap.svg" width="860" alt="Contribution heatmap" />

<br><br>

<h3><code>alidebbich@github ~ $ whoami</code></h3>
<table>
  <tr>
    <td valign="top"><img src="./avi-ascii.svg" width="370" alt="ASCII portrait" /></td>
    <td valign="top"><img src="./info-card.svg" width="490" alt="Info card" /></td>
  </tr>
</table>

<br>

---

## 🎨 How This Works

This profile README is built entirely with **self-contained SVG animations** — no external JavaScript, no third-party services, no GitHub token needed.

### Three Animated Components

1. **Contribution Heatmap** (`contrib-heatmap.svg`)
   - Scrapes your real GitHub contribution data (public HTML only)
   - Renders as a 53-week × 7-day grid with GitHub's official green palette
   - Reveals diagonally with staggered fade-in animation
   - Refreshes daily via GitHub Actions (6:17 UTC)

2. **ASCII Portrait** (`avi-ascii.svg`)
   - Convert any photo → grayscale → ASCII using density ramps
   - Self-types row-by-row with clip-path wipe animations
   - Zero static, one monochrome color (light gray)
   - High contrast makes the subject pop against white backgrounds

3. **Info Card** (`info-card.svg`)
   - Neofetch-style panel showing Now, Prev, Stack, Highlights
   - Lines fade and slide in on a stagger
   - Customize the content directly in `scripts/make_info_card.py`

### Why SVG?

- **GitHub strips `<script>` and most inline CSS** from README.md
- **SVG `<img>` tags render with full SMIL/CSS animation support**
- **No rate limits, no dependencies**, just committed SVG files
- **Loads instantly** — the art is already in your repo

---

## 🚀 Set Up Your Own

### 1. Create the profile repo

```bash
# Your username must match this pattern exactly
gh repo create alidebbich --public --clone
cd alidebbich
mkdir -p scripts data .github/workflows
```

### 2. Install Python dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # or: .venv\Scripts\activate on Windows
pip install -r scripts/requirements.txt
```

**requirements.txt:**
```
requests==2.32.3
beautifulsoup4==4.12.3
pillow==10.0.0
numpy==1.24.3
opencv-python==4.8.0.74
rembg==2.0.50
```

### 3. Generate the ASCII portrait (one-time)

```bash
# Prep your photo: remove background, boost contrast
python scripts/prep_photo.py your-photo.jpg

# Convert to self-typing SVG
python scripts/make_ascii_svg.py source-prepped.png
```

This creates `avi-ascii.svg` — a monochrome ASCII portrait that types itself in.

### 4. Generate the info card

Edit `scripts/make_info_card.py` to customize your role, stack, and highlights. Then:

```bash
python scripts/make_info_card.py
```

Creates `info-card.svg` — a neofetch-style panel with fade-in animations.

### 5. Fetch and render your contributions

```bash
python scripts/fetch_contributions.py alidebbich
python scripts/render_heatmap_svg.py
```

Creates `data/contributions.json` and `contrib-heatmap.svg` — your real contribution graph animated.

### 6. Compose the README

Copy the layout from this README into your own `README.md`:
- Replace `alidebbich` with your username
- Adjust SVG widths if needed (keep the sum of columns equal to the heatmap width for alignment)

### 7. Set up daily automation (GitHub Actions)

Create `.github/workflows/update-profile-art.yml`:

```yaml
name: Update profile art

on:
  schedule:
    - cron: "17 6 * * *"   # ~06:17 UTC daily
  workflow_dispatch: {}
  push:
    branches: [main]

permissions:
  contents: write

jobs:
  heatmap:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      
      - run: pip install -r scripts/requirements.txt
      
      - run: python scripts/fetch_contributions.py alidebbich
      
      - run: python scripts/render_heatmap_svg.py
      
      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: "chore: refresh contribution graph [skip ci]"
          file_pattern: "data/contributions.json contrib-heatmap.svg"
```

Trigger it once from the **Actions** tab → **workflow_dispatch** to verify the first run.

---

## 🛠️ Customization

### Change the info card content

Edit the `card_data` list in `scripts/make_info_card.py`:

```python
card_data = [
    ("Now", "Your current role"),
    ("Prev", "Where you were"),
    ("Stack", "Your tech stack"),
    ("Highlights", "Your achievement"),
]
```

Then run `python scripts/make_info_card.py` again.

### Use a different photo

```bash
python scripts/prep_photo.py new-photo.jpg
python scripts/make_ascii_svg.py source-prepped.png
```

### Adjust ASCII width and CLAHE

In `scripts/make_ascii_svg.py`:
```python
ascii_art = img_to_ascii(input_file, width=120)  # Default: 100
```

In `scripts/prep_photo.py`:
```python
clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))  # Tweak these
```

Higher `clipLimit` = more aggressive contrast boost.

---

## 📊 FAQ

**Q: Do I need a GitHub token?**  
A: No. The heatmap scrapes the public HTML at `github.com/users/<username>/contributions`, which needs no auth.

**Q: Will the animations play on GitHub?**  
A: Yes. GitHub renders `<img>` tags with SVG animation support. It's SMIL (Synchronized Multimedia Integration Language), not JavaScript.

**Q: Why does my ASCII portrait look washed out?**  
A: The photo prep uses rembg (background removal) and CLAHE (contrast boost). If it's still flat:
- Try a higher `clipLimit` in `prep_photo.py`
- Use a photo with strong lighting/shadows
- Check that rembg detected your subject correctly

**Q: Can I loop the animations?**  
A: The current setup plays once and freezes (`fill="freeze"`). To loop, change it to `fill="remove"` in the SVG scripts, but once is more polished for a profile.

**Q: What if the workflow fails?**  
A: Check the **Actions** tab for error logs. Common issues:
- rembg download timing out (it's large) — retry manually
- Network timeout fetching GitHub HTML — check your internet
- Permission issues with auto-commit — verify `contents: write` is set

---

## 📁 Project Structure

```
alidebbich/
├── .github/workflows/
│   └── update-profile-art.yml       # Daily heatmap refresh
├── scripts/
│   ├── requirements.txt
│   ├── prep_photo.py                # Remove bg, boost contrast
│   ├── make_ascii_svg.py            # Photo → typewriter ASCII
│   ├── make_info_card.py            # Generate neofetch card
│   ├── fetch_contributions.py       # Scrape GitHub contributions
│   └── render_heatmap_svg.py        # Render contribution grid
├── data/
│   └── contributions.json           # Updated daily
├── avi-ascii.svg                    # Portrait (static, update manually)
├── info-card.svg                    # Info panel (static, update manually)
├── contrib-heatmap.svg              # Heatmap (auto-updated daily)
└── README.md                        # This file
```

---

## 🎯 Why This Approach?

- **No broken images**: Art is committed to the repo, never expires
- **No rate limits**: All scripts run locally or against public GitHub pages
- **Full control**: Customize every color, font, animation timing
- **Learning value**: Great example of SMIL animations, SVG generation, GitHub Actions, and web scraping without auth

---

Built with ❤️ using Python, SVG, and GitHub Actions.
Inspired by [avivashishta.com](https://avivashishta.com/posts/animated-profile-readme)

</div>
