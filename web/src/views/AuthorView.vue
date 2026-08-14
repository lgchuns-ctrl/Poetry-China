<template>
  <div class="author-view">
    <div class="section-header">
      <h2 class="section-title">诗人行迹</h2>
      <p class="section-desc">选择一位诗人，看见他的诗中中国</p>
    </div>

    <!-- 诗人选择 -->
    <div class="author-selector">
      <div class="author-tabs">
        <button v-for="a in availableAuthors" :key="a.name"
          :class="['author-tab', { active: selectedAuthor === a.name }, 'dynasty-' + a.dynasty]"
          @click="selectAuthor(a.name)">
          <span class="author-name">{{ a.name }}</span>
          <span class="author-count">{{ a.workCount }}首</span>
        </button>
      </div>
    </div>

    <div v-show="selectedAuthor" class="author-content">
      <!-- 诗人信息 -->
      <div class="author-info">
        <h3 class="author-title">{{ selectedAuthor }}</h3>
        <p class="author-meta" v-if="currentAuthorData">
          {{ currentAuthorData.dynasty }}代诗人 · {{ authorWorkCount }}首作品 · 覆盖{{ authorPlaceCount }}个地点
        </p>
        <p class="author-bio" v-if="currentAuthorData?.biography_summary">
          {{ currentAuthorData.biography_summary }}
        </p>
      </div>

      <!-- 诗人地图 -->
      <div class="author-map-container" ref="authorMapRef"></div>

      <!-- 统计数据 -->
      <div class="author-stats">
        <div class="stat-card">
          <span class="stat-value">{{ authorPlaceCount }}</span>
          <span class="stat-label">书写地点</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ authorTopImagery }}</span>
          <span class="stat-label">最常写意象</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ authorTopTheme }}</span>
          <span class="stat-label">主要主题</span>
        </div>
        <div class="stat-card">
          <span class="stat-value">{{ authorWorkCount }}</span>
          <span class="stat-label">收录作品</span>
        </div>
      </div>

      <!-- 地点列表 -->
      <div class="author-places">
        <h4 class="places-title">诗中山河</h4>
        <div class="places-grid">
          <div v-for="p in authorPlaces" :key="p.name" class="place-card" @click="showPlaceDetail(p)">
            <div class="place-card-header">
              <span class="place-card-name">{{ p.name }}</span>
              <span class="place-card-type" :class="'type-' + p.type">{{ typeLabel(p.type) }}</span>
            </div>
            <div class="place-card-bar">
              <div class="place-bar-fill" :style="{ width: p.pct + '%' }"></div>
            </div>
            <span class="place-card-count">{{ p.count }}次书写</span>
          </div>
        </div>
      </div>

      <transition name="slide-up">
        <div v-if="selectedPlaceDetail" class="place-detail-card">
          <div class="place-detail-header">
            <div>
              <h4 class="place-detail-title">{{ selectedPlaceDetail.name }}</h4>
              <p class="place-detail-meta">
                <span class="place-card-type" :class="'type-' + selectedPlaceDetail.type">{{ typeLabel(selectedPlaceDetail.type) }}</span>
                <span v-if="selectedPlaceInfo?.modern_province">今{{ selectedPlaceInfo.modern_province }}{{ selectedPlaceInfo.modern_name ? ' · ' + selectedPlaceInfo.modern_name : '' }}</span>
                <span>{{ selectedPlaceDetail.count }}次书写</span>
              </p>
            </div>
            <button class="place-detail-close" @click="selectedPlaceDetail = null">×</button>
          </div>
          <div class="place-detail-poems" v-if="selectedPlacePoems.length">
            <div v-for="p in selectedPlacePoems" :key="p.work_id" class="place-detail-poem">
              <p class="place-detail-poem-title">{{ p.title }}</p>
              <p class="place-detail-poem-text">{{ p.displayText }}</p>
            </div>
          </div>
        </div>
      </transition>

      <!-- 代表作品 -->
      <div class="author-poems" v-if="authorPoems.length">
        <h4 class="poems-title">代表作品</h4>
        <div class="poems-list">
          <div v-for="p in authorPoems" :key="p.work_id" class="poem-card">
            <p class="poem-title">{{ p.title }}</p>
            <p class="poem-text">{{ p.displayText }}</p>
            <div class="poem-tags" v-if="p.place_mentions.length || p.imagery.length">
              <span v-for="pl in p.place_mentions.slice(0, 3)" :key="pl" class="tag place-tag">{{ pl }}</span>
              <span v-for="im in p.imagery.slice(0, 3)" :key="im" class="tag imagery-tag">{{ im }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="!selectedAuthor" class="author-empty">
      <p>请选择一位诗人，查看他的诗中中国</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { loadAuthors, loadWorks, loadPlaceMentions, loadPlaceSummary, loadAnalysis, type Author } from '../utils/data'

const authors = ref<Author[]>([])
const allWorks = ref<any[]>([])
const allMentions = ref<any[]>([])
const placeSummary = ref<Record<string, any>>({})
const analysisData = ref<any>({})

const selectedAuthor = ref('')
const selectedPlaceDetail = ref<any>(null)
const authorMapRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

// 可用诗人列表（有地名提及且作品数较多）
const availableAuthors = computed(() => {
  const authorWorkCounts: Record<string, number> = {}
  const authorDynasty: Record<string, string> = {}
  
  for (const w of allWorks.value) {
    authorWorkCounts[w.author_name] = (authorWorkCounts[w.author_name] || 0) + 1
    authorDynasty[w.author_name] = w.dynasty
  }
  
  // 筛选有地名提及的诗人
  const authorsWithPlaces = new Set<string>()
  for (const w of allWorks.value) {
    if (w.place_mentions.length > 0) {
      authorsWithPlaces.add(w.author_name)
    }
  }
  
  const targetAuthors = ['李白', '杜甫', '王维', '白居易', '孟浩然', '杜牧', '李商隐',
    '王昌龄', '高适', '刘禹锡', '苏轼', '辛弃疾', '李清照', '柳永', '陆游', '欧阳修',
    '晏殊', '周邦彦', '秦观', '黄庭坚', '王安石', '贺铸', '张先', '范仲淹',
    '贾岛', '李贺', '韦应物', '岑参', '张继', '韦庄']
  
  const result = targetAuthors
    .filter(name => authorsWithPlaces.has(name) && authorWorkCounts[name])
    .map(name => ({
      name,
      workCount: authorWorkCounts[name],
      dynasty: authorDynasty[name]
    }))
    .sort((a, b) => {
      // 先按朝代分组，再按作品数排序
      if (a.dynasty !== b.dynasty) return a.dynasty === '唐' ? -1 : 1
      return b.workCount - a.workCount
    })
  
  return result.length > 0 ? result : Object.entries(authorWorkCounts)
    .filter(([name]) => authorsWithPlaces.has(name))
    .map(([name, count]) => ({ name, workCount: count, dynasty: authorDynasty[name] }))
    .sort((a, b) => b.workCount - a.workCount)
    .slice(0, 20)
})

const currentAuthorData = computed(() => {
  return authors.value.find(a => a.author_name === selectedAuthor.value)
})

const authorWorks = computed(() => {
  return allWorks.value.filter(w => w.author_name === selectedAuthor.value)
})

const authorWorkCount = computed(() => authorWorks.value.length)

const authorMentions = computed(() => {
  return allMentions.value.filter(m => m.author_name === selectedAuthor.value)
})

const authorPlaceCount = computed(() => {
  const places = new Set(authorMentions.value.map(m => m.place_name_normalized))
  return places.size
})

const authorPlaces = computed(() => {
  const placeCount: Record<string, { name: string; type: string; count: number }> = {}
  for (const m of authorMentions.value) {
    const name = m.place_name_normalized
    if (!placeCount[name]) {
      placeCount[name] = { name, type: m.place_type, count: 0 }
    }
    placeCount[name].count++
  }
  const result = Object.values(placeCount).sort((a, b) => b.count - a.count)
  const max = result[0]?.count || 1
  return result.map(p => ({ ...p, pct: Math.round(p.count / max * 100) }))
})

const authorPoems = computed(() => {
  return authorWorks.value
    .filter(w => w.place_mentions.length > 0)
    .slice(0, 10)
    .map(w => ({
      ...w,
      displayText: w.text.split('\n').slice(0, 4).join('\n')
    }))
})

const selectedPlaceInfo = computed(() => {
  if (!selectedPlaceDetail.value) return null
  const summary = placeSummary.value[selectedPlaceDetail.value.name]
  return summary || null
})

const selectedPlacePoems = computed(() => {
  if (!selectedPlaceDetail.value) return []
  return authorWorks.value
    .filter(w => w.place_mentions.includes(selectedPlaceDetail.value.name))
    .slice(0, 3)
    .map(w => ({
      work_id: w.work_id,
      title: w.title,
      displayText: w.text.split('\n').slice(0, 4).join('\n')
    }))
})

const authorTopImagery = computed(() => {
  const imgCount: Record<string, number> = {}
  for (const w of authorWorks.value) {
    for (const img of w.imagery) {
      imgCount[img] = (imgCount[img] || 0) + 1
    }
  }
  const sorted = Object.entries(imgCount).sort((a, b) => b[1] - a[1])
  return sorted[0]?.[0] || '—'
})

const authorTopTheme = computed(() => {
  const themeCount: Record<string, number> = {}
  for (const w of authorWorks.value) {
    for (const t of w.themes) {
      themeCount[t] = (themeCount[t] || 0) + 1
    }
  }
  const sorted = Object.entries(themeCount).sort((a, b) => b[1] - a[1])
  return sorted[0]?.[0] || '—'
})

function selectAuthor(name: string) {
  selectedAuthor.value = name
  nextTick(() => {
    renderAuthorMap()
  })
}

function typeLabel(type: string): string {
  const labels: Record<string, string> = {
    city: '城', mountain: '山', river: '河', lake: '湖',
    pass: '关', building: '迹', historic_region: '域', other: '他'
  }
  return labels[type] || type
}

function getSymbol(type: string): string {
  const symbols: Record<string, string> = {
    city: 'circle', mountain: 'triangle', river: 'diamond',
    lake: 'roundRect', pass: 'pin', building: 'rect',
    historic_region: 'circle', other: 'circle'
  }
  return symbols[type] || 'circle'
}

function getColor(type: string): string {
  const colors: Record<string, string> = {
    city: '#8b3a3a', mountain: '#4a7c59', river: '#2e5c6e',
    lake: '#5b8a72', pass: '#b8860b', building: '#7a6a5a',
    historic_region: '#9a8a7a', other: '#aaa'
  }
  return colors[type] || '#999'
}

function renderAuthorMap() {
  if (!chart && authorMapRef.value) {
    chart = echarts.init(authorMapRef.value)
    resizeHandler = () => chart?.resize()
    window.addEventListener('resize', resizeHandler)
  }
  if (!chart || !authorMapRef.value) return
  
  const places = authorPlaces.value
  if (places.length === 0) return
  
  const maxCount = places[0]?.count || 1
  
  // 从place_summary获取坐标
  const scatterData = places.map(p => {
    const ps = placeSummary.value[p.name]
    if (!ps) return null
    return {
      name: p.name,
      value: [ps.longitude, ps.latitude, p.count],
      itemStyle: {
        color: getColor(p.type),
        opacity: 0.85,
        borderColor: '#fff',
        borderWidth: 1,
      },
      symbol: getSymbol(p.type),
      symbolSize: 10 + (p.count / maxCount) * 25,
      placeData: p,
    }
  }).filter(d => d !== null)
  
  const dynasty = currentAuthorData.value?.dynasty || '唐'
  const dynastyColor = dynasty === '唐' ? '#8b3a3a' : '#2e5c6e'
  
  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const p = params.data?.placeData
        if (!p) return ''
        return `<div style="font-weight:600">${p.name}</div>
                <div style="font-size:12px;color:#666">${typeLabel(p.type)} · ${p.count}次书写</div>`
      },
      backgroundColor: 'rgba(250, 246, 237, 0.98)',
      borderColor: '#d4c9a8',
      borderWidth: 1,
      textStyle: { color: '#1a1a1a', fontFamily: 'serif' }
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      center: [105, 36],
      itemStyle: {
        areaColor: '#e8dfca',
        borderColor: '#c9b896',
        borderWidth: 0.5,
      },
      emphasis: {
        itemStyle: { areaColor: '#ddd0b0' },
      },
    },
    series: [{
      type: 'scatter',
      coordinateSystem: 'geo',
      data: scatterData,
      zlevel: 2,
      label: {
        show: true,
        position: 'right',
        formatter: (params: any) => params.data?.name || '',
        fontSize: 11,
        color: dynastyColor,
        fontFamily: 'serif',
      },
    }],
  }
  
  chart.setOption(option, true)
}

