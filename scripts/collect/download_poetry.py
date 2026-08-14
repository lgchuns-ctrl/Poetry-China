#!/usr/bin/env python3
"""
数据采集脚本 - 从 chinese-poetry GitHub 仓库下载唐诗宋词数据
数据源: https://github.com/chinese-poetry/chinese-poetry
许可证: MIT License
"""

import urllib.request
import urllib.parse
import json
import ssl
import os
import time
import hashlib

# SSL context for HTTPS
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

BASE_URL = 'https://raw.githubusercontent.com/chinese-poetry/chinese-poetry/master/'
RAW_DIR = os.path.join(os.path.dirname(__file__), '../../data/raw')

# 目标诗人 - 我们要重点覆盖的诗人
TARGET_TANG_POETS = {
    '李白', '杜甫', '王維', '白居易', '孟浩然', '杜牧', '李商隱',
    '王昌齡', '高適', '岑參', '劉禹錫', '韓愈', '柳宗元', '韋應物',
    '賈島', '李賀', '溫庭筠', '元稹', '張九齡', '陳子昂', '宋之問',
    '駱賓王', '盧照鄰', '楊炯', '沈佺期', '崔顥', '王之渙', '儲光羲',
    '常建', '張繼', '韓翃', '韋莊', '杜審言', '李頎', '張籍', '王勃',
    '許渾', '馬戴', '姚合', '方干', '秦韜玉', '金昌緒',
    # 繁体变体
    '李白', '杜甫', '王維', '白居易', '孟浩然', '杜牧', '李商隱',
}

TARGET_SONG_CI_AUTHORS = {
    '蘇軾', '辛棄疾', '李清照', '柳永', '陸游', '歐陽修',
    '晏殊', '晏幾道', '周邦彥', '姜夔', '秦觀', '黃庭堅',
    '王安石', '賀鑄', '張先', '範仲淹', '張孝祥', '陳亮',
    '劉克莊', '吳文英', '張炎', '王沂孫', '周密', '陳與義',
    '朱敦儒', '葉夢得', '向子諲', '韓元吉',
}


def download_json(url, retries=3):
    """下载JSON数据"""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resp = urllib.request.urlopen(req, context=ctx, timeout=60)
            return json.loads(resp.read())
        except Exception as e:
            if attempt < retries - 1:
                print(f'  Retry {attempt+1}/{retries}... ({e})')
                time.sleep(2)
            else:
                raise


def download_tang_poetry(max_files=15):
    """下载唐诗数据"""
    print('=== 下载唐诗数据 ===')
    all_poems = []
    for i in range(0, max_files * 1000, 1000):
        filename = f'poet.tang.{i}.json'
        path = urllib.parse.quote(f'全唐诗/{filename}')
        url = BASE_URL + path
        print(f'  下载 {filename}...', end=' ')
        try:
            data = download_json(url)
            all_poems.extend(data)
            print(f'OK ({len(data)} 首)')
        except Exception as e:
            print(f'FAIL: {e}')
            break
        time.sleep(0.3)
    
    print(f'唐诗总计: {len(all_poems)} 首')
    return all_poems


def download_song_ci(max_files=6):
    """下载宋词数据"""
    print('\n=== 下载宋词数据 ===')
    all_ci = []
    for i in range(0, max_files * 1000, 1000):
        filename = f'ci.song.{i}.json'
        path = urllib.parse.quote(f'宋词/{filename}')
        url = BASE_URL + path
        print(f'  下载 {filename}...', end=' ')
        try:
            data = download_json(url)
            all_ci.extend(data)
            print(f'OK ({len(data)} 首)')
        except Exception as e:
            print(f'FAIL: {e}')
            break
        time.sleep(0.3)
    
    print(f'宋词总计: {len(all_ci)} 首')
    return all_ci


def download_authors():
    """下载作者信息"""
    print('\n=== 下载作者数据 ===')
    authors = {}
    
    # 唐诗作者
    path = urllib.parse.quote('全唐诗/authors.tang.json')
    url = BASE_URL + path
    print('  下载唐诗作者...', end=' ')
    try:
        data = download_json(url)
        for a in data:
            authors[a['name']] = {
                'name': a['name'],
                'desc': a.get('desc', ''),
                'id': a.get('id', ''),
                'dynasty': '唐'
            }
        print(f'OK ({len(data)} 位)')
    except Exception as e:
        print(f'FAIL: {e}')
    
    time.sleep(0.5)
    
    # 宋词作者
    path = urllib.parse.quote('宋词/author.song.json')
    url = BASE_URL + path
    print('  下载宋词作者...', end=' ')
    try:
        data = download_json(url)
        for a in data:
            name = a.get('name', '')
            if name and name not in authors:
                authors[name] = {
                    'name': name,
                    'desc': a.get('desc', ''),
                    'id': a.get('id', ''),
                    'dynasty': '宋'
                }
        print(f'OK ({len(data)} 位)')
    except Exception as e:
        print(f'FAIL: {e}')
    
    print(f'作者总计: {len(authors)} 位')
    return authors


