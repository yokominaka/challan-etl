from pathlib import Path
import sqlite3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
import os

sns.set_theme(style="whitegrid")

# Dynamically locate the database inside e_challan_etl/data/
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "echallan_db.sqlite"
FIGURES_DIR = BASE_DIR / "reports" / "figures"
os.makedirs(FIGURES_DIR, exist_ok=True)

print(f"Connecting to database at: {DB_PATH}")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM echallan_records", conn)
conn.close()

# Convert Date to datetime
df["Date"] = pd.to_datetime(df["Date"])

print(f"Loaded {len(df)} records from database.\n")

city_summary = (
    df.groupby("City")
    .agg(
        Total_Challans=("Challan_ID", "count"),
        Total_Fine_Assessed_PKR=("Fine_Amount_PKR", "sum"),
        Total_Revenue_Collected_PKR=("Amount_Collected_PKR", "sum"),
        Avg_Revenue_Per_Challan_PKR=("Amount_Collected_PKR", "mean"),
    )
    .reset_index()
)

city_summary["Recovery_Rate%"] = (
    city_summary["Total_Revenue_Collected_PKR"]
    / city_summary["Total_Fine_Assessed_PKR"]
) * 100

city_summary = city_summary.sort_values(
    by="Total_Revenue_Collected_PKR", ascending=False
)

print("=== City Revenue & Recovery Rates Summary ===")

print(city_summary.to_string(index=False))

fig, ax1 = plt.subplots(figsize=(10, 5))

color = "tab:blue"
ax1.set_xlabel("City", fontsize=12)
ax1.set_ylabel("Total Revenue Collected In PKR", color=color, fontsize=12)

bars = ax1.bar(
    city_summary["City"],
    city_summary["Total_Revenue_Collected_PKR"],
    color=color,
    alpha=0.7,
    width=0.4,
)
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()
color = "tab:red"

ax2.set_ylabel("Payment Recovery Rate %", color=color, fontsize=12)
line = ax2.plot(
    city_summary["City"],
    city_summary["Recovery_Rate%"],
    color=color,
    marker="o",
    linewidth=2.5,
)

ax2.tick_params(axis="y", labelcolor=color)
ax2.set_ylim(0, 100)

plt.title("City Wise Traffic & Recovery rate Performance", fontsize=14, pad=15)
plt.tight_layout()
# plt.show()
obj1_path=FIGURES_DIR / "obj1_city_revenue_recovery.png"
plt.savefig(obj1_path,dpi=300,bbox_inches ="tight")
print(f"Saved plot to: {obj1_path}")
plt.close()

enforcement_summary = (
    df.groupby("Enforcement_Method")
    .agg(
        Total_Challans=("Challan_ID", "count"),
        Total_Assessed_PKR=("Fine_Amount_PKR", "sum"),
        Total_Collected_PKR=("Amount_Collected_PKR", "sum"),
        Avg_Fine_PKR=("Fine_Amount_PKR", "mean"),
    )
    .reset_index()
)

enforcement_summary["Recovery_Rate_%"] = (
    enforcement_summary["Total_Collected_PKR"]
    / enforcement_summary["Total_Assessed_PKR"]
) * 100

print("\n===Enforcement Method Efficiency Summary===")
print(enforcement_summary.to_string(index=False))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

sns.barplot(
    data=enforcement_summary,
    x="Enforcement_Method",
    y="Total_Challans",
    ax=ax1,
    palette="Blues_d",
)
ax1.set_title("Total Challans Issued by Enforcement Method", fontsize=13)
ax1.set_xlabel("Enforcement Method", fontsize=12)
ax1.set_ylabel("Total Challans Issued", fontsize=12)

sns.barplot(
    data=enforcement_summary,
    x="Enforcement_Method",
    y="Recovery_Rate_%",
    ax=ax2,
    palette="Greens_d",
)
ax2.set_title("Payment Recovery Rate by Enforcement Method", fontsize=13)
ax2.set_xlabel("Enforcement Method")
ax2.set_ylabel("Recovery Rate (%)")
ax2.set_ylim(0, 100)

for p in ax2.patches:
    ax2.annotate(
        f"{p.get_height():.1f}%",
        (p.get_x() + p.get_width() / 2.0, p.get_height()),
        ha="center",
        va="center",
        xytext=(0, 8),
        textcoords="offset points",
    )
plt.suptitle("Enforcement Mechanism Performance Analysis", fontsize=15, y=0.95)
plt.tight_layout()
# plt.show()

obj2_path = FIGURES_DIR / "obj2_enforcement_efficiency.png"
plt.savefig(obj2_path, dpi=300, bbox_inches="tight")
print(f"🖼️ Saved plot to: {obj2_path}")
plt.close()

day_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

weekly_summary = (
    df.groupby("Day_of_Week")
    .agg(
        Total_Challans=("Challan_ID", "count"),
        Total_Revenue_Collected_PKR=("Amount_Collected_PKR", "sum"),
    )
    .reindex(day_order)
    .reset_index()
)

