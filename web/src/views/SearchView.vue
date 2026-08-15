<template>
  <div class="search-view">
    <StoryHeader
      chapter="05 · 一句诗"
      title="一句诗，落在何处？"
      subtitle="最后，请你自己验证：诗与山河之间，确实存在连接。"
      question="输入一句诗、一个地名或一位诗人，把它重新放回地图。"
    />

    <!-- 搜索框 -->
    <div class="search-box">
      <input 
        v-model="query" 
        class="search-input" 
        placeholder="如：烟花三月下扬州 / 扬州 / 庐山"
        @input="onSearch"
        @keydown.enter="onSearch"
      />
      <button class="search-btn" @click="onSearch">寻诗</button>
    </div>

    <!-- 快捷搜索 -->
    <div class="quick-search">
      <span class="quick-label">试试搜索：</span>
      <button v-for="q in quickQueries" :key="q" class="quick-btn" @click="quickSearch(q)">{{ q }}</button>
    </div>

    <div v-if="detectedPlace" class="locate-card">
      <div class="locate-marker">定位</div>
      <div>
        <h3 class="locate-title">{{ detectedPlace.place_name }}</h3>
        <p class="locate-meta">
          今{{ detectedPlace.modern_province }} · {{ detectedPlace.modern_name || detectedPlace.place_name }}
          <span v-if="detectedPlace.place_type" class="locate-type">{{ typeLabel(detectedPlace.place_type) }}</span>
        </p>
      </div>
    </div>

    <!-- 搜索结果 -->
    <div class="search-results" v-if="results.length > 0">
      <p class="result-count">找到 {{ results.length }} 条结果</p>
      <div class="result-list">
        <div v-for="r in results" :key="r.work_id" class="result-item" :class="{ selected: selectedResult?.work_id === r.work_id }" @click="showResultDetail(r)">
          <div class="result-header">
            <span class="result-title">{{ r.title }}</span>
            <span class="result-author">{{ r.author }}</span>
            <span class="result-dynasty" :class="'dynasty-' + r.dynasty">{{ r.dynasty }}</span>
          </div>
          <p class="result-text" v-html="highlightText(r.text, query)"></p>
          <div class="result-tags" v-if="r.places.length || r.themes.length || r.imagery.length">
            <span v-for="p in r.places.slice(0, 5)" :key="p" class="tag place-tag">{{ p }}</span>
            <span v-for="t in r.themes.slice(0, 3)" :key="t" class="tag theme-tag">{{ t }}</span>
            <span v-for="i in r.imagery.slice(0, 3)" :key="i" class="tag imagery-tag">{{ i }}</span>
          </div>
        </div>
      </div>

      <transition name="slide-up">
        <div v-if="selectedWork" class="result-detail">
          <div class="result-detail-header">
            <div>
              <h3 class="result-detail-title">{{ selectedWork.title }}</h3>
              <p class="result-detail-meta">{{ selectedWork.author }} · {{ selectedWork.dynasty }}</p>
            </div>
            <button class="result-detail-close" @click="selectedResult = null">×</button>
          </div>
          <pre class="result-detail-text">{{ selectedWork.text }}</pre>
          <div class="result-tags" v-if="selectedWork.place_mentions.length || selectedWork.imagery.length || selectedWork.themes.length">
            <span v-for="p in selectedWork.place_mentions" :key="p" class="tag place-tag">{{ p }}</span>
            <span v-for="t in selectedWork.themes" :key="t" class="tag theme-tag">{{ t }}</span>
            <span v-for="i in selectedWork.imagery" :key="i" class="tag imagery-tag">{{ i }}</span>
          </div>
        </div>
      </transition>
    </div>

    <div v-else-if="searched && results.length === 0" class="no-results">
      <p>未找到包含「{{ query }}」的作品</p>
      <p class="no-results-hint">试试搜索其他诗句或地名</p>
    </div>

    <div v-else class="search-hint">
      <div class="hint-cards">
        <div class="hint-card" v-for="h in hints" :key="h.title">
          <p class="hint-icon">{{ h.icon }}</p>
          <p class="hint-title">{{ h.title }}</p>
          <p class="hint-desc">{{ h.desc }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { loadSearchIndex, loadWorks, loadPlaces, type SearchItem, type Place } from '../utils/data'
import StoryHeader from '../components/StoryHeader.vue'

const query = ref('')
const searched = ref(false)
const searchIndex = ref<SearchItem[]>([])
const places = ref<Place[]>([])
const worksMap = ref<Record<string, any>>({})
const selectedResult = ref<SearchItem | null>(null)
const detectedPlace = ref<Place | null>(null)

const results = ref<SearchItem[]>([])

const selectedWork = computed(() => {
  if (!selectedResult.value) return null
  return worksMap.value[selectedResult.value.work_id] || null
})

const quickQueries = ['烟花三月下扬州', '庐山', '长安', '黄河', '洞庭湖', '黄鹤楼', '江南', '玉门关']

const hints = [
  { icon: '诗', title: '搜索诗句', desc: '输入完整诗句，如"飞流直下三千尺"' },
  { icon: '地', title: '搜索地名', desc: '输入地名，如"扬州"、"庐山"、"长安"' },
  { icon: '人', title: '搜索作者', desc: '输入诗人名，如"李白"、"苏轼"' },
  { icon: '象', title: '搜索意象', desc: '输入意象词，如"月"、"酒"、"雁"' },
]

function onSearch() {
  searched.value = true
  const q = query.value.trim()
  if (!q) {
    results.value = []
    searched.value = false
    detectedPlace.value = null
    return
  }

  const place = places.value.find(p =>
    p.place_name === q ||
    p.place_name_normalized === q ||
    p.historical_name === q ||
    (p.aliases || []).includes(q) ||
    p.place_name.includes(q) ||
    q.includes(p.place_name) ||
    (p.aliases || []).some(a => a.includes(q) || q.includes(a))
  )
  detectedPlace.value = place || null
  
  results.value = searchIndex.value.filter(item => {
    return item.text.includes(q) || 
           item.title.includes(q) || 
           item.author.includes(q) ||
           item.places.some(p => p.includes(q) || q.includes(p))
  }).slice(0, 50)
}

function typeLabel(type: string): string {
  const labels: Record<string, string> = {
    city: '城市', mountain: '山岳', river: '河流', lake: '湖泊',
    pass: '关隘', building: '古迹', historic_region: '地域', other: '其他'
  }
  return labels[type] || ''
}

function quickSearch(q: string) {
  query.value = q
  onSearch()
}

function highlightText(text: string, q: string) {
  if (!q) return text
  const escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return text.replace(new RegExp(escaped, 'g'), `<mark class="highlight">${q}</mark>`)
}

function showResultDetail(r: SearchItem) {
  selectedResult.value = r
}

onMounted(async () => {
  try {
    const [index, works, placeData] = await Promise.all([
      loadSearchIndex(),
      loadWorks(),
      loadPlaces()
    ])
    searchIndex.value = index
    places.value = placeData
    for (const w of works) {
      worksMap.value[w.work_id] = w
    }
  } catch(e) {
    console.error('Failed to load search index:', e)
  }
})
</script>

<style scoped>
.search-view {
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

/* 搜索框 */
.search-box {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.search-input {
  flex: 1;
  padding: 0.8rem 1rem;
  font-size: 1rem;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-card);
  color: var(--color-ink);
  font-family: var(--font-serif);
  outline: none;
  transition: border-color 0.2s;
}

.search-input:focus {
  border-color: var(--color-accent);
}

.search-btn {
  padding: 0.8rem 1.5rem;
  font-size: 0.95rem;
  color: #fff;
  background: var(--color-accent);
  border-radius: var(--radius);
  letter-spacing: 0.1em;
}

.search-btn:hover {
  background: var(--color-ink);
}

/* 快捷搜索 */
.quick-search {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 1.5rem;
}

.quick-label {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
}

.quick-btn {
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
  color: var(--color-ink-light);
  border: 1px solid var(--color-border);
  border-radius: 12px;
  background: var(--color-card);
}

.quick-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

/* 地点定位 */
.locate-card {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin: 0.8rem 0 1.2rem;
  padding: 1rem 1.2rem;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
}

.locate-marker {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  flex-shrink: 0;
  font-size: 0.72rem;
  color: #fff;
  background: var(--color-accent);
  border-radius: 50%;
}

.locate-title {
  font-size: 1.1rem;
  color: var(--color-ink);
}

.locate-meta {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  margin-top: 0.1rem;
}

.locate-type {
  margin-left: 0.5rem;
  padding: 1px 7px;
  font-size: 0.7rem;
  color: #fff;
  background: var(--color-accent);
  border-radius: 9px;
}

/* 结果 */
.result-count {
  font-size: 0.85rem;
  color: var(--color-ink-muted);
  margin-bottom: 0.8rem;
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.result-item {
  padding: 1rem 1.2rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s;
}

.result-item:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-sm);
}

.result-item.selected {
  border-color: var(--color-accent);
  background: rgba(139, 58, 58, 0.04);
}

.result-detail {
  margin-top: 1rem;
  padding: 1.2rem 1.4rem;
  background: var(--color-bg-alt);
  border-left: 3px solid var(--color-accent);
  border-radius: 0 var(--radius) var(--radius) 0;
}

.result-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.8rem;
}

