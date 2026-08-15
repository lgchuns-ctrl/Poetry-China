<template>
  <div class="compare-view">
    <StoryHeader
      chapter="02 · 从长安到江南"
      title="诗词也在迁徙"
      subtitle="从唐到宋，文学地图的重心发生了什么变化？"
      question="切换唐与宋，观察同一片山河上的文学光点如何移动。"
    />

    <div class="mode-switch">
      <button :class="['mode-btn', 'tang-mode', { active: mode === 'tang' }]" @click="mode = 'tang'">唐诗</button>
      <button :class="['mode-btn', 'both-mode', { active: mode === 'both' }]" @click="mode = 'both'">唐 ↔ 宋</button>
      <button :class="['mode-btn', 'song-mode', { active: mode === 'song' }]" @click="mode = 'song'">宋词</button>
    </div>

    <div class="compare-layout">
      <div class="dynasty-map" ref="mapContainerRef"></div>

      <aside class="compare-aside">
        <h3 class="aside-title">{{ mode === 'tang' ? '唐诗的高频地点' : mode === 'song' ? '宋词的高频地点' : '唐与宋的高频地点' }}</h3>
        <ol class="rank-list">
          <li v-for="(item, i) in currentRank" :key="item.name">
            <span class="rank-no">{{ i + 1 }}</span>
            <span class="rank-name">{{ item.name }}</span>
            <span class="rank-count">{{ item.count }}</span>
          </li>
        </ol>
        <p class="aside-note">圆点大小表示该地点在当前朝代数据中的书写次数。</p>
      </aside>
    </div>

    <Finding
      label="我们发现"
      :title="dynastyFindingTitle"
      :items="dynastyFindingItems"
      note="这是文学数据中的统计现象，不等于对历史因果的证明；它可以与唐宋时期的政治、经济和文化空间变化形成一种值得关注的呼应。"
    />

    <div class="core-line">
      从长安到江南，改变的不只是地名，也是诗词观看世界的方式。
    </div>

    <div class="secondary-section">
      <div class="secondary-tabs">
        <button
          v-for="t in secondaryTabs"
          :key="t.id"
          :class="['secondary-tab', { active: activeTab === t.id }]"
          @click="activeTab = t.id"
        >
          {{ t.label }}
        </button>
      </div>

      <div v-if="activeTab === 'types'" class="type-comparison">
        <div v-for="t in typeComparison" :key="t.type" class="type-row">
          <div class="type-label">{{ typeLabel(t.type) }}</div>
          <div class="type-bars">
            <div class="type-bar-item tang">
              <span class="type-count">{{ t.tang }}</span>
              <div class="type-bar-track"><div class="type-bar-fill tang-fill" :style="{ width: t.tangPct + '%' }"></div></div>
            </div>
            <div class="type-bar-item song">
              <div class="type-bar-track"><div class="type-bar-fill song-fill" :style="{ width: t.songPct + '%' }"></div></div>
              <span class="type-count">{{ t.song }}</span>
            </div>
          </div>
        </div>
        <div class="type-legend"><span class="legend-tang">唐诗</span><span class="legend-song">宋词</span></div>
      </div>

      <div v-if="activeTab === 'imagery'" class="imagery-comparison">
        <div class="imagery-grid">
          <div v-for="img in imageryComparison" :key="img.name" class="imagery-cell">
            <div class="imagery-name">{{ img.name }}</div>
            <div class="imagery-bars">
              <div class="img-bar tang">
                <div class="img-fill tang-fill" :style="{ height: img.tangPct + '%' }"></div>
                <span class="img-count">{{ img.tang }}</span>
              </div>
              <div class="img-bar song">
                <div class="img-fill song-fill" :style="{ height: img.songPct + '%' }"></div>
                <span class="img-count">{{ img.song }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="activeTab === 'themes'" class="theme-comparison">
        <div v-for="t in themeComparison" :key="t.name" class="theme-cmp-row">
          <span class="theme-cmp-label">{{ t.name }}</span>
          <div class="theme-cmp-bars">
            <div class="theme-cmp-bar tang">
              <div class="theme-cmp-fill tang-fill" :style="{ width: t.tangPct + '%' }"><span>{{ t.tang }}</span></div>
            </div>
            <div class="theme-cmp-bar song">
              <div class="theme-cmp-fill song-fill" :style="{ width: t.songPct + '%' }"><span>{{ t.song }}</span></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { loadPlaceSummary, loadWorks } from '../utils/data'
import StoryHeader from '../components/StoryHeader.vue'
import Finding from '../components/Finding.vue'

const mode = ref<'tang' | 'song' | 'both'>('tang')
const activeTab = ref('types')
const placeSummary = ref<Record<string, any>>({})
const allWorks = ref<any[]>([])
const mapContainerRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const secondaryTabs = [
  { id: 'types', label: '地点类型' },
  { id: 'imagery', label: '意象' },
  { id: 'themes', label: '主题' },
]

const tangRank = computed(() => {
  return Object.entries(placeSummary.value)
    .map(([name, ps]) => ({ name, count: Number(ps.tang_count) || 0 }))
    .filter(p => p.count > 0)
    .sort((a, b) => b.count - a.count)
    .slice(0, 8)
})

const songRank = computed(() => {
  return Object.entries(placeSummary.value)
    .map(([name, ps]) => ({ name, count: Number(ps.song_count) || 0 }))
    .filter(p => p.count > 0)
    .sort((a, b) => b.count - a.count)
    .slice(0, 8)
})

const currentRank = computed(() => {
  if (mode.value === 'tang') return tangRank.value
  if (mode.value === 'song') return songRank.value
  const combined = new Map<string, number>()
  for (const p of [...tangRank.value, ...songRank.value]) combined.set(p.name, p.count)
  return [...combined.entries()].map(([name, count]) => ({ name, count })).sort((a, b) => b.count - a.count).slice(0, 8)
})

const dynastyFindingTitle = computed(() => {
  if (mode.value === 'tang') return '唐诗的文学光点，更多落在北方与内陆'
  if (mode.value === 'song') return '宋词的文学光点，更多向江南与东南移动'
  return '两张文学地图的重心，并不相同'
})

const dynastyFindingItems = computed(() => {
  if (mode.value === 'tang') {
    return [
      `唐诗中书写频率最高的地点是「${tangRank.value[0]?.name}」（${tangRank.value[0]?.count} 次），紧随其后的是「${tangRank.value[1]?.name}」和「${tangRank.value[2]?.name}」。`,
      '长安、洛阳、黄河、洞庭湖、湘江、塞北等地点，在唐诗中形成了强烈的存在感。',
      '这些地点大多与都城、行旅、山河与边塞经验联系在一起。'
    ]
  }
  if (mode.value === 'song') {
    return [
      `宋词中书写频率最高的地点是「${songRank.value[0]?.name}」（${songRank.value[0]?.count} 次），西湖、扬州、苏州等江南地点进入前列。`,
      '江南从一种泛称，越来越频繁地成为具体生活、风景与情感的书写对象。',
      '这并不意味着宋词不再写北方，而是文学空间的构成方式发生了变化。'
    ]
  }
  return [
    `唐诗前列以「${tangRank.value[0]?.name}」「${tangRank.value[1]?.name}」为代表；宋词前列则以「${songRank.value[0]?.name}」「${songRank.value[1]?.name}」为代表。`,
    '两代诗人在同一片山河上，投下的是不同亮度、不同重心的文学光点。'
  ]
})

const typeComparison = computed(() => {
  const stats: Record<string, { type: string; tang: number; song: number }> = {}
  for (const ps of Object.values(placeSummary.value)) {
    const type = ps.place_type || 'other'
    if (!stats[type]) stats[type] = { type, tang: 0, song: 0 }
    stats[type].tang += Number(ps.tang_count) || 0
    stats[type].song += Number(ps.song_count) || 0
  }
  const list = Object.values(stats).filter(t => t.tang > 0 || t.song > 0)
  const maxTang = Math.max(1, ...list.map(t => t.tang))
  const maxSong = Math.max(1, ...list.map(t => t.song))
  return list.map(t => ({
    ...t,
    tangPct: Math.round((t.tang / maxTang) * 100),
    songPct: Math.round((t.song / maxSong) * 100),
  }))
})

const imageryComparison = computed(() => {
  const stats: Record<string, { name: string; tang: number; song: number }> = {}
  for (const w of allWorks.value) {
    const key = w.dynasty === '唐' ? 'tang' : 'song'
    for (const img of w.imagery || []) {
      if (!stats[img]) stats[img] = { name: img, tang: 0, song: 0 }
      stats[img][key as 'tang' | 'song']++
    }
  }
  const top = Object.values(stats).sort((a, b) => (b.tang + b.song) - (a.tang + a.song)).slice(0, 12)
  const max = Math.max(1, ...top.map(img => Math.max(img.tang, img.song)))
  return top.map(img => ({
    ...img,
    tangPct: Math.round((img.tang / max) * 100),
    songPct: Math.round((img.song / max) * 100),
  }))
})

const themeComparison = computed(() => {
  const stats: Record<string, { name: string; tang: number; song: number }> = {}
  for (const w of allWorks.value) {
    const key = w.dynasty === '唐' ? 'tang' : 'song'
    for (const theme of w.themes || []) {
      if (theme === '其他') continue
      if (!stats[theme]) stats[theme] = { name: theme, tang: 0, song: 0 }
      stats[theme][key as 'tang' | 'song']++
    }
  }
  const top = Object.values(stats).sort((a, b) => (b.tang + b.song) - (a.tang + a.song)).slice(0, 10)
  const max = Math.max(1, ...top.map(t => Math.max(t.tang, t.song)))
  return top.map(t => ({
    ...t,
    tangPct: Math.round((t.tang / max) * 100),
    songPct: Math.round((t.song / max) * 100),
  }))
})

function typeLabel(type: string): string {
  const labels: Record<string, string> = {
    city: '城市', mountain: '山岳', river: '河流', lake: '湖泊',
    pass: '关隘', building: '古迹', historic_region: '地域', other: '其他'
  }
  return labels[type] || type
}

function renderCompareMap() {
  if (!chart || !mapContainerRef.value || Object.keys(placeSummary.value).length === 0) return

  const list = Object.entries(placeSummary.value)
    .map(([name, ps]) => ({ name, ...ps }))
    .filter(p => (mode.value === 'song' ? Number(p.song_count) > 0 : Number(p.tang_count) > 0))

  const buildSeries = (key: 'tang' | 'song', color: string) => {
    const values = list.filter(p => Number(p[`${key}_count`]) > 0)
    const max = Math.max(1, ...values.map(p => Number(p[`${key}_count`])))
    return {
      name: key === 'tang' ? '唐诗' : '宋词',
      type: 'scatter' as const,
      coordinateSystem: 'geo' as const,
      data: values.map(p => ({
        name: p.name,
        value: [p.longitude, p.latitude, Number(p[`${key}_count`])],
        symbolSize: 9 + (Number(p[`${key}_count`]) / max) * 28,
        itemStyle: {
          color,
          opacity: mode.value === 'both' ? 0.72 : 0.88,
          borderColor: '#faf6ed',
          borderWidth: 1,
          shadowBlur: 10,
          shadowColor: 'rgba(0,0,0,0.12)',
        },
        label: {
          show: Number(p[`${key}_count`]) >= (key === 'song' ? 15 : 60),
          position: 'right',
          formatter: p.name,
          fontSize: 11,
          color,
          fontFamily: 'serif',
        },
        emphasis: { scale: 1.35 },
      })),
    }
  }

  const series: any[] = []
  if (mode.value === 'tang' || mode.value === 'both') series.push(buildSeries('tang', '#8b3a3a'))
  if (mode.value === 'song' || mode.value === 'both') series.push(buildSeries('song', '#2e5c6e'))

  chart.setOption({
    backgroundColor: 'transparent',
    animationDuration: 1000,
    animationDurationUpdate: 1200,
    animationEasingUpdate: 'cubicOut',
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => `${params.seriesName} · ${params.name} · ${params.value?.[2]} 次书写`,
      backgroundColor: 'rgba(250, 246, 237, 0.98)',
      borderColor: '#d4c9a8',
      textStyle: { color: '#1a1a1a', fontFamily: 'serif' },
    },
    legend: mode.value === 'both' ? { bottom: 0, textStyle: { color: '#1a1a1a', fontFamily: 'serif' } } : { show: false },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.18,
      center: [105, 36],
      itemStyle: {
        areaColor: '#e8dfca',
        borderColor: '#c9b896',
        borderWidth: 0.5,
      },
      emphasis: { itemStyle: { areaColor: '#ddd0b0' } },
    },
    series,
  }, true)
}

