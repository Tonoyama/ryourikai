import plotly.graph_objects as go
from plotly.subplots import make_subplots

# === 全品目: 購入価格 vs 実質コスト ===

items = [
    # (品目, カテゴリ, 購入価格, 実質コスト, 備考)
    # 肉類
    ("本マグロ中落ち", "肉類", 2354, 2354, "全量使用"),
    ("比内地鶏ガラ", "肉類", 1944, 1944, "全量使用"),
    ("豚バラブロック", "肉類", 1706, 1706, "全量使用（+500g追加必要）"),
    ("比内地鶏 鶏皮", "肉類", 1404, 546, "必要390g/1000g"),
    ("豚背ガラ", "肉類", 1056, 1056, "全量使用"),
    ("米澤豚モモ", "肉類", 1477, 1477, "ほぼ全量使用"),
    ("比内地鶏ミンチ", "肉類", 594, 594, "全量使用"),
    ("豚バラ追加500g", "肉類", 850, 850, "全量使用"),
    ("鶏卵", "肉類", 507, 507, "全量使用"),
    # デザート
    ("バニラビーンズ 10本", "デザート", 2480, 744, "3本/10本使用"),
    ("白バラクリーム48%", "デザート", 1208, 1208, "ほぼ全量"),
    ("冷凍パイシート", "デザート", 1485, 1485, "全量使用"),
    ("粉飴 1kg", "デザート", 1256, 126, "100g/1kg使用"),
    ("冷凍ラズベリー", "デザート", 900, 900, "全量使用（装飾）"),
    ("紅ほっぺ", "デザート", 578, 578, "全量使用"),
    ("スナップドラゴン", "デザート", 442, 442, "全量使用（装飾）"),
    ("スキムミルク", "デザート", 400, 50, "40g使用"),
    # ドリンク
    ("清美タンゴール10kg", "ドリンク", 3480, 3480, "全量使用"),
    ("完熟レモン", "ドリンク", 1296, 1296, "全量使用"),
    ("スパークリンググレープ", "ドリンク", 626, 626, "全量使用"),
    # 製麺・調味料
    ("春よ恋 2.5kg", "製麺・調味料", 648, 343, "1.32kg/2.5kg使用"),
    ("生茶葉 100g", "製麺・調味料", 1188, 143, "12g/100g使用"),
    ("有明海苔", "製麺・調味料", 944, 944, "全量使用"),
    ("真妻わさび", "製麺・調味料", 880, 880, "全量使用"),
    ("黒トリュフ", "製麺・調味料", 1000, 960, "48g/50g使用"),
    # その他
    ("調味料・牛乳等", "その他", 3500, 3500, "推定"),
]

# ソート（購入価格降順）
items.sort(key=lambda x: x[2], reverse=True)

names = [i[0] for i in items]
purchase = [i[2] for i in items]
effective = [i[3] for i in items]
waste = [i[2] - i[3] for i in items]
cats = [i[1] for i in items]
notes = [i[4] for i in items]

total_purchase = sum(purchase)
total_effective = sum(effective)
total_waste = total_purchase - total_effective

# カテゴリ別集計
cat_order = ["肉類", "デザート", "ドリンク", "製麺・調味料", "その他"]
colors = {"肉類": "#e74c3c", "デザート": "#f39c12", "ドリンク": "#3498db", "製麺・調味料": "#2ecc71", "その他": "#95a5a6"}

cat_purchase = {}
cat_effective = {}
for item in items:
    cat = item[1]
    cat_purchase[cat] = cat_purchase.get(cat, 0) + item[2]
    cat_effective[cat] = cat_effective.get(cat, 0) + item[3]

# === チャート ===
fig = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "bar"}, {"type": "pie"}],
        [{"type": "bar", "colspan": 2}, None],
    ],
    subplot_titles=(
        "カテゴリ別: 購入価格 vs 実質コスト",
        f"余り ¥{total_waste:,} の内訳",
        "全品目: 購入価格（色付き）vs 実質コスト（黒枠）",
    ),
    vertical_spacing=0.12,
    horizontal_spacing=0.1,
)

