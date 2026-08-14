<template>
  <div class="home">
    <!-- 首页Hero -->
    <div class="hero" ref="heroRef">
      <div class="hero-bg">
        <div class="ink-splash ink-1"></div>
        <div class="ink-splash ink-2"></div>
        <div class="ink-splash ink-3"></div>
      </div>
      <div class="hero-content" :class="{ visible: heroVisible }">
        <h1 class="hero-title">
          <span class="title-char" v-for="(ch, i) in '诗行中国'" :key="i" :style="{ animationDelay: i * 0.15 + 's' }">{{ ch }}</span>
        </h1>
        <p class="hero-subtitle">唐诗宋词中的山河地图</p>
        <p class="hero-tagline">千年前，一句诗落在山河之间。</p>
        <div class="hero-stats" v-if="stats">
          <div class="stat-item">
            <span class="stat-num">{{ formatNum(stats.tang_poems) }}</span>
            <span class="stat-label">唐诗</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">{{ formatNum(stats.song_ci) }}</span>
            <span class="stat-label">宋词</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">{{ formatNum(stats.total_authors) }}</span>
            <span class="stat-label">诗人</span>
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

    <!-- 流动诗句 -->
    <div class="flowing-poems" ref="flowRef">
      <div class="section-header">
        <h2 class="section-title">诗句山河</h2>
        <p class="section-desc">每一个地点，都有一句诗为之停留</p>
      </div>
      <div class="poem-flow-container">
        <div v-for="(item, idx) in displayPoems" :key="idx" class="poem-flow-card" :style="{ animationDelay: idx * 0.1 + 's' }">
          <p class="poem-text">{{ item.text }}</p>
          <p class="poem-author">—— {{ item.author }} ·《{{ item.title }}》</p>
          <p class="poem-place">
            <span class="place-icon" :class="'icon-' + item.type">{{ item.typeLabel }}</span>
            {{ item.place }}
          </p>
        </div>
      </div>
    </div>

    <!-- 研究发现 -->
    <div class="findings" v-if="conclusions.length">
      <div class="section-header">
        <h2 class="section-title">数据发现</h2>
        <p class="section-desc">由数据生成的核心结论</p>
      </div>
      <div class="findings-grid">
        <div v-for="c in conclusions.slice(0, 6)" :key="c.conclusion_id" class="finding-card">
          <p class="finding-text">{{ c.text }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { loadMetadata, loadConclusions, loadPlaceSummary, type Conclusion } from '../utils/data'

const stats = ref<any>(null)
const conclusions = ref<Conclusion[]>([])
const heroVisible = ref(false)
const flowRef = ref<HTMLElement>()
const placeSummary = ref<Record<string, any>>({})

// 精选诗句（从数据中选取有地点的经典诗句）
const selectedPoems = computed(() => {
  const poems: { text: string; author: string; title: string; place: string; type: string; typeLabel: string }[] = []
  
  // 从place_summary中选取高频地点的诗句
  const placeData = placeSummary.value
  if (Object.keys(placeData).length === 0) return poems
  
  // 手动精选一些经典诗句
  const classics = [
    { text: '故人西辞黄鹤楼，烟花三月下扬州', author: '李白', title: '黄鹤楼送孟浩然之广陵', place: '扬州', type: 'city', typeLabel: '城' },
    { text: '飞流直下三千尺，疑是银河落九天', author: '李白', title: '望庐山瀑布', place: '庐山', type: 'mountain', typeLabel: '山' },
    { text: '孤帆远影碧空尽，唯见长江天际流', author: '李白', title: '黄鹤楼送孟浩然之广陵', place: '长江', type: 'river', typeLabel: '河' },
    { text: '气蒸云梦泽，波撼岳阳城', author: '孟浩然', title: '望洞庭湖赠张丞相', place: '洞庭湖', type: 'lake', typeLabel: '湖' },
    { text: '羌笛何须怨杨柳，春风不度玉门关', author: '王之涣', title: '凉州词', place: '玉门关', type: 'pass', typeLabel: '关' },
    { text: '会当凌绝顶，一览众山小', author: '杜甫', title: '望岳', place: '泰山', type: 'mountain', typeLabel: '山' },
    { text: '姑苏城外寒山寺，夜半钟声到客船', author: '张继', title: '枫桥夜泊', place: '苏州', type: 'city', typeLabel: '城' },
    { text: '日出江花红胜火，春来江水绿如蓝', author: '白居易', title: '忆江南', place: '江南', type: 'historic_region', typeLabel: '域' },
    { text: '欲把西湖比西子，淡妆浓抹总相宜', author: '苏轼', title: '饮湖上初晴后雨', place: '西湖', type: 'lake', typeLabel: '湖' },
    { text: '大江东去，浪淘尽，千古风流人物', author: '苏轼', title: '念奴娇·赤壁怀古', place: '长江', type: 'river', typeLabel: '河' },
    { text: '星垂平野阔，月涌大江流', author: '杜甫', title: '旅夜书怀', place: '长江', type: 'river', typeLabel: '河' },
    { text: '黄河远上白云间，一片孤城万仞山', author: '王之涣', title: '凉州词', place: '黄河', type: 'river', typeLabel: '河' },
  ]
  
  return classics
})

const displayPoems = computed(() => selectedPoems.value.slice(0, 8))

function formatNum(n: number) {
  if (n >= 10000) return (n / 10000).toFixed(1) + '万'
  return n.toLocaleString()
}

function enterMap() {
  const el = document.getElementById('map')
  if (el) el.scrollIntoView({ behavior: 'smooth' })
}

onMounted(async () => {
  setTimeout(() => { heroVisible.value = true }, 100)
  
  try {
    const meta = await loadMetadata()
    stats.value = meta.stats
  } catch(e) { console.error('Failed to load metadata:', e) }
  
  try {
    conclusions.value = await loadConclusions()
  } catch(e) { console.error('Failed to load conclusions:', e) }
  
  try {
    placeSummary.value = await loadPlaceSummary()
  } catch(e) { console.error('Failed to load place summary:', e) }
})
</script>

<style scoped>
.home {
  background: var(--color-bg);
}

/* Hero */
.hero {
  position: relative;
  height: 100vh;
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

.ink-1 {
  width: 500px;
  height: 500px;
  background: #1a1a1a;
  top: 10%;
  left: 5%;
  animation: float-slow 20s ease-in-out infinite;
}

.ink-2 {
  width: 400px;
  height: 400px;
  background: #8b3a3a;
  top: 50%;
  right: 10%;
  animation: float-slow 25s ease-in-out infinite reverse;
}

.ink-3 {
  width: 300px;
  height: 300px;
  background: #2e5c6e;
  bottom: 5%;
  left: 40%;
  animation: float-slow 18s ease-in-out infinite;
}

@keyframes float-slow {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.hero-content {
  text-align: center;
  z-index: 1;
  opacity: 0;
  transition: opacity 1s ease;
}

.hero-content.visible {
  opacity: 1;
}

.hero-title {
  font-size: clamp(2.5rem, 8vw, 5rem);
  font-weight: 700;
  color: var(--color-ink);
  letter-spacing: 0.15em;
  margin-bottom: 0.5rem;
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
  font-size: clamp(0.9rem, 2vw, 1.2rem);
  color: var(--color-ink-light);
  letter-spacing: 0.2em;
  margin-bottom: 1.5rem;
}

.hero-tagline {
  font-size: clamp(0.85rem, 1.8vw, 1rem);
  color: var(--color-ink-muted);
  margin-bottom: 3rem;
  font-style: italic;
}

.hero-stats {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: clamp(1.5rem, 3vw, 2.2rem);
  font-weight: 700;
  color: var(--color-accent);
}

.stat-label {
  font-size: 0.8rem;
  color: var(--color-ink-muted);
  letter-spacing: 0.1em;
  margin-top: 0.2rem;
}

.stat-divider {
  width: 1px;
  height: 30px;
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

/* 流动诗句 */
.flowing-poems {
  padding: 4rem 2rem;
  background: var(--color-bg-alt);
}

.section-header {
  text-align: center;
  margin-bottom: 2.5rem;
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

/* 研究发现 */
.findings {
  padding: 4rem 2rem;
}

.findings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.finding-card {
  background: var(--color-card);
  border-left: 3px solid var(--color-accent);
  padding: 1.2rem 1.5rem;
  border-radius: 0 var(--radius) var(--radius) 0;
  box-shadow: var(--shadow-sm);
}

.finding-text {
  font-size: 0.9rem;
  color: var(--color-ink);
  line-height: 1.7;
}

@media (max-width: 768px) {
  .hero-stats {
    flex-wrap: wrap;
    gap: 1rem;
  }
  .stat-divider { display: none; }
  .poem-flow-container {
    grid-template-columns: 1fr;
  }
}
</style>
