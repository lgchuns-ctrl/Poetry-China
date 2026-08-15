<template>
  <div class="map-view">
    <StoryHeader
      chapter="01 · 山河有记忆"
      title="哪些地方被中国诗词反复书写？"
      subtitle="有些地方，因为被一代代诗人不断书写，成为中国人的共同文学记忆。"
      question="诗词最爱写哪里？"
    />

    <!-- 筛选栏 -->
    <div class="filter-bar">
      <div class="filter-group">
        <span class="filter-label">朝代</span>
        <div class="filter-options">
          <button v-for="d in dynasties" :key="d.value" 
            :class="['filter-btn', { active: filters.dynasty === d.value }]"
            @click="setFilter('dynasty', d.value)">{{ d.label }}</button>
        </div>
      </div>
      
      <div class="filter-group" v-if="topAuthors.length">
        <span class="filter-label">诗人</span>
        <select class="filter-select" v-model="filters.author" @change="onFilterChange">
          <option value="">全部诗人</option>
          <option v-for="a in topAuthors" :key="a" :value="a">{{ a }}</option>
        </select>
      </div>

      <div class="filter-group">
        <span class="filter-label">主题</span>
        <select class="filter-select" v-model="filters.theme" @change="onFilterChange">
          <option value="">全部主题</option>
          <option v-for="t in themes" :key="t" :value="t">{{ t }}</option>
        </select>
      </div>

      <div class="filter-group">
        <span class="filter-label">意象</span>
        <select class="filter-select" v-model="filters.imagery" @change="onFilterChange">
          <option value="">全部意象</option>
          <option v-for="i in topImagery" :key="i" :value="i">{{ i }}</option>
        </select>
      </div>

      <button v-if="hasActiveFilter" class="filter-reset" @click="resetFilters">重置</button>
    </div>

    <!-- 地图容器 -->
    <div class="map-container" ref="mapContainerRef"></div>

    <!-- 地图图例 -->
    <div class="map-legend">
      <div class="legend-item" v-for="lt in legendTypes" :key="lt.type">
        <span class="legend-symbol" :class="'sym-' + lt.type"></span>
        <span class="legend-label">{{ lt.label }}</span>
      </div>
    </div>

    <!-- 高频地点 -->
    <div class="top-places-strip" v-if="topPlacesBySummary.length">
      <span class="top-places-label">诗词最爱写</span>
      <button
        v-for="(p, i) in topPlacesBySummary.slice(0, 8)"
        :key="p.name"
        class="top-place-chip"
        :class="{ 'is-top': i === 0 }"
        @click="focusPlace(p.name)"
      >
        <span class="top-place-rank">{{ i + 1 }}</span>
        <span>{{ p.name }}</span>
        <small>{{ p.mention_count }}次</small>
      </button>
    </div>

    <Finding
      title="一座城，如何成为一个时代的文学中心？"
      :items="chapterFindingItems"
      note="这是基于现有数据的统计现象，不等同于对历史地理事实的因果判断。"
    />

    <!-- 地点详情 -->
    <transition name="slide-up">
      <div v-if="selectedPlace" class="place-detail" ref="detailRef">
        <div class="detail-header">
          <div>
            <h3 class="detail-title">{{ selectedPlace.place_name }}</h3>
            <p class="detail-sub">
              <span :class="'type-badge type-' + selectedPlace.place_type">{{ typeLabel(selectedPlace.place_type) }}</span>
              今{{ selectedPlace.modern_province }}{{ selectedPlace.modern_name ? ' · ' + selectedPlace.modern_name : '' }}
            </p>
          </div>
          <button class="detail-close" @click="selectedPlace = null">×</button>
        </div>

        <div class="detail-stats">
          <div class="d-stat">
            <span class="d-num">{{ selectedPlace.mention_count }}</span>
            <span class="d-label">次书写</span>
          </div>
          <div class="d-stat">
            <span class="d-num">{{ selectedPlace.authors?.length || 0 }}</span>
            <span class="d-label">位诗人</span>
          </div>
          <div class="d-stat">
            <span class="d-num text-tang">{{ selectedPlace.tang_count }}</span>
            <span class="d-label">唐诗</span>
          </div>
          <div class="d-stat">
            <span class="d-num text-song">{{ selectedPlace.song_count }}</span>
            <span class="d-label">宋词</span>
          </div>
        </div>

        <!-- 代表诗人 -->
        <div class="detail-section" v-if="placeAuthors.length">
          <h4 class="detail-section-title">代表诗人</h4>
          <div class="author-chips">
            <span v-for="a in placeAuthors" :key="a.name" class="author-chip" :class="'dynasty-' + a.dynasty">
              {{ a.name }} <small>{{ a.count }}首</small>
            </span>
          </div>
        </div>

        <!-- 代表诗句 -->
        <div class="detail-section" v-if="placePoems.length">
          <h4 class="detail-section-title">代表诗句</h4>
          <div class="poem-list">
            <div v-for="p in placePoems" :key="p.work_id" class="poem-item">
              <p class="poem-line">{{ p.text }}</p>
              <p class="poem-meta">—— {{ p.author }} ·《{{ p.title }}》</p>
            </div>
          </div>
        </div>

        <!-- 意象 -->
        <div class="detail-section" v-if="placeImagery.length">
          <h4 class="detail-section-title">高频意象</h4>
          <div class="imagery-chips">
            <span v-for="i in placeImagery" :key="i.name" class="imagery-chip">{{ i.name }} {{ i.count }}</span>
          </div>
        </div>

        <!-- 主题 -->
        <div class="detail-section" v-if="placeThemes.length">
          <h4 class="detail-section-title">主题分布</h4>
          <div class="theme-bars">
            <div v-for="t in placeThemes" :key="t.name" class="theme-bar">
              <span class="theme-name">{{ t.name }}</span>
              <div class="bar-track">
                <div class="bar-fill" :style="{ width: t.pct + '%' }"></div>
              </div>
              <span class="theme-count">{{ t.count }}</span>
            </div>
          </div>
        </div>

        <!-- 定位置信度 -->
        <div class="detail-section" v-if="selectedPlace.mapping_level">
          <p class="confidence-note">
            <span class="confidence-label">定位精度：</span>
            <span :class="'confidence-level level-' + selectedPlace.mapping_level">{{ confidenceLabel(selectedPlace.mapping_level) }}</span>
          </p>
        </div>
      </div>
    </transition>

    <!-- 第一个典型故事：长安 -->
    <transition name="slide-up">
      <CaseStudy
        v-if="showChangAnStory"
        kicker="第一个典型故事 · 长安诗境"
        title="长安：一座被反复书写的城"
        :lead="changanLead"
        :stats="changanStats"
        question="可是这张文学地图并没有一直保持不变。"
      >
        <div class="case-grid">
          <div class="case-column">
            <h4 class="case-subtitle">代表诗人</h4>
            <div class="author-chips">
              <span v-for="a in changanAuthors" :key="a.name" class="author-chip" :class="'dynasty-' + a.dynasty">
                {{ a.name }} <small>{{ a.count }}首</small>
              </span>
            </div>

            <h4 class="case-subtitle">高频意象</h4>
            <div class="imagery-chips">
              <span v-for="i in changanImagery" :key="i.name" class="imagery-chip">{{ i.name }} {{ i.count }}</span>
            </div>

            <h4 class="case-subtitle">高频主题</h4>
            <div class="theme-bars">
              <div v-for="t in changanThemes" :key="t.name" class="theme-bar">
                <span class="theme-name">{{ t.name }}</span>
                <div class="bar-track"><div class="bar-fill" :style="{ width: t.pct + '%' }"></div></div>
                <span class="theme-count">{{ t.count }}</span>
              </div>
            </div>
          </div>

          <div class="case-column">
            <h4 class="case-subtitle">代表作品</h4>
            <div class="poem-list">
              <div v-for="p in changanPoems" :key="p.work_id" class="poem-item">
                <p class="poem-line">{{ p.text }}</p>
                <p class="poem-meta">—— {{ p.author }} ·《{{ p.title }}》</p>
              </div>
            </div>
          </div>
        </div>
      </CaseStudy>
    </transition>

    <div v-if="!showChangAnStory" class="story-hint">
      点击地图上的「长安」，进入第一个典型故事。
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed, watch, nextTick } from 'vue'
import * as echarts from 'echarts'
import { loadPlaceSummary, loadWorks, loadPlaceMentions, loadAnalysis } from '../utils/data'
import StoryHeader from '../components/StoryHeader.vue'
import Finding from '../components/Finding.vue'
import CaseStudy from '../components/CaseStudy.vue'

const mapContainerRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const placeSummary = ref<Record<string, any>>({})
const allWorks = ref<any[]>([])
const allMentions = ref<any[]>([])
const analysisData = ref<any>({})

const selectedPlace = ref<any>(null)
const detailRef = ref<HTMLElement>()

const filters = ref({
  dynasty: 'all' as 'all' | '唐' | '宋',
  author: '',
  theme: '',
  imagery: ''
})

const dynasties = [
  { value: 'all', label: '全部' },
  { value: '唐', label: '唐诗' },
  { value: '宋', label: '宋词' },
]

const legendTypes = [
  { type: 'city', label: '城市' },
  { type: 'mountain', label: '山岳' },
  { type: 'river', label: '河流' },
  { type: 'lake', label: '湖泊' },
  { type: 'pass', label: '关隘' },
  { type: 'building', label: '古迹' },
  { type: 'historic_region', label: '地域' },
]

const themesList = ['山水', '田园', '边塞', '送别', '思乡', '怀古', '咏史', '爱情', '羁旅', '饮酒', '节令', '咏物', '其他']
const topImageryList = ['月', '风', '云', '雨', '雪', '酒', '舟', '雁', '花', '柳', '松', '竹', '梅', '山', '水', '江', '楼', '剑', '马', '鹤']