# 1. カテゴリ別 購入 vs 実質（グループ棒グラフ）
for cat in cat_order:
    fig.add_trace(
        go.Bar(
            name=f"{cat}（購入）",
            x=[cat],
            y=[cat_purchase[cat]],
            marker_color=colors[cat],
            opacity=0.4,
            text=[f"¥{cat_purchase[cat]:,}"],
            textposition="outside",
            showlegend=False,
        ),
        row=1, col=1,
    )
    fig.add_trace(
        go.Bar(
            name=f"{cat}（実質）",
            x=[cat],
            y=[cat_effective[cat]],
            marker_color=colors[cat],
            text=[f"¥{cat_effective[cat]:,}"],
            textposition="outside",
            showlegend=False,
        ),
        row=1, col=1,
    )

# 2. 余りの円グラフ
waste_items = [(items[i][0], waste[i]) for i in range(len(items)) if waste[i] > 0]
waste_items.sort(key=lambda x: x[1], reverse=True)
fig.add_trace(
    go.Pie(
        labels=[w[0] for w in waste_items],
        values=[w[1] for w in waste_items],
        textinfo="label+value",
        texttemplate="%{label}<br>¥%{value:,}",
        hole=0.3,
    ),
    row=1, col=2,
)

# 3. 全品目 横棒グラフ（購入価格 vs 実質コスト）
sorted_idx = sorted(range(len(items)), key=lambda i: items[i][2])
s_names = [names[i] for i in sorted_idx]
s_purchase = [purchase[i] for i in sorted_idx]
s_effective = [effective[i] for i in sorted_idx]
s_cats = [cats[i] for i in sorted_idx]
s_waste = [waste[i] for i in sorted_idx]

# 購入価格（薄い色）
fig.add_trace(
    go.Bar(
        y=s_names,
        x=s_purchase,
        orientation="h",
        marker_color=[colors[c] for c in s_cats],
        opacity=0.3,
        name="購入価格",
        text=[f"¥{v:,}" for v in s_purchase],
        textposition="outside",
        showlegend=True,
    ),
    row=2, col=1,
)

# 実質コスト（濃い色）
fig.add_trace(
    go.Bar(
        y=s_names,
        x=s_effective,
        orientation="h",
        marker_color=[colors[c] for c in s_cats],
        opacity=1.0,
        name="実質コスト",
        text=[f"¥{v:,}" if s_purchase[i] != s_effective[i] else "" for i, v in enumerate(s_effective)],
        textposition="inside",
        showlegend=True,
    ),
    row=2, col=1,
)

fig.update_layout(
    title=dict(
        text=(
            f"ラーメン料理会 材料費分析<br>"
            f"<sub>購入合計: ¥{total_purchase:,}（¥{total_purchase//12:,}/人）"
            f"　→　実質コスト: ¥{total_effective:,}（¥{total_effective//12:,}/人）"
            f"　｜　余り: ¥{total_waste:,}</sub>"
        ),
        font=dict(size=18),
    ),
    height=1100,
    width=1200,
    font=dict(size=11),
    barmode="overlay",
    legend=dict(x=0.7, y=0.35),
)

fig.update_yaxes(row=1, col=1, title_text="金額（円）")
fig.update_xaxes(row=2, col=1, title_text="金額（円）")

fig.write_html("/Users/ytonoyam/Dev/ryourikai/cost_effective.html")
print(f"購入合計: ¥{total_purchase:,}（¥{total_purchase//12:,}/人）")
print(f"実質コスト: ¥{total_effective:,}（¥{total_effective//12:,}/人）")
print(f"余り（今後使える分）: ¥{total_waste:,}")
print("Saved: cost_effective.html")