function showPlaceDetail(p: any) {
  selectedPlaceDetail.value = p
  if (chart) {
    chart.dispatchAction({ type: 'highlight', seriesIndex: 0, name: p.name })
  }
}

let resizeHandler: () => void

onMounted(async () => {
  // 加载地图
  try {
    const resp = await fetch(`${import.meta.env.BASE_URL}data/china_map.json`)
    const geoJson = await resp.json()
    echarts.registerMap('china', geoJson)
  } catch(e) {
    console.error('Failed to load map:', e)
  }
  
  try {
    const [au, w, m, ps, an] = await Promise.all([
      loadAuthors(),
      loadWorks(),
      loadPlaceMentions(),
      loadPlaceSummary(),
      loadAnalysis()
    ])
    authors.value = au
    allWorks.value = w
    allMentions.value = m
    placeSummary.value = ps
    analysisData.value = an
  } catch(e) {
    console.error('Failed to load author data:', e)
  }
  
  // 默认选择李白
  if (availableAuthors.value.length > 0) {
    selectAuthor(availableAuthors.value[0].name)
  }
})

onUnmounted(() => {
  if (chart) chart.dispose()
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})

watch(selectedAuthor, () => {
  nextTick(() => renderAuthorMap())
})
</script>

<style scoped>
.author-view {
  max-width: 1200px;
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

/* 诗人选择 */
.author-selector {
  margin-bottom: 1.5rem;
  overflow-x: auto;
}

.author-tabs {
  display: flex;
  gap: 0.5rem;
  padding: 0.5rem;
  min-width: max-content;
}

.author-tab {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 0.5rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-card);
  min-width: 70px;
  transition: all 0.2s;
}

