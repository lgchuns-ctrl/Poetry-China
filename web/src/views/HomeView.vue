<template>
  <div class="home">
    <!-- 序章：提出问题 -->
    <div class="hero" ref="heroRef">
      <div class="hero-bg">
        <div class="ink-splash ink-1"></div>
        <div class="ink-splash ink-2"></div>
        <div class="ink-splash ink-3"></div>
      </div>

      <div class="hero-content" :class="{ visible: heroVisible }">
        <h1 class="hero-title">
          <span class="title-char" v-for="(ch, i) in '诗行中国'" :key="i" :style="{ animationDelay: i * 0.13 + 's' }">{{ ch }}</span>
        </h1>
        <p class="hero-subtitle">唐诗宋词中的山河地图</p>
        <p class="hero-slogan">从长安到江南，诗词也在迁徙。</p>

        <div class="hero-question">
          <p>为什么唐诗反复书写长安与洛阳，而到了宋词，江南、杭州、扬州越来越频繁地进入文字？</p>
          <p>为什么李白、杜甫和苏轼，面对同一片山河，却写出了完全不同的中国？</p>
        </div>

        <p v-if="totalWorksExact" class="hero-data-line">
          我们将 {{ totalWorksExact }} 首唐诗宋词重新放回地图，试图寻找诗人、山河与时代之间的关系。
        </p>

        <div class="hero-stats" v-if="stats">
          <div class="stat-item">
            <span class="stat-num">{{ formatNum(stats.total_works) }}</span>
            <span class="stat-label">诗词</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">{{ formatNum(stats.total_authors) }}</span>
            <span class="stat-label">诗人</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">{{ formatNum(stats.total_places) }}</span>
            <span class="stat-label">文学地点</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">{{ formatNum(stats.total_mentions) }}</span>
            <span class="stat-label">山河书写</span>
          </div>
        </div>

        <button class="hero-btn" @click="enterMap">
          <span>进入诗词山河</span>
        </button>
      </div>
    </div>

    <!-- 序章地图：一张文学中国开始显现 -->
    <div class="prologue">
      <div class="prologue-header">
        <span class="prologue-chapter">序章 · 诗从哪里落下？</span>
        <h2 class="prologue-title">当两万余首诗词重新落回地图</h2>
        <p class="prologue-desc">一张并不均匀的文学中国开始显现。</p>
      </div>
      <div class="prologue-map" ref="mapRef"></div>
      <p class="prologue-caption">圆点越大，表示这一地点在诗词中被书写的次数越多。地图正在缓慢亮起。</p>
    </div>

    <!-- 我们发现 -->
    <div class="findings" v-if="findings.length">
      <div class="section-header">
        <h2 class="section-title">我们从两万余首诗词里，看到了什么？</h2>
        <p class="section-desc">以下是作品继续展开的四条线索</p>
      </div>
      <div class="findings-grid">
        <div v-for="(item, i) in findings" :key="i" class="home-finding">
          <span class="home-finding-index">0{{ i + 1 }}</span>
          <h3 class="home-finding-title">{{ item.title }}</h3>
          <p class="home-finding-text">{{ item.text }}</p>
        </div>
      </div>
    </div>

    <!-- 先听几句诗 -->
    <div class="flowing-poems">
      <div class="section-header">
        <h2 class="section-title">诗如何落在山河之间</h2>
        <p class="section-desc">从一句诗开始，看见地点、诗人与情感被同时写下</p>
      </div>
      <div class="poem-flow-container">
        <div v-for="(item, idx) in displayPoems" :key="idx" class="poem-flow-card" :style="{ animationDelay: idx * 0.08 + 's' }">
          <p class="poem-text">{{ item.text }}</p>
          <p class="poem-author">—— {{ item.author }} ·《{{ item.title }}》</p>
          <p class="poem-place">
            <span class="place-icon" :class="'icon-' + item.type">{{ item.typeLabel }}</span>
            {{ item.place }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { loadMetadata, loadPlaceSummary, loadAnalysis } from '../utils/data'

const stats = ref<any>(null)
const heroVisible = ref(false)
const placeSummary = ref<Record<string, any>>({})
const analysisData = ref<any>({})
const mapRef = ref<HTMLElement>()
let mapChart: echarts.ECharts | null = null

const totalWorksExact = computed(() => {
  const n = Number(stats.value?.total_works)
  return Number.isFinite(n) ? n.toLocaleString('zh-CN') : ''
})

const topPlaces = computed(() => {
  return Object.entries(placeSummary.value)
    .map(([name, ps]) => ({ name, ...ps }))
    .sort((a, b) => b.mention_count - a.mention_count)
})

const topPlace = computed(() => topPlaces.value[0])

const dynastyTop = computed(() => {
  const tang = [...topPlaces.value].sort((a, b) => b.tang_count - a.tang_count)[0]
  const song = [...topPlaces.value].sort((a, b) => b.song_count - a.song_count)[0]
  return { tang, song }
})

const findings = computed(() => {
  if (!topPlace.value) return []

  const changanImagery = analysisData.value.place_imagery?.['长安']
    ? Object.entries(analysisData.value.place_imagery['长安'] as Record<string, number>)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 3)
        .map(([name]) => name)
    : ['日', '风', '月']

  const libaiPlaces = analysisData.value.author_diversity?.['李白']?.unique_places
  const dufuPlaces = analysisData.value.author_diversity?.['杜甫']?.unique_places
  const tang = dynastyTop.value.tang
  const song = dynastyTop.value.song

  return [
    {
      title: '有些城市，成为时代性的文学中心',
      text: `当前数据集中，地图上最常被书写的地点是「${topPlace.value.name}」，共 ${topPlace.value.mention_count} 次。一个地点被反复书写，便开始进入一代人的共同记忆。`
    },
    {
      title: '从唐到宋，文学地图发生了明显变化',
      text: tang && song
        ? `唐诗中书写频率最高的是「${tang.name}」（${tang.tang_count} 次）；宋词中最高的是「${song.name}」（${song.song_count} 次）。地理重心正在移动。`
        : '从唐到宋，高频文学地点的构成正在发生变化。'
    },
    {
      title: '不同诗人的“诗中中国”差异巨大',
      text: `仅统计作品中的地点提及，杜甫涉及 ${dufuPlaces ?? '—'} 个不同地点，李白涉及 ${libaiPlaces ?? '—'} 个。两个诗人的山河，并不重合。`
    },
    {
      title: '山河不仅被书写，也被赋予情感',
      text: `在「长安」的书写中，${changanImagery.join('、')} 是最常见的高频意象。地点开始与特定意象、主题和情感建立稳定联系。`
    }
  ]
})