print("\n=== Weekly Operational Rhythm Summary ===")
print(weekly_summary.to_string(index=False))

categories=list(weekly_summary["Day_of_Week"])
values=list(weekly_summary["Total_Challans"])

angles = np.linspace(0, 2*np.pi,len(categories),endpoint=False).tolist()
values_closed=values + [values[0]]
angles_closed=angles + [angles[0]]

fix,ax = plt.subplots(figsize=(8,8), subplot_kw=dict(polar=True))

ax.plot(
    angles_closed,
    values_closed,
    color="#1b5e20",
    linewidth=2.5,
    linestyle="solid",
)
ax.fill(angles_closed, values_closed, color="#4caf50", alpha=0.25)
ax.set_xticks(angles)
ax.set_xticklabels(categories, fontsize=11,fontweight="bold")

plt.title(
    "Weekly Violation Intensity: Operational Rhythm",
    fontsize=15,
    pad=25,
    fontweight="bold",
)
plt.tight_layout()
# plt.show()

obj3_path = FIGURES_DIR / "obj3_weekly_operational_rhythm.png"
plt.savefig(obj3_path, dpi=300, bbox_inches="tight")
print(f"Saved plot to: {obj3_path}")
plt.close()

matrix = pd.crosstab(df["Vehicle_Type"],df["Violation_Type"], margins = False)

matrix_pct = (
    pd.crosstab(
        df["Vehicle_Type"],
        df["Violation_Type"],
        normalize="index",
    )
    * 100
)
plt.figure(figsize=(12,6))
sns.heatmap(
    matrix_pct,
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    cbar_kws={"label": "Percentage of Vehicle Total (%)"},
    linewidths=0.5,
)

plt.title(
    "Strategic Policy Matrix: Violation Distribution by Vehicle Type (%)",
    fontsize=14,
    pad=15,
    fontweight="bold",
)
plt.xlabel("Violation Type", fontsize=12)
plt.ylabel("Vehicle Type", fontsize=12)
plt.tight_layout()
# plt.show()

obj4_path = FIGURES_DIR / "obj4_strategic_policy_matrix.png"
plt.savefig(obj4_path, dpi=300, bbox_inches="tight")
print(f"🖼️ Saved plot to: {obj4_path}")
plt.close()

provincial_summary = (
    df.groupby(["Province", "Payment_Status"])
    .agg(
        Total_Challans=("Challan_ID", "count"),
        Total_Fine_Assessed_PKR=("Fine_Amount_PKR", "sum"),
        Total_Amount_Collected_PKR=("Amount_Collected_PKR", "sum"),
    )
    .reset_index())

print(provincial_summary.to_string(index=False))

provinicial_pivot= provincial_summary.pivot(index="Province",columns="Payment_Status",values="Total_Fine_Assessed_PKR").fillna(0)

plt.figure(figsize=(10,6))

provinicial_pivot.plot(kind="bar", stacked=True, color=["#1b5e20","#f57c00","#d32f2f"], figsize=(10,6))

plt.title(
    "Provincial Traffic Fine Assessment Segmented by Settlement Status",
    fontsize=14,
    pad=15,
    fontweight="bold",

)
plt.xlabel("Province", fontsize=12)
plt.ylabel("Total Fine Assessed (PKR)", fontsize=12)
plt.legend(title="Payment Status")
plt.xticks(rotation=0)
plt.tight_layout()
# plt.show()
obj5_path = FIGURES_DIR / "obj5_provincial_revenue_breakdown.png"
plt.savefig(obj5_path, dpi=300, bbox_inches="tight")
print(f"🖼️ Saved plot to: {obj5_path}")
plt.close()


fig,(ax1,ax2) = plt.subplots(1,2,figsize=(15,6))

sns.boxplot(data=df, x="Vehicle_Type", y="Fine_Amount_PKR",ax=ax1,palette="Set2")

ax1.set_title(
    "Fine Distribution by Vehicle Category", fontsize=13, fontweight="bold"
)
ax1.set_xlabel("Vehicle Type")
ax1.set_ylabel("Fine Amount (PKR)")
ax1.tick_params(axis="x",rotation=15)

yearly_trend = (df.groupby("Year")["Amount_Collected_PKR"].sum().reset_index())

sns.lineplot(data=yearly_trend,x="Year",y="Amount_Collected_PKR",marker="o",color="#2980b9",linewidth=2.5,ax=ax2)

ax2.set_title(
    "Year-over-Year Total Revenue Collection (2018–2026)",
    fontsize=13,
    fontweight="bold",
)
ax2.set_xlabel("Year")
ax2.set_ylabel("Total Revenue Collected (PKR)")

plt.tight_layout()
# plt.show()

obj6_7_path = FIGURES_DIR / "obj6_7_fine_dist_yearly_trends.png"
plt.savefig(obj6_7_path, dpi=300, bbox_inches="tight")
print(f"Saved plot to: {obj6_7_path}")
plt.close()