async function loadChinaMap() {
  const resp = await fetch(`${import.meta.env.BASE_URL}data/china_map.json`)
  const geoJson = await resp.json()
  echarts.registerMap('china', geoJson)
}

let resizeHandler: () => void

onMounted(async () => {
  if (mapContainerRef.value) {
    chart = echarts.init(mapContainerRef.value)
    resizeHandler = () => chart?.resize()
    window.addEventListener('resize', resizeHandler)
  }

  try {
    const [ps, works] = await Promise.all([loadPlaceSummary(), loadWorks()])
    placeSummary.value = ps
    allWorks.value = works
  } catch (e) {
    console.error('Failed to load comparison data:', e)
  }

  try {
    await loadChinaMap()
  } catch (e) {
    console.error('Failed to load map:', e)
  }

  renderCompareMap()
})

onUnmounted(() => {
  if (chart) chart.dispose()
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})

watch(mode, () => renderCompareMap())
</script>

<style scoped>
.compare-view {
  max-width: 1280px;
  margin: 0 auto;
}

.mode-switch {
  display: flex;
  justify-content: center;
  gap: 0.6rem;
  margin-bottom: 1.4rem;
}

.mode-btn {
  min-width: 92px;
  padding: 0.55rem 1rem;
  font-size: 0.9rem;
  letter-spacing: 0.1em;
  color: var(--color-ink-light);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  transition: all 0.25s;
}

