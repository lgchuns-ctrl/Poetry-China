<template>
  <div class="app-container">
    <!-- 导航栏 -->
    <nav class="nav-bar" :class="{ scrolled: isScrolled }">
      <div class="nav-content">
        <div class="nav-logo" @click="scrollTo('home')">
          <span class="logo-main">诗行中国</span>
          <span class="logo-sub">唐诗宋词中的山河地图</span>
        </div>
        <ul class="nav-links">
          <li v-for="item in navItems" :key="item.id">
            <a :href="'#' + item.id" :class="{ active: activeSection === item.id }" @click.prevent="scrollTo(item.id)">
              {{ item.label }}
            </a>
          </li>
        </ul>
        <button class="nav-toggle" @click="mobileMenuOpen = !mobileMenuOpen">
          <span></span><span></span><span></span>
        </button>
      </div>
      <transition name="slide-up">
        <ul v-if="mobileMenuOpen" class="nav-mobile">
          <li v-for="item in navItems" :key="item.id">
            <a @click.prevent="scrollTo(item.id); mobileMenuOpen = false">{{ item.label }}</a>
          </li>
        </ul>
      </transition>
    </nav>

    <!-- 首页 -->
    <section id="home" class="section section-home">
      <HomeView />
    </section>

    <!-- 诗词山河地图 -->
    <section id="map" class="section section-map">
      <MapView />
    </section>

    <!-- 唐宋对照 -->
    <section id="compare" class="section section-compare">
      <CompareView />
    </section>

    <!-- 诗人行迹 -->
    <section id="author" class="section section-author">
      <AuthorView />
    </section>

    <!-- 一句诗在哪里 -->
    <section id="search" class="section section-search">
      <SearchView />
    </section>

    <!-- 数据与方法 -->
    <section id="data" class="section section-data">
      <DataMethodView />
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <p class="footer-title">诗行中国 · 唐诗宋词中的山河地图</p>
      <p class="footer-sub">循诗而行，在千年文字中重新看见中国山河</p>
      <p class="footer-note">数据来源：chinese-poetry (MIT License) · 本作品为数字人文研究项目</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import HomeView from './views/HomeView.vue'
import MapView from './views/MapView.vue'
import CompareView from './views/CompareView.vue'
import AuthorView from './views/AuthorView.vue'
import SearchView from './views/SearchView.vue'
import DataMethodView from './views/DataMethodView.vue'

const isScrolled = ref(false)
const mobileMenuOpen = ref(false)
const activeSection = ref('home')

const navItems = [
  { id: 'home', label: '首页' },
  { id: 'map', label: '诗词山河' },
  { id: 'compare', label: '唐宋对照' },
  { id: 'author', label: '诗人行迹' },
  { id: 'search', label: '一句诗在哪里' },
  { id: 'data', label: '数据与方法' },
]

function scrollTo(id: string) {
  const el = document.getElementById(id)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'start' })
    activeSection.value = id
  }
}

function handleScroll() {
  isScrolled.value = window.scrollY > 80
  // 检测当前section
  for (let i = navItems.length - 1; i >= 0; i--) {
    const el = document.getElementById(navItems[i].id)
    if (el && el.getBoundingClientRect().top <= 120) {
      activeSection.value = navItems[i].id
      break
    }
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll, { passive: true })
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
}

.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(245, 241, 232, 0.95);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--color-border-light);
  transition: all 0.3s;
}

.nav-bar.scrolled {
  box-shadow: var(--shadow-sm);
}

.nav-content {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.6rem 2rem;
  height: 60px;
}

.nav-logo {
  cursor: pointer;
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
}

.logo-main {
  font-size: 1.3rem;
  font-weight: 700;
  color: var(--color-ink);
  letter-spacing: 0.1em;
}

.logo-sub {
  font-size: 0.72rem;
  color: var(--color-ink-muted);
  letter-spacing: 0.05em;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 0.3rem;
}

.nav-links a {
  display: block;
  padding: 0.4rem 0.8rem;
  font-size: 0.88rem;
  color: var(--color-ink-light);
  border-radius: var(--radius);
  transition: all 0.2s;
}

.nav-links a:hover, .nav-links a.active {
  color: var(--color-accent);
  background: rgba(139, 58, 58, 0.06);
}

.nav-toggle {
  display: none;
  flex-direction: column;
  gap: 4px;
  padding: 4px;
}

.nav-toggle span {
  width: 20px;
  height: 2px;
  background: var(--color-ink);
  transition: 0.3s;
}

.nav-mobile {
  display: none;
  list-style: none;
  flex-direction: column;
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-border);
  padding: 0.5rem 0;
}

.nav-mobile a {
  display: block;
  padding: 0.8rem 2rem;
  color: var(--color-ink-light);
}

.section {
  min-height: 100vh;
  padding: 80px 2rem 4rem;
  max-width: 1400px;
  margin: 0 auto;
}

.section-home {
  min-height: 100vh;
  max-width: 100%;
  padding: 0;
}

.footer {
  text-align: center;
  padding: 3rem 2rem 4rem;
  border-top: 1px solid var(--color-border);
  background: var(--color-bg-alt);
}

.footer-title {
  font-size: 1.1rem;
  color: var(--color-ink);
  margin-bottom: 0.3rem;
}

.footer-sub {
  font-size: 0.85rem;
  color: var(--color-ink-muted);
  margin-bottom: 0.8rem;
}

.footer-note {
  font-size: 0.72rem;
  color: var(--color-ink-muted);
}

@media (max-width: 768px) {
  .nav-content {
    padding: 0 1rem;
  }
  .nav-links {
    display: none;
  }
  .nav-toggle {
    display: flex;
  }
  .nav-mobile {
    display: flex;
  }
  .logo-sub {
    display: none;
  }
  .section {
    padding: 70px 1rem 3rem;
  }
}
</style>
