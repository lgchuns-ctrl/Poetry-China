#!/usr/bin/env python3
"""
唐宋诗词地名词典 - 古今地名映射数据库
包含城市、山川、河流、湖泊、关隘、古迹、历史地域
经纬度来源: 公开地理数据，基于现代行政区划

字段说明:
  place_name: 诗词中出现的地名
  place_name_normalized: 标准化名称
  place_type: city/mountain/river/lake/pass/building/historic_region/other
  historical_name: 历史地名
  modern_name: 现代名称
  modern_province: 现代省份
  modern_city: 现代城市
  longitude: 经度
  latitude: 纬度
  mapping_level: exact/county/city/province/approximate/region
  mapping_source: 映射来源
  aliases: 别名/曾用名列表
"""

# 地名词典
PLACE_DICTIONARY = [
    # ========== 城市 ==========
    {"place_name": "长安", "place_name_normalized": "长安", "place_type": "city",
     "historical_name": "长安", "modern_name": "西安", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.94, "latitude": 34.27, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["镐京", "大兴城", "京兆"]},
    
    {"place_name": "洛阳", "place_name_normalized": "洛阳", "place_type": "city",
     "historical_name": "洛阳", "modern_name": "洛阳", "modern_province": "河南", "modern_city": "洛阳",
     "longitude": 112.45, "latitude": 34.62, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["洛城", "东都", "神都", "洛京"]},
    
    {"place_name": "扬州", "place_name_normalized": "扬州", "place_type": "city",
     "historical_name": "扬州", "modern_name": "扬州", "modern_province": "江苏", "modern_city": "扬州",
     "longitude": 119.42, "latitude": 32.39, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["广陵", "江都", "维扬"]},
    
    {"place_name": "姑苏", "place_name_normalized": "苏州", "place_type": "city",
     "historical_name": "姑苏", "modern_name": "苏州", "modern_province": "江苏", "modern_city": "苏州",
     "longitude": 120.62, "latitude": 31.30, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["苏州", "吴门", "平江"]},
    
    {"place_name": "苏州", "place_name_normalized": "苏州", "place_type": "city",
     "historical_name": "苏州", "modern_name": "苏州", "modern_province": "江苏", "modern_city": "苏州",
     "longitude": 120.62, "latitude": 31.30, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "杭州", "place_name_normalized": "杭州", "place_type": "city",
     "historical_name": "杭州", "modern_name": "杭州", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 120.16, "latitude": 30.27, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "临安", "place_name_normalized": "杭州", "place_type": "city",
     "historical_name": "临安", "modern_name": "杭州", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 120.16, "latitude": 30.27, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["钱塘", "武林", "余杭"]},
    
    {"place_name": "钱塘", "place_name_normalized": "杭州", "place_type": "city",
     "historical_name": "钱塘", "modern_name": "杭州", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 120.16, "latitude": 30.27, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "开封", "place_name_normalized": "开封", "place_type": "city",
     "historical_name": "开封", "modern_name": "开封", "modern_province": "河南", "modern_city": "开封",
     "longitude": 114.31, "latitude": 34.80, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "汴京", "place_name_normalized": "开封", "place_type": "city",
     "historical_name": "汴京", "modern_name": "开封", "modern_province": "河南", "modern_city": "开封",
     "longitude": 114.31, "latitude": 34.80, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["汴梁", "东京", "大梁", "浚仪"]},
    
    {"place_name": "汴梁", "place_name_normalized": "开封", "place_type": "city",
     "historical_name": "汴梁", "modern_name": "开封", "modern_province": "河南", "modern_city": "开封",
     "longitude": 114.31, "latitude": 34.80, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "东京", "place_name_normalized": "开封", "place_type": "city",
     "historical_name": "东京", "modern_name": "开封", "modern_province": "河南", "modern_city": "开封",
     "longitude": 114.31, "latitude": 34.80, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "成都", "place_name_normalized": "成都", "place_type": "city",
     "historical_name": "成都", "modern_name": "成都", "modern_province": "四川", "modern_city": "成都",
     "longitude": 104.07, "latitude": 30.67, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["锦官城", "锦城", "蓉城"]},
    
    {"place_name": "锦官城", "place_name_normalized": "成都", "place_type": "city",
     "historical_name": "锦官城", "modern_name": "成都", "modern_province": "四川", "modern_city": "成都",
     "longitude": 104.07, "latitude": 30.67, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "金陵", "place_name_normalized": "南京", "place_type": "city",
     "historical_name": "金陵", "modern_name": "南京", "modern_province": "江苏", "modern_city": "南京",
     "longitude": 118.80, "latitude": 32.06, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["建康", "石头城", "江宁", "应天"]},
    
    {"place_name": "建康", "place_name_normalized": "南京", "place_type": "city",
     "historical_name": "建康", "modern_name": "南京", "modern_province": "江苏", "modern_city": "南京",
     "longitude": 118.80, "latitude": 32.06, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "南京", "place_name_normalized": "南京", "place_type": "city",
     "historical_name": "南京", "modern_name": "南京", "modern_province": "江苏", "modern_city": "南京",
     "longitude": 118.80, "latitude": 32.06, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "江夏", "place_name_normalized": "武汉", "place_type": "city",
     "historical_name": "江夏", "modern_name": "武汉", "modern_province": "湖北", "modern_city": "武汉",
     "longitude": 114.31, "latitude": 30.59, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["夏口", "武昌", "汉口", "汉阳"]},
    
    {"place_name": "武昌", "place_name_normalized": "武汉", "place_type": "city",
     "historical_name": "武昌", "modern_name": "武汉", "modern_province": "湖北", "modern_city": "武汉",
     "longitude": 114.31, "latitude": 30.59, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "长沙", "place_name_normalized": "长沙", "place_type": "city",
     "historical_name": "长沙", "modern_name": "长沙", "modern_province": "湖南", "modern_city": "长沙",
     "longitude": 112.94, "latitude": 28.23, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["潭州"]},
    
    {"place_name": "襄阳", "place_name_normalized": "襄阳", "place_type": "city",
     "historical_name": "襄阳", "modern_name": "襄阳", "modern_province": "湖北", "modern_city": "襄阳",
     "longitude": 112.14, "latitude": 32.04, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["襄州"]},
    
    {"place_name": "荆州", "place_name_normalized": "荆州", "place_type": "city",
     "historical_name": "荆州", "modern_name": "荆州", "modern_province": "湖北", "modern_city": "荆州",
     "longitude": 112.24, "latitude": 30.33, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["江陵", "郢都"]},
    
    {"place_name": "江陵", "place_name_normalized": "荆州", "place_type": "city",
     "historical_name": "江陵", "modern_name": "荆州", "modern_province": "湖北", "modern_city": "荆州",
     "longitude": 112.24, "latitude": 30.33, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "夔州", "place_name_normalized": "奉节", "place_type": "city",
     "historical_name": "夔州", "modern_name": "奉节", "modern_province": "重庆", "modern_city": "奉节",
     "longitude": 109.46, "latitude": 31.05, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": ["奉节", "白帝城"]},
    
    {"place_name": "白帝城", "place_name_normalized": "奉节", "place_type": "building",
     "historical_name": "白帝城", "modern_name": "奉节", "modern_province": "重庆", "modern_city": "奉节",
     "longitude": 109.57, "latitude": 31.05, "mapping_level": "exact",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "九江", "place_name_normalized": "九江", "place_type": "city",
     "historical_name": "九江", "modern_name": "九江", "modern_province": "江西", "modern_city": "九江",
     "longitude": 115.99, "latitude": 29.72, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["浔阳", "江州", "柴桑"]},
    
    {"place_name": "浔阳", "place_name_normalized": "九江", "place_type": "city",
     "historical_name": "浔阳", "modern_name": "九江", "modern_province": "江西", "modern_city": "九江",
     "longitude": 115.99, "latitude": 29.72, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "泉州", "place_name_normalized": "泉州", "place_type": "city",
     "historical_name": "泉州", "modern_name": "泉州", "modern_province": "福建", "modern_city": "泉州",
     "longitude": 118.67, "latitude": 24.87, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["刺桐"]},
    
    {"place_name": "福州", "place_name_normalized": "福州", "place_type": "city",
     "historical_name": "福州", "modern_name": "福州", "modern_province": "福建", "modern_city": "福州",
     "longitude": 119.30, "latitude": 26.08, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["榕城", "三山"]},
    
    {"place_name": "广州", "place_name_normalized": "广州", "place_type": "city",
     "historical_name": "广州", "modern_name": "广州", "modern_province": "广东", "modern_city": "广州",
     "longitude": 113.27, "latitude": 23.13, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["番禺", "羊城", "穗城"]},
    
    {"place_name": "桂林", "place_name_normalized": "桂林", "place_type": "city",
     "historical_name": "桂林", "modern_name": "桂林", "modern_province": "广西", "modern_city": "桂林",
     "longitude": 110.30, "latitude": 25.27, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "徐州", "place_name_normalized": "徐州", "place_type": "city",
     "historical_name": "徐州", "modern_name": "徐州", "modern_province": "江苏", "modern_city": "徐州",
     "longitude": 117.19, "latitude": 34.26, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["彭城"]},
    
    {"place_name": "彭城", "place_name_normalized": "徐州", "place_type": "city",
     "historical_name": "彭城", "modern_name": "徐州", "modern_province": "江苏", "modern_city": "徐州",
     "longitude": 117.19, "latitude": 34.26, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "咸阳", "place_name_normalized": "咸阳", "place_type": "city",
     "historical_name": "咸阳", "modern_name": "咸阳", "modern_province": "陕西", "modern_city": "咸阳",
     "longitude": 108.72, "latitude": 34.33, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "汉中", "place_name_normalized": "汉中", "place_type": "city",
     "historical_name": "汉中", "modern_name": "汉中", "modern_province": "陕西", "modern_city": "汉中",
     "longitude": 107.03, "latitude": 33.07, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["南郑"]},
    
    {"place_name": "敦煌", "place_name_normalized": "敦煌", "place_type": "city",
     "historical_name": "敦煌", "modern_name": "敦煌", "modern_province": "甘肃", "modern_city": "敦煌",
     "longitude": 94.66, "latitude": 40.14, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": ["沙州"]},
    
    {"place_name": "凉州", "place_name_normalized": "武威", "place_type": "city",
     "historical_name": "凉州", "modern_name": "武威", "modern_province": "甘肃", "modern_city": "武威",
     "longitude": 102.64, "latitude": 37.93, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["武威"]},
    
    {"place_name": "甘州", "place_name_normalized": "张掖", "place_type": "city",
     "historical_name": "甘州", "modern_name": "张掖", "modern_province": "甘肃", "modern_city": "张掖",
     "longitude": 100.43, "latitude": 38.93, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["张掖"]},
    
    {"place_name": "兰州", "place_name_normalized": "兰州", "place_type": "city",
     "historical_name": "兰州", "modern_name": "兰州", "modern_province": "甘肃", "modern_city": "兰州",
     "longitude": 103.83, "latitude": 36.06, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["金城"]},
    
    {"place_name": "天水", "place_name_normalized": "天水", "place_type": "city",
     "historical_name": "天水", "modern_name": "天水", "modern_province": "甘肃", "modern_city": "天水",
     "longitude": 105.72, "latitude": 34.58, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["秦州"]},
    
    {"place_name": "太原", "place_name_normalized": "太原", "place_type": "city",
     "historical_name": "太原", "modern_name": "太原", "modern_province": "山西", "modern_city": "太原",
     "longitude": 112.55, "latitude": 37.87, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["并州", "晋阳"]},
    
    {"place_name": "并州", "place_name_normalized": "太原", "place_type": "city",
     "historical_name": "并州", "modern_name": "太原", "modern_province": "山西", "modern_city": "太原",
     "longitude": 112.55, "latitude": 37.87, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "幽州", "place_name_normalized": "北京", "place_type": "city",
     "historical_name": "幽州", "modern_name": "北京", "modern_province": "北京", "modern_city": "北京",
     "longitude": 116.41, "latitude": 39.90, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["蓟", "范阳"]},
    
    {"place_name": "安陆", "place_name_normalized": "安陆", "place_type": "city",
     "historical_name": "安陆", "modern_name": "安陆", "modern_province": "湖北", "modern_city": "安陆",
     "longitude": 113.70, "latitude": 31.26, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "越州", "place_name_normalized": "绍兴", "place_type": "city",
     "historical_name": "越州", "modern_name": "绍兴", "modern_province": "浙江", "modern_city": "绍兴",
     "longitude": 120.58, "latitude": 30.03, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["会稽", "山阴", "绍兴"]},
    
    {"place_name": "会稽", "place_name_normalized": "绍兴", "place_type": "city",
     "historical_name": "会稽", "modern_name": "绍兴", "modern_province": "浙江", "modern_city": "绍兴",
     "longitude": 120.58, "latitude": 30.03, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "宣州", "place_name_normalized": "宣城", "place_type": "city",
     "historical_name": "宣州", "modern_name": "宣城", "modern_province": "安徽", "modern_city": "宣城",
     "longitude": 118.76, "latitude": 30.95, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["宣城"]},
    
    {"place_name": "池州", "place_name_normalized": "池州", "place_type": "city",
     "historical_name": "池州", "modern_name": "池州", "modern_province": "安徽", "modern_city": "池州",
     "longitude": 117.49, "latitude": 30.66, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "当涂", "place_name_normalized": "当涂", "place_type": "city",
     "historical_name": "当涂", "modern_name": "当涂", "modern_province": "安徽", "modern_city": "马鞍山",
     "longitude": 118.49, "latitude": 31.55, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "南昌", "place_name_normalized": "南昌", "place_type": "city",
     "historical_name": "南昌", "modern_name": "南昌", "modern_province": "江西", "modern_city": "南昌",
     "longitude": 115.86, "latitude": 28.68, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["洪州", "豫章"]},
    
    {"place_name": "洪州", "place_name_normalized": "南昌", "place_type": "city",
     "historical_name": "洪州", "modern_name": "南昌", "modern_province": "江西", "modern_city": "南昌",
     "longitude": 115.86, "latitude": 28.68, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "豫章", "place_name_normalized": "南昌", "place_type": "city",
     "historical_name": "豫章", "modern_name": "南昌", "modern_province": "江西", "modern_city": "南昌",
     "longitude": 115.86, "latitude": 28.68, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "阆中", "place_name_normalized": "阆中", "place_type": "city",
     "historical_name": "阆中", "modern_name": "阆中", "modern_province": "四川", "modern_city": "南充",
     "longitude": 105.94, "latitude": 31.55, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "蓬莱", "place_name_normalized": "蓬莱", "place_type": "city",
     "historical_name": "蓬莱", "modern_name": "蓬莱", "modern_province": "山东", "modern_city": "烟台",
     "longitude": 120.75, "latitude": 37.81, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": ["登州"]},
    
    {"place_name": "登州", "place_name_normalized": "蓬莱", "place_type": "city",
     "historical_name": "登州", "modern_name": "蓬莱", "modern_province": "山东", "modern_city": "烟台",
     "longitude": 120.75, "latitude": 37.81, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "镇江", "place_name_normalized": "镇江", "place_type": "city",
     "historical_name": "镇江", "modern_name": "镇江", "modern_province": "江苏", "modern_city": "镇江",
     "longitude": 119.42, "latitude": 32.20, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["京口", "润州", "丹徒"]},
    
    {"place_name": "京口", "place_name_normalized": "镇江", "place_type": "city",
     "historical_name": "京口", "modern_name": "镇江", "modern_province": "江苏", "modern_city": "镇江",
     "longitude": 119.42, "latitude": 32.20, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "常州", "place_name_normalized": "常州", "place_type": "city",
     "historical_name": "常州", "modern_name": "常州", "modern_province": "江苏", "modern_city": "常州",
     "longitude": 119.95, "latitude": 31.77, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": ["毗陵", "兰陵"]},
    
    {"place_name": "无锡", "place_name_normalized": "无锡", "place_type": "city",
     "historical_name": "无锡", "modern_name": "无锡", "modern_province": "江苏", "modern_city": "无锡",
     "longitude": 120.30, "latitude": 31.57, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "池州", "place_name_normalized": "池州", "place_type": "city",
     "historical_name": "池州", "modern_name": "池州", "modern_province": "安徽", "modern_city": "池州",
     "longitude": 117.49, "latitude": 30.66, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "滁州", "place_name_normalized": "滁州", "place_type": "city",
     "historical_name": "滁州", "modern_name": "滁州", "modern_province": "安徽", "modern_city": "滁州",
     "longitude": 118.32, "latitude": 32.30, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "合州", "place_name_normalized": "合川", "place_type": "city",
     "historical_name": "合州", "modern_name": "合川", "modern_province": "重庆", "modern_city": "重庆",
     "longitude": 106.28, "latitude": 29.98, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "忠州", "place_name_normalized": "忠县", "place_type": "city",
     "historical_name": "忠州", "modern_name": "忠县", "modern_province": "重庆", "modern_city": "重庆",
     "longitude": 108.04, "latitude": 30.30, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "万州", "place_name_normalized": "万州", "place_type": "city",
     "historical_name": "万州", "modern_name": "万州", "modern_province": "重庆", "modern_city": "重庆",
     "longitude": 108.41, "latitude": 30.81, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "夔门", "place_name_normalized": "奉节", "place_type": "pass",
     "historical_name": "夔门", "modern_name": "奉节", "modern_province": "重庆", "modern_city": "奉节",
     "longitude": 109.55, "latitude": 31.04, "mapping_level": "exact",
     "mapping_source": "历史地理学通识", "aliases": ["瞿塘关"]},
    
    # ========== 山 ==========
    {"place_name": "庐山", "place_name_normalized": "庐山", "place_type": "mountain",
     "historical_name": "庐山", "modern_name": "庐山", "modern_province": "江西", "modern_city": "九江",
     "longitude": 115.99, "latitude": 29.56, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["匡庐", "南山"]},
    
    {"place_name": "匡庐", "place_name_normalized": "庐山", "place_type": "mountain",
     "historical_name": "匡庐", "modern_name": "庐山", "modern_province": "江西", "modern_city": "九江",
     "longitude": 115.99, "latitude": 29.56, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "泰山", "place_name_normalized": "泰山", "place_type": "mountain",
     "historical_name": "泰山", "modern_name": "泰山", "modern_province": "山东", "modern_city": "泰安",
     "longitude": 117.10, "latitude": 36.26, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["岱宗", "东岳", "岱岳"]},
    
    {"place_name": "岱宗", "place_name_normalized": "泰山", "place_type": "mountain",
     "historical_name": "岱宗", "modern_name": "泰山", "modern_province": "山东", "modern_city": "泰安",
     "longitude": 117.10, "latitude": 36.26, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "华山", "place_name_normalized": "华山", "place_type": "mountain",
     "historical_name": "华山", "modern_name": "华山", "modern_province": "陕西", "modern_city": "渭南",
     "longitude": 110.09, "latitude": 34.48, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["太华山", "西岳"]},
    
    {"place_name": "嵩山", "place_name_normalized": "嵩山", "place_type": "mountain",
     "historical_name": "嵩山", "modern_name": "嵩山", "modern_province": "河南", "modern_city": "郑州",
     "longitude": 113.02, "latitude": 34.51, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["中岳", "嵩岳"]},
    
    {"place_name": "衡山", "place_name_normalized": "衡山", "place_type": "mountain",
     "historical_name": "衡山", "modern_name": "衡山", "modern_province": "湖南", "modern_city": "衡阳",
     "longitude": 112.72, "latitude": 27.28, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["南岳", "岣嵝山"]},
    
    {"place_name": "恒山", "place_name_normalized": "恒山", "place_type": "mountain",
     "historical_name": "恒山", "modern_name": "恒山", "modern_province": "山西", "modern_city": "大同",
     "longitude": 113.74, "latitude": 39.68, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["北岳"]},
    
    {"place_name": "峨眉山", "place_name_normalized": "峨眉山", "place_type": "mountain",
     "historical_name": "峨眉山", "modern_name": "峨眉山", "modern_province": "四川", "modern_city": "乐山",
     "longitude": 103.34, "latitude": 29.52, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["峨嵋", "峨眉"]},
    
    {"place_name": "峨嵋", "place_name_normalized": "峨眉山", "place_type": "mountain",
     "historical_name": "峨嵋", "modern_name": "峨眉山", "modern_province": "四川", "modern_city": "乐山",
     "longitude": 103.34, "latitude": 29.52, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "五台山", "place_name_normalized": "五台山", "place_type": "mountain",
     "historical_name": "五台山", "modern_name": "五台山", "modern_province": "山西", "modern_city": "忻州",
     "longitude": 113.59, "latitude": 39.02, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["清凉山"]},
    
    {"place_name": "九华山", "place_name_normalized": "九华山", "place_type": "mountain",
     "historical_name": "九华山", "modern_name": "九华山", "modern_province": "安徽", "modern_city": "池州",
     "longitude": 117.80, "latitude": 30.50, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "黄山", "place_name_normalized": "黄山", "place_type": "mountain",
     "historical_name": "黄山", "modern_name": "黄山", "modern_province": "安徽", "modern_city": "黄山",
     "longitude": 118.16, "latitude": 30.13, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["黄岳"]},
    
    {"place_name": "终南山", "place_name_normalized": "终南山", "place_type": "mountain",
     "historical_name": "终南山", "modern_name": "终南山", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.75, "latitude": 34.00, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["南山", "太乙山"]},
    
    {"place_name": "南山", "place_name_normalized": "终南山", "place_type": "mountain",
     "historical_name": "南山", "modern_name": "终南山", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.75, "latitude": 34.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "骊山", "place_name_normalized": "骊山", "place_type": "mountain",
     "historical_name": "骊山", "modern_name": "骊山", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 109.22, "latitude": 34.37, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["丽山"]},
    
    {"place_name": "天姥山", "place_name_normalized": "天姥山", "place_type": "mountain",
     "historical_name": "天姥山", "modern_name": "天姥山", "modern_province": "浙江", "modern_city": "绍兴",
     "longitude": 120.95, "latitude": 29.05, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "天台山", "place_name_normalized": "天台山", "place_type": "mountain",
     "historical_name": "天台山", "modern_name": "天台山", "modern_province": "浙江", "modern_city": "台州",
     "longitude": 121.01, "latitude": 29.25, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["天台"]},
    
    {"place_name": "武夷山", "place_name_normalized": "武夷山", "place_type": "mountain",
     "historical_name": "武夷山", "modern_name": "武夷山", "modern_province": "福建", "modern_city": "南平",
     "longitude": 117.94, "latitude": 27.67, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "茅山", "place_name_normalized": "茅山", "place_type": "mountain",
     "historical_name": "茅山", "modern_name": "茅山", "modern_province": "江苏", "modern_city": "镇江",
     "longitude": 119.30, "latitude": 31.80, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["句曲山"]},
    
    {"place_name": "巫山", "place_name_normalized": "巫山", "place_type": "mountain",
     "historical_name": "巫山", "modern_name": "巫山", "modern_province": "重庆", "modern_city": "重庆",
     "longitude": 109.88, "latitude": 31.08, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "赤壁", "place_name_normalized": "赤壁", "place_type": "other",
     "historical_name": "赤壁", "modern_name": "赤壁", "modern_province": "湖北", "modern_city": "赤壁",
     "longitude": 113.71, "latitude": 29.73, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": ["蒲圻"]},
    
    {"place_name": "首阳山", "place_name_normalized": "首阳山", "place_type": "mountain",
     "historical_name": "首阳山", "modern_name": "首阳山", "modern_province": "甘肃", "modern_city": "定西",
     "longitude": 104.25, "latitude": 35.48, "mapping_level": "approximate",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    # ========== 河流 ==========
    {"place_name": "黄河", "place_name_normalized": "黄河", "place_type": "river",
     "historical_name": "黄河", "modern_name": "黄河", "modern_province": "跨省", "modern_city": "",
     "longitude": 112.00, "latitude": 35.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["大河", "浊河"]},
    
    {"place_name": "长江", "place_name_normalized": "长江", "place_type": "river",
     "historical_name": "长江", "modern_name": "长江", "modern_province": "跨省", "modern_city": "",
     "longitude": 114.31, "latitude": 30.59, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["大江", "江", "扬子江"]},
    
    {"place_name": "大江", "place_name_normalized": "长江", "place_type": "river",
     "historical_name": "大江", "modern_name": "长江", "modern_province": "跨省", "modern_city": "",
     "longitude": 114.31, "latitude": 30.59, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "扬子江", "place_name_normalized": "长江", "place_type": "river",
     "historical_name": "扬子江", "modern_name": "长江", "modern_province": "跨省", "modern_city": "",
     "longitude": 119.00, "latitude": 32.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "渭水", "place_name_normalized": "渭河", "place_type": "river",
     "historical_name": "渭水", "modern_name": "渭河", "modern_province": "陕西", "modern_city": "渭南",
     "longitude": 109.50, "latitude": 34.50, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["渭河"]},
    
    {"place_name": "渭河", "place_name_normalized": "渭河", "place_type": "river",
     "historical_name": "渭河", "modern_name": "渭河", "modern_province": "陕西", "modern_city": "渭南",
     "longitude": 109.50, "latitude": 34.50, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "洛水", "place_name_normalized": "洛河", "place_type": "river",
     "historical_name": "洛水", "modern_name": "洛河", "modern_province": "河南", "modern_city": "洛阳",
     "longitude": 112.45, "latitude": 34.62, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["洛河"]},
    
    {"place_name": "汉水", "place_name_normalized": "汉江", "place_type": "river",
     "historical_name": "汉水", "modern_name": "汉江", "modern_province": "湖北", "modern_city": "武汉",
     "longitude": 112.50, "latitude": 32.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["汉江", "沔水"]},
    
    {"place_name": "汉江", "place_name_normalized": "汉江", "place_type": "river",
     "historical_name": "汉江", "modern_name": "汉江", "modern_province": "湖北", "modern_city": "武汉",
     "longitude": 112.50, "latitude": 32.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "湘水", "place_name_normalized": "湘江", "place_type": "river",
     "historical_name": "湘水", "modern_name": "湘江", "modern_province": "湖南", "modern_city": "长沙",
     "longitude": 112.94, "latitude": 28.23, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["湘江", "潇湘"]},
    
    {"place_name": "湘江", "place_name_normalized": "湘江", "place_type": "river",
     "historical_name": "湘江", "modern_name": "湘江", "modern_province": "湖南", "modern_city": "长沙",
     "longitude": 112.94, "latitude": 28.23, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "资水", "place_name_normalized": "资江", "place_type": "river",
     "historical_name": "资水", "modern_name": "资江", "modern_province": "湖南", "modern_city": "益阳",
     "longitude": 112.30, "latitude": 28.60, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["资江"]},
    
    {"place_name": "沅水", "place_name_normalized": "沅江", "place_type": "river",
     "historical_name": "沅水", "modern_name": "沅江", "modern_province": "湖南", "modern_city": "常德",
     "longitude": 111.70, "latitude": 28.90, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["沅江"]},
    
    {"place_name": "澧水", "place_name_normalized": "澧水", "place_type": "river",
     "historical_name": "澧水", "modern_name": "澧水", "modern_province": "湖南", "modern_city": "张家界",
     "longitude": 110.50, "latitude": 29.70, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "淮水", "place_name_normalized": "淮河", "place_type": "river",
     "historical_name": "淮水", "modern_name": "淮河", "modern_province": "安徽", "modern_city": "",
     "longitude": 117.00, "latitude": 32.50, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["淮河"]},
    
    {"place_name": "汴水", "place_name_normalized": "汴河", "place_type": "river",
     "historical_name": "汴水", "modern_name": "汴河", "modern_province": "河南", "modern_city": "开封",
     "longitude": 114.31, "latitude": 34.80, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["汴河", "通济渠"]},
    
    {"place_name": "嘉陵江", "place_name_normalized": "嘉陵江", "place_type": "river",
     "historical_name": "嘉陵江", "modern_name": "嘉陵江", "modern_province": "重庆", "modern_city": "重庆",
     "longitude": 106.50, "latitude": 29.50, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "锦江", "place_name_normalized": "锦江", "place_type": "river",
     "historical_name": "锦江", "modern_name": "锦江", "modern_province": "四川", "modern_city": "成都",
     "longitude": 104.07, "latitude": 30.67, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["濯锦江"]},
    
    {"place_name": "灞水", "place_name_normalized": "灞河", "place_type": "river",
     "historical_name": "灞水", "modern_name": "灞河", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 109.00, "latitude": 34.30, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["灞河", "霸水"]},
    
    {"place_name": "泾水", "place_name_normalized": "泾河", "place_type": "river",
     "historical_name": "泾水", "modern_name": "泾河", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.50, "latitude": 34.60, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["泾河"]},
    
    {"place_name": "漓江", "place_name_normalized": "漓江", "place_type": "river",
     "historical_name": "漓江", "modern_name": "漓江", "modern_province": "广西", "modern_city": "桂林",
     "longitude": 110.30, "latitude": 25.27, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["漓水"]},
    
    {"place_name": "钱塘江", "place_name_normalized": "钱塘江", "place_type": "river",
     "historical_name": "钱塘江", "modern_name": "钱塘江", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 120.16, "latitude": 30.27, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["浙江", "之江", "罗刹江"]},
    
    {"place_name": "浙江", "place_name_normalized": "钱塘江", "place_type": "river",
     "historical_name": "浙江", "modern_name": "钱塘江", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 120.16, "latitude": 30.27, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "珠江", "place_name_normalized": "珠江", "place_type": "river",
     "historical_name": "珠江", "modern_name": "珠江", "modern_province": "广东", "modern_city": "广州",
     "longitude": 113.27, "latitude": 23.13, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    # ========== 湖泊 ==========
    {"place_name": "洞庭湖", "place_name_normalized": "洞庭湖", "place_type": "lake",
     "historical_name": "洞庭湖", "modern_name": "洞庭湖", "modern_province": "湖南", "modern_city": "岳阳",
     "longitude": 112.60, "latitude": 29.33, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["洞庭", "云梦泽"]},
    
    {"place_name": "鄱阳湖", "place_name_normalized": "鄱阳湖", "place_type": "lake",
     "historical_name": "鄱阳湖", "modern_name": "鄱阳湖", "modern_province": "江西", "modern_city": "九江",
     "longitude": 116.30, "latitude": 29.02, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["彭蠡", "彭蠡湖", "彭泽"]},
    
    {"place_name": "彭蠡", "place_name_normalized": "鄱阳湖", "place_type": "lake",
     "historical_name": "彭蠡", "modern_name": "鄱阳湖", "modern_province": "江西", "modern_city": "九江",
     "longitude": 116.30, "latitude": 29.02, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "太湖", "place_name_normalized": "太湖", "place_type": "lake",
     "historical_name": "太湖", "modern_name": "太湖", "modern_province": "江苏", "modern_city": "苏州",
     "longitude": 120.09, "latitude": 31.25, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["震泽", "具区", "笠泽"]},
    
    {"place_name": "西湖", "place_name_normalized": "西湖", "place_type": "lake",
     "historical_name": "西湖", "modern_name": "西湖", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 120.15, "latitude": 30.25, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["西子湖", "西子"]},
    
    {"place_name": "镜湖", "place_name_normalized": "鉴湖", "place_type": "lake",
     "historical_name": "镜湖", "modern_name": "鉴湖", "modern_province": "浙江", "modern_city": "绍兴",
     "longitude": 120.58, "latitude": 30.03, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["鉴湖"]},
    
    {"place_name": "鉴湖", "place_name_normalized": "鉴湖", "place_type": "lake",
     "historical_name": "鉴湖", "modern_name": "鉴湖", "modern_province": "浙江", "modern_city": "绍兴",
     "longitude": 120.58, "latitude": 30.03, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "巢湖", "place_name_normalized": "巢湖", "place_type": "lake",
     "historical_name": "巢湖", "modern_name": "巢湖", "modern_province": "安徽", "modern_city": "合肥",
     "longitude": 117.50, "latitude": 31.60, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "滇池", "place_name_normalized": "滇池", "place_type": "lake",
     "historical_name": "滇池", "modern_name": "滇池", "modern_province": "云南", "modern_city": "昆明",
     "longitude": 102.72, "latitude": 24.97, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["昆明湖"]},
    
    # ========== 关隘 ==========
    {"place_name": "玉门关", "place_name_normalized": "玉门关", "place_type": "pass",
     "historical_name": "玉门关", "modern_name": "玉门关遗址", "modern_province": "甘肃", "modern_city": "敦煌",
     "longitude": 93.87, "latitude": 40.35, "mapping_level": "exact",
     "mapping_source": "考古遗址数据", "aliases": []},
    
    {"place_name": "阳关", "place_name_normalized": "阳关", "place_type": "pass",
     "historical_name": "阳关", "modern_name": "阳关遗址", "modern_province": "甘肃", "modern_city": "敦煌",
     "longitude": 92.10, "latitude": 40.00, "mapping_level": "exact",
     "mapping_source": "考古遗址数据", "aliases": []},
    
    {"place_name": "潼关", "place_name_normalized": "潼关", "place_type": "pass",
     "historical_name": "潼关", "modern_name": "潼关", "modern_province": "陕西", "modern_city": "渭南",
     "longitude": 110.31, "latitude": 34.54, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "函谷关", "place_name_normalized": "函谷关", "place_type": "pass",
     "historical_name": "函谷关", "modern_name": "函谷关", "modern_province": "河南", "modern_city": "三门峡",
     "longitude": 111.16, "latitude": 34.63, "mapping_level": "exact",
     "mapping_source": "考古遗址数据", "aliases": []},
    
    {"place_name": "剑门关", "place_name_normalized": "剑门关", "place_type": "pass",
     "historical_name": "剑门关", "modern_name": "剑门关", "modern_province": "四川", "modern_city": "广元",
     "longitude": 105.50, "latitude": 32.18, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["剑阁"]},
    
    {"place_name": "剑阁", "place_name_normalized": "剑门关", "place_type": "pass",
     "historical_name": "剑阁", "modern_name": "剑门关", "modern_province": "四川", "modern_city": "广元",
     "longitude": 105.50, "latitude": 32.18, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "雁门关", "place_name_normalized": "雁门关", "place_type": "pass",
     "historical_name": "雁门关", "modern_name": "雁门关", "modern_province": "山西", "modern_city": "忻州",
     "longitude": 112.45, "latitude": 39.20, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "大散关", "place_name_normalized": "大散关", "place_type": "pass",
     "historical_name": "大散关", "modern_name": "大散关", "modern_province": "陕西", "modern_city": "宝鸡",
     "longitude": 106.81, "latitude": 34.42, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["散关"]},
    
    {"place_name": "萧关", "place_name_normalized": "萧关", "place_type": "pass",
     "historical_name": "萧关", "modern_name": "萧关", "modern_province": "宁夏", "modern_city": "固原",
     "longitude": 106.20, "latitude": 36.00, "mapping_level": "approximate",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "居庸关", "place_name_normalized": "居庸关", "place_type": "pass",
     "historical_name": "居庸关", "modern_name": "居庸关", "modern_province": "北京", "modern_city": "北京",
     "longitude": 116.07, "latitude": 40.29, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    # ========== 建筑/古迹 ==========
    {"place_name": "黄鹤楼", "place_name_normalized": "黄鹤楼", "place_type": "building",
     "historical_name": "黄鹤楼", "modern_name": "黄鹤楼", "modern_province": "湖北", "modern_city": "武汉",
     "longitude": 114.30, "latitude": 30.55, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "岳阳楼", "place_name_normalized": "岳阳楼", "place_type": "building",
     "historical_name": "岳阳楼", "modern_name": "岳阳楼", "modern_province": "湖南", "modern_city": "岳阳",
     "longitude": 113.11, "latitude": 29.38, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "鹳雀楼", "place_name_normalized": "鹳雀楼", "place_type": "building",
     "historical_name": "鹳雀楼", "modern_name": "鹳雀楼", "modern_province": "山西", "modern_city": "运城",
     "longitude": 110.82, "latitude": 34.80, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["鹳鹊楼"]},
    
    {"place_name": "滕王阁", "place_name_normalized": "滕王阁", "place_type": "building",
     "historical_name": "滕王阁", "modern_name": "滕王阁", "modern_province": "江西", "modern_city": "南昌",
     "longitude": 115.88, "latitude": 28.68, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "大雁塔", "place_name_normalized": "大雁塔", "place_type": "building",
     "historical_name": "大雁塔", "modern_name": "大雁塔", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.96, "latitude": 34.22, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "华清池", "place_name_normalized": "华清池", "place_type": "building",
     "historical_name": "华清池", "modern_name": "华清池", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 109.22, "latitude": 34.37, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["华清宫"]},
    
    {"place_name": "寒山寺", "place_name_normalized": "寒山寺", "place_type": "building",
     "historical_name": "寒山寺", "modern_name": "寒山寺", "modern_province": "江苏", "modern_city": "苏州",
     "longitude": 120.57, "latitude": 31.31, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "灵隐寺", "place_name_normalized": "灵隐寺", "place_type": "building",
     "historical_name": "灵隐寺", "modern_name": "灵隐寺", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 120.10, "latitude": 30.24, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "乐游原", "place_name_normalized": "乐游原", "place_type": "other",
     "historical_name": "乐游原", "modern_name": "乐游原遗址", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.96, "latitude": 34.25, "mapping_level": "approximate",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "曲江", "place_name_normalized": "曲江池", "place_type": "other",
     "historical_name": "曲江", "modern_name": "曲江池遗址", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.97, "latitude": 34.21, "mapping_level": "approximate",
     "mapping_source": "历史地理学通识", "aliases": ["曲江池"]},
    
    {"place_name": "石头城", "place_name_normalized": "石头城", "place_type": "building",
     "historical_name": "石头城", "modern_name": "石头城遗址", "modern_province": "江苏", "modern_city": "南京",
     "longitude": 118.76, "latitude": 32.07, "mapping_level": "approximate",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "铜雀台", "place_name_normalized": "铜雀台", "place_type": "building",
     "historical_name": "铜雀台", "modern_name": "铜雀台遗址", "modern_province": "河北", "modern_city": "邯郸",
     "longitude": 114.60, "latitude": 36.30, "mapping_level": "approximate",
     "mapping_source": "历史地理学通识", "aliases": ["铜爵台"]},
    
    {"place_name": "杜甫草堂", "place_name_normalized": "杜甫草堂", "place_type": "building",
     "historical_name": "杜甫草堂", "modern_name": "杜甫草堂", "modern_province": "四川", "modern_city": "成都",
     "longitude": 104.02, "latitude": 30.66, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "武侯祠", "place_name_normalized": "武侯祠", "place_type": "building",
     "historical_name": "武侯祠", "modern_name": "武侯祠", "modern_province": "四川", "modern_city": "成都",
     "longitude": 104.05, "latitude": 30.64, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "白帝城", "place_name_normalized": "白帝城", "place_type": "building",
     "historical_name": "白帝城", "modern_name": "白帝城", "modern_province": "重庆", "modern_city": "奉节",
     "longitude": 109.57, "latitude": 31.05, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    # ========== 历史地域 ==========
    {"place_name": "江南", "place_name_normalized": "江南", "place_type": "historic_region",
     "historical_name": "江南", "modern_name": "江南地区", "modern_province": "跨省", "modern_city": "",
     "longitude": 120.00, "latitude": 31.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["江左", "江东"]},
    
    {"place_name": "塞北", "place_name_normalized": "塞北", "place_type": "historic_region",
     "historical_name": "塞北", "modern_name": "长城以北地区", "modern_province": "跨省", "modern_city": "",
     "longitude": 115.00, "latitude": 42.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["塞外", "边塞", "关外"]},
    
    {"place_name": "巴蜀", "place_name_normalized": "巴蜀", "place_type": "historic_region",
     "historical_name": "巴蜀", "modern_name": "四川盆地", "modern_province": "四川/重庆", "modern_city": "",
     "longitude": 104.00, "latitude": 30.50, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["蜀", "巴", "蜀中"]},
    
    {"place_name": "潇湘", "place_name_normalized": "潇湘", "place_type": "historic_region",
     "historical_name": "潇湘", "modern_name": "湖南地区", "modern_province": "湖南", "modern_city": "",
     "longitude": 112.50, "latitude": 27.50, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "中原", "place_name_normalized": "中原", "place_type": "historic_region",
     "historical_name": "中原", "modern_name": "中原地区", "modern_province": "河南", "modern_city": "",
     "longitude": 113.50, "latitude": 34.50, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["中州", "中土"]},
    
    {"place_name": "关中", "place_name_normalized": "关中", "place_type": "historic_region",
     "historical_name": "关中", "modern_name": "关中平原", "modern_province": "陕西", "modern_city": "",
     "longitude": 108.50, "latitude": 34.30, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["关西"]},
    
    {"place_name": "河西", "place_name_normalized": "河西", "place_type": "historic_region",
     "historical_name": "河西", "modern_name": "河西走廊", "modern_province": "甘肃", "modern_city": "",
     "longitude": 100.00, "latitude": 39.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["河西走廊"]},
    
    {"place_name": "陇右", "place_name_normalized": "陇右", "place_type": "historic_region",
     "historical_name": "陇右", "modern_name": "陇东/陇西地区", "modern_province": "甘肃", "modern_city": "",
     "longitude": 104.00, "latitude": 35.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["陇"]},
    
    {"place_name": "岭南", "place_name_normalized": "岭南", "place_type": "historic_region",
     "historical_name": "岭南", "modern_name": "岭南地区", "modern_province": "广东/广西", "modern_city": "",
     "longitude": 113.30, "latitude": 23.50, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "荆楚", "place_name_normalized": "荆楚", "place_type": "historic_region",
     "historical_name": "荆楚", "modern_name": "湖北湖南地区", "modern_province": "湖北/湖南", "modern_city": "",
     "longitude": 112.50, "latitude": 30.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["楚"]},
    
    {"place_name": "吴越", "place_name_normalized": "吴越", "place_type": "historic_region",
     "historical_name": "吴越", "modern_name": "江浙地区", "modern_province": "江苏/浙江", "modern_city": "",
     "longitude": 120.00, "latitude": 31.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "燕赵", "place_name_normalized": "燕赵", "place_type": "historic_region",
     "historical_name": "燕赵", "modern_name": "河北地区", "modern_province": "河北", "modern_city": "",
     "longitude": 114.50, "latitude": 38.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "齐鲁", "place_name_normalized": "齐鲁", "place_type": "historic_region",
     "historical_name": "齐鲁", "modern_name": "山东地区", "modern_province": "山东", "modern_city": "",
     "longitude": 117.00, "latitude": 36.70, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "黔中", "place_name_normalized": "黔中", "place_type": "historic_region",
     "historical_name": "黔中", "modern_name": "贵州地区", "modern_province": "贵州", "modern_city": "",
     "longitude": 106.70, "latitude": 26.60, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": ["黔"]},
    
    {"place_name": "塞上", "place_name_normalized": "塞北", "place_type": "historic_region",
     "historical_name": "塞上", "modern_name": "长城以北地区", "modern_province": "跨省", "modern_city": "",
     "longitude": 115.00, "latitude": 42.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "边塞", "place_name_normalized": "边塞", "place_type": "historic_region",
     "historical_name": "边塞", "modern_name": "边疆地区", "modern_province": "跨省", "modern_city": "",
     "longitude": 105.00, "latitude": 40.00, "mapping_level": "region",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    # ========== 其他重要地点 ==========
    {"place_name": "三峡", "place_name_normalized": "三峡", "place_type": "other",
     "historical_name": "三峡", "modern_name": "长江三峡", "modern_province": "重庆/湖北", "modern_city": "",
     "longitude": 110.50, "latitude": 31.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["瞿塘峡", "巫峡", "西陵峡"]},
    
    {"place_name": "瞿塘峡", "place_name_normalized": "瞿塘峡", "place_type": "other",
     "historical_name": "瞿塘峡", "modern_name": "瞿塘峡", "modern_province": "重庆", "modern_city": "奉节",
     "longitude": 109.55, "latitude": 31.04, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["夔峡"]},
    
    {"place_name": "巫峡", "place_name_normalized": "巫峡", "place_type": "other",
     "historical_name": "巫峡", "modern_name": "巫峡", "modern_province": "重庆", "modern_city": "巫山",
     "longitude": 110.00, "latitude": 31.08, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "西陵峡", "place_name_normalized": "西陵峡", "place_type": "other",
     "historical_name": "西陵峡", "modern_name": "西陵峡", "modern_province": "湖北", "modern_city": "宜昌",
     "longitude": 111.20, "latitude": 31.00, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "龙门", "place_name_normalized": "龙门", "place_type": "other",
     "historical_name": "龙门", "modern_name": "龙门石窟", "modern_province": "河南", "modern_city": "洛阳",
     "longitude": 112.48, "latitude": 34.55, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["伊阙"]},
    
    {"place_name": "昆仑", "place_name_normalized": "昆仑山", "place_type": "mountain",
     "historical_name": "昆仑", "modern_name": "昆仑山", "modern_province": "跨省", "modern_city": "",
     "longitude": 90.00, "latitude": 36.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["昆仑山"]},
    
    {"place_name": "天山", "place_name_normalized": "天山", "place_type": "mountain",
     "historical_name": "天山", "modern_name": "天山", "modern_province": "新疆", "modern_city": "",
     "longitude": 86.00, "latitude": 43.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "阴山", "place_name_normalized": "阴山", "place_type": "mountain",
     "historical_name": "阴山", "modern_name": "阴山", "modern_province": "内蒙古", "modern_city": "",
     "longitude": 108.00, "latitude": 41.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "祁连山", "place_name_normalized": "祁连山", "place_type": "mountain",
     "historical_name": "祁连山", "modern_name": "祁连山", "modern_province": "甘肃/青海", "modern_city": "",
     "longitude": 100.00, "latitude": 38.50, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "贺兰山", "place_name_normalized": "贺兰山", "place_type": "mountain",
     "historical_name": "贺兰山", "modern_name": "贺兰山", "modern_province": "宁夏", "modern_city": "银川",
     "longitude": 106.00, "latitude": 38.60, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "六盘山", "place_name_normalized": "六盘山", "place_type": "mountain",
     "historical_name": "六盘山", "modern_name": "六盘山", "modern_province": "宁夏/甘肃", "modern_city": "",
     "longitude": 106.00, "latitude": 35.50, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": ["陇山"]},
    
    {"place_name": "陇山", "place_name_normalized": "六盘山", "place_type": "mountain",
     "historical_name": "陇山", "modern_name": "六盘山", "modern_province": "宁夏/甘肃", "modern_city": "",
     "longitude": 106.00, "latitude": 35.50, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "终南", "place_name_normalized": "终南山", "place_type": "mountain",
     "historical_name": "终南", "modern_name": "终南山", "modern_province": "陕西", "modern_city": "西安",
     "longitude": 108.75, "latitude": 34.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "少室山", "place_name_normalized": "少室山", "place_type": "mountain",
     "historical_name": "少室山", "modern_name": "少室山", "modern_province": "河南", "modern_city": "郑州",
     "longitude": 112.95, "latitude": 34.50, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "敬亭山", "place_name_normalized": "敬亭山", "place_type": "mountain",
     "historical_name": "敬亭山", "modern_name": "敬亭山", "modern_province": "安徽", "modern_city": "宣城",
     "longitude": 118.73, "latitude": 30.97, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "北固山", "place_name_normalized": "北固山", "place_type": "mountain",
     "historical_name": "北固山", "modern_name": "北固山", "modern_province": "江苏", "modern_city": "镇江",
     "longitude": 119.47, "latitude": 32.22, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "金山", "place_name_normalized": "金山", "place_type": "mountain",
     "historical_name": "金山", "modern_name": "金山", "modern_province": "江苏", "modern_city": "镇江",
     "longitude": 119.42, "latitude": 32.23, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "焦山", "place_name_normalized": "焦山", "place_type": "mountain",
     "historical_name": "焦山", "modern_name": "焦山", "modern_province": "江苏", "modern_city": "镇江",
     "longitude": 119.45, "latitude": 32.24, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "鹿门山", "place_name_normalized": "鹿门山", "place_type": "mountain",
     "historical_name": "鹿门山", "modern_name": "鹿门山", "modern_province": "湖北", "modern_city": "襄阳",
     "longitude": 112.25, "latitude": 32.10, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": ["鹿门"]},
    
    {"place_name": "岘山", "place_name_normalized": "岘山", "place_type": "mountain",
     "historical_name": "岘山", "modern_name": "岘山", "modern_province": "湖北", "modern_city": "襄阳",
     "longitude": 112.15, "latitude": 32.00, "mapping_level": "exact",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "富春山", "place_name_normalized": "富春山", "place_type": "mountain",
     "historical_name": "富春山", "modern_name": "富春山", "modern_province": "浙江", "modern_city": "杭州",
     "longitude": 119.80, "latitude": 29.90, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    # 更多城市
    {"place_name": "陈州", "place_name_normalized": "淮阳", "place_type": "city",
     "historical_name": "陈州", "modern_name": "淮阳", "modern_province": "河南", "modern_city": "周口",
     "longitude": 114.52, "latitude": 33.73, "mapping_level": "county",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "商州", "place_name_normalized": "商洛", "place_type": "city",
     "historical_name": "商州", "modern_name": "商洛", "modern_province": "陕西", "modern_city": "商洛",
     "longitude": 109.94, "latitude": 33.87, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "金城", "place_name_normalized": "兰州", "place_type": "city",
     "historical_name": "金城", "modern_name": "兰州", "modern_province": "甘肃", "modern_city": "兰州",
     "longitude": 103.83, "latitude": 36.06, "mapping_level": "city",
     "mapping_source": "历史地理学通识", "aliases": []},
    
    {"place_name": "阴山", "place_name_normalized": "阴山", "place_type": "mountain",
     "historical_name": "阴山", "modern_name": "阴山", "modern_province": "内蒙古", "modern_city": "",
     "longitude": 108.00, "latitude": 41.00, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    # 河流补充
    {"place_name": "汨罗江", "place_name_normalized": "汨罗江", "place_type": "river",
     "historical_name": "汨罗江", "modern_name": "汨罗江", "modern_province": "湖南", "modern_city": "岳阳",
     "longitude": 112.80, "latitude": 28.80, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "滁水", "place_name_normalized": "滁河", "place_type": "river",
     "historical_name": "滁水", "modern_name": "滁河", "modern_province": "安徽", "modern_city": "滁州",
     "longitude": 118.32, "latitude": 32.30, "mapping_level": "approximate",
     "mapping_source": "公开地理数据", "aliases": []},
    
    {"place_name": "楚水", "place_name_normalized": "楚水", "place_type": "river",
     "historical_name": "楚水", "modern_name": "楚水", "modern_province": "陕西", "modern_city": "商洛",
     "longitude": 109.94, "latitude": 33.87, "mapping_level": "approximate",
     "mapping_source": "历史地理学通识", "aliases": []},
]

# 排除列表 - 容易误判为地名的词
EXCLUDE_WORDS = {
    '南山', '西山', '东山', '北山', '前山', '后山', '高山', '深山', '空山', '春山', '秋山',
    '远山', '青山', '寒山', '孤山', '千山', '万山', '群山', '名山', '江山', '河山',
    '水上', '水下', '山上', '山下', '水上', '山下', '海上', '天下', '地上',
    '西楼', '东楼', '南楼', '北楼', '高楼', '小楼', '楼头', '楼前', '楼上', '楼下',
    '东南', '西北', '东北', '西南', '上方', '下方', '前方', '后方',
    '东门', '西门', '南门', '北门', '前门', '后门',
    '东风', '西风', '南风', '北风', '东风',
    '长风', '清风', '秋风', '春风', '寒风', '微风', '悲风', '惊风', '朔风',
    '西州', '东州',
    '北庭',  # 可能是地名也可能是泛指
    '水', '山', '河', '湖', '江', '城', '关', '桥', '楼', '台', '亭', '阁', '门', '宫', '寺',
    '天', '地', '云', '风', '雨', '雪', '月', '日', '星', '海',
}


def build_index():
    """构建地名索引，方便快速查找"""
    index = {}
    for i, place in enumerate(PLACE_DICTIONARY):
        # 主名
        name = place['place_name']
        if name not in EXCLUDE_WORDS:
            index[name] = i
        # 别名
        for alias in place.get('aliases', []):
            if alias and alias not in EXCLUDE_WORDS:
                index[alias] = i
    return index


def get_place_by_name(name):
    """根据名称获取地点信息"""
    idx = build_index()
    if name in idx:
        return PLACE_DICTIONARY[idx[name]]
    return None


def get_all_place_names():
    """获取所有地名列表（含别名）"""
    names = set()
    idx = build_index()
    for name in idx:
        if name not in EXCLUDE_WORDS and len(name) >= 2:
            names.add(name)
    return names


if __name__ == '__main__':
    idx = build_index()
    print(f"地名词典: {len(PLACE_DICTIONARY)} 条")
    print(f"索引条目: {len(idx)} 个（含别名）")
    
    # 统计类型
    type_counts = {}
    for p in PLACE_DICTIONARY:
        t = p['place_type']
        type_counts[t] = type_counts.get(t, 0) + 1
    for t, c in sorted(type_counts.items()):
        print(f"  {t}: {c}")
