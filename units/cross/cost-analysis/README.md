# Unit: Cost Analysis — コスト・粉ブレンド可視化（横断）

## Intent
コース料理全体のコスト構造・粉ブレンドマトリクスを Python で可視化し、HTML として共有可能な形で保存する。本番前の見積もり・粉選定検証・コース別配分の調整に使用。

## Success Criteria
- `src/` のスクリプトを実行すると `dist/` に最新の HTML が生成される
- コース単位・食材単位・粉マトリクスのいずれの観点でも見られる

## Components

### Source (`src/`)
- `visualize.py` — エントリポイント／総合
- `visualize_course.py` — コース別コスト
- `visualize_current.py` — 現行レシピのコスト
- `visualize_flour.py` — 粉ブレンドマトリクス

### Output (`dist/`)
- `cost_breakdown.html` — コスト内訳
- `cost_by_course.html` — コース別
- `cost_current.html` — 現行スナップショット
- `flour_matrix.html` — 粉マトリクス
- `pie-cutting-guide.svg` — 切り分けガイド

## Consumers
- 全 dish Unit（特に Ramen I/II の麺・スープ材料コスト）
- `units/cross/procurement`