.author-tab:hover {
  border-color: var(--color-accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.author-tab.active {
  border-width: 2px;
  box-shadow: var(--shadow-md);
}

.author-tab.dynasty-唐.active {
  border-color: var(--color-tang);
  background: rgba(139, 58, 58, 0.05);
}

.author-tab.dynasty-宋.active {
  border-color: var(--color-song);
  background: rgba(46, 92, 110, 0.05);
}

.author-name {
  font-size: 0.9rem;
  color: var(--color-ink);
}

.author-count {
  font-size: 0.7rem;
  color: var(--color-ink-muted);
  margin-top: 2px;
}

/* 诗人内容 */
.author-info {
  text-align: center;
  margin-bottom: 1.5rem;
  padding: 1.5rem;
  background: var(--color-card);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border-light);
}

.author-title {
  font-size: 1.5rem;
  color: var(--color-ink);
  margin-bottom: 0.3rem;
}

.author-meta {
  font-size: 0.82rem;
  color: var(--color-ink-muted);
  margin-bottom: 0.5rem;
}

.author-bio {
  font-size: 0.8rem;
  color: var(--color-ink-light);
  line-height: 1.8;
  max-width: 700px;
  margin: 0 auto;
  text-align: left;
}

.author-map-container {
  width: 100%;
  height: 500px;
  background: linear-gradient(135deg, #f5f1e8 0%, #ede5d0 100%);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  margin-bottom: 1.5rem;
}

/* 统计 */
.author-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  text-align: center;
  padding: 1rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius);
}