const topAuthors = computed(() => {
  if (!analysisData.value.top_authors) return []
  return analysisData.value.top_authors.slice(0, 20).map((a: any) => a.author)
})

const topPlacesBySummary = computed(() => {
  return Object.entries(placeSummary.value)
    .map(([name, ps]) => ({ name, ...ps }))
    .sort((a, b) => b.mention_count - a.mention_count)
})

const chapterFindingItems = computed(() => {
  const top = topPlacesBySummary.value.slice(0, 3)
  if (top.length < 3) return []
  return [
    `当前数据集中，被书写最多的是「${top[0].name}」，共 ${top[0].mention_count} 次；其次是「${top[1].name}」 ${top[1].mention_count} 次、「${top[2].name}」 ${top[2].mention_count} 次。`,
    '文学地点的分布高度不均匀：少数城市、山脉与河流反复出现，另一些地方则几乎不被书写。',
    '这说明诗词中的“山河”不是平均分配的地理知识，而是被文学传统不断选择和强化的记忆。'
  ]
})

const changanSummary = computed(() => placeSummary.value['长安'] || null)
const showChangAnStory = computed(() => selectedPlace.value?.place_name === '长安' && Boolean(changanSummary.value))

const changanAuthors = computed(() => {
  if (!changanSummary.value) return []
  const mentions = allMentions.value.filter(m => m.place_name_normalized === '长安')
  const count: Record<string, { name: string; count: number; dynasty: string }> = {}
  for (const m of mentions) {
    if (!count[m.author_name]) count[m.author_name] = { name: m.author_name, count: 0, dynasty: m.dynasty }
    count[m.author_name].count++
  }
  return Object.values(count).sort((a, b) => b.count - a.count).slice(0, 8)
})

const changanImagery = computed(() => {
  const data = analysisData.value.place_imagery?.['长安'] || {}
  return Object.entries(data as Record<string, number>)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([name, count]) => ({ name, count }))
})

