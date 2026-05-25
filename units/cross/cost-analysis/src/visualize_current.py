import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now_jst = datetime.now(JST).strftime("%Y-%m-%d %H:%M")

# === 現在の全品目（その他雑費なし、生茶葉削除、アイス削除、トリュフ削除） ===

items = [
    # CSV list
    ("清美タンゴール 10kg", "ドリンク", 3480),
    ("本マグロ中落ち 5kg", "前菜", 2354),
    ("比内地鶏ガラ 2.7kg", "Ramen I", 1944),
    ("豚バラブロック 1kg", "Ramen II", 1706),
    ("ニップン冷凍パイシート", "デザート", 1485),
    ("比内地鶏 鶏皮 1kg", "Ramen I", 1404),
    ("愛媛 完熟レモン 1kg", "ドリンク", 1296),
    ("生茶葉 50g", "グラニテ", 594),
    ("豚背ガラ 4kg", "Ramen II", 1056),
    ("有明海苔 20枚", "Ramen II", 944),
    ("冷凍ラズベリー 170g", "デザート", 900),
    ("真妻わさび 200g", "前菜", 880),
    ("春よ恋 2.5kg", "製麺", 648),
    ("スパークリンググレープ", "ドリンク", 626),
    ("比内地鶏ミンチ", "Ramen I", 594),
    ("紅ほっぺ 500g", "デザート", 578),
    ("スナップドラゴン 50g", "デザート", 442),
    ("鶏卵 10個", "共通", 307),
    # 別途購入
    ("米澤豚モモ 1.2kg", "Ramen I", 1477),
    ("豚バラ追加 500g", "Ramen II", 850),
    ("鶏卵追加 8個", "共通", 200),
    ("穂先メンマ水煮 360g", "Ramen II", 300),
    ("コカ・コーラ 2L", "ドリンク", 200),
    ("炭酸水 2L", "ドリンク", 150),
    ("天然水 2L", "ドリンク", 100),
    ("長ネギ", "共通", 650),
    ("どんぶり容器", "共通", 686),
    ("生クリーム", "デザート", 388),
    ("牛乳 750ml", "デザート", 200),
]

# カテゴリ集計
cat_map = {}
for name, cat, price in items:
    cat_map.setdefault(cat, []).append((name, price))

cat_totals = {cat: sum(v for _, v in items_list) for cat, items_list in cat_map.items()}

total = sum(price for _, _, price in items)
per_person_12 = total / 12
per_person_10 = total / 10

# コース順
course_order = ["前菜", "Ramen I", "グラニテ", "Ramen II", "デザート", "ドリンク", "製麺", "共通"]
course_colors = {
    "前菜": "#e74c3c",
    "Ramen I": "#ff6b6b",
    "グラニテ": "#1abc9c",
    "Ramen II": "#f38181",
    "デザート": "#f39c12",
    "ドリンク": "#3498db",
    "製麺": "#2ecc71",
    "共通": "#95a5a6",
}

# === チャート ===
fig = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "bar", "colspan": 2}, None],
        [{"type": "pie"}, {"type": "bar"}],
    ],
    subplot_titles=(
        "全品目 金額ランキング",
        "カテゴリ別 割合",
        "カテゴリ別 金額（10人割り）",
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.1,
)

# 1. 全品目 横棒（金額順）
items_sorted = sorted(items, key=lambda x: x[2])
fig.add_trace(
    go.Bar(
        y=[i[0] for i in items_sorted],
        x=[i[2] for i in items_sorted],
        orientation="h",
        marker_color=[course_colors.get(i[1], "#95a5a6") for i in items_sorted],
        text=[f"¥{i[2]:,}" for i in items_sorted],
        textposition="outside",
        hovertemplate="%{y}<br>¥%{x:,}<extra></extra>",
    ),
    row=1, col=1,
)

# 2. 円グラフ
pie_labels = [c for c in course_order if cat_totals.get(c, 0) > 0]
pie_values = [cat_totals[c] for c in pie_labels]
pie_colors = [course_colors[c] for c in pie_labels]

fig.add_trace(
    go.Pie(
        labels=pie_labels,
        values=pie_values,
        marker=dict(colors=pie_colors),
        textinfo="label+value+percent",
        texttemplate="%{label}<br>¥%{value:,}<br>(%{percent})",
        hole=0.3,
    ),
    row=2, col=1,
)

# 3. カテゴリ別棒グラフ（10人割り表示）
bar_labels = [c for c in course_order if cat_totals.get(c, 0) > 0]
bar_values = [cat_totals[c] for c in bar_labels]
bar_colors = [course_colors[c] for c in bar_labels]

fig.add_trace(
    go.Bar(
        x=bar_labels,
        y=bar_values,
        marker_color=bar_colors,
        text=[f"¥{v:,}<br>(¥{v//10:,}/人)" for v in bar_values],
        textposition="outside",
    ),
    row=2, col=2,
)

fig.update_layout(
    title=dict(
        text=(
            f"ラーメン料理会 材料費内訳（{now_jst} JST）<br>"
            f"<sub>総合計: ¥{total:,}　｜　"
            f"12人提供 / 10人負担: ¥{per_person_10:,.0f}/人　｜　"
            f"</sub>"
        ),
        font=dict(size=18),
    ),
    height=1100,
    width=1200,
    showlegend=False,
    font=dict(size=11),
)

fig.update_xaxes(row=1, col=1, title_text="金額（円）")
fig.update_yaxes(row=2, col=2, title_text="金額（円）")

fig.write_html("/Users/ytonoyam/Dev/ryourikai/cost_current.html")
print(f"総合計: ¥{total:,}")
print(f"12人提供 / 10人負担: ¥{per_person_10:,.0f}/人")
print()
for c in course_order:
    if cat_totals.get(c, 0) > 0:
        print(f"  {c:12s}  ¥{cat_totals[c]:>6,}  (¥{cat_totals[c]//10:,}/人)")
print(f"  {'合計':12s}  ¥{total:>6,}  (¥{total//10:,}/人)")
