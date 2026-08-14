<template>
  <div class="data-method-view">
    <div class="section-header">
      <h2 class="section-title">数据与方法</h2>
      <p class="section-desc">数据来源、处理流程与技术说明</p>
    </div>

    <div class="dm-content" v-if="metadata">
      <!-- 数据概览 -->
      <div class="dm-card">
        <h3 class="dm-card-title">数据概览</h3>
        <div class="dm-stats">
          <div class="dm-stat">
            <span class="dm-stat-num">{{ metadata.stats.tang_poems }}</span>
            <span class="dm-stat-label">唐诗</span>
          </div>
          <div class="dm-stat">
            <span class="dm-stat-num">{{ metadata.stats.song_ci }}</span>
            <span class="dm-stat-label">宋词</span>
          </div>
          <div class="dm-stat">
            <span class="dm-stat-num">{{ metadata.stats.total_authors }}</span>
            <span class="dm-stat-label">诗人</span>
          </div>
          <div class="dm-stat">
            <span class="dm-stat-num">{{ metadata.stats.total_places }}</span>
            <span class="dm-stat-label">地点</span>
          </div>
          <div class="dm-stat">
            <span class="dm-stat-num">{{ metadata.stats.total_mentions }}</span>
            <span class="dm-stat-label">地名提及</span>
          </div>
        </div>
      </div>

      <!-- 数据来源 -->
      <div class="dm-card">
        <h3 class="dm-card-title">数据来源</h3>
        <div v-for="src in metadata.data_sources" :key="src.name" class="dm-source">
          <p class="src-name">{{ src.name }}</p>
          <p class="src-url">{{ src.url }}</p>
          <p class="src-license">许可证：{{ src.license }}</p>
        </div>
        <p class="dm-note">
          唐宋诗词原文属公版内容，数据来源于 chinese-poetry GitHub 仓库（MIT 许可证）。
          仓库数据来自《全唐诗》和《全宋词》等古典文集的数字化版本。
        </p>
      </div>

      <!-- 处理流程 -->
      <div class="dm-card" v-if="methodology">
        <h3 class="dm-card-title">处理流程</h3>
        <div class="process-flow">
          <div v-for="(step, i) in methodology.processing_steps" :key="i" class="process-step">
            <span class="step-num">{{ i + 1 }}</span>
            <span class="step-text">{{ step }}</span>
          </div>
        </div>
      </div>

      <!-- 地名识别 -->
      <div class="dm-card" v-if="methodology">
        <h3 class="dm-card-title">地名识别方法</h3>
        <p class="dm-text">{{ methodology.place_extraction_method }}</p>
        <div class="dm-subsection">
          <h4 class="dm-subtitle">地名词典规模</h4>
          <p class="dm-text">{{ methodology.place_dictionary_size }} 条地名记录</p>
        </div>
        <div class="dm-subsection">
          <h4 class="dm-subtitle">三种地点区分</h4>
          <ul class="dm-list">
            <li><strong>作品提及地点 (mentioned_place)</strong>：诗词文本中明确出现的地名，表示"作品写到了这里"</li>
            <li><strong>创作地点 (writing_place)</strong>：可靠资料明确说明某诗创作于某地</li>
            <li><strong>作者行迹地点 (biographical_place)</strong>：诗人生平可靠记录中曾在某地生活、任职、旅行</li>
          </ul>
          <p class="dm-note">本系统第一版主要使用 mentioned_place，即"诗词书写了哪里"。</p>
        </div>
      </div>

      <!-- NER验证 -->
      <div class="dm-card" v-if="methodology?.ner_validation">
        <h3 class="dm-card-title">地名NER质量验证</h3>
        <div class="ner-stats">
          <div class="ner-stat">
            <span class="ner-num">{{ methodology.ner_validation.sample_size }}</span>
            <span class="ner-label">抽样数</span>
          </div>
          <div class="ner-stat">
            <span class="ner-num">{{ methodology.ner_validation.correct }}</span>
            <span class="ner-label">正确识别</span>
          </div>
          <div class="ner-stat">
            <span class="ner-num">{{ methodology.ner_validation.false_positive }}</span>
            <span class="ner-label">误识别</span>
          </div>
          <div class="ner-stat">
            <span class="ner-num">{{ methodology.ner_validation.possible_missed }}</span>
            <span class="ner-label">可能遗漏</span>
          </div>
          <div class="ner-stat highlight">
            <span class="ner-num">{{ (methodology.ner_validation.precision * 100).toFixed(1) }}%</span>
            <span class="ner-label">精确率</span>
          </div>
        </div>
        <p class="dm-note">{{ methodology.ner_validation.note }}</p>
      </div>

      <!-- 古今地名映射 -->
      <div class="dm-card">
        <h3 class="dm-card-title">古今地名映射说明</h3>
        <p class="dm-text">
          系统建立了历史地名到现代位置的映射表，同时保留原始历史地名和现代名称。
          网页展示中，历史地名以大字显示，现代位置以小字标注。
        </p>
        <div class="mapping-table">
          <div class="mapping-row" v-for="m in mappingExamples" :key="m.historical">
            <span class="map-historical">{{ m.historical }}</span>
            <span class="map-arrow">→</span>
            <span class="map-modern">{{ m.modern }}</span>
            <span class="map-level" :class="'level-' + m.level">{{ m.levelLabel }}</span>
          </div>
        </div>
      </div>

      <!-- 定位精度说明 -->
      <div class="dm-card" v-if="methodology">
        <h3 class="dm-card-title">定位精度说明</h3>
        <div class="level-list">
          <div v-for="(desc, level) in methodology.place_types" :key="level" class="level-item">
            <span class="level-badge" :class="'level-' + level">{{ level }}</span>
            <span class="level-desc">{{ desc }}</span>
          </div>
        </div>
      </div>

      <!-- 局限性 -->
      <div class="dm-card" v-if="methodology">
        <h3 class="dm-card-title">研究局限性</h3>
        <ul class="dm-list">
          <li v-for="(lim, i) in methodology.limitations" :key="i">{{ lim }}</li>
        </ul>
      </div>

      <!-- 研究结论 -->
      <div class="dm-card" v-if="conclusions.length">
        <h3 class="dm-card-title">数据驱动结论</h3>
        <div class="conclusions-list">
          <div v-for="c in conclusions" :key="c.conclusion_id" class="conclusion-item">
            <span class="conclusion-id">{{ c.conclusion_id }}</span>
            <p class="conclusion-text">{{ c.text }}</p>
            <span class="conclusion-metric">指标：{{ c.metric }}</span>
          </div>
        </div>
        <p class="dm-note">以上结论均由程序从数据中计算生成，非人工撰写。</p>
      </div>

      <!-- 技术栈 -->
      <div class="dm-card">
        <h3 class="dm-card-title">技术栈</h3>
        <div class="tech-stack">
          <span class="tech-item">Python 3.12</span>
          <span class="tech-item">Node.js</span>
          <span class="tech-item">opencc-js (繁简转换)</span>
          <span class="tech-item">Vue 3</span>
          <span class="tech-item">TypeScript</span>
          <span class="tech-item">Vite</span>
          <span class="tech-item">ECharts 5</span>
        </div>
      </div>

      <!-- 版权说明 -->
      <div class="dm-card">
        <h3 class="dm-card-title">版权说明</h3>
        <p class="dm-text">
          古典唐诗宋词正文属公版内容，可自由用于研究展示。
          本网站不复制现代商业网站的翻译、赏析、注释内容。
          网页中展示的结构化数据和描述均由本项目基于数据分析自行生成。
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { loadMetadata, loadMethodology, loadConclusions, type Conclusion } from '../utils/data'

