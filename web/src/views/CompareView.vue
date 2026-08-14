<template>
  <div class="compare-view">
    <div class="section-header">
      <h2 class="section-title">唐宋山河对照</h2>
      <p class="section-desc">唐诗与宋词的山河书写，各有何不同</p>
    </div>

    <div class="compare-tabs">
      <button v-for="t in tabs" :key="t.id" 
        :class="['tab-btn', { active: activeTab === t.id }]"
        @click="activeTab = t.id">{{ t.label }}</button>
    </div>

    <div class="compare-content">
      <!-- 地点频率对比 -->
      <div v-if="activeTab === 'places'" class="compare-grid">
        <div class="compare-panel tang-panel">
          <h3 class="panel-title">唐诗 · 高频地点</h3>
          <div class="bar-list">
            <div v-for="(item, i) in tangTopPlaces" :key="i" class="bar-row">
              <span class="bar-label">{{ item.name }}</span>
              <div class="bar-track">
                <div class="bar-fill tang-fill" :style="{ width: item.pct + '%' }"></div>
              </div>
              <span class="bar-value">{{ item.count }}</span>
            </div>
          </div>
        </div>
        <div class="compare-divider"></div>
        <div class="compare-panel song-panel">
          <h3 class="panel-title">宋词 · 高频地点</h3>
          <div class="bar-list">
            <div v-for="(item, i) in songTopPlaces" :key="i" class="bar-row">
              <span class="bar-label">{{ item.name }}</span>
              <div class="bar-track">
                <div class="bar-fill song-fill" :style="{ width: item.pct + '%' }"></div>
              </div>
              <span class="bar-value">{{ item.count }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 类型对比 -->
      <div v-if="activeTab === 'types'" class="type-comparison">
        <div v-for="t in typeComparison" :key="t.type" class="type-row">
          <div class="type-label">
            <span class="type-icon" :class="'icon-' + t.type">{{ typeLabel(t.type) }}</span>
          </div>
          <div class="type-bars">
            <div class="type-bar-item tang">
              <span class="type-count">{{ t.tang }}</span>
              <div class="type-bar-track">
                <div class="type-bar-fill tang-fill" :style="{ width: t.tangPct + '%' }"></div>
              </div>
            </div>
            <div class="type-bar-item song">
              <div class="type-bar-track">
                <div class="type-bar-fill song-fill" :style="{ width: t.songPct + '%' }"></div>
              </div>
              <span class="type-count">{{ t.song }}</span>
            </div>
          </div>
        </div>
        <div class="type-legend">
          <span class="legend-tang">唐诗</span>
          <span class="legend-song">宋词</span>
        </div>
      </div>

      <!-- 意象对比 -->
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

      <!-- 主题对比 -->
      <div v-if="activeTab === 'themes'" class="theme-comparison">
        <div v-for="t in themeComparison" :key="t.name" class="theme-cmp-row">
          <span class="theme-cmp-label">{{ t.name }}</span>
          <div class="theme-cmp-bars">
            <div class="theme-cmp-bar tang">
              <div class="theme-cmp-fill tang-fill" :style="{ width: t.tangPct + '%' }">
                <span class="theme-cmp-num">{{ t.tang }}</span>
              </div>
            </div>
            <div class="theme-cmp-bar song">
              <div class="theme-cmp-fill song-fill" :style="{ width: t.songPct + '%' }">
                <span class="theme-cmp-num">{{ t.song }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 数据说明 -->
    <div class="compare-note">
      <p>* 以上对比基于当前数据集的统计结果，不做过度文化推断。</p>
      <p>* 数据由程序计算生成，非人工筛选。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { loadDynastyPlaceSummary, loadPlaceSummary, loadWorks } from '../utils/data'

const activeTab = ref('places')
const dynastyData = ref<any>({})
const placeSummary = ref<Record<string, any>>({})
const allWorks = ref<any[]>([])

const tabs = [
  { id: 'places', label: '高频地点' },
  { id: 'types', label: '地点类型' },
  { id: 'imagery', label: '意象' },
  { id: 'themes', label: '主题' },
]

const tangPlaces = computed(() => {
  const d = dynastyData.value['唐'] || {}
  return Object.entries(d).map(([name, count]) => ({ name, count: count as number }))
    .sort((a, b) => b.count - a.count)
})

const songPlaces = computed(() => {
  const d = dynastyData.value['宋'] || {}
  return Object.entries(d).map(([name, count]) => ({ name, count: count as number }))
    .sort((a, b) => b.count - a.count)
})

const tangTopPlaces = computed(() => {
  const top = tangPlaces.value.slice(0, 15)
  const max = top[0]?.count || 1
  return top.map(p => ({ ...p, pct: Math.round(p.count / max * 100) }))
})

const songTopPlaces = computed(() => {
  const top = songPlaces.value.slice(0, 15)
  const max = top[0]?.count || 1
  return top.map(p => ({ ...p, pct: Math.round(p.count / max * 100) }))
})

const typeComparison = computed(() => {
  const stats: Record<string, { type: string; tang: number; song: number }> = {}

  for (const ps of Object.values(placeSummary.value)) {
    const type = ps.place_type || 'other'
    if (!stats[type]) {
      stats[type] = { type, tang: 0, song: 0 }
    }
    stats[type].tang += Number(ps.tang_count) || 0
    stats[type].song += Number(ps.song_count) || 0
  }

  const list = Object.values(stats).filter(t => t.tang > 0 || t.song > 0)
  const maxTang = Math.max(1, ...list.map(t => t.tang))
  const maxSong = Math.max(1, ...list.map(t => t.song))

  return list.map(t => ({
    ...t,
    tangPct: Math.round(t.tang / maxTang * 100),
    songPct: Math.round(t.song / maxSong * 100),
  }))
})

const imageryComparison = computed(() => {
  const stats: Record<string, { name: string; tang: number; song: number }> = {}

  for (const w of allWorks.value) {
    const dynasty = w.dynasty === '唐' ? 'tang' : 'song'
    for (const img of w.imagery || []) {
      if (!stats[img]) {
        stats[img] = { name: img, tang: 0, song: 0 }
      }
      stats[img][dynasty]++
    }
  }

  const top = Object.values(stats)
    .sort((a, b) => (b.tang + b.song) - (a.tang + a.song))
    .slice(0, 12)
  const max = Math.max(1, ...top.map(img => Math.max(img.tang, img.song)))

  return top.map(img => ({
    ...img,
    tangPct: Math.round(img.tang / max * 100),
    songPct: Math.round(img.song / max * 100),
  }))
})

const themeComparison = computed(() => {
  const stats: Record<string, { name: string; tang: number; song: number }> = {}

  for (const w of allWorks.value) {
    const dynasty = w.dynasty === '唐' ? 'tang' : 'song'
    for (const theme of w.themes || []) {
      if (theme === '其他') continue
      if (!stats[theme]) {
        stats[theme] = { name: theme, tang: 0, song: 0 }
      }
      stats[theme][dynasty]++
    }
  }

  const top = Object.values(stats)
    .sort((a, b) => (b.tang + b.song) - (a.tang + a.song))
    .slice(0, 10)
  const max = Math.max(1, ...top.map(theme => Math.max(theme.tang, theme.song)))

  return top.map(theme => ({
    ...theme,
    tangPct: Math.round(theme.tang / max * 100),
    songPct: Math.round(theme.song / max * 100),
  }))
})

function typeLabel(type: string): string {
  const labels: Record<string, string> = {
    city: '城市', mountain: '山岳', river: '河流', lake: '湖泊',
    pass: '关隘', building: '古迹', historic_region: '地域', other: '其他'
  }
  return labels[type] || type
}

onMounted(async () => {
  try {
    const [dp, ps, w] = await Promise.all([
      loadDynastyPlaceSummary(),
      loadPlaceSummary(),
      loadWorks()
    ])
    dynastyData.value = dp
    placeSummary.value = ps
    allWorks.value = w
  } catch(e) {
    console.error('Failed to load comparison data:', e)
  }
})
</script>

<style scoped>
.compare-view {
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

.compare-tabs {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.tab-btn {
  padding: 0.5rem 1.2rem;
  font-size: 0.88rem;
  color: var(--color-ink-light);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: var(--color-bg);
}

.tab-btn:hover {
  border-color: var(--color-accent);
}

.tab-btn.active {
  background: var(--color-ink);
  color: #fff;
  border-color: var(--color-ink);
}

.compare-content {
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-sm);
  min-height: 400px;
}

/* 地点对比 */
.compare-grid {
  display: grid;
  grid-template-columns: 1fr 1px 1fr;
  gap: 0;
}

.compare-panel {
  padding: 0 1.5rem;
}

.compare-divider {
  background: var(--color-border-light);
}

.panel-title {
  font-size: 1rem;
  text-align: center;
  margin-bottom: 1.2rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid var(--color-border-light);
}

.tang-panel .panel-title { color: var(--color-tang); }
.song-panel .panel-title { color: var(--color-song); }

.bar-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.bar-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.82rem;
}

.bar-label {
  width: 60px;
  text-align: right;
  color: var(--color-ink);
  flex-shrink: 0;
}

.bar-track {
  flex: 1;
  height: 18px;
  background: var(--color-bg-alt);
  border-radius: 2px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.8s ease;
}

.tang-fill { background: var(--color-tang); }
.song-fill { background: var(--color-song); }

.bar-value {
  width: 30px;
  text-align: left;
  color: var(--color-ink-muted);
  flex-shrink: 0;
}

/* 类型对比 */
.type-comparison {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 600px;
  margin: 0 auto;
}

.type-row {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.type-label {
  width: 60px;
  text-align: center;
}

.type-icon {
  display: inline-block;
  padding: 2px 10px;
  font-size: 0.8rem;
  border-radius: 12px;
  color: #fff;
  background: var(--color-accent);
}

.type-bars {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.type-bar-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.type-bar-item.song {
  flex-direction: row-reverse;
}

.type-bar-track {
  flex: 1;
  height: 16px;
  background: var(--color-bg-alt);
  border-radius: 2px;
  overflow: hidden;
}

.type-bar-fill {
  height: 100%;
  transition: width 0.8s ease;
}

.type-count {
  width: 30px;
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-ink-muted);
}

.type-legend {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 1rem;
}

.legend-tang { color: var(--color-tang); font-size: 0.85rem; }
.legend-song { color: var(--color-song); font-size: 0.85rem; }

/* 意象对比 */
.imagery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
  gap: 1rem;
}

.imagery-cell {
  text-align: center;
}

.imagery-name {
  font-size: 1rem;
  color: var(--color-ink);
  margin-bottom: 0.5rem;
}

.imagery-bars {
  display: flex;
  gap: 4px;
  justify-content: center;
  align-items: flex-end;
  height: 120px;
}

.img-bar {
  width: 24px;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  align-items: center;
  position: relative;
}

.img-fill {
  width: 100%;
  border-radius: 2px 2px 0 0;
  transition: height 0.8s ease;
  min-height: 2px;
}

.img-count {
  position: absolute;
  top: -16px;
  font-size: 0.72rem;
  color: var(--color-ink-muted);
}

/* 主题对比 */
.theme-comparison {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
  max-width: 700px;
  margin: 0 auto;
}

.theme-cmp-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.theme-cmp-label {
  width: 60px;
  text-align: right;
  font-size: 0.82rem;
  color: var(--color-ink);
  flex-shrink: 0;
}

.theme-cmp-bars {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.theme-cmp-bar {
  height: 18px;
  background: var(--color-bg-alt);
  border-radius: 2px;
  overflow: hidden;
}

.theme-cmp-fill {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 6px;
  transition: width 0.8s ease;
  min-width: 20px;
}

.theme-cmp-num {
  font-size: 0.72rem;
  color: #fff;
}

.compare-note {
  margin-top: 1rem;
  text-align: center;
  font-size: 0.75rem;
  color: var(--color-ink-muted);
}

.compare-note p {
  margin-bottom: 0.2rem;
}

@media (max-width: 768px) {
  .compare-grid {
    grid-template-columns: 1fr;
  }
  .compare-divider {
    display: none;
  }
  .compare-panel {
    padding: 0;
    margin-bottom: 1.5rem;
  }
  .imagery-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}
</style>
