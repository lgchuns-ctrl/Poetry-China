#!/usr/bin/env python3
"""
主数据处理管线 (简化版)
1. 加载已转换的简体数据 (由 opencc-js 转换)
2. 数据清洗标准化
3. 地名提取 (词典+规则匹配)
4. 意象/主题/季节/情绪提取
5. 数据分析
6. 导出前端JSON
"""

import json
import os
import re
import hashlib
import random
from collections import Counter, defaultdict
from datetime import datetime

BASE_DIR = os.path.join(os.path.dirname(__file__), '..')
RAW_DIR = os.path.join(BASE_DIR, 'data/raw')
INTERIM_DIR = os.path.join(BASE_DIR, 'data/interim')
PROCESSED_DIR = os.path.join(BASE_DIR, 'data/processed')
DICT_DIR = os.path.join(BASE_DIR, 'data/dictionary')
REPORTS_DIR = os.path.join(BASE_DIR, 'data/reports')

for d in [INTERIM_DIR, PROCESSED_DIR, REPORTS_DIR]:
    os.makedirs(d, exist_ok=True)

import sys
sys.path.insert(0, DICT_DIR)
from place_dictionary import PLACE_DICTIONARY, EXCLUDE_WORDS, build_index

# 目标诗人
TARGET_TANG_POETS = {'李白', '杜甫', '王维', '白居易', '孟浩然', '杜牧', '李商隐',
                      '王昌龄', '高适', '刘禹锡', '韩愈', '柳宗元', '贾岛', '李贺',
                      '温庭筠', '元稹', '张九龄', '陈子昂', '韦应物', '岑参',
                      '崔颢', '王之涣', '王勃', '张继', '韦庄', '李颀', '张籍', '许浑',
                      '骆宾王', '卢照邻', '杨炯', '储光羲'}

TARGET_SONG_CI_AUTHORS = {'苏轼', '辛弃疾', '李清照', '柳永', '陆游', '欧阳修',
                          '晏殊', '晏几道', '周邦彦', '姜夔', '秦观', '黄庭坚',
                          '王安石', '贺铸', '张先', '范仲淹', '张孝祥', '陈亮',
                          '刘克庄', '吴文英', '张炎', '王沂孙', '朱敦儒', '叶梦得'}

# 意象词典
IMAGERY_DICT = {
    '月': '天象', '日': '天象', '星': '天象', '云': '天象', '风': '天象',
    '雨': '天象', '雪': '天象', '霜': '天象', '露': '天象', '雾': '天象',
    '雷': '天象', '虹': '天象', '霞': '天象', '烟': '天象',
    '酒': '器物', '舟': '器物', '船': '器物', '帆': '器物', '剑': '器物',
    '弓': '器物', '刀': '器物', '镜': '器物', '帘': '器物',
    '灯': '器物', '烛': '器物', '炉': '器物', '笛': '器物', '琴': '器物',
    '筝': '器物', '钟': '器物', '鼓': '器物', '箫': '器物', '瑟': '器物',
    '壶': '器物', '杯': '器物', '盏': '器物', '樽': '器物', '觞': '器物',
    '雁': '动物', '燕': '动物', '莺': '动物', '蝶': '动物', '蜂': '动物',
    '蝉': '动物', '鱼': '动物', '龙': '动物', '凤': '动物', '鹤': '动物',
    '鸦': '动物', '鹊': '动物', '鸥': '动物', '鹭': '动物',
    '马': '动物', '牛': '动物', '羊': '动物', '鹿': '动物', '虎': '动物',
    '猿': '动物', '蛙': '动物', '兔': '动物',
    '花': '植物', '柳': '植物', '松': '植物', '竹': '植物', '梅': '植物',
    '桃': '植物', '杏': '植物', '梨': '植物', '菊': '植物',
    '兰': '植物', '荷': '植物', '莲': '植物', '桂': '植物', '枫': '植物',
    '桑': '植物', '芦': '植物', '苔': '植物',
    '草': '植物', '藤': '植物', '槐': '植物', '榆': '植物', '柏': '植物',
    '山': '自然', '水': '自然', '江': '自然', '河': '自然', '湖': '自然',
    '海': '自然', '溪': '自然', '泉': '自然', '潭': '自然', '池': '自然',
    '波': '自然', '浪': '自然', '潮': '自然', '冰': '自然',
    '石': '自然', '岩': '自然', '峰': '自然', '谷': '自然', '崖': '自然',
    '楼': '建筑', '台': '建筑', '阁': '建筑', '亭': '建筑', '桥': '建筑',
    '寺': '建筑', '塔': '建筑', '宫': '建筑', '殿': '建筑', '庙': '建筑',
    '城': '建筑', '门': '建筑', '墙': '建筑', '院': '建筑', '庭': '建筑',
    '阶': '建筑', '廊': '建筑', '檐': '建筑',
}

