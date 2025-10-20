<script setup lang="ts">
import { ref } from 'vue'

const features = ref([
    {
        title: 'Financial Data Analysis',
        description: 'Advanced analytics and visualization tools for financial market data',
        icon: '📊',
        color: '#667eea'
    },
    {
        title: 'Stock Market Insights',
        description: 'Real-time stock data processing and trend analysis',
        icon: '📈',
        color: '#764ba2'
    },
    {
        title: 'Risk Assessment',
        description: 'Comprehensive risk analysis and portfolio management tools',
        icon: '🛡️',
        color: '#f093fb'
    },
    {
        title: 'Market Prediction',
        description: 'Machine learning models for market trend forecasting',
        icon: '🔮',
        color: '#4facfe'
    }
])

const stats = ref([
    { label: 'Data Points', value: '10M+', icon: '📊' },
    { label: 'Stocks Tracked', value: '5K+', icon: '📈' },
    { label: 'Algorithms', value: '50+', icon: '⚡' },
    { label: 'Accuracy Rate', value: '95%', icon: '🎯' }
])
</script>

<template>
    <div class="home">
        <!-- Hero Section -->
        <section class="hero">
            <div class="hero-content">
                <h1 class="hero-title">
                    Financial Data Mining Platform
                </h1>
                <p class="hero-description">
                    Advanced tools and analytics for comprehensive financial market analysis,
                    risk assessment, and predictive modeling.
                </p>
                <div class="hero-actions">
                    <button class="btn-primary" @click="$router.push('/rawdata')">
                        Explore Data
                    </button>
                    <button class="btn-secondary" @click="$router.push('/book')">
                        View Resources
                    </button>
                </div>
            </div>
            <div class="hero-visual">
                <div class="chart-placeholder">
                    📈 Financial Analytics
                </div>
            </div>
        </section>

        <!-- Stats Section -->
        <section class="stats-section">
            <div class="stats-grid">
                <div v-for="stat in stats" :key="stat.label" class="stat-card">
                    <div class="stat-icon">{{ stat.icon }}</div>
                    <div class="stat-value">{{ stat.value }}</div>
                    <div class="stat-label">{{ stat.label }}</div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section class="features-section">
            <h2 class="section-title">Key Features</h2>
            <div class="features-grid">
                <div v-for="feature in features" :key="feature.title" class="feature-card"
                    :style="{ '--card-color': feature.color }">
                    <div class="feature-icon">{{ feature.icon }}</div>
                    <h3 class="feature-title">{{ feature.title }}</h3>
                    <p class="feature-description">{{ feature.description }}</p>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.home {
    max-width: 1200px;
    margin: 0 auto;
}

/* Hero Section */
.hero {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4rem;
    align-items: center;
    margin-bottom: 4rem;
    padding: 2rem 0;
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    line-height: 1.2;
}

.hero-description {
    font-size: 1.2rem;
    color: #666;
    margin-bottom: 2rem;
    line-height: 1.6;
}

.hero-actions {
    display: flex;
    gap: 1rem;
}

.btn-primary,
.btn-secondary {
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.btn-secondary {
    background: transparent;
    color: #667eea;
    border: 2px solid #667eea;
}

.btn-secondary:hover {
    background: #667eea;
    color: white;
}

.hero-visual {
    display: flex;
    justify-content: center;
    align-items: center;
}

.chart-placeholder {
    width: 300px;
    height: 200px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: 600;
    font-size: 1.2rem;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

/* Stats Section */
.stats-section {
    margin-bottom: 4rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 2rem;
}

.stat-card {
    text-align: center;
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease;
}

.stat-card:hover {
    transform: translateY(-5px);
}

.stat-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.stat-value {
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: #666;
    font-weight: 500;
}

/* Features Section */
.features-section {
    margin-bottom: 4rem;
}

.section-title {
    text-align: center;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 3rem;
    color: #333;
}

.features-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem;
}

.feature-card {
    padding: 2rem;
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    border-top: 4px solid var(--card-color);
    transition: transform 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.feature-title {
    font-size: 1.5rem;
    font-weight: 600;
    margin-bottom: 1rem;
    color: #333;
}

.feature-description {
    color: #666;
    line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 768px) {
    .hero {
        grid-template-columns: 1fr;
        text-align: center;
        gap: 2rem;
    }

    .hero-title {
        font-size: 2rem;
    }

    .stats-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .features-grid {
        grid-template-columns: 1fr;
    }

    .hero-actions {
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .stats-grid {
        grid-template-columns: 1fr;
    }

    .hero-title {
        font-size: 1.75rem;
    }

    .hero-actions {
        flex-direction: column;
        align-items: center;
    }

    .btn-primary,
    .btn-secondary {
        width: 100%;
        max-width: 200px;
    }
}
</style>
