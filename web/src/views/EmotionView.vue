<template>
  <div class="emotion-view">
    <StoryHeader
      chapter="04 · 山河如何成为情感"
      title="为什么不同地点会形成不同的文学记忆？"
      subtitle="一座山、一条河、一座关，反复出现在诗句里，也慢慢带上自己的情绪。"
      question="选择地点，看看它最常和哪些意象、主题一起出现。"
    />

    <div class="place-selector">
      <button
        v-for="name in placeOptions"
        :key="name"
        :class="['place-btn', { active: selectedPlace === name }]"
        @click="selectedPlace = name"
      >
        {{ name }}
      </button>
    </div>

    <div class="emotion-layout">
      <div class="emotion-map" ref="mapRef"></div>

      <div class="emotion-detail" v-if="selectedSummary">
        <h3 class="detail-title">{{ selectedPlace }}</h3>
        <p class="detail-sub">
          今{{ selectedSummary.modern_province }}{{ selectedSummary.modern_name ? ' · ' + selectedSummary.modern_name : '' }}
        </p>

        <div class="detail-stats">
          <div class="d-stat"><span class="d-num">{{ selectedSummary.mention_count }}</span><span class="d-label">次书写</span></div>
          <div class="d-stat"><span class="d-num text-tang">{{ selectedSummary.tang_count }}</span><span class="d-label">唐诗</span></div>
          <div class="d-stat"><span class="d-num text-song">{{ selectedSummary.song_count }}</span><span class="d-label">宋词</span></div>
        </div>

        <div class="detail-block" v-if="selectedImageryList.length">
          <h4 class="block-title">高频意象</h4>
          <div class="chip-list">
            <span v-for="i in selectedImageryList" :key="i.name" class="chip">{{ i.name }} <small>{{ i.count }}</small></span>
          </div>
        </div>

        <div class="detail-block" v-if="selectedThemeList.length">
          <h4 class="block-title">高频主题</h4>
          <div class="chip-list">
            <span v-for="t in selectedThemeList" :key="t.name" class="chip theme-chip">{{ t.name }} <small>{{ t.count }}</small></span>
          </div>
        </div>

        <div class="detail-block" v-if="selectedPoems.length">
          <h4 class="block-title">代表诗句</h4>
          <div class="poem-list">
            <div v-for="p in selectedPoems" :key="p.work_id" class="poem-item">
              <p class="poem-text">{{ p.text }}</p>
              <p class="poem-meta">—— {{ p.author }} ·《{{ p.title }}》</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="imagery-question">
      <h3>如果只看「{{ selectedImagery || '一种意象' }}」，中国会变成什么样？</h3>
      <p>点击一个意象，地图会只留下与它相关的文学地点。</p>
    </div>

    <div class="imagery-selector">
      <button
        v-for="name in imageryOptions"
        :key="name"
        :class="['imagery-btn', { active: selectedImagery === name }]"
        @click="selectedImagery = selectedImagery === name ? '' : name"
      >
        {{ name }}
      </button>
    </div>

    <p v-if="selectedImagery" class="imagery-copy">
      同一个「{{ selectedImagery }}」，在不同山河之间承载着不同的诗意。
    </p>

    <Finding
      title="地点与情感，在诗中互相塑造"
      :items="emotionFindingItems"
      note="意象与主题来自现有数据的规则统计，是文学关联的证据，不是对文化起源的判断。"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import * as echarts from 'echarts'
import { loadPlaceSummary, loadWorks, loadAnalysis } from '../utils/data'
import StoryHeader from '../components/StoryHeader.vue'
import Finding from '../components/Finding.vue'

const placeOptions = ['长安', '扬州', '庐山', '江南', '玉门关', '黄河']
const imageryOptions = ['月', '酒', '风', '雪', '舟', '雁', '柳']

const selectedPlace = ref('长安')
const selectedImagery = ref('')
const placeSummary = ref<Record<string, any>>({})
const allWorks = ref<any[]>([])
const analysisData = ref<any>({})
const mapRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const selectedSummary = computed(() => placeSummary.value[selectedPlace.value] || null)