def save_raw_data(tang_poems, song_ci, authors):
    """保存原始数据"""
    os.makedirs(RAW_DIR, exist_ok=True)
    
    # 保存唐诗
    with open(os.path.join(RAW_DIR, 'tang_poetry_raw.json'), 'w', encoding='utf-8') as f:
        json.dump(tang_poems, f, ensure_ascii=False, indent=2)
    print(f'\n保存唐诗原始数据: {len(tang_poems)} 首')
    
    # 保存宋词
    with open(os.path.join(RAW_DIR, 'song_ci_raw.json'), 'w', encoding='utf-8') as f:
        json.dump(song_ci, f, ensure_ascii=False, indent=2)
    print(f'保存宋词原始数据: {len(song_ci)} 首')
    
    # 保存作者
    with open(os.path.join(RAW_DIR, 'authors_raw.json'), 'w', encoding='utf-8') as f:
        json.dump(list(authors.values()), f, ensure_ascii=False, indent=2)
    print(f'保存作者原始数据: {len(authors)} 位')
    
    # 保存数据源记录
    sources = [
        {
            'source_id': 'src_001',
            'source_title': 'chinese-poetry GitHub 仓库 - 全唐诗',
            'source_url': 'https://github.com/chinese-poetry/chinese-poetry/tree/master/全唐诗',
            'publisher': 'JackeyGao / chinese-poetry',
            'source_type': 'GitHub公开数据集',
            'license': 'MIT License',
            'accessed_at': '2026-08-07',
            'notes': '清康熙四十四年彭定求等编校《全唐诗》，约55000首唐诗。数据以JSON格式分发，繁体存储。'
        },
        {
            'source_id': 'src_002',
            'source_title': 'chinese-poetry GitHub 仓库 - 宋词',
            'source_url': 'https://github.com/chinese-poetry/chinese-poetry/tree/master/宋词',
            'publisher': 'JackeyGao / chinese-poetry',
            'source_type': 'GitHub公开数据集',
            'license': 'MIT License',
            'accessed_at': '2026-08-07',
            'notes': '两宋时期1564位词人，21050首词。数据以JSON格式分发，繁体存储。'
        },
        {
            'source_id': 'src_003',
            'source_title': 'chinese-poetry GitHub 仓库 - 作者信息',
            'source_url': 'https://github.com/chinese-poetry/chinese-poetry/blob/master/全唐诗/authors.tang.json',
            'publisher': 'JackeyGao / chinese-poetry',
            'source_type': 'GitHub公开数据集',
            'license': 'MIT License',
            'accessed_at': '2026-08-07',
            'notes': '唐诗作者3675位，宋词作者约1500位。含作者简介（繁体）。'
        }
    ]
    with open(os.path.join(RAW_DIR, 'sources.json'), 'w', encoding='utf-8') as f:
        json.dump(sources, f, ensure_ascii=False, indent=2)


def main():
    print('========================================')
    print('《诗行中国》数据采集')
    print('========================================\n')
    
    # 下载数据
    tang_poems = download_tang_poetry(max_files=15)
    song_ci = download_song_ci(max_files=6)
    authors = download_authors()
    
    # 保存
    save_raw_data(tang_poems, song_ci, authors)
    
    # 统计
    print(f'\n=== 采集完成 ===')
    print(f'唐诗: {len(tang_poems)} 首')
    print(f'宋词: {len(song_ci)} 首')
    print(f'作者: {len(authors)} 位')
    
    # 检查目标诗人覆盖情况
    print(f'\n=== 目标诗人覆盖情况 ===')
    tang_authors_set = set(a for a in authors.values() if a['dynasty'] == '唐')
    
    # 统计各诗人作品数
    poet_counts = {}
    for poem in tang_poems:
        author = poem.get('author', '')
        poet_counts[author] = poet_counts.get(author, 0) + 1
    
    target_simplified = ['李白', '杜甫', '王维', '白居易', '孟浩然', '杜牧', '李商隐',
                         '王昌龄', '高适', '岑参', '刘禹锡', '韩愈', '柳宗元',
                         '贾岛', '李贺', '温庭筠', '元稹', '张九龄', '陈子昂']
    target_traditional = ['李白', '杜甫', '王維', '白居易', '孟浩然', '杜牧', '李商隱',
                          '王昌齡', '高適', '岑參', '劉禹錫', '韓愈', '柳宗元',
                          '賈島', '李賀', '溫庭筠', '元稹', '張九齡', '陳子昂']
    
    for t_name, s_name in zip(target_traditional, target_simplified):
        count = poet_counts.get(t_name, poet_counts.get(s_name, 0))
        print(f'  {s_name}: {count} 首')
    
    # 宋词作者统计
    ci_author_counts = {}
    for ci in song_ci:
        author = ci.get('author', '')
        ci_author_counts[author] = ci_author_counts.get(author, 0) + 1
    
    ci_targets = ['蘇軾', '辛棄疾', '李清照', '柳永', '陸游', '歐陽修',
                  '晏殊', '周邦彥', '姜夔', '秦觀', '黃庭堅', '王安石']
    ci_targets_s = ['苏轼', '辛弃疾', '李清照', '柳永', '陆游', '欧阳修',
                     '晏殊', '周邦彦', '姜夔', '秦观', '黄庭坚', '王安石']
    
    for t_name, s_name in zip(ci_targets, ci_targets_s):
        count = ci_author_counts.get(t_name, 0)
        print(f'  {s_name}: {count} 阕')


if __name__ == '__main__':
    main()
