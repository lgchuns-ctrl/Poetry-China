<template>
  <div class="epilogue-view">
    <span class="epilogue-chapter">终章</span>
    <h2 class="epilogue-title">山河从来不是诗词的背景</h2>

    <div class="epilogue-text">
      <p>
        从长安到江南，从李白的远游到杜甫的漂泊，一座城、一条河、一座山，
        不断进入诗人的文字，也进入中国人的共同记忆。
      </p>
      <p>
        当{{ totalWorksLabel }}首唐诗宋词重新落回地图，我们看到的不是静止的地理坐标，
        而是一个随着时代变化、人生经历和情感表达不断流动的“文学中国”。
      </p>
    </div>

    <div class="epilogue-thread">
      <span>山河有记忆</span>
      <i>→</i>
      <span>从长安到江南</span>
      <i>→</i>
      <span>一人一山河</span>
      <i>→</i>
      <span>山河成为情感</span>
    </div>

    <p class="epilogue-final">诗行千年，山河有声。</p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { loadMetadata } from '../utils/data'

const stats = ref<any>(null)

const totalWorksLabel = computed(() => {
  const n = Number(stats.value?.total_works)
  return Number.isFinite(n) ? n.toLocaleString('zh-CN') : '两万余'
})

onMounted(async () => {
  try {
    const meta = await loadMetadata()
    stats.value = meta.stats
  } catch (e) {
    console.error('Failed to load epilogue stats:', e)
  }
})
</script>

<style scoped>
.epilogue-view {
  max-width: 860px;
  margin: 0 auto;
  padding: 4rem 1rem;
  text-align: center;
}

.epilogue-chapter {
  display: inline-block;
  margin-bottom: 1rem;
  padding: 0.2rem 0.9rem;
  font-size: 0.78rem;
  letter-spacing: 0.2em;
  color: var(--color-accent);
  border: 1px solid var(--color-accent);
  border-radius: 999px;
}

.epilogue-title {
  font-size: clamp(1.8rem, 5vw, 3rem);
  color: var(--color-ink);
  letter-spacing: 0.08em;
}

.epilogue-text {
  margin: 2rem auto 0;
  max-width: 700px;
  display: flex;
  flex-direction: column;
  gap: 1.3rem;
  text-align: left;
}

.epilogue-text p {
  font-size: 1rem;
  line-height: 2;
  color: var(--color-ink-light);
}

.epilogue-thread {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 0.7rem;
  margin: 2.5rem auto 2.8rem;
  color: var(--color-ink-muted);
  font-size: 0.82rem;
  letter-spacing: 0.08em;
}

.epilogue-thread i {
  font-style: normal;
  color: var(--color-accent);
}

.epilogue-final {
  font-size: clamp(1.4rem, 4vw, 2.2rem);
  letter-spacing: 0.18em;
  color: var(--color-accent);
}
</style>
