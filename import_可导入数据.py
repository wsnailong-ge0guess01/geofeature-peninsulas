# -*- coding: utf-8 -*-
"""
GeoFeature 可导入数据 → 网页内置库 一键导入脚本
--------------------------------------------------
把「半岛_可导入数据.geojson」里的半岛，合并进网页的 FEATURES 数组
（转成点要素），生成一个新 HTML，不覆盖原文件。

用法（Windows 在 cmd 里）：
    cd /d D:\待删除
    python import_可导入数据.py geo_features_tiles_全球半岛版.html

可选参数：
    --only 共识译名      只导入「共识译名」条目
    --only 共识译名,音译名  只导入这两类
    （不加 --only 则全部导入：共识译名+音译名+待补译名）
    --nature tl          只把「音译名/待补译名」作为可选，同上用中文更直观

输出：
    原名_已导入.html   （例如 geo_features_tiles_全球半岛版_已导入.html）
"""
import sys, json, re, os, argparse

def build_obj(props, coord):
    lon, lat = coord
    name = props.get('name') or props.get('name_en') or ''
    en = props.get('name_en', '')
    src = props.get('src', '')
    # 名称性质 → 网页 src 码：cs=共识译名 / tl=音译名 / un=待补译名
    nature = props.get('nature', '')
    code = {'共识译名': 'cs', '音译名': 'tl', '待补译名': 'un'}.get(nature, 'tl')
    o = {'type': 'peninsula', 'name': name, 'en': en,
         'pt': [round(float(lon), 5), round(float(lat), 5)],
         'rank': 3, 'country': props.get('country', ''), 'src': code}
    gid = str(props.get('geonameid', '')).strip()
    if gid.isdigit():
        o['geonameid'] = int(gid)
    return o

def obj_to_js(o):
    # 转成与网页内既有条目风格一致的 JS 对象字面量
    parts = ['"type": %s' % json.dumps(o['type'], ensure_ascii=False),
             '"name": %s' % json.dumps(o['name'], ensure_ascii=False),
             '"en": %s' % json.dumps(o['en'], ensure_ascii=False),
             '"pt": %s' % json.dumps(o['pt']),
             '"rank": %s' % o['rank'],
             '"country": %s' % json.dumps(o['country'], ensure_ascii=False),
             '"src": %s' % json.dumps(o['src'], ensure_ascii=False)]
    if 'geonameid' in o:
        parts.append('"geonameid": %d' % o['geonameid'])
    return '{' + ', '.join(parts) + '}'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('html', help='网页文件，如 geo_features_tiles_全球半岛版.html')
    ap.add_argument('--geojson', default='半岛_可导入数据.geojson')
    ap.add_argument('--only', default='', help='只导入这些名称性质，逗号分隔')
    ap.add_argument('--out', default='')
    args = ap.parse_args()

    use = set(x.strip() for x in args.only.split(',') if x.strip())
    gj = json.load(open(args.geojson, encoding='utf-8'))

    objs = []
    skip = 0
    for f in gj['features']:
        pr = f['properties']
        if use and pr.get('nature') not in use:
            skip += 1
            continue
        coord = f['geometry']['coordinates']
        objs.append(obj_to_js(build_obj(pr, coord)))

    s = open(args.html, encoding='utf-8').read()
    m = re.search(r'var FEATURES = \[', s)
    if not m:
        print('未找到 var FEATURES，请确认这是 GeoFeature 网页文件'); sys.exit(1)
    end = s.index('\n];', m.end())
    block = s[m.end():end]
    block = block.rstrip()
    if block.endswith(','):
        block = block[:-1]
    add = ',\n' + ',\n'.join(objs)
    new_s = s[:m.end()] + block + add + s[end:]

    out = args.out or (os.path.splitext(args.html)[0] + '_已导入.html')
    open(out, 'w', encoding='utf-8').write(new_s)
    print('已导入 %d 条（跳过 %d 条）' % (len(objs), skip))
    print('输出文件：%s' % out)

if __name__ == '__main__':
    main()
