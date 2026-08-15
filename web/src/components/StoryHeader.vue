<template>
  <header class="story-header">
    <span v-if="chapter" class="story-chapter">{{ chapter }}</span>
    <h2 class="story-title">{{ title }}</h2>
    <p v-if="subtitle" class="story-subtitle">{{ subtitle }}</p>
    <p v-if="question" class="story-question">{{ question }}</p>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  chapter?: string
  title: string
  subtitle?: string
  question?: string
}>()
</script>

<style scoped>
.story-header {
  max-width: 900px;
  margin: 0 auto 2.2rem;
  text-align: center;
}

.story-chapter {
  display: inline-block;
  margin-bottom: 0.7rem;
  padding: 0.2rem 0.9rem;
  font-size: 0.78rem;
  letter-spacing: 0.18em;
  color: var(--color-accent);
  border: 1px solid var(--color-accent);
  border-radius: 999px;
}

.story-title {
  font-size: clamp(1.8rem, 4vw, 2.8rem);
  font-weight: 700;
  color: var(--color-ink);
  letter-spacing: 0.08em;
  line-height: 1.35;
}

.story-subtitle {
  margin-top: 0.8rem;
  font-size: clamp(1rem, 2.2vw, 1.35rem);
  color: var(--color-accent);
  letter-spacing: 0.08em;
}

.story-question {
  margin-top: 1rem;
  font-size: 0.92rem;
  line-height: 1.9;
  color: var(--color-ink-muted);
}
</style>