.mode-btn:hover {
  transform: translateY(-1px);
  border-color: var(--color-accent);
}

.tang-mode.active {
  color: #fff;
  background: var(--color-tang);
  border-color: var(--color-tang);
}

.song-mode.active {
  color: #fff;
  background: var(--color-song);
  border-color: var(--color-song);
}

.both-mode.active {
  color: #fff;
  background: var(--color-ink);
  border-color: var(--color-ink);
}

.compare-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 320px;
  gap: 1.2rem;
}

.dynasty-map {
  height: 640px;
  background: linear-gradient(135deg, #f5f1e8 0%, #ede5d0 100%);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.compare-aside {
  padding: 1.3rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.aside-title {
  font-size: 0.95rem;
  color: var(--color-ink);
  margin-bottom: 1rem;
}

.rank-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.rank-list li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.86rem;
}

.rank-no {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  font-size: 0.68rem;
  color: var(--color-accent);
  border: 1px solid var(--color-border);
  border-radius: 50%;
}

.rank-name {
  flex: 1;
  color: var(--color-ink-light);
}

.rank-count {
  color: var(--color-ink-muted);
  font-size: 0.78rem;
}

.aside-note {
  margin-top: 1rem;
  font-size: 0.72rem;
  line-height: 1.7;
  color: var(--color-ink-muted);
}

.core-line {
  margin: 2rem auto 1.5rem;
  max-width: 820px;
  text-align: center;
  font-size: clamp(1.2rem, 3vw, 1.8rem);
  line-height: 1.7;
  color: var(--color-accent);
  letter-spacing: 0.06em;
}

.secondary-section {
  margin-top: 2rem;
  padding: 1.5rem 1.8rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
}

.secondary-tabs {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.secondary-tab {
  padding: 0.35rem 0.9rem;
  font-size: 0.82rem;
  color: var(--color-ink-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-bg);
}

.secondary-tab.active {
  color: #fff;
  background: var(--color-ink);
  border-color: var(--color-ink);
}

.type-comparison {
  max-width: 680px;
  margin: 0 auto;
}

.type-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  margin-bottom: 0.5rem;
}

.type-label {
  width: 60px;
  font-size: 0.82rem;
  color: var(--color-ink);
  text-align: right;
}

.type-bars {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.type-bar-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
}

.type-bar-item.song { flex-direction: row-reverse; }
.type-bar-track { flex: 1; height: 14px; background: var(--color-bg-alt); border-radius: 3px; overflow: hidden; }
.type-bar-fill { height: 100%; transition: width 0.8s ease; }
.type-count { width: 32px; font-size: 0.74rem; color: var(--color-ink-muted); text-align: center; }
.tang-fill { background: var(--color-tang); }
.song-fill { background: var(--color-song); }
.type-legend { display: flex; justify-content: center; gap: 1.6rem; margin-top: 1rem; font-size: 0.8rem; }
.legend-tang { color: var(--color-tang); }
.legend-song { color: var(--color-song); }

.imagery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 1rem;
}

