"""Figure 1, research model. Publication-quality vector output for the journal version.

Outputs (figures/): fig1_research_model.pdf   vector, for the LaTeX submission
                    fig1_research_model.png   600 dpi, for the Word version
                    fig1_research_model.svg   editable source if a copy editor needs it
Design rules: single accent color, grayscale-safe (verdicts carry words, not color alone),
serif type to match the manuscript, hairline rules, no decorative fills.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIXGeneral", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "pdf.fonttype": 42, "ps.fonttype": 42,   # embed real fonts, not outlines
    "svg.fonttype": "none",
})

INK   = "#000000"
GREY  = "#5b6670"
RULE  = "#9aa4ae"
ACC   = "#1f4e79"
FILL  = "#ffffff"
SOFT  = "#f4f6f8"

W, H = 7.48, 5.6             # inches: 190 mm double-column width
fig = plt.figure(figsize=(W, H), dpi=600)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(-11, 73); ax.axis("off")

def box(x, y, w, h, title, sub=None, fs=8.6, sfs=7.2, ec=INK, lw=0.9, fc=FILL, bold=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.32,rounding_size=0.7",
                                fc=fc, ec=ec, lw=lw, zorder=3))
    ax.text(x + w/2, y + h/2 + (1.55 if sub else 0), title, ha="center", va="center",
            fontsize=fs, fontweight="bold" if bold else "normal", color=INK, zorder=4)
    if sub:
        ax.text(x + w/2, y + h/2 - 1.85, sub, ha="center", va="center",
                fontsize=sfs, color=GREY, zorder=4, linespacing=1.35)

def arrow(pts, lw=0.9, color=INK, ls="-", head=True):
    for i in range(len(pts) - 1):
        st = "-|>" if (head and i == len(pts) - 2) else "-"
        ax.add_patch(FancyArrowPatch(pts[i], pts[i+1], arrowstyle=st, mutation_scale=8,
                                     lw=lw, color=color, linestyle=ls, zorder=2,
                                     shrinkA=0, shrinkB=0, joinstyle="miter"))

def hlabel(x, y, text):
    ax.text(x, y, text, ha="center", va="center", fontsize=8.4, fontweight="bold",
            color=ACC, zorder=5,
            bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"))

def verdict(x, y, word, detail):
    ax.text(x, y + 1.6, word, ha="left", va="center", fontsize=7.8, color=INK,
            fontweight="bold", zorder=4)
    ax.text(x, y - 1.5, detail, ha="left", va="center", fontsize=7.2, color=GREY, zorder=4)

# ----------------------------------------------------------------- panel (a)
ax.text(1.5, 71.0, "(a)", fontsize=9.0, fontweight="bold", color=INK)
ax.text(6.0, 71.0, "Hypothesised effects of generative-AI exposure", fontsize=9.0, color=INK)

box(1.5, 44.0, 21, 9.4, "Treated × Post", "GenAI-exposed CPC class,\nfilings from January 2023")

box(35, 59.6, 27, 8.4, "Science-to-technology lag", "log(1 + days), pair level")
box(35, 43.8, 27, 9.6, "Fresh-science share", "citations to papers three years\nold or younger, patent level")
box(35, 29.4, 27, 8.4, "Cross-firm similarity", "cosine of abstract vectors")

arrow([(22.5, 50.6), (35, 63.8)]); hlabel(28.2, 58.2, "H1")
arrow([(22.5, 48.6), (35, 48.6)]); hlabel(28.7, 50.0, "H2")
arrow([(12.0, 44.0), (12.0, 33.6), (35, 33.6)]); hlabel(24.6, 35.1, "H4")

verdict(64.5, 63.8, "NOT SUPPORTED", "+0.214 log points; median patent unchanged")
verdict(64.5, 48.6, "SUPPORTED", "−5.56 pp; displaced mass at four to eight years")
verdict(64.5, 33.6, "NOT SUPPORTED", "+0.0006, not significant")

ax.add_line(plt.Line2D([1.5, 98.5], [25.0, 25.0], color=RULE, lw=0.7, zorder=1))

# ----------------------------------------------------------------- panel (b)
ax.text(1.5, 22.4, "(b)", fontsize=9.0, fontweight="bold", color=INK)
ax.text(6.0, 22.4, "Where the composition shift lives: H3, instrument versus subject matter",
        fontsize=9.0, color=INK)

box(37, 12.6, 26, 6.6, "Fresh-science share", "the H2 estimate, −5.56 pp", fs=8.2, sfs=7.1, fc=SOFT)
xs = [(2.0, "Dose gradient", "HIGH vs LOW inside G06N\nmoderator, §6.2"),
      (37.0, "Generative CPC codes", "excluded and re-estimated\nsample decomposition, §6.8"),
      (72.0, "Firm adoption", "exposure × post, firm FE\nmoderator, §6.9")]
for x, ttl, sub in xs:
    box(x, 1.6, 26, 7.2, ttl, sub, fs=8.2, sfs=7.0)
for xc in (15.0, 50.0, 85.0):
    arrow([(50, 12.6), (50, 10.9), (xc, 10.9), (xc, 8.8)], lw=0.8)

ax.text(50, -2.6, "Instrument channel NOT SUPPORTED:  −2.73 pp and not significant once generative-coded patents are excluded;  "
                  "adopting firms retain fresh science better (+4.54 pp), the opposite sign.",
        ha="center", va="center", fontsize=7.3, color=INK, zorder=4)

ax.text(1.5, -7.6,
        "All specifications include CPC class and filing-year fixed effects; assignee and cited-publication-year fixed effects are added where indicated. "
        "Standard errors are clustered by class × filing year.\nThe design contains moderation and no mediation: no indirect effect is estimated or claimed.",
        ha="left", va="center", fontsize=7.0, color=GREY, linespacing=1.5)

for ext in ("pdf", "png", "svg"):
    fig.savefig(f"figures/fig1_research_model.{ext}", dpi=600,
                bbox_inches="tight", pad_inches=0.06, facecolor="white")
print("saved pdf / png / svg")