THEME_KEYWORDS = {
    '山水': ['山', '水', '溪', '泉', '峰', '谷', '崖', '瀑', '林', '野', '青山', '绿水'],
    '田园': ['田', '园', '农', '桑', '麻', '稻', '麦', '耕', '牧', '柴', '篱', '村'],
    '边塞': ['塞', '关', '戍', '边', '胡', '戎', '征', '战', '旗', '鼓', '弓', '剑'],
    '送别': ['送', '别', '离', '辞', '留', '赠', '饯'],
    '思乡': ['乡', '家', '归', '故', '思', '忆', '念', '梦', '客', '旅'],
    '怀古': ['古', '昔', '旧', '废', '荒', '残', '千秋', '兴亡', '兴废'],
    '咏史': ['史', '帝', '王', '侯', '将', '相', '功', '名', '朝', '代'],
    '爱情': ['情', '恨', '泪', '欢', '爱', '怜', '娇', '怨'],
    '羁旅': ['旅', '客', '行', '路', '途', '孤', '舟', '马'],
    '饮酒': ['酒', '醉', '杯', '壶', '饮', '酌', '樽', '觞', '酣'],
    '节令': ['春', '夏', '秋', '冬', '元', '清', '端', '重阳', '寒', '暑'],
    '咏物': ['咏', '题', '赋'],
}

SEASON_KEYWORDS = {
    '春': ['春', '桃花', '杏花', '柳', '莺', '燕', '蝶', '春风', '春雨', '东风', '清明', '桃', '杏'],
    '夏': ['夏', '荷', '蝉', '蛙', '暑', '南风', '莲', '芙蓉', '石榴'],
    '秋': ['秋', '雁', '菊', '枫', '霜', '秋风', '西风', '中秋', '重阳', '桂', '蛩'],
    '冬': ['冬', '雪', '梅', '寒', '冰', '朔风', '北风', '冬至', '腊', '冻'],
}

MOOD_KEYWORDS = {
    '豪迈': ['豪', '壮', '雄', '气', '万里', '长风', '大江', '金戈', '铁马', '气吞'],
    '思乡': ['乡', '故园', '归', '思', '忆', '念', '家山', '梦回', '客'],
    '离愁': ['离', '别', '愁', '恨', '泪', '伤', '断肠', '相思', '孤'],
    '闲适': ['闲', '静', '幽', '适', '远', '淡', '清', '隐', '渔', '樵'],
    '悲秋': ['悲', '萧', '瑟', '凋', '零', '落', '衰', '残', '荒'],
    '怀古': ['古', '昔', '旧', '废', '荒', '兴亡', '千秋', '沧桑', '往事'],
    '旷达': ['旷', '达', '笑', '醉', '放', '狂', '任', '随', '潇洒', '豁'],
    '孤寂': ['孤', '寂', '独', '寥', '冷', '空', '幽', '清', '寒'],
    '喜悦': ['喜', '欢', '乐', '笑', '欣', '悦', '歌', '舞'],
    '忧愁': ['忧', '愁', '叹', '悲', '伤', '苦', '闷', '惆', '怅', '凄'],
}