.stat-value {
  display: block;
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-accent);
}

.stat-label {
  display: block;
  font-size: 0.75rem;
  color: var(--color-ink-muted);
  margin-top: 0.2rem;
}

/* 地点 */
.places-title, .poems-title {
  font-size: 1.1rem;
  color: var(--color-ink);
  margin-bottom: 1rem;
  padding-left: 0.5rem;
  border-left: 3px solid var(--color-accent);
}

.places-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.8rem;
  margin-bottom: 2rem;
}

.place-card {
  padding: 0.8rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius);
  cursor: pointer;
  transition: all 0.2s;
}

.place-card:hover {
  border-color: var(--color-accent);
  transform: translateY(-2px);
  box-shadow: var(--shadow-sm);
}

.place-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.5rem;
}

.place-card-name {
  font-size: 0.9rem;
  color: var(--color-ink);
}

.place-card-type {
  font-size: 0.7rem;
  padding: 1px 6px;
  border-radius: 8px;
  color: #fff;
}

.place-card-bar {
  height: 6px;
  background: var(--color-bg-alt);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 0.3rem;
}

.place-bar-fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: 3px;
  transition: width 0.5s ease;
}

.place-card-count {
  font-size: 0.72rem;
  color: var(--color-ink-muted);
}

.place-detail-card {
  margin-bottom: 2rem;
  padding: 1.2rem 1.4rem;
  background: var(--color-bg-alt);
  border-left: 3px solid var(--color-accent);
  border-radius: 0 var(--radius) var(--radius) 0;
}

