<template>
  <section class="case-study">
    <span v-if="kicker" class="case-kicker">{{ kicker }}</span>
    <h3 class="case-title">{{ title }}</h3>
    <p v-if="lead" class="case-lead">{{ lead }}</p>

    <div v-if="stats && stats.length" class="case-stats">
      <div v-for="(s, i) in stats" :key="i" class="case-stat">
        <span class="case-stat-value">{{ s.value }}</span>
        <span class="case-stat-label">{{ s.label }}</span>
      </div>
    </div>

    <div class="case-body">
      <slot />
    </div>

    <p v-if="question" class="case-question">{{ question }}</p>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  kicker?: string
  title: string
  lead?: string
  stats?: { value: string | number; label: string }[]
  question?: string
}>()
</script>

<style scoped>
.case-study {
  margin: 2.2rem 0;
  padding: 1.8rem 2rem;
  background:
    radial-gradient(circle at 90% 10%, rgba(139, 58, 58, 0.07), transparent 36%),
    var(--color-card);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
}

.case-kicker {
  display: inline-block;
  margin-bottom: 0.6rem;
  font-size: 0.74rem;
  letter-spacing: 0.2em;
  color: var(--color-accent);
}

.case-title {
  font-size: clamp(1.35rem, 3vw, 2rem);
  color: var(--color-ink);
  letter-spacing: 0.08em;
}

.case-lead {
  margin-top: 0.7rem;
  font-size: 0.92rem;
  line-height: 1.9;
  color: var(--color-ink-light);
  max-width: 780px;
}

.case-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  margin: 1.3rem 0;
}

.case-stat {
  display: flex;
  flex-direction: column;
  min-width: 82px;
}

.case-stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-accent);
}

.case-stat-label {
  margin-top: 0.1rem;
  font-size: 0.74rem;
  color: var(--color-ink-muted);
}

.case-body {
  color: var(--color-ink-light);
}

.case-question {
  margin-top: 1.2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--color-border-light);
  font-size: 0.94rem;
  line-height: 1.8;
  color: var(--color-accent);
}

@media (max-width: 768px) {
  .case-study {
    padding: 1.3rem 1.1rem;
  }
}
</style>