const changanThemes = computed(() => {
  const data = analysisData.value.place_theme?.['长安'] || {}
  const entries = Object.entries(data as Record<string, number>).sort((a, b) => b[1] - a[1]).slice(0, 5)
  const total = entries.reduce((sum, [, count]) => sum + count, 0)
  return entries.map(([name, count]) => ({
    name,
    count,
    pct: total > 0 ? Math.round((count / total) * 100) : 0
  }))
})

const changanPoems = computed(() => {
  if (!changanSummary.value) return []
  const ids = new Set(changanSummary.value.work_ids || [])
  const works = allWorks.value.filter(w => ids.has(w.work_id))
  const preferred = ['李白', '杜甫', '王维', '岑参', '白居易']
  const picked: any[] = []
  for (const author of preferred) {
    const w = works.find(work => work.author_name === author)
    if (w) picked.push(w)
    if (picked.length >= 3) break
  }
  return picked.map(w => ({
    work_id: w.work_id,
    author: w.author_name,
    title: w.title,
    text: w.text.split('\n')[0]
  }))
})

const changanLead = computed(() => {
  if (!changanSummary.value) return ''
  const themes = changanThemes.value.map(t => t.name).slice(0, 4).join('、')
  return `长安不仅是一座城市。在当前数据里，它反复与${themes || '羁旅、思乡、咏史、节令'}等主题一起出现。`
})

const changanStats = computed(() => {
  if (!changanSummary.value) return []
  return [
    { value: changanSummary.value.mention_count, label: '次书写' },
    { value: `${changanSummary.value.tang_count} / ${changanSummary.value.song_count}`, label: '唐诗 / 宋词' },
    { value: changanSummary.value.authors?.length || 0, label: '涉及诗人' },
    { value: changanSummary.value.work_ids?.length || 0, label: '收录作品' },
  ]
})

function focusPlace(name: string) {
  const place = topPlacesBySummary.value.find(p => p.name === name)
  if (!place) return
  selectedPlace.value = { ...place, place_name: place.name }
  nextTick(() => detailRef.value?.scrollIntoView({ behavior: 'smooth', block: 'nearest' }))
}

const themes = computed(() => themesList)
const topImagery = computed(() => topImageryList)

const hasActiveFilter = computed(() => {
  return filters.value.dynasty !== 'all' || filters.value.author || filters.value.theme || filters.value.imagery
})

function setFilter(key: keyof typeof filters.value, value: string) {
  (filters.value as Record<string, string>)[key] = value
  onFilterChange()
}

function onFilterChange() {
  renderMap()
}

function resetFilters() {
  filters.value = { dynasty: 'all', author: '', theme: '', imagery: '' }
  renderMap()
}

// 过滤后的地点数据
const filteredPlaces = computed(() => {
  const result: any[] = []
  
  for (const [name, ps] of Object.entries(placeSummary.value)) {
    let count = ps.mention_count
    let tangCount = ps.tang_count
    let songCount = ps.song_count
    let authors = [...ps.authors]
    let workIds = [...ps.work_ids]
    
    // 朝代过滤
    if (filters.value.dynasty === '唐') {
      count = tangCount
      songCount = 0
    } else if (filters.value.dynasty === '宋') {
      count = songCount
      tangCount = 0
    }
    
    if (count === 0) continue
    
    // 诗人过滤
    if (filters.value.author) {
      const filteredMentions = allMentions.value.filter(m => 
        m.place_name_normalized === name && m.author_name === filters.value.author
      )
      count = filteredMentions.length
      tangCount = filteredMentions.filter(m => m.dynasty === '唐').length
      songCount = filteredMentions.filter(m => m.dynasty === '宋').length
      authors = [...new Set(filteredMentions.map(m => m.author_name))]
      workIds = [...new Set(filteredMentions.map(m => m.work_id))]
      
      if (count === 0) continue
    }
    
    // 主题过滤
    if (filters.value.theme) {
      const filteredWorkIds = allWorks.value
        .filter(w => workIds.includes(w.work_id) && w.themes.includes(filters.value.theme))
        .map(w => w.work_id)
      const filteredMentions = allMentions.value.filter(m => 
        m.place_name_normalized === name && filteredWorkIds.includes(m.work_id)
      )
      count = filteredMentions.length
      tangCount = filteredMentions.filter(m => m.dynasty === '唐').length
      songCount = filteredMentions.filter(m => m.dynasty === '宋').length
      workIds = filteredWorkIds
      
      if (count === 0) continue
    }
    
    // 意象过滤
    if (filters.value.imagery) {
      const filteredWorkIds = allWorks.value
        .filter(w => workIds.includes(w.work_id) && w.imagery.includes(filters.value.imagery))
        .map(w => w.work_id)
      const filteredMentions = allMentions.value.filter(m => 
        m.place_name_normalized === name && filteredWorkIds.includes(m.work_id)
      )
      count = filteredMentions.length
      workIds = filteredWorkIds
      
      if (count === 0) continue
    }
    
    result.push({
      ...ps,
      place_name: name,
      mention_count: count,
      tang_count: tangCount,
      song_count: songCount,
      authors,
      work_ids: workIds,
    })
  }
  
  return result.sort((a, b) => b.mention_count - a.mention_count)
})