.place-detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 0.8rem;
}

.place-detail-title {
  font-size: 1.1rem;
  color: var(--color-ink);
}

.place-detail-meta {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;
  font-size: 0.78rem;
  color: var(--color-ink-muted);
  margin-top: 0.25rem;
}

.place-detail-close {
  font-size: 1.4rem;
  line-height: 1;
  color: var(--color-ink-muted);
  padding: 0 0.2rem;
}

.place-detail-close:hover {
  color: var(--color-ink);
}

.place-detail-poems {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.place-detail-poem {
  padding: 0.6rem 0.8rem;
  background: var(--color-card);
  border-radius: var(--radius);
}

.place-detail-poem-title {
  font-size: 0.85rem;
  color: var(--color-accent);
  margin-bottom: 0.2rem;
}

.place-detail-poem-text {
  font-size: 0.82rem;
  color: var(--color-ink);
  line-height: 1.8;
  white-space: pre-wrap;
}

/* 作品 */
.poems-list {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.poem-card {
  padding: 1rem 1.2rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius);
}

.poem-title {
  font-size: 0.95rem;
  color: var(--color-accent);
  margin-bottom: 0.3rem;
}

.poem-text {
  font-size: 0.88rem;
  color: var(--color-ink);
  line-height: 1.8;
  white-space: pre-wrap;
}

.poem-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin-top: 0.5rem;
}

.tag {
  font-size: 0.7rem;
  padding: 1px 6px;
  border-radius: 8px;
}

.place-tag {
  background: rgba(139, 58, 58, 0.1);
  color: var(--color-accent);
}

.imagery-tag {
  background: rgba(74, 124, 89, 0.1);
  color: #4a7c59;
}

.type-city { background: #8b3a3a; }
.type-mountain { background: #4a7c59; }
.type-river { background: #2e5c6e; }
.type-lake { background: #5b8a72; }
.type-pass { background: #b8860b; }
.type-building { background: #7a6a5a; }
.type-historic_region { background: #9a8a7a; }

.author-empty {
  text-align: center;
  padding: 4rem 2rem;
  color: var(--color-ink-muted);
}

@media (max-width: 768px) {
  .author-stats {
    grid-template-columns: repeat(2, 1fr);
  }
  .author-map-container {
    height: 350px;
  }
  .places-grid {
    grid-template-columns: 1fr;
  }
}
</style>
