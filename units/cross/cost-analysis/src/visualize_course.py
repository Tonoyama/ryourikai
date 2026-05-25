import plotly.graph_objects as go
from plotly.subplots import make_subplots

# === コース品目ごとの実質コスト ===

courses = {
    "前菜\n鮪中落ち": [
        ("本マグロ中落ち", 2354),
        # 青種・赤種わさび、たまりは価格に含めない（未確定）
    ],
    "Ramen I\n比内地鶏清湯": [
        ("比内地鶏ガラ", 1944),
        ("比内地鶏 鶏皮(390g分)", 546),
        ("比内地鶏ミンチ(雲吞)", 594),
        ("黒トリュフ(48g)", 960),
        ("春よ恋(600g分)", 165),
        ("生茶葉(12g分)", 143),  # グラニテの茶葉
        ("調味料等(タレ・昆布・生姜)", 500),
    ],
    "お口直し\nグラニテ": [
        ("グラニュー糖・レモン果汁等", 100),
        # 生茶葉はRamen Iに計上済み（コース内の流れ）
    ],
    "Ramen II\n濃厚豚骨": [
        ("豚背ガラ", 1056),
        ("豚バラブロック(焼豚)", 1706),
        ("豚バラ追加500g", 850),
        ("有明海苔", 944),
        ("鶏卵(味玉12個分)", 350),
        ("春よ恋(720g分)", 187),
        ("調味料等(タレ・メンマ・マー油)", 600),
    ],
    "Dessert\nRaspberry Pi\n(アイスなし)": [
        ("冷凍パイシート", 1485),
        ("紅ほっぺ", 578),
        ("冷凍ラズベリー", 900),
        ("スナップドラゴン", 442),
        ("鶏卵(パイ卵黄3個分)", 57),
        ("マデイラワイン等", 0),  # 価格に含めない
    ],
    "Dessert\nバニラアイス\n+ガストリック": [
        ("生クリーム45%", 583),
        ("バニラビーンズ(3本分)", 744),
        ("粉飴(100g分)", 126),
        ("牛乳(750ml)", 200),
        ("鶏卵(アイス卵黄3個分)", 100),
        ("グラニュー糖", 50),
        ("バルサミコ酢(ガストリック)", 100),
    ],
    "ドリンク\n6種": [
        ("清美タンゴール10kg", 3480),
        ("広島レモン(2個)", 523),
        ("スパークリンググレープ", 626),
        ("コーラ・エルダーフラワー等", 700),
    ],
}

# Ramen I に 実山椒（ツミレ・トッピング両用）を追加
courses["Ramen I\n比内地鶏清湯"].append(("実山椒(50g)", 458))

# 集計
course_names = []
course_totals = []
for course, items in courses.items():
    total = sum(v for _, v in items)
    course_names.append(course)
    course_totals.append(total)

grand_total = sum(course_totals)

# デザート合計（アイスあり vs なし）
dessert_pie_only = course_totals[4]  # Raspberry Piのみ
dessert_ice = course_totals[5]  # アイス+ガストリック
dessert_total = dessert_pie_only + dessert_ice

# === チャート ===
fig = make_subplots(
    rows=2, cols=2,
    specs=[
        [{"type": "bar", "colspan": 2}, None],
        [{"type": "pie"}, {"type": "bar"}],
    ],
    subplot_titles=(
        "コース品目ごとの実質コスト",
        "コース全体の割合",
        "デザート: アイスあり vs なし",
    ),
    vertical_spacing=0.15,
    horizontal_spacing=0.1,
)

# 色
course_colors = ["#e74c3c", "#ff6b6b", "#95e1d3", "#f38181", "#f39c12", "#fce38a", "#3498db"]

# 1. コース品目ごとの棒グラフ
fig.add_trace(
    go.Bar(
        x=course_names,
        y=course_totals,
        marker_color=course_colors,
        text=[f"¥{v:,}<br>(¥{v//12:,}/人)" for v in course_totals],
        textposition="outside",
        textfont=dict(size=11),
    ),
    row=1, col=1,
)

# 2. 円グラフ
fig.add_trace(
    go.Pie(
        labels=course_names,
        values=course_totals,
        marker=dict(colors=course_colors),
        textinfo="label+percent",
        texttemplate="%{label}<br>%{percent}",
        hole=0.3,
        textfont=dict(size=10),
    ),
    row=2, col=1,
)

# 3. デザート アイスあり vs なし
dessert_labels = ["パイのみ\n(アイスなし)", "アイス+ガストリック", "デザート合計"]
dessert_values = [dessert_pie_only, dessert_ice, dessert_total]
dessert_colors_bar = ["#f39c12", "#fce38a", "#e67e22"]

fig.add_trace(
    go.Bar(
        x=dessert_labels,
        y=dessert_values,
        marker_color=dessert_colors_bar,
        text=[
            f"¥{dessert_pie_only:,}<br>(¥{dessert_pie_only//12:,}/人)",
            f"¥{dessert_ice:,}<br>(¥{dessert_ice//12:,}/人)",
            f"¥{dessert_total:,}<br>(¥{dessert_total//12:,}/人)",
        ],
        textposition="outside",
    ),
    row=2, col=2,
)

# アノテーション
fig.add_annotation(
    x="デザート合計",
    y=dessert_total + 500,
    text=f"アイスを省くと<br>¥{dessert_ice:,}節約<br>(¥{dessert_ice//12:,}/人)",
    showarrow=True,
    arrowhead=2,
    font=dict(size=12, color="red"),
    row=2, col=2,
)

fig.update_layout(
    title=dict(
        text=(
            f"ラーメン料理会 コース品目別コスト分析<br>"
            f"<sub>実質コスト合計: ¥{grand_total:,}（¥{grand_total//12:,}/人）</sub>"
        ),
        font=dict(size=18),
    ),
    height=1000,
    width=1200,
    showlegend=False,
    font=dict(size=11),
)

fig.update_yaxes(row=1, col=1, title_text="金額（円）")
fig.update_yaxes(row=2, col=2, title_text="金額（円）")

fig.write_html("/Users/ytonoyam/Dev/ryourikai/units/cross/cost-analysis/dist/cost_by_course.html")

# テキスト出力
print("=" * 50)
print("コース品目ごとの実質コスト")
print("=" * 50)
for name, total in zip(course_names, course_totals):
    label = name.replace("\n", " ")
    print(f"  {label:30s}  ¥{total:>6,}  (¥{total//12:,}/人)")
print("-" * 50)
print(f"  {'合計':30s}  ¥{grand_total:>6,}  (¥{grand_total//12:,}/人)")
print()
print(f"  デザート（パイのみ）:  ¥{dessert_pie_only:,}  (¥{dessert_pie_only//12:,}/人)")
print(f"  デザート（アイス追加）: ¥{dessert_ice:,}  (¥{dessert_ice//12:,}/人)")
print(f"  アイスを省くと ¥{dessert_ice:,} 節約（¥{dessert_ice//12:,}/人）")
