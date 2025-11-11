#!/usr/bin/env python3
# Generates a publication-ready horizontal timeline with staggered callouts
# No external deps beyond matplotlib.

import textwrap
import matplotlib.pyplot as plt

# ---- EDIT THESE EVENTS ONLY ----
# time is hours from fast start; label lines are short, we'll wrap them
events = [
    dict(t=0,   title="Fast start",                note="Day 0 • 1:30 PM"),
    dict(t=24,  title="Day 1",                     note="Hyperglycemia persists; ketones low"),
    dict(t=48,  title="Day 2",                     note="Marked sympathetic tone; still no ketosis"),
    dict(t=60,  title="Seroquel given",            note="Evening; sedation lowers sympathetic output"),
    dict(t=66,  title="Ketosis shift",             note="β-HB begins rising after quetiapine"),
    dict(t=72,  title="Fast end",                  note="~72 h total"),
    dict(t=73,  title="Refeed (½ cup granola)",    note="Acute migraine onset"),
    dict(t=75,  title="Post-fast abdominal pain",  note="Persistent through the day"),
]

# Horizontal axis range (pad so text never clips)
xmin, xmax = -4, 80

# Stagger labels above/below to prevent overlaps
# pattern alternates y= +1.0 / -1.0 / +1.0 / ...
ys = []
toggle = 1
for _ in events:
    ys.append(1.0 if toggle == 1 else -1.0)
    toggle *= -1

# ---- PLOTTING ----
plt.figure(figsize=(12, 5))  # wider canvas helps readability
ax = plt.gca()
ax.set_xlim(xmin, xmax)
ax.set_ylim(-2, 2)

# Draw baseline timeline
ax.hlines(0, xmin, xmax, linewidth=2)

# Common text formatter (no color choices to comply with your request)
def wrap(s, width=28):
    return "\n".join(textwrap.wrap(s, width=width, break_long_words=False))

# Plot each event with a dot and an arrow to a callout box
for (ev, y) in zip(events, ys):
    x = ev["t"]

    # event marker on the baseline
    ax.plot([x], [0], marker="o", markersize=6)

    # vertical stem
    ax.vlines(x, 0, y*0.65, linewidth=1)

    # callout position (a bit away from the stem)
    xtext = x
    ytext = y*0.95

    # build label text
    title = ev["title"]
    note  = ev.get("note", "")
    label = title if not note else f"{title}\n{note}"
    label = wrap(label, width=28)

    # arrowprops without explicit color
    arrowprops = dict(arrowstyle="-", lw=0.8, shrinkA=0, shrinkB=0)

    # annotation with a light bounding box (no color specified)
    ax.annotate(
        label,
        xy=(x, y*0.65),
        xytext=(xtext, ytext),
        ha="center",
        va="center",
        arrowprops=arrowprops,
        bbox=dict(boxstyle="round,pad=0.35", fc="white", ec="black", lw=0.8),
    )

# Axis cosmetics
ax.set_yticks([])
ax.set_xlabel("Hours from fast start")
ax.set_title("72-Hour Fast Timeline with Seroquel-Linked Ketosis Shift")

plt.tight_layout()
plt.savefig("figures/timeline_fast_case.png", dpi=300)
plt.savefig("figures/timeline_fast_case.svg")  # vector for manuscripts
print("Wrote figures/timeline_fast_case.png and .svg")