.imagery-cell { text-align: center; }
.imagery-name { font-size: 1rem; color: var(--color-ink); margin-bottom: 0.5rem; }
.imagery-bars { display: flex; gap: 4px; justify-content: center; align-items: flex-end; height: 120px; }
.img-bar { width: 24px; height: 100%; display: flex; flex-direction: column; justify-content: flex-end; align-items: center; position: relative; }
.img-fill { width: 100%; border-radius: 2px 2px 0 0; min-height: 2px; transition: height 0.8s ease; }
.img-count { position: absolute; top: -16px; font-size: 0.7rem; color: var(--color-ink-muted); }

.theme-comparison {
  max-width: 700px;
  margin: 0 auto;
}

.theme-cmp-row { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.45rem; }
.theme-cmp-label { width: 52px; text-align: right; font-size: 0.8rem; color: var(--color-ink); }
.theme-cmp-bars { flex: 1; display: flex; flex-direction: column; gap: 2px; }
.theme-cmp-bar { height: 16px; background: var(--color-bg-alt); border-radius: 2px; overflow: hidden; }
.theme-cmp-fill { height: 100%; display: flex; align-items: center; justify-content: flex-end; padding-right: 6px; color: #fff; font-size: 0.7rem; min-width: 20px; transition: width 0.8s ease; }

@media (max-width: 900px) {
  .compare-layout { grid-template-columns: 1fr; }
  .dynasty-map { height: 460px; }
  .imagery-grid { grid-template-columns: repeat(4, 1fr); }
}
</style>
