# 诗行中国——唐诗宋词中的山河地图

> 循诗而行，在千年文字中重新看见中国山河

## 在线访问

GitHub Pages 地址：<https://lgchuns-ctrl.github.io/Poetry-China/>

## 项目简介

本项目是一个数字人文研究与应用项目，通过对唐诗宋词文本的系统性数据挖掘，提取其中出现的地理地名，将其映射到现代中国地图上，以交互式可视化的方式展现唐宋诗词中的山河版图。

项目涵盖 **21,008 首诗词**（唐诗 15,008 首 + 宋词 6,000 首），覆盖 **1,141 位诗人**，识别 **190 个文学地点**，提取 **5,341 次地名提及**。

## 快速开始

```bash
cd web
npm install
npm run dev
```

浏览器访问 http://localhost:5173 即可查看完整网页效果。

## 构建与发布

```bash
cd web
npm run build
```

构建产物位于 `web/dist/`。如需发布到 GitHub Pages，在项目根目录执行：

```powershell
powershell -ExecutionPolicy Bypass -File scripts\publish_to_ghpages.ps1
```

如遇 Git Credential Manager 崩溃，可先使用令牌 URL 推送，再在脚本后追加 `-NoCredentialHelper`，具体见团队内部的《GitHub 上传与更新指南》。

## 目录结构

```
poetry-china/
├── data/                   # 数据目录
│   ├── raw/                # 原始数据（繁体）
│   ├── interim/            # 中间数据（简体转换后）
│   ├── processed/          # 处理后数据（JSON）
│   ├── dictionary/         # 地名词典
│   └── reports/            # 数据质量报告
├── scripts/                # 数据处理脚本
│   ├── collect/            # 数据采集
│   ├── clean/              # 繁简转换
│   ├── extract/            # 地名提取
│   ├── process_pipeline.py # 主处理流水线
│   └── validate/           # 数据验证
├── web/                    # 前端应用
│   ├── src/
│   │   ├── views/          # 6 个视图组件
│   │   ├── utils/          # 数据加载工具
│   │   └── styles/         # 全局样式
│   ├── public/data/        # 13 个 JSON 数据文件
│   └── package.json
├── docs/                   # 项目文档
└── README.md
```

## 技术栈

| 层级 | 技术 |
|------|------|
| 数据采集 | Node.js + GitHub API |
| 数据处理 | Python 3.12（标准库） |
| 繁简转换 | opencc-js |
| 前端框架 | Vue 3 + TypeScript |
| 构建工具 | Vite 5 |
| 可视化 | ECharts 5 |
| 地图数据 | DataV.GeoAtlas |

## 网页功能

1. **首页** — 项目概览、核心数据、经典诗词展示
2. **诗词地图** — ECharts 中国地图散点图，支持朝代/诗人/主题/意象筛选
3. **唐宋对比** — 地名、地点类型、意象、主题四维度对比
4. **诗人行迹** — 个体诗人地理分布与行迹地图
5. **全文检索** — 跨诗词/标题/作者/地名搜索
6. **数据方法** — 数据来源、处理流程、NER 验证、映射说明

## 数据来源

- [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) — MIT 许可证
- 中国地图 GeoJSON — DataV.GeoAtlas

## 许可证

本项目仅供学术研究和教学使用。