// 经典诗句用于引出下一章，不是统计结论
const selectedPoems = [
  { text: '故人西辞黄鹤楼，烟花三月下扬州', author: '李白', title: '黄鹤楼送孟浩然之广陵', place: '扬州', type: 'city', typeLabel: '城' },
  { text: '长安一片月，万户捣衣声', author: '李白', title: '子夜四时歌·秋歌', place: '长安', type: 'city', typeLabel: '城' },
  { text: '飞流直下三千尺，疑是银河落九天', author: '李白', title: '望庐山瀑布', place: '庐山', type: 'mountain', typeLabel: '山' },
  { text: '羌笛何须怨杨柳，春风不度玉门关', author: '王之涣', title: '凉州词', place: '玉门关', type: 'pass', typeLabel: '关' },
  { text: '日出江花红胜火，春来江水绿如蓝', author: '白居易', title: '忆江南', place: '江南', type: 'historic_region', typeLabel: '域' },
  { text: '欲把西湖比西子，淡妆浓抹总相宜', author: '苏轼', title: '饮湖上初晴后雨', place: '西湖', type: 'lake', typeLabel: '湖' },
  { text: '星垂平野阔，月涌大江流', author: '杜甫', title: '旅夜书怀', place: '长江', type: 'river', typeLabel: '河' },
  { text: '黄河远上白云间，一片孤城万仞山', author: '王之涣', title: '凉州词', place: '黄河', type: 'river', typeLabel: '河' },
]

const displayPoems = computed(() => selectedPoems.slice(0, 8))

function formatNum(n: number) {
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  return n.toLocaleString('zh-CN')
}