// 地点详情数据
const placeAuthors = computed(() => {
  if (!selectedPlace.value) return []
  const name = selectedPlace.value.place_name
  const mentions = allMentions.value.filter(m => m.place_name_normalized === name || m.place_name === name)
  const authorCount: Record<string, { name: string; count: number; dynasty: string }> = {}
  for (const m of mentions) {
    if (!authorCount[m.author_name]) {
      authorCount[m.author_name] = { name: m.author_name, count: 0, dynasty: m.dynasty }
    }
    authorCount[m.author_name].count++
  }
  return Object.values(authorCount).sort((a, b) => b.count - a.count).slice(0, 12)
})

const placePoems = computed(() => {
  if (!selectedPlace.value) return []
  const name = selectedPlace.value.place_name
  const mentions = allMentions.value.filter(m => m.place_name_normalized === name || m.place_name === name)
  const workIds = [...new Set(mentions.map(m => m.work_id))].slice(0, 5)
  const works = allWorks.value.filter(w => workIds.includes(w.work_id))
  
  return works.map(w => {
    const text = w.text.split('\n')[0]
    return { work_id: w.work_id, text, author: w.author_name, title: w.title }
  }).slice(0, 5)
})

const placeImagery = computed(() => {
  if (!selectedPlace.value) return []
  const name = selectedPlace.value.place_name
  const mentions = allMentions.value.filter(m => m.place_name_normalized === name || m.place_name === name)
  const workIds = mentions.map(m => m.work_id)
  const works = allWorks.value.filter(w => workIds.includes(w.work_id))
  const imgCount: Record<string, number> = {}
  for (const w of works) {
    for (const img of w.imagery) {
      imgCount[img] = (imgCount[img] || 0) + 1
    }
  }
  return Object.entries(imgCount).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([name, count]) => ({ name, count }))
})

const placeThemes = computed(() => {
  if (!selectedPlace.value) return []
  const name = selectedPlace.value.place_name
  const mentions = allMentions.value.filter(m => m.place_name_normalized === name || m.place_name === name)
  const workIds = mentions.map(m => m.work_id)
  const works = allWorks.value.filter(w => workIds.includes(w.work_id))
  const themeCount: Record<string, number> = {}
  let total = 0
  for (const w of works) {
    for (const t of w.themes) {
      themeCount[t] = (themeCount[t] || 0) + 1
      total++
    }
  }
  return Object.entries(themeCount).sort((a, b) => b[1] - a[1]).slice(0, 8).map(([name, count]) => ({
    name, count, pct: total > 0 ? Math.round(count / total * 100) : 0
  }))
})

function typeLabel(type: string): string {
  const labels: Record<string, string> = {
    city: '城市', mountain: '山岳', river: '河流', lake: '湖泊',
    pass: '关隘', building: '古迹', historic_region: '地域', other: '其他'
  }
  return labels[type] || type
}

function confidenceLabel(level: string): string {
  const labels: Record<string, string> = {
    exact: '精确', city: '城市级', county: '县级',
    province: '省级', approximate: '近似', region: '区域级', unknown: '未知'
  }
  return labels[level] || level
}