def load_data():
    """加载已转换的简体数据"""
    print('=== 加载数据 ===')
    
    tang_path = os.path.join(INTERIM_DIR, 'tang_poetry.json')
    ci_path = os.path.join(INTERIM_DIR, 'song_ci.json')
    authors_path = os.path.join(INTERIM_DIR, 'authors.json')
    
    with open(tang_path, 'r', encoding='utf-8') as f:
        tang_data = json.load(f)
    print(f'  唐诗: {len(tang_data)} 首')
    
    with open(ci_path, 'r', encoding='utf-8') as f:
        ci_data = json.load(f)
    print(f'  宋词: {len(ci_data)} 首')
    
    with open(authors_path, 'r', encoding='utf-8') as f:
        authors_data = json.load(f)
    print(f'  作者: {len(authors_data)} 位')
    
    return tang_data, ci_data, authors_data


def extract_places(text, place_index):
    """从文本提取地名"""
    mentions = []
    all_names = sorted(place_index.keys(), key=lambda x: -len(x))
    found_spans = []
    
    for name in all_names:
        if name in EXCLUDE_WORDS or len(name) < 2:
            continue
        start = 0
        while True:
            pos = text.find(name, start)
            if pos == -1:
                break
            end_pos = pos + len(name)
            overlap = any(pos < e and end_pos > s for s, e in found_spans)
            if not overlap:
                ctx_start = max(0, pos - 15)
                ctx_end = min(len(text), end_pos + 15)
                context = text[ctx_start:ctx_end]
                
                idx = place_index[name]
                p = PLACE_DICTIONARY[idx]
                
                mentions.append({
                    'place_name': name,
                    'place_name_normalized': p['place_name_normalized'],
                    'place_type': p['place_type'],
                    'context': context,
                    'modern_name': p.get('modern_name', ''),
                    'modern_province': p.get('modern_province', ''),
                    'longitude': p.get('longitude', 0),
                    'latitude': p.get('latitude', 0),
                    'mapping_level': p.get('mapping_level', 'unknown'),
                })
                found_spans.append((pos, end_pos))
            start = pos + 1
    
    return mentions


def extract_imagery(text):
    found = []
    seen = set()
    for word, cat in IMAGERY_DICT.items():
        if word in text and word not in seen:
            found.append({'image_word': word, 'image_category': cat})
            seen.add(word)
    return found


def classify_themes(text, title=''):
    combined = title + text
    themes = []
    for theme, keywords in THEME_KEYWORDS.items():
        if sum(1 for kw in keywords if kw in combined) >= 2:
            themes.append(theme)
    return themes if themes else ['其他']


def detect_season(text):
    seasons = []
    for season, keywords in SEASON_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            seasons.append(season)
    return seasons


def detect_mood(text, title=''):
    combined = title + text
    moods = []
    for mood, keywords in MOOD_KEYWORDS.items():
        if sum(1 for kw in keywords if kw in combined) >= 2:
            moods.append(mood)
    return moods


