import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
now_jst = datetime.now(JST).strftime("%Y-%m-%d %H:%M")

# === 粉データ ===
flours = [
    # (名前, タンパク質%, 灰分%, 原料, 推奨ラーメン, 食感キーワード)
    ("麺無双", 12.0, 0.35, "外国産", "万能", "コシ・粘り"),
    ("特 飛龍", 10.8, 0.35, "外国産", "醤油・中華そば", "バランス良い"),
    ("荒武者", 12.5, 0.40, "外国産", "つけ麺・濃厚系", "力強い弾力"),
    ("勇", 13.0, 0.42, "外国産", "博多豚骨", "歯切れ良い"),
    ("ゆめちから特", 11.5, 0.34, "北海道産", "清湯・醤油", "もちもち"),
    ("飛行船", 11.2, 0.40, "北海道産", "清湯・塩", "もちもち・甘み"),
    ("特龍翔", 11.0, 0.35, "外国産", "汎用", "粘弾性"),
    ("オーション", 13.0, 0.52, "外国産(2等粉)", "二郎・家系", "ゴワゴワ・野性的"),
    ("特ナンバーワン", 11.2, 0.34, "外国産", "清湯・醤油・塩", "なめらか"),
]

names = [f[0] for f in flours]
protein = [f[1] for f in flours]
ash = [f[2] for f in flours]
origin = [f[3] for f in flours]
ramen_type = [f[4] for f in flours]
texture = [f[5] for f in flours]

# 色: 推奨ラーメンタイプ別
color_map = {
    "清湯・塩": "#3498db",
    "清湯・醤油": "#2980b9",
    "清湯・醤油・塩": "#1abc9c",
    "醤油・中華そば": "#27ae60",
    "万能": "#95a5a6",
    "汎用": "#bdc3c7",
    "つけ麺・濃厚系": "#e74c3c",
    "博多豚骨": "#c0392b",
    "二郎・家系": "#8e44ad",
}
colors = [color_map.get(r, "#95a5a6") for r in ramen_type]

# マーカーサイズ: 国産は大きく
sizes = [20 if "北海道" in o else 14 for o in origin]

# === チャート ===
fig = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "scatter", "colspan": 2}, None],
        [{"type": "bar"}, {"type": "bar"}],
    ],
    subplot_titles=(
        "タンパク質 × 灰分 マトリックス（粉の性格マップ）",
        "タンパク質含有量 比較",
        "灰分 比較",
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.1,
)

# 1. 散布図（メインマトリックス）
for i, name in enumerate(names):
    fig.add_trace(
        go.Scatter(
            x=[protein[i]],
            y=[ash[i]],
            mode="markers+text",
            marker=dict(size=sizes[i], color=colors[i], line=dict(width=2, color="white")),
            text=[name],
            textposition="top center",
            textfont=dict(size=11, color=colors[i]),
            hovertemplate=(
                f"<b>{name}</b><br>"
                f"タンパク質: {protein[i]}%<br>"
                f"灰分: {ash[i]}%<br>"
                f"原料: {origin[i]}<br>"
                f"食感: {texture[i]}<br>"
                f"向き: {ramen_type[i]}"
                f"<extra></extra>"
            ),
            showlegend=False,
        ),
        row=1, col=1,
    )

# 象限ラベル
fig.add_annotation(x=10.5, y=0.50, text="風味強い・軽い食感", font=dict(size=10, color="gray"), showarrow=False, row=1, col=1)
fig.add_annotation(x=13.3, y=0.50, text="風味強い・コシ強い", font=dict(size=10, color="gray"), showarrow=False, row=1, col=1)
fig.add_annotation(x=10.5, y=0.32, text="上品・なめらか", font=dict(size=10, color="gray"), showarrow=False, row=1, col=1)
fig.add_annotation(x=13.3, y=0.32, text="コシ強い・色白", font=dict(size=10, color="gray"), showarrow=False, row=1, col=1)

# 象限線
fig.add_hline(y=0.38, line_dash="dot", line_color="lightgray", row=1, col=1)
fig.add_vline(x=11.8, line_dash="dot", line_color="lightgray", row=1, col=1)

# 推奨ゾーン
fig.add_shape(
    type="rect", x0=10.6, x1=11.8, y0=0.30, y1=0.42,
    line=dict(color="#3498db", width=2, dash="dash"),
    fillcolor="rgba(52,152,219,0.05)",
    row=1, col=1,
)
fig.add_annotation(x=11.2, y=0.30, text="← Ramen I 清湯向き", font=dict(size=10, color="#3498db"), showarrow=False, row=1, col=1)

fig.add_shape(
    type="rect", x0=11.8, x1=13.3, y0=0.36, y1=0.54,
    line=dict(color="#e74c3c", width=2, dash="dash"),
    fillcolor="rgba(231,76,60,0.05)",
    row=1, col=1,
)
fig.add_annotation(x=12.6, y=0.54, text="Ramen II 豚骨向き →", font=dict(size=10, color="#e74c3c"), showarrow=False, row=1, col=1)

# 2. タンパク質 棒グラフ
sorted_by_protein = sorted(range(len(flours)), key=lambda i: protein[i])
fig.add_trace(
    go.Bar(
        x=[names[i] for i in sorted_by_protein],
        y=[protein[i] for i in sorted_by_protein],
        marker_color=[colors[i] for i in sorted_by_protein],
        text=[f"{protein[i]}%" for i in sorted_by_protein],
        textposition="outside",
    ),
    row=2, col=1,
)

# 3. 灰分 棒グラフ
sorted_by_ash = sorted(range(len(flours)), key=lambda i: ash[i])
fig.add_trace(
    go.Bar(
        x=[names[i] for i in sorted_by_ash],
        y=[ash[i] for i in sorted_by_ash],
        marker_color=[colors[i] for i in sorted_by_ash],
        text=[f"{ash[i]}%" for i in sorted_by_ash],
        textposition="outside",
    ),
    row=2, col=2,
)

fig.update_layout(
    title=dict(
        text=(
            f"製麺用小麦粉 特徴マトリックス（{now_jst} JST）<br>"
            f"<sub>●大=北海道産　青系=清湯向き　赤系=濃厚系向き　紫=二郎系</sub>"
        ),
        font=dict(size=18),
    ),
    height=1100,
    width=1200,
    showlegend=False,
    font=dict(size=11),
)

fig.update_xaxes(title_text="タンパク質（%）", row=1, col=1)
fig.update_yaxes(title_text="灰分（%）", row=1, col=1)
fig.update_yaxes(title_text="タンパク質（%）", row=2, col=1)
fig.update_yaxes(title_text="灰分（%）", row=2, col=2)

fig.write_html("/Users/ytonoyam/Dev/ryourikai/flour_matrix.html")
print("Saved: flour_matrix.html")