// 地点类型符号
function getSymbol(type: string): string {
  const symbols: Record<string, string> = {
    city: 'circle', mountain: 'triangle', river: 'diamond',
    lake: 'roundRect', pass: 'pin', building: 'rect',
    historic_region: 'circle', other: 'circle'
  }
  return symbols[type] || 'circle'
}

function getColor(type: string, dynasty?: string): string {
  if (dynasty === '唐') return '#8b3a3a'
  if (dynasty === '宋') return '#2e5c6e'
  
  const colors: Record<string, string> = {
    city: '#8b3a3a', mountain: '#4a7c59', river: '#2e5c6e',
    lake: '#5b8a72', pass: '#b8860b', building: '#7a6a5a',
    historic_region: '#9a8a7a', other: '#aaa'
  }
  return colors[type] || '#999'
}

function getSize(count: number, max: number): number {
  const min = 8
  const range = 30
  if (max === 0) return min
  return min + (count / max) * range
}

async function renderMap() {
  if (!chart || !mapContainerRef.value) return
  
  const places = filteredPlaces.value
  if (places.length === 0) {
    chart.setOption({ series: [] })
    return
  }
  
  const maxCount = Math.max(...places.map(p => p.mention_count))
  
  // 构建散点数据
  const scatterData = places.map(p => ({
    name: p.place_name,
    value: [p.longitude, p.latitude, p.mention_count],
    itemStyle: {
      color: getColor(p.place_type, filters.value.dynasty === 'all' ? undefined : filters.value.dynasty),
      opacity: 0.85,
      borderColor: '#fff',
      borderWidth: 1,
      shadowBlur: 10,
      shadowColor: 'rgba(0,0,0,0.15)'
    },
    symbol: getSymbol(p.place_type),
    symbolSize: getSize(p.mention_count, maxCount),
    placeData: p,
  }))
  
  const option: echarts.EChartsOption = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const p = params.data?.placeData
        if (!p) return ''
        return `<div style="font-size:14px;font-weight:600;margin-bottom:4px">${p.place_name}</div>
                <div style="font-size:12px;color:#666">${typeLabel(p.place_type)} · 今${p.modern_province || ''}</div>
                <div style="margin-top:6px">
                  <span style="color:#8b3a3a">唐诗 ${p.tang_count}</span> · 
                  <span style="color:#2e5c6e">宋词 ${p.song_count}</span>
                </div>
                <div style="font-size:12px;color:#999;margin-top:2px">${p.mention_count}次书写 · ${p.authors?.length || 0}位诗人</div>`
      },
      backgroundColor: 'rgba(250, 246, 237, 0.98)',
      borderColor: '#d4c9a8',
      borderWidth: 1,
      padding: [8, 12],
      textStyle: { color: '#1a1a1a', fontFamily: 'serif' }
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      center: [105, 36],
      label: { show: false },
      itemStyle: {
        areaColor: '#e8dfca',
        borderColor: '#c9b896',
        borderWidth: 0.5,
      },
      emphasis: {
        itemStyle: {
          areaColor: '#ddd0b0',
        },
        label: { show: false }
      },
      select: {
        itemStyle: { areaColor: '#e8dfca' }
      }
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'geo',
        data: scatterData,
        zlevel: 2,
        emphasis: {
          scale: 1.5,
          itemStyle: {
            borderWidth: 2,
            shadowBlur: 20,
          }
        },
        label: {
          show: true,
          position: 'right',
          formatter: (params: any) => {
            const p = params.data?.placeData
            if (!p) return ''
            return p.mention_count >= 5 ? p.place_name : ''
          },
          fontSize: 11,
          color: '#333',
          fontFamily: 'serif',
          offset: [4, 0],
        },
      }
    ]
  }
  
  chart.setOption(option, true)
  
  // 点击事件
  chart.off('click')
  chart.on('click', (params: any) => {
    if (params.data?.placeData) {
      selectedPlace.value = params.data.placeData
      nextTick(() => {
        detailRef.value?.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
      })
    }
  })
}