.result-detail-title {
  font-size: 1.1rem;
  color: var(--color-ink);
}

.result-detail-meta {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
}

.result-detail-close {
  font-size: 1.4rem;
  line-height: 1;
  color: var(--color-ink-muted);
  padding: 0 0.2rem;
}

.result-detail-close:hover {
  color: var(--color-ink);
}

.result-detail-text {
  font-family: var(--font-serif);
  font-size: 0.9rem;
  line-height: 1.9;
  color: var(--color-ink);
  white-space: pre-wrap;
  margin-bottom: 0.8rem;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.result-title {
  font-size: 0.95rem;
  color: var(--color-accent);
}

.result-author {
  font-size: 0.82rem;
  color: var(--color-ink-light);
}

.result-dynasty {
  font-size: 0.72rem;
  padding: 1px 8px;
  border-radius: 10px;
  color: #fff;
}

.dynasty-唐 { background: var(--color-tang); }
.dynasty-宋 { background: var(--color-song); }

.result-text {
  font-size: 0.88rem;
  color: var(--color-ink);
  line-height: 1.8;
  white-space: pre-wrap;
  margin-bottom: 0.5rem;
}

:deep(.highlight) {
  background: rgba(184, 134, 11, 0.25);
  color: var(--color-accent);
  padding: 0 2px;
  border-radius: 2px;
}

.result-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.tag {
  font-size: 0.72rem;
  padding: 1px 6px;
  border-radius: 8px;
}

.place-tag { background: rgba(139, 58, 58, 0.1); color: var(--color-accent); }
.theme-tag { background: rgba(74, 124, 89, 0.1); color: #4a7c59; }
.imagery-tag { background: rgba(46, 92, 110, 0.1); color: var(--color-song); }

/* 无结果 */
.no-results {
  text-align: center;
  padding: 3rem;
  color: var(--color-ink-muted);
}

.no-results-hint {
  font-size: 0.8rem;
  margin-top: 0.5rem;
}

/* 提示 */
.search-hint {
  margin-top: 2rem;
}

.hint-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}

.hint-card {
  text-align: center;
  padding: 1.5rem 1rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
}

.hint-icon {
  font-size: 1.5rem;
  color: var(--color-accent);
  margin-bottom: 0.5rem;
}

.hint-title {
  font-size: 0.9rem;
  color: var(--color-ink);
  margin-bottom: 0.3rem;
}

.hint-desc {
  font-size: 0.78rem;
  color: var(--color-ink-muted);
}

@media (max-width: 768px) {
  .hint-cards {
    grid-template-columns: 1fr;
  }
}
</style>
