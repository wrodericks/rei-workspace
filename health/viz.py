#!/usr/bin/env python3
"""Health dashboard visualization for Warren's tracking data."""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Data ──────────────────────────────────────────────────────────────────────
dates = ['Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 17', 'Apr 18', 'Apr 19', 'Apr 20*']
calories = [2029, 2555, 1810, 1710, 1832, 1855, 1838, 1262]
protein =  [151,  149,  145,  135,  161,  102,  146,  103]
carbs =    [182,  116,  149,  110,  156,  185,  157,  100]
fat =      [79,   137,  78,   62,   60,   73,   79,   51]
fibre =    [31,   10,   20,   17,   19,   9,    16,   10]
sugar =    [42,   39,   46,   26,   50,   78,   47,   16]

# Targets
cal_target = 1900
protein_target = 150
carbs_target = 150
fat_target = 80
fibre_target = 25
sugar_target = 40

# Weight (only days 1–4 available)
weight_dates = ['Apr 13', 'Apr 14', 'Apr 15', 'Apr 16', 'Apr 20']
weight_kg = [120.0, 119.2, 118.6, 118.4, 118.1]
weight_lbs = [264.6, 262.8, 261.4, 261.2, 260.6]

x = np.arange(len(dates))
x_weight = np.arange(len(weight_dates))

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#444',
    'axes.labelcolor': '#ccc',
    'xtick.color': '#aaa',
    'ytick.color': '#aaa',
    'text.color': '#eee',
    'grid.color': '#333',
    'grid.alpha': 0.5,
    'font.family': 'sans-serif',
    'font.size': 10,
})

fig = plt.figure(figsize=(16, 18))
fig.suptitle("Warren's Health Dashboard — Apr 13–20, 2026", 
             fontsize=16, fontweight='bold', color='#e0e0e0', y=0.98)

# Subtitle
fig.text(0.5, 0.965, '★ Apr 20 is in progress (evening meal not yet logged)',
         ha='center', fontsize=9, color='#888', style='italic')

gs = fig.add_gridspec(4, 2, hspace=0.45, wspace=0.35,
                       left=0.08, right=0.95, top=0.95, bottom=0.04)

# ── 1. Calories ───────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, :])
colors = ['#e74c3c' if c > cal_target else '#2ecc71' for c in calories]
bars = ax1.bar(x, calories, color=colors, alpha=0.85, width=0.6, zorder=3)
ax1.axhline(cal_target, color='#f39c12', linewidth=1.5, linestyle='--', label=f'Target ({cal_target})', zorder=4)
ax1.set_title('Daily Calories', fontweight='bold', color='#e0e0e0', pad=8)
ax1.set_xticks(x)
ax1.set_xticklabels(dates)
ax1.set_ylabel('kcal')
ax1.set_ylim(0, 3000)
ax1.grid(axis='y', zorder=0)
ax1.legend(loc='upper right', framealpha=0.2)
for bar, val in zip(bars, calories):
    suffix = '*' if dates[bars.patches.index(bar)] == 'Apr 19*' else ''
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 40,
             f'{val:,}{suffix}', ha='center', va='bottom', fontsize=9, color='#ccc')

# ── 2. Protein ────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[1, 0])
colors_p = ['#e74c3c' if p < protein_target else '#2ecc71' for p in protein]
bars2 = ax2.bar(x, protein, color=colors_p, alpha=0.85, width=0.6, zorder=3)
ax2.axhline(protein_target, color='#f39c12', linewidth=1.5, linestyle='--', label=f'Target ({protein_target}g)', zorder=4)
ax2.set_title('Protein (g)', fontweight='bold', color='#e0e0e0', pad=8)
ax2.set_xticks(x)
ax2.set_xticklabels(dates, fontsize=8)
ax2.set_ylabel('grams')
ax2.set_ylim(0, 200)
ax2.grid(axis='y', zorder=0)
ax2.legend(loc='upper right', framealpha=0.2)
for bar, val in zip(bars2, protein):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
             f'{val}g', ha='center', va='bottom', fontsize=8, color='#ccc')

# ── 3. Sugar ─────────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[1, 1])
colors_s = ['#e74c3c' if s > sugar_target else '#2ecc71' for s in sugar]
bars3 = ax3.bar(x, sugar, color=colors_s, alpha=0.85, width=0.6, zorder=3)
ax3.axhline(sugar_target, color='#f39c12', linewidth=1.5, linestyle='--', label=f'Target (<{sugar_target}g)', zorder=4)
ax3.set_title('Sugar (g)', fontweight='bold', color='#e0e0e0', pad=8)
ax3.set_xticks(x)
ax3.set_xticklabels(dates, fontsize=8)
ax3.set_ylabel('grams')
ax3.set_ylim(0, 100)
ax3.grid(axis='y', zorder=0)
ax3.legend(loc='upper right', framealpha=0.2)
for bar, val in zip(bars3, sugar):
    ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
             f'{val}g', ha='center', va='bottom', fontsize=8, color='#ccc')