async function loadMapData() {
  try {
    const resp = await fetch(`${import.meta.env.BASE_URL}data/china_map.json`)
    const geoJson = await resp.json()
    echarts.registerMap('china', geoJson)
  } catch(e) {
    console.error('Failed to load map:', e)
  }
}

let resizeHandler: () => void

onMounted(async () => {
  // 初始化ECharts
  if (mapContainerRef.value) {
    chart = echarts.init(mapContainerRef.value)
    resizeHandler = () => chart?.resize()
    window.addEventListener('resize', resizeHandler)
  }
  
  // 加载地图数据
  await loadMapData()
  
  // 加载数据
  try {
    const [ps, works, mentions, analysis] = await Promise.all([
      loadPlaceSummary(),
      loadWorks(),
      loadPlaceMentions(),
      loadAnalysis()
    ])
    placeSummary.value = ps
    allWorks.value = works
    allMentions.value = mentions
    analysisData.value = analysis
  } catch(e) {
    console.error('Failed to load data:', e)
  }
  
  renderMap()
})

onUnmounted(() => {
  if (chart) chart.dispose()
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})

watch(filters, () => renderMap(), { deep: true })
</script>

<style scoped>
.map-view {
  position: relative;
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

/* 筛选栏 */
.filter-bar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  margin-bottom: 1rem;
  box-shadow: var(--shadow-sm);
}

.filter-group {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.filter-label {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  white-space: nowrap;
}

.filter-options {
  display: flex;
  gap: 0.3rem;
}

.filter-btn {
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
  color: var(--color-ink-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-bg);
}

.filter-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.filter-btn.active {
  background: var(--color-ink);
  color: #fff;
  border-color: var(--color-ink);
}

.filter-select {
  padding: 0.3rem 0.6rem;
  font-size: 0.8rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-bg);
  color: var(--color-ink);
  font-family: var(--font-serif);
  cursor: pointer;
}

.filter-reset {
  padding: 0.3rem 0.8rem;
  font-size: 0.8rem;
  color: var(--color-accent);
  border: 1px solid var(--color-accent);
  border-radius: var(--radius);
}

.filter-reset:hover {
  background: var(--color-accent);
  color: #fff;
}