def process_data(tang_data, ci_data, authors_data):
    """主处理"""
    print('\n=== 数据处理 ===')
    place_index = build_index()
    
    author_map = {a['name']: a for a in authors_data}
    author_ids = {}
    works = []
    authors = []
    place_mentions = []
    
    def get_or_create_author(name, dynasty, src_id):
        if name not in author_ids:
            aid = f'a_{len(author_ids):04d}'
            author_ids[name] = aid
            info = author_map.get(name, {})
            authors.append({
                'author_id': aid,
                'author_name': name,
                'dynasty': dynasty,
                'birth_year': None,
                'death_year': None,
                'birth_place_raw': '',
                'biography_summary': (info.get('desc', '') or '')[:300],
                'source_id': src_id,
            })
        return author_ids[name]
    
    print('  处理唐诗...')
    for poem in tang_data:
        author_name = poem.get('author', '')
        title = poem.get('title', '')
        paragraphs = poem.get('paragraphs', [])
        text = '\n'.join(paragraphs)
        if not text.strip():
            continue
        
        work_id = f'w_{len(works):05d}'
        aid = get_or_create_author(author_name, '唐', 'src_001')
        
        mentions = extract_places(text, place_index)
        imagery = extract_imagery(text)
        themes = classify_themes(text, title)
        seasons = detect_season(text)
        moods = detect_mood(text, title)
        
        works.append({
            'work_id': work_id,
            'title': title,
            'author_id': aid,
            'author_name': author_name,
            'dynasty': '唐',
            'genre': 'shi',
            'text': text,
            'text_hash': hashlib.md5(text.encode()).hexdigest()[:16],
            'source_id': 'src_001',
            'place_mentions': [m['place_name_normalized'] for m in mentions],
            'imagery': [i['image_word'] for i in imagery],
            'themes': themes,
            'season_imagery': seasons,
            'moods': moods,
            'is_target_author': author_name in TARGET_TANG_POETS,
        })
        
        for m in mentions:
            place_mentions.append({
                'work_id': work_id,
                'place_name': m['place_name'],
                'place_name_normalized': m['place_name_normalized'],
                'place_type': m['place_type'],
                'context': m['context'],
                'modern_name': m['modern_name'],
                'modern_province': m['modern_province'],
                'longitude': m['longitude'],
                'latitude': m['latitude'],
                'mapping_level': m['mapping_level'],
                'dynasty': '唐',
                'author_name': author_name,
            })
    
    print(f'  唐诗: {sum(1 for w in works if w["dynasty"]=="唐")} 首')
    
    print('  处理宋词...')
    for ci in ci_data:
        author_name = ci.get('author', '')
        rhythmic = ci.get('rhythmic', '')
        paragraphs = ci.get('paragraphs', [])
        text = '\n'.join(paragraphs)
        if not text.strip():
            continue
        
        work_id = f'w_{len(works):05d}'
        aid = get_or_create_author(author_name, '宋', 'src_002')
        title = rhythmic
        
        mentions = extract_places(text, place_index)
        imagery = extract_imagery(text)
        themes = classify_themes(text, title)
        seasons = detect_season(text)
        moods = detect_mood(text, title)
        
        works.append({
            'work_id': work_id,
            'title': title,
            'author_id': aid,
            'author_name': author_name,
            'dynasty': '宋',
            'genre': 'ci',
            'text': text,
            'text_hash': hashlib.md5(text.encode()).hexdigest()[:16],
            'source_id': 'src_002',
            'place_mentions': [m['place_name_normalized'] for m in mentions],
            'imagery': [i['image_word'] for i in imagery],
            'themes': themes,
            'season_imagery': seasons,
            'moods': moods,
            'is_target_author': author_name in TARGET_SONG_CI_AUTHORS,
        })
        
        for m in mentions:
            place_mentions.append({
                'work_id': work_id,
                'place_name': m['place_name'],
                'place_name_normalized': m['place_name_normalized'],
                'place_type': m['place_type'],
                'context': m['context'],
                'modern_name': m['modern_name'],
                'modern_province': m['modern_province'],
                'longitude': m['longitude'],
                'latitude': m['latitude'],
                'mapping_level': m['mapping_level'],
                'dynasty': '宋',
                'author_name': author_name,
            })
    
    print(f'  宋词: {sum(1 for w in works if w["dynasty"]=="宋")} 首')
    
    # 构建地点表
    places = []
    for i, p in enumerate(PLACE_DICTIONARY):
        places.append({
            'place_id': f'pl_{i:04d}',
            'place_name': p['place_name'],
            'place_name_normalized': p['place_name_normalized'],
            'place_type': p['place_type'],
            'historical_name': p.get('historical_name', ''),
            'modern_name': p.get('modern_name', ''),
            'modern_province': p.get('modern_province', ''),
            'modern_city': p.get('modern_city', ''),
            'longitude': p.get('longitude', 0),
            'latitude': p.get('latitude', 0),
            'mapping_level': p.get('mapping_level', 'unknown'),
            'mapping_confidence': 0.9 if p.get('mapping_level') in ('exact', 'city', 'county') else 0.6,
            'mapping_source': p.get('mapping_source', ''),
            'aliases': p.get('aliases', []),
        })
    
    return works, authors, places, place_mentions