function enterMap() {
  const el = document.getElementById('map')
  if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function renderPrologueMap() {
  if (!mapChart || !mapRef.value || topPlaces.value.length === 0) return

  const places = topPlaces.value.slice(0, 14)
  const max = places[0].mention_count
  const data = places.map((p, idx) => ({
    name: p.name,
    value: [p.longitude, p.latitude, p.mention_count],
    symbolSize: 10 + (p.mention_count / max) * 28,
    itemStyle: {
      color: p.place_type === 'city' ? '#8b3a3a' : p.place_type === 'mountain' ? '#4a7c59' : '#2e5c6e',
      opacity: 0.88,
      borderColor: '#faf6ed',
      borderWidth: 1,
    },
    label: {
      show: p.mention_count >= 60,
      position: 'right',
      formatter: p.name,
      color: '#1a1a1a',
      fontSize: 11,
      fontFamily: 'serif',
    },
    emphasis: { scale: 1.4 },
    animationDelay: idx * 130,
  }))

  mapChart.setOption({
    backgroundColor: 'transparent',
    animationDuration: 1200,
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => `${params.name} · ${params.value?.[2]} 次书写`,
      backgroundColor: 'rgba(250, 246, 237, 0.98)',
      borderColor: '#d4c9a8',
      textStyle: { color: '#1a1a1a', fontFamily: 'serif' },
    },
    geo: {
      map: 'china',
      roam: false,
      zoom: 1.25,
      center: [105, 36],
      silent: true,
      itemStyle: {
        areaColor: '#e8dfca',
        borderColor: '#c9b896',
        borderWidth: 0.5,
      },
    },
    series: [
      {
        type: 'scatter',
        coordinateSystem: 'geo',
        data,
        zlevel: 2,
        animationDelay: (idx: number) => idx * 130,
      },
    ],
  })
}

async function loadChinaMap() {
  const resp = await fetch(`${import.meta.env.BASE_URL}data/china_map.json`)
  const geoJson = await resp.json()
  echarts.registerMap('china', geoJson)
}

let resizeHandler: () => void

onMounted(async () => {
  setTimeout(() => { heroVisible.value = true }, 80)

  if (mapRef.value) {
    mapChart = echarts.init(mapRef.value)
    resizeHandler = () => mapChart?.resize()
    window.addEventListener('resize', resizeHandler)
  }

  try {
    const [meta, ps, analysis] = await Promise.all([
      loadMetadata(),
      loadPlaceSummary(),
      loadAnalysis()
    ])
    stats.value = meta.stats
    placeSummary.value = ps
    analysisData.value = analysis
  } catch (e) {
    console.error('Failed to load home data:', e)
  }

  try {
    await loadChinaMap()
  } catch (e) {
    console.error('Failed to load map:', e)
  }

  renderPrologueMap()
})

onUnmounted(() => {
  if (mapChart) mapChart.dispose()
  if (resizeHandler) window.removeEventListener('resize', resizeHandler)
})
</script>

<style scoped>
.home {
  background: var(--color-bg);
}

/* Hero */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  background: linear-gradient(180deg, #f5f1e8 0%, #efe8d9 100%);
}