const selectedImageryList = computed(() => {
  const data = analysisData.value.place_imagery?.[selectedPlace.value] || {}
  return Object.entries(data as Record<string, number>)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name, count]) => ({ name, count }))
})

const selectedThemeList = computed(() => {
  const data = analysisData.value.place_theme?.[selectedPlace.value] || {}
  return Object.entries(data as Record<string, number>)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 8)
    .map(([name, count]) => ({ name, count }))
})

const selectedPoems = computed(() => {
  return allWorks.value
    .filter(w => (w.place_mentions || []).includes(selectedPlace.value))
    .slice(0, 3)
    .map(w => ({
      work_id: w.work_id,
      author: w.author_name,
      title: w.title,
      text: w.text.split('\n')[0],
    }))
})

const emotionFindingItems = computed(() => {
  if (!selectedSummary.value) return []
  const imagery = selectedImageryList.value.slice(0, 3).map(i => i.name).join('、')
  const themes = selectedThemeList.value.slice(0, 3).map(t => t.name).join('、')
  return [
    `「${selectedPlace.value}」在当前数据中被书写 ${selectedSummary.value.mention_count} 次，其中唐诗 ${selectedSummary.value.tang_count} 次、宋词 ${selectedSummary.value.song_count} 次。`,
    `它与「${imagery || '—'}」等意象、与「${themes || '—'}」等主题高频共现。`,
    '因此，地点不只是坐标；它在一代代书写中，逐渐成为可以被辨认的情感记忆。'
  ]
})

function renderMap() {
  if (!chart || !mapRef.value || Object.keys(placeSummary.value).length === 0) return

  let data: any[] = []
  if (selectedImagery.value) {
    const placeImagery = analysisData.value.place_imagery || {}
    const entries = Object.entries(placeImagery as Record<string, Record<string, number>>)
      .filter(([, imgs]) => Number(imgs?.[selectedImagery.value]) > 0)
      .map(([name, imgs]) => {
        const ps = placeSummary.value[name]
        return ps
          ? { name, count: Number(imgs[selectedImagery.value]), ps }
          : null
      })
      .filter(Boolean)
      .sort((a: any, b: any) => b.count - a.count)
      .slice(0, 40) as any[]
    const max = Math.max(1, ...data.map((p: any) => p.count))
    data = data.map((p: any) => ({
      name: p.name,
      value: [p.ps.longitude, p.ps.latitude, p.count],
      symbolSize: 8 + (p.count / max) * 26,
      itemStyle: { color: '#8b3a3a', opacity: 0.86, borderColor: '#faf6ed', borderWidth: 1 },
      label: { show: p.count >= 4, position: 'right', formatter: p.name, color: '#8b3a3a', fontSize: 10, fontFamily: 'serif' },
      emphasis: { scale: 1.35 },
    }))
  } else if (selectedSummary.value) {
    data = [{
      name: selectedPlace.value,
      value: [selectedSummary.value.longitude, selectedSummary.value.latitude, selectedSummary.value.mention_count],
      symbolSize: 22,
      itemStyle: { color: '#8b3a3a', opacity: 0.92, borderColor: '#faf6ed', borderWidth: 2 },
      label: { show: true, position: 'right', formatter: selectedPlace.value, color: '#1a1a1a', fontSize: 13, fontFamily: 'serif' },
      emphasis: { scale: 1.3 },
    }]
  }

  chart.setOption({
    backgroundColor: 'transparent',
    animationDuration: 900,
    animationDurationUpdate: 900,
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => `${params.name} · ${params.value?.[2]} 次相关书写`,
      backgroundColor: 'rgba(250, 246, 237, 0.98)',
      borderColor: '#d4c9a8',
      textStyle: { color: '#1a1a1a', fontFamily: 'serif' },
    },
    geo: {
      map: 'china',
      roam: true,
      zoom: 1.2,
      center: [105, 36],
      itemStyle: { areaColor: '#e8dfca', borderColor: '#c9b896', borderWidth: 0.5 },
      emphasis: { itemStyle: { areaColor: '#ddd0b0' } },
    },
    series: [{
      type: 'scatter',
      coordinateSystem: 'geo',
      data,
      zlevel: 2,
    }],
  }, true)
}