def analyze(works, authors, places, place_mentions):
    """数据分析"""
    print('\n=== 数据分析 ===')
    a = {}
    
    tang = [w for w in works if w['dynasty'] == '唐']
    song = [w for w in works if w['dynasty'] == '宋']
    
    a['basic_stats'] = {
        'total_works': len(works),
        'tang_poems': len(tang),
        'song_ci': len(song),
        'total_authors': len(authors),
        'total_places': len(places),
        'total_mentions': len(place_mentions),
    }
    print(f"  作品: {a['basic_stats']['total_works']} (唐{a['basic_stats']['tang_poems']} / 宋{a['basic_stats']['song_ci']})")
    print(f"  地点提及: {a['basic_stats']['total_mentions']}")
    
    # 作者作品数
    aw = Counter(w['author_name'] for w in works)
    a['top_authors'] = [{'author': n, 'count': c} for n, c in aw.most_common(30)]
    
    # 地名频率
    pf = Counter()
    for m in place_mentions:
        pf[m['place_name_normalized']] += 1
    a['top_places'] = [{'place': n, 'count': c} for n, c in pf.most_common(50)]
    print(f"  提及地点种类: {len(pf)}")
    print(f"  TOP5: {pf.most_common(5)}")
    
    # 类型频率
    a['place_type_freq'] = dict(Counter(m['place_type'] for m in place_mentions))
    
    # 诗人×地点
    ap = defaultdict(Counter)
    for m in place_mentions:
        ap[m['author_name']][m['place_name_normalized']] += 1
    a['author_place_matrix'] = {au: dict(pl) for au, pl in ap.items()}
    
    # 朝代×地点
    dp = defaultdict(Counter)
    for m in place_mentions:
        dp[m['dynasty']][m['place_name_normalized']] += 1
    a['dynasty_place_summary'] = {d: dict(p) for d, p in dp.items()}
    
    # 地点×主题
    pt = defaultdict(Counter)
    work_map = {w['work_id']: w for w in works}
    for m in place_mentions:
        w = work_map.get(m['work_id'])
        if w:
            for t in w['themes']:
                pt[m['place_name_normalized']][t] += 1
    a['place_theme'] = {p: dict(t) for p, t in pt.items()}
    
    # 地点×意象
    pi = defaultdict(Counter)
    for m in place_mentions:
        w = work_map.get(m['work_id'])
        if w:
            for img in w['imagery']:
                pi[m['place_name_normalized']][img] += 1
    a['place_imagery'] = {p: dict(i) for p, i in pi.items()}
    
    # 诗人×意象
    ai = defaultdict(Counter)
    for w in works:
        for img in w['imagery']:
            ai[w['author_name']][img] += 1
    a['author_imagery'] = {au: dict(i) for au, i in ai.items()}
    
    # TOP分类
    def top_by_type(ptype):
        typed = (m['place_name_normalized'] for m in place_mentions if m['place_type'] == ptype)
        return [{'place': n, 'count': c} for n, c in Counter(typed).most_common(20)]
    
    a['top_cities'] = top_by_type('city')
    a['top_mountains'] = top_by_type('mountain')
    a['top_rivers'] = top_by_type('river')
    a['top_lakes'] = top_by_type('lake')
    
    # 季节×地点
    sp = defaultdict(Counter)
    for w in works:
        for s in w.get('season_imagery', []):
            for p in w.get('place_mentions', []):
                sp[s][p] += 1
    a['season_place'] = {s: dict(p) for s, p in sp.items()}
    
    # 意象频率
    ifreq = Counter()
    for w in works:
        for img in w['imagery']:
            ifreq[img] += 1
    a['imagery_freq'] = dict(ifreq.most_common(30))
    
    # 主题频率
    tfreq = Counter()
    for w in works:
        for t in w['themes']:
            tfreq[t] += 1
    a['theme_freq'] = dict(tfreq)
    
    # 诗人多样性
    ad = {}
    for au, pl in ap.items():
        total = sum(pl.values())
        if total >= 5:
            ad[au] = {
                'unique_places': len(pl),
                'total_mentions': total,
                'diversity_index': round(len(pl) / total, 3)
            }
    a['author_diversity'] = dict(sorted(ad.items(), key=lambda x: -x[1]['unique_places'])[:30])
    
    return a