.hero-bg {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.ink-splash {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.08;
}

.ink-1 { width: 500px; height: 500px; background: #1a1a1a; top: 10%; left: 5%; animation: float-slow 20s ease-in-out infinite; }
.ink-2 { width: 400px; height: 400px; background: #8b3a3a; top: 50%; right: 10%; animation: float-slow 25s ease-in-out infinite reverse; }
.ink-3 { width: 300px; height: 300px; background: #2e5c6e; bottom: 5%; left: 40%; animation: float-slow 18s ease-in-out infinite; }

@keyframes float-slow {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.hero-content {
  position: relative;
  z-index: 1;
  width: min(920px, 92vw);
  text-align: center;
  opacity: 0;
  transition: opacity 1s ease;
  padding: 5rem 0;
}

.hero-content.visible {
  opacity: 1;
}

.hero-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 700;
  color: var(--color-ink);
  letter-spacing: 0.15em;
}

.title-char {
  display: inline-block;
  opacity: 0;
  animation: char-appear 0.8s forwards;
}

@keyframes char-appear {
  from { opacity: 0; transform: translateY(30px); }
  to { opacity: 1; transform: translateY(0); }
}

.hero-subtitle {
  margin-top: 0.8rem;
  font-size: clamp(0.9rem, 2vw, 1.2rem);
  color: var(--color-ink-light);
  letter-spacing: 0.2em;
}

.hero-slogan {
  margin: 1.8rem auto 1.4rem;
  font-size: clamp(1.3rem, 3.5vw, 2rem);
  color: var(--color-accent);
  letter-spacing: 0.1em;
  line-height: 1.6;
}

.hero-question {
  max-width: 700px;
  margin: 0 auto;
  color: var(--color-ink-light);
  line-height: 2;
  font-size: 0.95rem;
}

.hero-data-line {
  max-width: 700px;
  margin: 1.2rem auto 2rem;
  font-size: 0.82rem;
  color: var(--color-ink-muted);
  line-height: 1.8;
}

.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.4rem;
  margin-bottom: 2.5rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: clamp(1.3rem, 3vw, 2rem);
  font-weight: 700;
  color: var(--color-accent);
}

.stat-label {
  font-size: 0.76rem;
  color: var(--color-ink-muted);
  letter-spacing: 0.08em;
  margin-top: 0.15rem;
}

.stat-divider {
  width: 1px;
  height: 28px;
  background: var(--color-border);
}

.hero-btn {
  padding: 0.8rem 2.5rem;
  font-size: 1rem;
  color: var(--color-ink);
  border: 1.5px solid var(--color-ink);
  border-radius: 2px;
  letter-spacing: 0.15em;
  transition: all 0.3s;
}

.hero-btn:hover {
  background: var(--color-ink);
  color: var(--color-bg);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 序章地图 */
.prologue {
  padding: 4rem 2rem 4.5rem;
  background: var(--color-bg-alt);
}

.prologue-header {
  max-width: 800px;
  margin: 0 auto 2rem;
  text-align: center;
}

.prologue-chapter {
  display: inline-block;
  margin-bottom: 0.7rem;
  padding: 0.2rem 0.9rem;
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  color: var(--color-accent);
  border: 1px solid var(--color-accent);
  border-radius: 999px;
}

.prologue-title {
  font-size: clamp(1.6rem, 4vw, 2.4rem);
  color: var(--color-ink);
  letter-spacing: 0.08em;
}

.prologue-desc {
  margin-top: 0.8rem;
  font-size: 0.9rem;
  color: var(--color-ink-muted);
}

.prologue-map {
  width: min(1000px, 100%);
  height: 540px;
  margin: 0 auto;
  background: linear-gradient(135deg, #f5f1e8 0%, #ede5d0 100%);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.prologue-caption {
  max-width: 700px;
  margin: 0.8rem auto 0;
  text-align: center;
  font-size: 0.76rem;
  color: var(--color-ink-muted);
}

/* 发现 */
.findings {
  padding: 4rem 2rem;
}

.section-header {
  text-align: center;
  margin-bottom: 2.2rem;
}

.section-title {
  font-size: clamp(1.5rem, 4vw, 2.2rem);
  color: var(--color-ink);
  letter-spacing: 0.08em;
  margin-bottom: 0.4rem;
}

.section-desc {
  font-size: 0.82rem;
  color: var(--color-ink-muted);
}

.findings-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
  max-width: 1050px;
  margin: 0 auto;
}

.home-finding {
  position: relative;
  padding: 1.4rem 1.5rem 1.4rem 4rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
}

.home-finding-index {
  position: absolute;
  left: 1.2rem;
  top: 1.25rem;
  font-size: 1.6rem;
  font-weight: 700;
  color: rgba(139, 58, 58, 0.2);
}

.home-finding-title {
  font-size: 0.98rem;
  color: var(--color-accent);
  margin-bottom: 0.45rem;
}

.home-finding-text {
  font-size: 0.86rem;
  line-height: 1.8;
  color: var(--color-ink-light);
}

/* 诗句示例 */
.flowing-poems {
  padding: 4rem 2rem;
  background: var(--color-bg-alt);
}

.poem-flow-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.poem-flow-card {
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius);
  padding: 1.5rem;
  opacity: 0;
  animation: card-appear 0.6s forwards;
  transition: transform 0.3s, box-shadow 0.3s;
}

.poem-flow-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}

@keyframes card-appear {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.poem-text {
  font-size: 1.05rem;
  color: var(--color-ink);
  line-height: 1.8;
  margin-bottom: 0.8rem;
}

.poem-author {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  margin-bottom: 0.5rem;
}

.poem-place {
  font-size: 0.8rem;
  color: var(--color-accent);
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.place-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  font-size: 0.7rem;
  border-radius: 50%;
  background: var(--color-accent);
  color: #fff;
}

.icon-city { background: #8b3a3a; }
.icon-mountain { background: #4a7c59; }
.icon-river { background: #2e5c6e; }
.icon-lake { background: #5b8a72; }
.icon-pass { background: #b8860b; }
.icon-historic_region { background: #7a6a5a; }

@media (max-width: 768px) {
  .hero-stats {
    flex-wrap: wrap;
    gap: 1rem;
  }
  .stat-divider { display: none; }
  .findings-grid { grid-template-columns: 1fr; }
  .prologue-map { height: 400px; }
  .poem-flow-container { grid-template-columns: 1fr; }
}
</style>
