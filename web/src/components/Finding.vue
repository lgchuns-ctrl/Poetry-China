<template>
  <aside class="finding">
    <div class="finding-label">{{ label || '我们发现' }}</div>
    <h3 v-if="title" class="finding-title">{{ title }}</h3>
    <ul v-if="items && items.length" class="finding-list">
      <li v-for="(item, i) in items" :key="i">{{ item }}</li>
    </ul>
    <p v-if="note" class="finding-note">{{ note }}</p>
  </aside>
</template>

<script setup lang="ts">
defineProps<{
  label?: string
  title?: string
  items?: string[]
  note?: string
}>()
</script>

<style scoped>
.finding {
  margin: 1.8rem 0;
  padding: 1.4rem 1.6rem;
  background: var(--color-card);
  border: 1px solid var(--color-border-light);
  border-left: 4px solid var(--color-accent);
  border-radius: 0 var(--radius-lg) var(--radius-lg) 0;
  box-shadow: var(--shadow-sm);
}

.finding-label {
  font-size: 0.76rem;
  letter-spacing: 0.2em;
  color: var(--color-accent);
  margin-bottom: 0.45rem;
}

.finding-title {
  font-size: 1.05rem;
  color: var(--color-ink);
  line-height: 1.6;
  margin-bottom: 0.5rem;
}

.finding-list {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.finding-list li {
  position: relative;
  padding-left: 1.1rem;
  font-size: 0.9rem;
  line-height: 1.8;
  color: var(--color-ink-light);
}

.finding-list li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.72em;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--color-accent);
}

.finding-note {
  margin-top: 0.8rem;
  font-size: 0.76rem;
  line-height: 1.7;
  color: var(--color-ink-muted);
}
</style>