async function loadChinaMap() {
  const resp = await fetch(`${import.meta.env.BASE_URL}data/china_map.json`)
  const geoJson = await resp.json()
  echarts.registerMap('china', geoJson)
}

let resizeHandler: () => void

onMounted(async () => {
  if (mapRef.value) {
    chart = echarts.init(mapRef.value)
    resizeHandler = () => chart?.resize()
    window.addEventListener('resize', resizeHandler)
  }

  try {
    const [ps, works, analysis] = await Promise.all([
      loadPlaceSummary(),
      loadWorks(),
      loadAnalysis()
    ])
    placeSummary.value = ps
    allWorks.value = works
    analysisData.value = analysis
  } catch (e) {
    console.error('Failed to load emotion data:', e)
  }

  try {
    await loadChinaMap()
  } catch (e) {
    console.error('Failed to load map:', e)
  }

  renderMap()
})

onUnmounted(() => {
  if (chart) chart.dispose()
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})

watch([selectedPlace, selectedImagery], () => renderMap())
</script>

<style scoped>
.emotion-view {
  max-width: 1280px;
  margin: 0 auto;
}

.place-selector,
.imagery-selector {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.3rem;
}

.place-btn,
.imagery-btn {
  min-width: 66px;
  padding: 0.45rem 0.9rem;
  font-size: 0.9rem;
  color: var(--color-ink-light);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 999px;
  transition: all 0.2s;
}

.place-btn:hover,
.imagery-btn:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.place-btn.active,
.imagery-btn.active {
  color: #fff;
  background: var(--color-accent);
  border-color: var(--color-accent);
}

.emotion-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) 380px;
  gap: 1.2rem;
}

.emotion-map {
  height: 560px;
  background: linear-gradient(135deg, #f5f1e8 0%, #ede5d0 100%);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.emotion-detail {
  padding: 1.4rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  max-height: 560px;
  overflow-y: auto;
}

.detail-title {
  font-size: 1.6rem;
  color: var(--color-ink);
}

.detail-sub {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  margin: 0.25rem 0 1rem;
}

.detail-stats {
  display: flex;
  gap: 1.2rem;
  margin-bottom: 1.2rem;
}

.d-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.d-num {
  font-size: 1.35rem;
  font-weight: 700;
  color: var(--color-accent);
}

.d-label {
  font-size: 0.72rem;
  color: var(--color-ink-muted);
}

.detail-block {
  margin-bottom: 1.1rem;
}

.block-title {
  margin-bottom: 0.5rem;
  font-size: 0.86rem;
  color: var(--color-ink);
  padding-left: 0.5rem;
  border-left: 3px solid var(--color-accent);
}

.chip-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.chip {
  padding: 2px 8px;
  font-size: 0.75rem;
  color: var(--color-accent);
  background: rgba(139, 58, 58, 0.08);
  border-radius: 10px;
}

.chip small {
  color: var(--color-ink-muted);
}

.theme-chip {
  color: var(--color-song);
  background: rgba(46, 92, 110, 0.08);
}

.poem-list {
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}

.poem-item {
  padding: 0.55rem 0.75rem;
  background: var(--color-bg-alt);
  border-radius: var(--radius);
}

.poem-text {
  font-size: 0.86rem;
  line-height: 1.7;
  color: var(--color-ink);
}

.poem-meta {
  margin-top: 0.2rem;
  font-size: 0.72rem;
  color: var(--color-ink-muted);
}

.imagery-question {
  margin: 2.2rem 0 1rem;
  text-align: center;
}

.imagery-question h3 {
  font-size: clamp(1.2rem, 3vw, 1.7rem);
  color: var(--color-ink);
  letter-spacing: 0.06em;
}

.imagery-question p {
  margin-top: 0.5rem;
  font-size: 0.82rem;
  color: var(--color-ink-muted);
}

.imagery-copy {
  margin: 0.4rem 0 1.2rem;
  text-align: center;
  font-size: 0.95rem;
  color: var(--color-accent);
  letter-spacing: 0.04em;
}

@media (max-width: 900px) {
  .emotion-layout {
    grid-template-columns: 1fr;
  }
  .emotion-map {
    height: 420px;
  }
  .emotion-detail {
    max-height: none;
  }
}
</style>