/* 地图 */
.map-container {
  width: 100%;
  height: 600px;
  background: linear-gradient(135deg, #f5f1e8 0%, #ede5d0 100%);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

/* 图例 */
.map-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
  padding: 0.8rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.legend-symbol {
  width: 12px;
  height: 12px;
  border-radius: 2px;
}

.sym-city { background: #8b3a3a; border-radius: 50%; }
.sym-mountain { background: #4a7c59; transform: rotate(45deg); }
.sym-river { background: #2e5c6e; }
.sym-lake { background: #5b8a72; border-radius: 6px; }
.sym-pass { background: #b8860b; clip-path: polygon(50% 0%, 100% 100%, 0% 100%); }
.sym-building { background: #7a6a5a; }
.sym-historic_region { background: #9a8a7a; border-radius: 50%; border: 2px dashed #9a8a7a; }

.legend-label {
  font-size: 0.75rem;
  color: var(--color-ink-muted);
}

/* 高频地点 */
.top-places-strip {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  margin: 1.4rem 0 0.4rem;
}

.top-places-label {
  margin-right: 0.4rem;
  font-size: 0.78rem;
  color: var(--color-ink-muted);
  letter-spacing: 0.1em;
}

.top-place-chip {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.32rem 0.65rem;
  font-size: 0.8rem;
  color: var(--color-ink-light);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 999px;
}

.top-place-chip:hover,
.top-place-chip.is-top {
  color: var(--color-accent);
  border-color: var(--color-accent);
}

.top-place-rank {
  font-size: 0.68rem;
  color: var(--color-ink-muted);
}

.top-place-chip small {
  font-size: 0.7rem;
  color: var(--color-ink-muted);
}

/* 长安故事 */
.case-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 1.2rem;
}

.case-subtitle {
  font-size: 0.88rem;
  color: var(--color-ink);
  margin: 1rem 0 0.5rem;
  padding-left: 0.5rem;
  border-left: 3px solid var(--color-accent);
}

.case-subtitle:first-child {
  margin-top: 0;
}

.story-hint {
  margin: 1.4rem 0 0;
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  letter-spacing: 0.04em;
}

/* 地点详情 */
.place-detail {
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border-light);
}

.detail-title {
  font-size: 1.5rem;
  color: var(--color-ink);
  margin-bottom: 0.3rem;
}

.detail-sub {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.type-badge {
  display: inline-block;
  padding: 1px 8px;
  font-size: 0.72rem;
  border-radius: 10px;
  color: #fff;
}

.type-city { background: #8b3a3a; }
.type-mountain { background: #4a7c59; }
.type-river { background: #2e5c6e; }
.type-lake { background: #5b8a72; }
.type-pass { background: #b8860b; }
.type-building { background: #7a6a5a; }
.type-historic_region { background: #9a8a7a; }

.detail-close {
  font-size: 1.5rem;
  color: var(--color-ink-muted);
  line-height: 1;
  padding: 0 0.3rem;
}

.detail-close:hover {
  color: var(--color-ink);
}

.detail-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 1.5rem;
}

.d-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.d-num {
  font-size: 1.5rem;
  font-weight: 700;
}

.d-label {
  font-size: 0.75rem;
  color: var(--color-ink-muted);
}

.detail-section {
  margin-bottom: 1.2rem;
}

.detail-section-title {
  font-size: 0.9rem;
  color: var(--color-ink);
  margin-bottom: 0.5rem;
  padding-left: 0.5rem;
  border-left: 3px solid var(--color-accent);
}

.author-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.author-chip {
  padding: 2px 8px;
  font-size: 0.78rem;
  border-radius: 12px;
  background: var(--color-bg-alt);
}

.author-chip small {
  color: var(--color-ink-muted);
}

.dynasty-唐 { border-left: 2px solid #8b3a3a; }
.dynasty-宋 { border-left: 2px solid #2e5c6e; }

.poem-list {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.poem-item {
  padding: 0.5rem 0.8rem;
  background: var(--color-bg-alt);
  border-radius: var(--radius);
}

.poem-line {
  font-size: 0.88rem;
  color: var(--color-ink);
  line-height: 1.7;
}

.poem-meta {
  font-size: 0.72rem;
  color: var(--color-ink-muted);
  margin-top: 0.2rem;
}

.imagery-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
}

.imagery-chip {
  padding: 2px 8px;
  font-size: 0.75rem;
  border-radius: 10px;
  background: rgba(139, 58, 58, 0.1);
  color: var(--color-accent);
}

.theme-bars {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.theme-bar {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-name {
  width: 50px;
  font-size: 0.78rem;
  color: var(--color-ink-light);
}

.bar-track {
  flex: 1;
  height: 8px;
  background: var(--color-bg-alt);
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: var(--color-accent);
  border-radius: 4px;
  transition: width 0.5s ease;
}

.theme-count {
  width: 24px;
  text-align: right;
  font-size: 0.75rem;
  color: var(--color-ink-muted);
}

.confidence-note {
  font-size: 0.78rem;
  color: var(--color-ink-muted);
}

.confidence-level {
  padding: 1px 6px;
  border-radius: 8px;
  font-size: 0.72rem;
}

.level-exact { background: #4a7c59; color: #fff; }
.level-city { background: #4a7c59; color: #fff; }
.level-county { background: #5b8a72; color: #fff; }
.level-province { background: #b8860b; color: #fff; }
.level-approximate { background: #b8860b; color: #fff; }
.level-region { background: #7a6a5a; color: #fff; }
.level-unknown { background: #ccc; }

@media (max-width: 768px) {
  .map-container { height: 400px; }
  .filter-bar { gap: 0.5rem; padding: 0.6rem; }
  .detail-stats { gap: 1rem; }
  .d-num { font-size: 1.2rem; }
  .case-grid { grid-template-columns: 1fr; }
}
</style>
