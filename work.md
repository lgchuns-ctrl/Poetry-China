# 开发日志

## 2026-08-07 项目开发全流程

### 一、数据采集阶段

1. **数据源调研**：确定使用 GitHub 开源项目 chinese-poetry 作为数据源，该仓库收录了全唐诗和全宋词的 JSON 格式数据，MIT 许可证。
2. **数据下载**：编写 Node.js 下载脚本（`scripts/collect/download_data.js`），通过 https 模块从 GitHub raw content 下载唐诗 15 个文件（15,008 首）和宋词 6 个文件（6,000 首），以及作者信息文件。下载过程中处理了 URL 编码问题和超时重试逻辑（5 次重试，3 秒间隔）。
3. **繁简转换**：使用 opencc-js 库编写转换脚本（`scripts/clean/convert_t2s.js`），将所有繁体文本转换为简体，包括作者名、标题、正文和描述字段。

### 二、数据处理阶段

1. **地名词典构建**：在 `data/dictionary/place_dictionary.py` 中构建了包含 190+ 条目的地名词典，涵盖城市、山岳、河流、湖泊、关隘、建筑、历史区域等 7 大类。每条记录包含：地名、规范化名称、类型、历史名称、现代名称、省份、城市、经纬度、映射级别、别名等字段。同时定义了排除词表（如"南山""东风""西楼"）以减少误识别。
2. **NER 地名提取**：在 `process_pipeline.py` 中实现了基于词典+规则的地名提取算法，包括：字符串精确匹配、别名映射、重叠预防（优先匹配长名）、排除词过滤。
3. **多维分析**：实现了地名频次统计、诗人×地名矩阵、朝代×地名分布、地名×主题关联、地名×意象关联、诗人多样性指数等多维度分析。
4. **NER 质量验证**：随机抽取 150 条提取结果进行人工验证，精确率 100%，并记录了可能遗漏的地名。
5. **数据导出**：将处理结果导出为 13 个 JSON 文件，同时写入 `data/processed/` 和 `web/public/data/`。

### 三、前端开发阶段

1. **项目搭建**：Vue 3 + TypeScript + Vite 5 + ECharts 5，配置了 `@` 路径别名和 ECharts 代码分割。
2. **视图组件**：开发了 6 个视图组件：
   - `HomeView.vue` — 首页，含动画标题、数据统计、经典诗词卡片
   - `MapView.vue` — 核心地图视图，ECharts geo scatter + 多维筛选 + 地点详情面板
   - `CompareView.vue` — 唐宋对比，4 个 tab（地名/类型/意象/主题）
   - `AuthorView.vue` — 诗人行迹，个体诗人地图 + 统计卡片
   - `SearchView.vue` — 全文检索，高亮匹配 + 快捷搜索
   - `DataMethodView.vue` — 数据方法，流程展示 + NER 验证 + 映射说明
3. **视觉设计**：宣纸白（#f5f1e8）底色 + 墨黑（#1a1a1a）文字 + 朱砂（#8b3a3a）强调色，唐色 #8b3a3a、宋色 #2e5c6e，衬线字体栈。
4. **地图数据**：从 DataV.GeoAtlas 下载简化版中国 GeoJSON（35 省级行政区）。

### 四、环境适配

在 OpenHarmony ARM64 平台上遇到了以下兼容性问题并逐一解决：

1. **Rollup 原生模块**：`@rollup/rollup-openharmony-arm64` 的 .node 文件因系统安全策略无法加载（ERR_DLOPEN_FAILED）。解决方案：下载 `@rollup/wasm-node` 的 tarball，提取 WASM 版 native.js 和 bindings_wasm 文件替换原生版本。
2. **esbuild 平台不支持**：esbuild 不支持 openharmony 平台。解决方案：下载 `@esbuild/android-arm`（WASM 版本）tarball，手动安装到 `node_modules/@esbuild/android-arm/`，并 patch esbuild 的 `main.js` 将 `openharmony arm64 LE` 加入 `knownWebAssemblyFallbackPackages`。
3. **npm install 目录冲突**：npm 安装时 acorn 目录重命名失败（ENOTEMPTY）。通过手动下载 tarball 并解压绕过。

### 五、质量保障

1. TypeScript 类型检查通过（`vue-tsc --noEmit` 零错误）。
2. 修复了 MapView.vue 中 `setFilter` 函数的类型索引错误。
3. 开发服务器在 localhost:5173 成功启动，所有页面和 API 正常响应。

### 六、数据统计

| 指标 | 数值 |
|------|------|
| 唐诗 | 15,008 首 |
| 宋词 | 6,000 首 |
| 诗人 | 1,141 位 |
| 地名 | 190 个 |
| 地名提及 | 5,341 次 |
| NER 精确率 | 100% |
| 被提及最多 | 长安（347 次） |
| 覆盖最广诗人 | 杜甫（86 个地点） |