const metadata = ref<any>(null)
const methodology = ref<any>(null)
const conclusions = ref<Conclusion[]>([])

const mappingExamples = [
  { historical: '长安', modern: '今陕西西安', level: 'city', levelLabel: '城市级' },
  { historical: '临安', modern: '今浙江杭州', level: 'city', levelLabel: '城市级' },
  { historical: '姑苏', modern: '今江苏苏州', level: 'city', levelLabel: '城市级' },
  { historical: '汴京', modern: '今河南开封', level: 'city', levelLabel: '城市级' },
  { historical: '金陵', modern: '今江苏南京', level: 'city', levelLabel: '城市级' },
  { historical: '庐山', modern: '今江西九江庐山', level: 'exact', levelLabel: '精确' },
  { historical: '玉门关', modern: '今甘肃敦煌', level: 'exact', levelLabel: '精确' },
  { historical: '江南', modern: '长江以南地区', level: 'region', levelLabel: '区域级' },
  { historical: '塞北', modern: '长城以北地区', level: 'region', levelLabel: '区域级' },
  { historical: '黄河', modern: '跨省河流', level: 'approximate', levelLabel: '近似' },
]

onMounted(async () => {
  try {
    const [meta, meth, concl] = await Promise.all([
      loadMetadata(),
      loadMethodology(),
      loadConclusions()
    ])
    metadata.value = meta
    methodology.value = meth
    conclusions.value = concl
  } catch(e) {
    console.error('Failed to load data:', e)
  }
})
</script>

