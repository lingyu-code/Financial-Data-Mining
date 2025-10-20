<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const isMenuOpen = ref(false)

const navigationItems = [
    { name: 'Home', path: '/', icon: '🏠' },
    { name: 'Financial Books', path: '/book', icon: '📚' },
    { name: 'Raw Data', path: '/rawdata', icon: '📊' }
]

const navigateTo = (path: string) => {
    router.push(path)
    isMenuOpen.value = false
}

const toggleMenu = () => {
    isMenuOpen.value = !isMenuOpen.value
}
</script>

<template>
    <nav class="navbar">
        <div class="nav-container">
            <!-- Logo/Brand -->
            <div class="nav-brand">
                <span class="brand-icon">📈</span>
                <span class="brand-text">Financial Data Mining</span>
            </div>

            <!-- Desktop Navigation -->
            <div class="nav-menu">
                <div v-for="item in navigationItems" :key="item.name" class="nav-item"
                    :class="{ active: $route.path === item.path }" @click="navigateTo(item.path)">
                    <span class="nav-icon">{{ item.icon }}</span>
                    <span class="nav-text">{{ item.name }}</span>
                </div>
            </div>

            <!-- Mobile Menu Button -->
            <button class="mobile-menu-button" @click="toggleMenu">
                <span class="menu-icon">☰</span>
            </button>
        </div>

        <!-- Mobile Navigation -->
        <div v-show="isMenuOpen" class="mobile-menu">
            <div v-for="item in navigationItems" :key="item.name" class="mobile-nav-item"
                :class="{ active: $route.path === item.path }" @click="navigateTo(item.path)">
                <span class="nav-icon">{{ item.icon }}</span>
                <span class="nav-text">{{ item.name }}</span>
            </div>
        </div>
    </nav>
</template>

<style scoped>
.navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 60px;
}

.nav-brand {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: white;
    font-weight: bold;
    font-size: 1.2rem;
}

.brand-icon {
    font-size: 1.5rem;
}

.nav-menu {
    display: flex;
    gap: 1rem;
    align-items: center;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.5rem 1rem;
    color: white;
    cursor: pointer;
    border-radius: 8px;
    transition: all 0.3s ease;
    font-weight: 500;
}

.nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

.nav-item.active {
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.nav-icon {
    font-size: 1.1rem;
}

.mobile-menu-button {
    display: none;
    background: none;
    border: none;
    color: white;
    font-size: 1.5rem;
    cursor: pointer;
    padding: 0.5rem;
}

.mobile-menu {
    display: none;
    background: rgba(102, 126, 234, 0.95);
    backdrop-filter: blur(10px);
    padding: 1rem;
}

.mobile-nav-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.75rem 1rem;
    color: white;
    cursor: pointer;
    border-radius: 6px;
    transition: background-color 0.3s ease;
    margin-bottom: 0.5rem;
}

.mobile-nav-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.mobile-nav-item.active {
    background: rgba(255, 255, 255, 0.2);
}

/* Responsive Design */
@media (max-width: 768px) {
    .nav-menu {
        display: none;
    }

    .mobile-menu-button {
        display: block;
    }

    .mobile-menu {
        display: block;
    }

    .nav-brand .brand-text {
        font-size: 1rem;
    }
}

@media (max-width: 480px) {
    .nav-brand .brand-text {
        display: none;
    }
}
</style>
