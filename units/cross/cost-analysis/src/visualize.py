import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px

# === データ ===

# カテゴリ別材料費
categories = {
    "肉類": [
        ("本マグロ中落ち", 2354),
        ("比内地鶏ガラ", 1944),
        ("豚バラブロック", 1706),
        ("比内地鶏 鶏皮", 1404),
        ("豚背ガラ", 1056),
        ("比内地鶏ミンチ", 594),
        ("実山椒(50g)", 458),
        ("豚バラ追加500g", 850),
        ("鶏卵", 507),
    ],
    "デザート": [
        ("生クリーム45%", 583),
        ("冷凍パイシート", 1485),
        ("粉飴", 1256),
        ("冷凍ラズベリー", 900),
        ("紅ほっぺ", 578),
        ("スナップドラゴン", 442),
    ],
    "ドリンク": [
        ("清美タンゴール10kg", 3480),
        ("広島レモン(2個)", 523),
        ("スパークリンググレープ", 626),
    ],
    "製麺・調味料": [
        ("春よ恋", 648),
        ("生茶葉", 1188),
        ("有明海苔", 944),
    ],
    "その他・雑費": [
        ("調味料・牛乳等", 3500),
    ],
}

# カテゴリ別合計
cat_labels = []
cat_values = []
for cat, items in categories.items():
    total = sum(v for _, v in items)
    cat_labels.append(cat)
    cat_values.append(total)

# 全品目フラット
all_items = []
all_values = []
all_cats = []
for cat, items in categories.items():
    for name, val in items:
        all_items.append(name)
        all_values.append(val)
        all_cats.append(cat)

# === チャート作成 ===
fig = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "pie"}, {"type": "bar"}],
        [{"type": "bar", "colspan": 2}, None],
    ],
    subplot_titles=(
        "カテゴリ別 内訳",
        "カテゴリ別 金額",
        "全品目 金額ランキング",
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.1,
)

# 1. 円グラフ（カテゴリ別）
colors = ["#e74c3c", "#f39c12", "#3498db", "#2ecc71", "#95a5a6"]
fig.add_trace(
    go.Pie(
        labels=cat_labels,
        values=cat_values,
        marker=dict(colors=colors),
        textinfo="label+percent+value",
        texttemplate="%{label}<br>¥%{value:,}<br>(%{percent})",
        hole=0.3,
    ),
    row=1, col=1,
)

# 2. 棒グラフ（カテゴリ別）
fig.add_trace(
    go.Bar(
        x=cat_labels,
        y=cat_values,
        marker_color=colors,
        text=[f"¥{v:,}" for v in cat_values],
        textposition="outside",
    ),
    row=1, col=2,
)

# 3. 全品目ランキング（横棒）
sorted_idx = sorted(range(len(all_values)), key=lambda i: all_values[i])
sorted_items = [all_items[i] for i in sorted_idx]
sorted_values = [all_values[i] for i in sorted_idx]
sorted_cats = [all_cats[i] for i in sorted_idx]

color_map = {cat: colors[i] for i, cat in enumerate(categories.keys())}
bar_colors = [color_map[c] for c in sorted_cats]

fig.add_trace(
    go.Bar(
        y=sorted_items,
        x=sorted_values,
        orientation="h",
        marker_color=bar_colors,
        text=[f"¥{v:,}" for v in sorted_values],
        textposition="outside",
    ),
    row=2, col=1,
)

# レイアウト
total = sum(all_values)
per_person = total / 12

fig.update_layout(
    title=dict(
        text=f"ラーメン料理会 材料費 総合計: ¥{total:,}（1人あたり ¥{per_person:,.0f}）",
        font=dict(size=20),
    ),
    showlegend=False,
    height=1000,
    width=1100,
    font=dict(size=12),
)

fig.update_yaxes(row=1, col=2, title_text="金額（円）")
fig.update_xaxes(row=2, col=1, title_text="金額（円）")

fig.write_html("/Users/ytonoyam/Dev/ryourikai/units/cross/cost-analysis/dist/cost_breakdown.html")
print(f"総合計: ¥{total:,}")
print(f"1人あたり: ¥{per_person:,.0f}")
print("Saved: cost_breakdown.html")