<style scoped>
.data-method-view {
  max-width: 900px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.8rem;
  color: var(--color-ink);
  letter-spacing: 0.1em;
  margin-bottom: 0.3rem;
}

.section-desc {
  font-size: 0.85rem;
  color: var(--color-ink-muted);
}

.dm-content {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.dm-card {
  padding: 1.5rem 2rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.dm-card-title {
  font-size: 1.1rem;
  color: var(--color-ink);
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--color-border-light);
}

.dm-stats {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.dm-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.dm-stat-num {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-accent);
}

.dm-stat-label {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
}

.dm-source {
  margin-bottom: 0.8rem;
  padding: 0.5rem 0;
}

.src-name {
  font-size: 0.9rem;
  color: var(--color-ink);
  font-weight: 600;
}

.src-url {
  font-size: 0.8rem;
  color: var(--color-accent);
}

.src-license {
  font-size: 0.78rem;
  color: var(--color-ink-muted);
}

.dm-note {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  margin-top: 0.5rem;
  line-height: 1.7;
}

.dm-text {
  font-size: 0.85rem;
  color: var(--color-ink-light);
  line-height: 1.8;
}

.dm-subsection {
  margin-top: 1rem;
}

.dm-subtitle {
  font-size: 0.9rem;
  color: var(--color-ink);
  margin-bottom: 0.5rem;
}

.dm-list {
  list-style: none;
  padding: 0;
}

.dm-list li {
  font-size: 0.85rem;
  color: var(--color-ink-light);
  line-height: 1.8;
  padding: 0.3rem 0 0.3rem 1rem;
  position: relative;
}

.dm-list li::before {
  content: '·';
  position: absolute;
  left: 0;
  color: var(--color-accent);
  font-weight: 700;
}

/* 处理流程 */
.process-flow {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.process-step {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.step-num {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  font-size: 0.75rem;
  color: #fff;
  background: var(--color-accent);
  border-radius: 50%;
  flex-shrink: 0;
}

.step-text {
  font-size: 0.85rem;
  color: var(--color-ink-light);
}

/* NER验证 */
.ner-stats {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.8rem;
}

.ner-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.ner-num {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-ink);
}

.ner-stat.highlight .ner-num {
  color: #4a7c59;
}

.ner-label {
  font-size: 0.75rem;
  color: var(--color-ink-muted);
}

/* 映射表 */
.mapping-table {
  margin-top: 0.8rem;
}

.mapping-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.3rem 0;
  font-size: 0.85rem;
  border-bottom: 1px solid var(--color-border-light);
}

.map-historical {
  font-weight: 600;
  color: var(--color-ink);
  min-width: 60px;
}

.map-arrow {
  color: var(--color-ink-muted);
}

.map-modern {
  color: var(--color-ink-light);
  flex: 1;
}

.map-level {
  font-size: 0.7rem;
  padding: 1px 6px;
  border-radius: 8px;
  color: #fff;
}

.level-exact { background: #4a7c59; }
.level-city { background: #4a7c59; }
.level-county { background: #5b8a72; }
.level-province { background: #b8860b; }
.level-approximate { background: #b8860b; }
.level-region { background: #7a6a5a; }
.level-unknown { background: #ccc; }

/* 定位精度 */
.level-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.level-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.level-badge {
  padding: 2px 8px;
  font-size: 0.75rem;
  border-radius: 8px;
  color: #fff;
  min-width: 80px;
  text-align: center;
}

.level-desc {
  font-size: 0.82rem;
  color: var(--color-ink-light);
}

/* 结论 */
.conclusions-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.conclusion-item {
  padding: 0.8rem 1rem;
  background: var(--color-bg-alt);
  border-left: 3px solid var(--color-accent);
  border-radius: 0 var(--radius) var(--radius) 0;
}

.conclusion-id {
  font-size: 0.72rem;
  color: var(--color-ink-muted);
  font-family: monospace;
}

.conclusion-text {
  font-size: 0.88rem;
  color: var(--color-ink);
  line-height: 1.7;
  margin: 0.2rem 0;
}

.conclusion-metric {
  font-size: 0.72rem;
  color: var(--color-ink-muted);
}

/* 技术栈 */
.tech-stack {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.tech-item {
  padding: 0.3rem 0.8rem;
  font-size: 0.82rem;
  color: var(--color-ink-light);
  background: var(--color-bg-alt);
  border: 1px solid var(--color-border-light);
  border-radius: 12px;
}

@media (max-width: 768px) {
  .dm-card { padding: 1rem; }
  .dm-stats { gap: 1rem; }
  .ner-stats { gap: 1rem; }
}
</style>