# ── 4. Carbs & Fat stacked ───────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[2, 0])
ax4.bar(x, carbs, color='#9b59b6', alpha=0.85, width=0.6, label='Carbs', zorder=3)
ax4.axhline(carbs_target, color='#9b59b6', linewidth=1.5, linestyle='--', alpha=0.6, label=f'Carbs target ({carbs_target}g)', zorder=4)
ax4.set_title('Carbohydrates (g)', fontweight='bold', color='#e0e0e0', pad=8)
ax4.set_xticks(x)
ax4.set_xticklabels(dates, fontsize=8)
ax4.set_ylabel('grams')
ax4.set_ylim(0, 250)
ax4.grid(axis='y', zorder=0)
ax4.legend(loc='upper right', framealpha=0.2, fontsize=8)
for i, val in enumerate(carbs):
    ax4.text(i, val + 3, f'{val}g', ha='center', va='bottom', fontsize=8, color='#ccc')

ax5 = fig.add_subplot(gs[2, 1])
colors_f = ['#e74c3c' if f > fat_target else '#3498db' for f in fat]
ax5.bar(x, fat, color=colors_f, alpha=0.85, width=0.6, zorder=3)
ax5.axhline(fat_target, color='#f39c12', linewidth=1.5, linestyle='--', label=f'Target (<{fat_target}g)', zorder=4)
ax5.set_title('Fat (g)', fontweight='bold', color='#e0e0e0', pad=8)
ax5.set_xticks(x)
ax5.set_xticklabels(dates, fontsize=8)
ax5.set_ylabel('grams')
ax5.set_ylim(0, 180)
ax5.grid(axis='y', zorder=0)
ax5.legend(loc='upper right', framealpha=0.2)
for i, val in enumerate(fat):
    ax5.text(i, val + 2, f'{val}g', ha='center', va='bottom', fontsize=8, color='#ccc')

# ── 5. Fibre ─────────────────────────────────────────────────────────────────
ax6 = fig.add_subplot(gs[3, 0])
colors_fi = ['#e74c3c' if f < fibre_target else '#2ecc71' for f in fibre]
ax6.bar(x, fibre, color=colors_fi, alpha=0.85, width=0.6, zorder=3)
ax6.axhline(fibre_target, color='#f39c12', linewidth=1.5, linestyle='--', label=f'Target ({fibre_target}g+)', zorder=4)
ax6.set_title('Fibre (g)', fontweight='bold', color='#e0e0e0', pad=8)
ax6.set_xticks(x)
ax6.set_xticklabels(dates, fontsize=8)
ax6.set_ylabel('grams')
ax6.set_ylim(0, 45)
ax6.grid(axis='y', zorder=0)
ax6.legend(loc='upper right', framealpha=0.2)
for i, val in enumerate(fibre):
    ax6.text(i, val + 0.5, f'{val}g', ha='center', va='bottom', fontsize=8, color='#ccc')

# ── 6. Weight trend ──────────────────────────────────────────────────────────
ax7 = fig.add_subplot(gs[3, 1])
ax7.plot(x_weight, weight_kg, color='#1abc9c', linewidth=2.5, marker='o',
         markersize=8, markerfacecolor='#16a085', zorder=3)
ax7.fill_between(x_weight, weight_kg, min(weight_kg) - 0.5, alpha=0.15, color='#1abc9c')
ax7.set_title('Weight (kg)', fontweight='bold', color='#e0e0e0', pad=8)
ax7.set_xticks(x_weight)
ax7.set_xticklabels(weight_dates, fontsize=8)
ax7.set_ylabel('kg')
ax7.set_ylim(117, 121.5)
ax7.grid(axis='y', zorder=0)
for i, (kg, lbs) in enumerate(zip(weight_kg, weight_lbs)):
    ax7.annotate(f'{kg} kg\n({lbs} lbs)', (i, kg),
                textcoords='offset points', xytext=(0, 10),
                ha='center', fontsize=8, color='#ccc')
# Goal line
ax7.axhline(81, color='#e74c3c', linewidth=1, linestyle=':', alpha=0.5, label='Goal (81 kg)')
ax7.legend(loc='lower right', framealpha=0.2, fontsize=8)

# ── Legend ────────────────────────────────────────────────────────────────────
green = mpatches.Patch(color='#2ecc71', alpha=0.85, label='On target')
red = mpatches.Patch(color='#e74c3c', alpha=0.85, label='Off target')
fig.legend(handles=[green, red], loc='lower center', ncol=2,
           framealpha=0.2, fontsize=9, bbox_to_anchor=(0.5, 0.01))

out = '/home/warren/.openclaw/workspace/health/dashboard.png'
plt.savefig(out, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
print(f'Saved: {out}')