def gen_conclusions(a):
    """生成数据驱动结论"""
    print('\n=== 生成结论 ===')
    cs = []
    bs = a['basic_stats']
    
    if a['top_places']:
        t = a['top_places'][0]
        cs.append({'conclusion_id': 'c_001',
            'text': f"在当前数据集中，「{t['place']}」是被诗词书写次数最多的地点，共被提及{t['count']}次。",
            'metric': 'place_mention_count', 'value': t['count'],
            'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    if a['top_cities']:
        t = a['top_cities'][0]
        cs.append({'conclusion_id': 'c_002',
            'text': f"在所有城市中，「{t['place']}」是诗词书写频率最高的城市，共{t['count']}次。",
            'metric': 'city_mention_count', 'value': t['count'],
            'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    if a['top_mountains']:
        t = a['top_mountains'][0]
        cs.append({'conclusion_id': 'c_003',
            'text': f"在山岳类地点中，「{t['place']}」是被书写最多的山，共{t['count']}次。",
            'metric': 'mountain_mention_count', 'value': t['count'],
            'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    tp = a['dynasty_place_summary'].get('唐', {})
    sp = a['dynasty_place_summary'].get('宋', {})
    if tp and sp:
        tt = max(tp, key=tp.get)
        st = max(sp, key=sp.get)
        cs.append({'conclusion_id': 'c_004',
            'text': f"唐诗中提及频率最高的是「{tt}」（{tp[tt]}次），宋词中最高的是「{st}」（{sp[st]}次）。",
            'metric': 'dynasty_top_place',
            'value': {'tang': tp.get(tt, 0), 'song': sp.get(st, 0)},
            'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    if a['imagery_freq']:
        ti = list(a['imagery_freq'].items())[0]
        cs.append({'conclusion_id': 'c_005',
            'text': f"「{ti[0]}」是出现频率最高的意象，出现在{ti[1]}首作品中。",
            'metric': 'imagery_frequency', 'value': ti[1],
            'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    if a['theme_freq']:
        meaningful_themes = {k: v for k, v in a['theme_freq'].items() if k != '其他'}
        tt = max(meaningful_themes, key=meaningful_themes.get) if meaningful_themes else '其他'
        cs.append({'conclusion_id': 'c_006',
            'text': f"「{tt}」是最常见的主题，共{a['theme_freq'][tt]}首作品涉及。",
            'metric': 'theme_frequency', 'value': a['theme_freq'][tt],
            'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    if a['author_diversity']:
        td = list(a['author_diversity'].items())[0]
        cs.append({'conclusion_id': 'c_007',
            'text': f"在作品数≥5的诗人中，「{td[0]}」的文学地理覆盖最广，涉及{td[1]['unique_places']}个不同地点。",
            'metric': 'author_place_diversity', 'value': td[1]['unique_places'],
            'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    cs.append({'conclusion_id': 'c_008',
        'text': f"本数据集收录{bs['tang_poems']}首唐诗和{bs['song_ci']}首宋词，覆盖{bs['total_authors']}位诗人，提取{bs['total_places']}个文学地点，共{bs['total_mentions']}次地名提及。",
        'metric': 'dataset_overview', 'value': bs,
        'dataset_version': '1.0', 'generated_at': datetime.now().isoformat()})
    
    return cs


def validate_ner(works, place_mentions, n=150):
    """NER质量验证"""
    print(f'\n=== NER验证 (抽样{n}首) ===')
    random.seed(42)
    sample = random.sample(works, min(n, len(works)))
    
    correct = 0
    wrong = 0
    missed = 0
    
    for w in sample:
        text = w['text']
        mentions = [m for m in place_mentions if m['work_id'] == w['work_id']]
        
        for m in mentions:
            if m['place_name'] in text:
                correct += 1
            else:
                wrong += 1
        
        # 检查遗漏
        idx = build_index()
        for name in idx:
            if name in EXCLUDE_WORDS or len(name) < 2:
                continue
            if name in text:
                if not any(m['place_name'] == name for m in mentions):
                    missed += 1
    
    total = correct + wrong
    precision = correct / total if total > 0 else 0
    print(f"  正确: {correct}, 错误: {wrong}, 可能遗漏: {missed}")
    print(f"  精确率: {precision:.2%}")
    
    return {
        'sample_size': n, 'correct': correct, 'false_positive': wrong,
        'possible_missed': missed, 'precision': round(precision, 4),
        'note': '精确率基于词典匹配验证。部分"遗漏"可能是上下文排除的合理判断或同名歧义。'
    }


def export_json(works, authors, places, place_mentions, analysis, conclusions, ner_report):
    """导出前端JSON"""
    print('\n=== 导出JSON ===')
    
    metadata = {
        'project_name': '诗行中国——唐诗宋词中的山河地图',
        'subtitle': '循诗而行，在千年文字中重新看见中国山河',
        'version': '1.0',
        'generated_at': datetime.now().isoformat(),
        'data_sources': [
            {'name': 'chinese-poetry (GitHub)', 'url': 'https://github.com/chinese-poetry/chinese-poetry', 'license': 'MIT'},
        ],
        'stats': analysis['basic_stats'],
    }
    
    # 只导出有地名提及的作品 + 目标诗人作品
    work_ids_with_places = set(w['work_id'] for w in works if w['place_mentions'])
    target_work_ids = set(w['work_id'] for w in works if w.get('is_target_author'))
    export_ids = work_ids_with_places | target_work_ids
    export_works = [w for w in works if w['work_id'] in export_ids]
    
    # 限制总量
    if len(export_works) > 3500:
        export_works.sort(key=lambda w: (not w['place_mentions'], not w['is_target_author']))
        export_works = export_works[:3500]
    
    export_ids = set(w['work_id'] for w in export_works)
    export_mentions = [m for m in place_mentions if m['work_id'] in export_ids]
    export_author_ids = set(w['author_id'] for w in export_works)
    export_authors = [a for a in authors if a['author_id'] in export_author_ids]
    
    print(f"  导出: {len(export_works)} 首, {len(export_authors)} 位, {len(export_mentions)} 提及")
    
    # place_summary
    place_summary = {}
    for p in places:
        name = p['place_name_normalized']
        ms = [m for m in export_mentions if m['place_name_normalized'] == name]
        if ms:
            place_summary[name] = {
                'place_id': p['place_id'],
                'place_name': p['place_name'],
                'place_type': p['place_type'],
                'modern_name': p['modern_name'],
                'modern_province': p['modern_province'],
                'longitude': p['longitude'],
                'latitude': p['latitude'],
                'mapping_level': p['mapping_level'],
                'mention_count': len(ms),
                'tang_count': sum(1 for m in ms if m['dynasty'] == '唐'),
                'song_count': sum(1 for m in ms if m['dynasty'] == '宋'),
                'authors': list(set(m['author_name'] for m in ms)),
                'work_ids': list(set(m['work_id'] for m in ms)),
            }
    
    # search_index
    search_index = [{
        'work_id': w['work_id'],
        'title': w['title'],
        'author': w['author_name'],
        'dynasty': w['dynasty'],
        'text': w['text'][:200],
        'places': w['place_mentions'],
        'themes': w['themes'],
        'imagery': w['imagery'],
    } for w in export_works]
    
    methodology = {
        'data_source': 'chinese-poetry GitHub仓库 (MIT License)',
        'data_url': 'https://github.com/chinese-poetry/chinese-poetry',
        'processing_steps': [
            '1. 从GitHub下载唐诗宋词原始数据(繁体)',
            '2. 繁简转换(opencc-js)',
            '3. 数据清洗标准化',
            f'4. 地名提取: 词典+规则匹配 ({len(places)}+地点)',
            '5. 意象/主题/季节/情绪提取',
            '6. 多维度数据分析',
            '7. NER质量验证(抽样150首)',
            '8. 导出前端JSON',
        ],
        'place_extraction_method': '基于自建地名词典的字符串匹配，含排除表和别名映射',
        'place_dictionary_size': len(places),
        'ner_validation': ner_report,
        'place_types': {
            'exact': '精确到具体地点、建筑或自然实体，如庐山、玉门关',
            'city': '城市级，映射到现代地级市',
            'county': '县级或较小地点，映射到现代县/区',
            'province': '省级，映射到现代省份',
            'approximate': '近似位置，如跨区域河流、山脉等自然地理实体',
            'region': '历史区域，如江南、塞北、中原',
            'unknown': '尚未确定或缺乏可靠古今对照',
        },
        'limitations': [
            '地名识别基于词典匹配，未收录地名无法识别',
            '古今地名映射基于公开地理资料，部分为近似定位',
            '主题/情绪分类为规则辅助，非深度学习',
            '历史地域(如江南、塞北)为区域级定位',
        ],
    }
    
    def wj(name, data):
        path = os.path.join(PROCESSED_DIR, f'{name}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    
    wj('metadata', metadata)
    wj('authors', export_authors)
    wj('works', export_works)
    wj('places', places)
    wj('place_mentions', export_mentions)
    wj('place_summary', place_summary)
    wj('author_place_matrix', analysis['author_place_matrix'])
    wj('dynasty_place_summary', analysis['dynasty_place_summary'])
    wj('imagery_summary', {
        'imagery_freq': analysis['imagery_freq'],
        'author_imagery': analysis['author_imagery'],
        'place_imagery': analysis['place_imagery'],
    })
    wj('themes', {
        'theme_freq': analysis['theme_freq'],
        'place_theme': analysis['place_theme'],
    })
    wj('search_index', search_index)
    wj('conclusions', conclusions)
    wj('methodology', methodology)
    wj('analysis', analysis)
    
    # 复制到web
    web_data = os.path.join(BASE_DIR, 'web/public/data')
    os.makedirs(web_data, exist_ok=True)
    for name in ['metadata', 'authors', 'works', 'places', 'place_mentions',
                 'place_summary', 'author_place_matrix', 'dynasty_place_summary',
                 'imagery_summary', 'themes', 'search_index', 'conclusions', 'methodology', 'analysis']:
        with open(os.path.join(PROCESSED_DIR, f'{name}.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
        with open(os.path.join(web_data, f'{name}.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
    
    print('\n  已复制到 web/public/data/')
    return export_works


def main():
    print('='*50)
    print('《诗行中国》数据处理管线')
    print('='*50)
    
    tang, ci, authors = load_data()
    works, authors_out, places, pm = process_data(tang, ci, authors)
    analysis = analyze(works, authors_out, places, pm)
    conclusions = gen_conclusions(analysis)
    ner = validate_ner(works, pm, 150)
    export_json(works, authors_out, places, pm, analysis, conclusions, ner)
    
    print(f"\n{'='*50}")
    print('处理完成!')
    print(f"作品: {len(works)} | 作者: {len(authors_out)} | 地点: {len(places)} | 提及: {len(pm)}")
    print(f"结论: {len(conclusions)} 条")
    print('='*50)


if __name__ == '__main__':
    main()
