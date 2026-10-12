# GeoFeature · 全球半岛版（Peninsulas）

全球地理要素识别项目（半岛专题）。内置可交互地图网页，并附带 **14,896 条全球半岛数据**（GeoNames TPEN 提取 + 中文名标注），游客可直接部署到自己的项目中。

## 内容
- `index.html` — 交互式网页（MapLibre GL 矢量瓦片底图），内置「📥 导入数据」按钮，支持拖拽 / 选择 `.csv`、`.geojson` 导入并自动合并到要素库。
- `半岛_可导入数据.csv` — 14,896 条半岛数据（含中文名、名称性质、原名/英文、国家、经纬度、geonameid）。
- `半岛_可导入数据.geojson` — 同上数据的 GeoJSON 版本（点要素）。
- `import_可导入数据.py` — 把 CSV 合并进 HTML 的本地脚本。
- `导入方法.txt` — 导入说明。

## 名称性质说明
- `共识译名`：采用的中文共识名。
- `音译名`：按原名音译得到的中文名。
- `待补译名`：原无中文名，按原名音译为「中文名（原名）」格式。

## 快速使用
1. 打开 `index.html`（GitHub Pages / 本地均可）。
2. 点「📥 导入数据」选择 `半岛_可导入数据.geojson` 或 `.csv`，或直接把文件拖到地图上。

## 部署到你自己的项目
```bash
git clone https://github.com/wsnailong-ge0guess01/geofeature-peninsulas.git
```
把 `index.html` 与数据文件拷贝进你的站点即可；数据为公开地理数据，可自由使用。

## 数据来源
GeoNames（CC BY 4.0）。中文名为项目生成/音译结果，冷门地名仅供展示，精确译名可自行校对。
