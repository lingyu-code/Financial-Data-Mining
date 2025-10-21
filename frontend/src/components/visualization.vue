<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Sample financial data for visualization
const stockData = ref([
    { date: '2024-01', price: 150, volume: 1000000 },
    { date: '2024-02', price: 165, volume: 1200000 },
    { date: '2024-03', price: 142, volume: 900000 },
    { date: '2024-04', price: 178, volume: 1500000 },
    { date: '2024-05', price: 195, volume: 1800000 },
    { date: '2024-06', price: 182, volume: 1300000 },
    { date: '2024-07', price: 210, volume: 2000000 },
    { date: '2024-08', price: 198, volume: 1600000 },
    { date: '2024-09', price: 225, volume: 2200000 },
    { date: '2024-10', price: 240, volume: 2500000 }
])

const portfolioData = ref([
    { name: 'Stocks', value: 45, color: '#667eea' },
    { name: 'Bonds', value: 25, color: '#764ba2' },
    { name: 'Cash', value: 15, color: '#f093fb' },
    { name: 'Real Estate', value: 10, color: '#4facfe' },
    { name: 'Commodities', value: 5, color: '#43e97b' }
])

const marketIndices = ref([
    { name: 'S&P 500', value: 4500, change: '+2.3%', trend: 'up' },
    { name: 'NASDAQ', value: 15000, change: '+3.1%', trend: 'up' },
    { name: 'Dow Jones', value: 35000, change: '+1.8%', trend: 'up' },
    { name: 'FTSE 100', value: 7500, change: '-0.5%', trend: 'down' }
])

const selectedChart = ref('line')
const timeRange = ref('6m')

const chartTypes = [
    { id: 'line', name: 'Line Chart', icon: '📈' },
    { id: 'bar', name: 'Bar Chart', icon: '📊' },
    { id: 'pie', name: 'Pie Chart', icon: '🥧' },
    { id: 'area', name: 'Area Chart', icon: '📉' }
]

const timeRanges = [
    { id: '1m', name: '1 Month' },
    { id: '3m', name: '3 Months' },
    { id: '6m', name: '6 Months' },
    { id: '1y', name: '1 Year' },
    { id: 'all', name: 'All Time' }
]

// Function to simulate chart rendering (in a real app, you'd use a charting library)
const renderChart = () => {
    console.log(`Rendering ${selectedChart.value} chart for ${timeRange.value} time range`)
}

onMounted(() => {
    renderChart()
})
</script>

<template>
    <div class="visualization">
        <!-- Header Section -->
        <section class="header-section">
            <h1 class="page-title">Financial Data Visualization</h1>
            <p class="page-description">
                Interactive charts and analytics for comprehensive financial market insights
            </p>
        </section>

        <!-- Controls Section -->
        <section class="controls-section">
            <div class="controls-grid">
                <div class="control-group">
                    <label class="control-label">Chart Type</label>
                    <div class="chart-type-selector">
                        <button v-for="chart in chartTypes" :key="chart.id" class="chart-type-btn"
                            :class="{ active: selectedChart === chart.id }" @click="selectedChart = chart.id">
                            <span class="chart-icon">{{ chart.icon }}</span>
                            <span class="chart-name">{{ chart.name }}</span>
                        </button>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Time Range</label>
                    <div class="time-range-selector">
                        <button v-for="range in timeRanges" :key="range.id" class="time-range-btn"
                            :class="{ active: timeRange === range.id }" @click="timeRange = range.id">
                            {{ range.name }}
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- Main Visualization Area -->
        <section class="visualization-section">
            <div class="chart-container">
                <div class="chart-header">
                    <h3 class="chart-title">Stock Price Analysis</h3>
                    <div class="chart-actions">
                        <button class="action-btn">Export</button>
                        <button class="action-btn">Share</button>
                    </div>
                </div>

                <div class="chart-placeholder">
                    <div class="chart-content">
                        <div class="chart-type-indicator">
                            {{chartTypes.find(c => c.id === selectedChart)?.icon}}
                            {{chartTypes.find(c => c.id === selectedChart)?.name}}
                        </div>
                        <div class="chart-data-preview">
                            <div v-for="item in stockData" :key="item.date" class="data-point">
                                <span class="date">{{ item.date }}</span>
                                <span class="price">${{ item.price }}</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Market Overview Section -->
        <section class="market-overview">
            <h2 class="section-title">Market Overview</h2>
            <div class="indices-grid">
                <div v-for="index in marketIndices" :key="index.name" class="index-card"
                    :class="{ 'trend-up': index.trend === 'up', 'trend-down': index.trend === 'down' }">
                    <div class="index-name">{{ index.name }}</div>
                    <div class="index-value">{{ index.value.toLocaleString() }}</div>
                    <div class="index-change" :class="index.trend">
                        {{ index.change }}
                    </div>
                </div>
            </div>
        </section>

        <!-- Portfolio Distribution Section -->
        <section class="portfolio-section">
            <h2 class="section-title">Portfolio Distribution</h2>
            <div class="portfolio-grid">
                <div class="pie-chart-placeholder">
                    <div class="pie-chart">
                        <div v-for="item in portfolioData" :key="item.name" class="pie-segment" :style="{
                            '--segment-color': item.color,
                            '--segment-value': item.value
                        }"></div>
                    </div>
                </div>
                <div class="portfolio-legend">
                    <div v-for="item in portfolioData" :key="item.name" class="legend-item">
                        <div class="legend-color" :style="{ backgroundColor: item.color }"></div>
                        <div class="legend-text">
                            <span class="legend-name">{{ item.name }}</span>
                            <span class="legend-value">{{ item.value }}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Data Metrics Section -->
        <section class="metrics-section">
            <h2 class="section-title">Key Metrics</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-icon">📈</div>
                    <div class="metric-value">24.5%</div>
                    <div class="metric-label">Annual Return</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">⚡</div>
                    <div class="metric-value">12.3%</div>
                    <div class="metric-label">Volatility</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">🛡️</div>
                    <div class="metric-value">0.85</div>
                    <div class="metric-label">Sharpe Ratio</div>
                </div>
                <div class="metric-card">
                    <div class="metric-icon">📊</div>
                    <div class="metric-value">95%</div>
                    <div class="metric-label">Accuracy</div>
                </div>
            </div>
        </section>
    </div>
</template>

<style scoped>
.visualization {
    max-width: 1200px;
    margin: 0 auto;
}

/* Header Section */
.header-section {
    text-align: center;
    margin-bottom: 3rem;
    padding: 2rem 0;
}

.page-title {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
}

.page-description {
    font-size: 1.2rem;
    color: #666;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Controls Section */
.controls-section {
    background: white;
    border-radius: 12px;
    padding: 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

.controls-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
}

.control-group {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.control-label {
    font-weight: 600;
    color: #333;
    font-size: 1.1rem;
}

.chart-type-selector,
.time-range-selector {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
}

.chart-type-btn,
.time-range-btn {
    padding: 0.75rem 1rem;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    background: white;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-weight: 500;
}

.chart-type-btn:hover,
.time-range-btn:hover {
    border-color: #667eea;
    transform: translateY(-2px);
}

.chart-type-btn.active,
.time-range-btn.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-color: #667eea;
}

.chart-icon {
    font-size: 1.2rem;
}

/* Visualization Section */
.visualization-section {
    margin-bottom: 3rem;
}

.chart-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    overflow: hidden;
}

.chart-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid #e1e5e9;
}

.chart-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
    margin: 0;
}

.chart-actions {
    display: flex;
    gap: 0.5rem;
}

.action-btn {
    padding: 0.5rem 1rem;
    border: 1px solid #667eea;
    border-radius: 6px;
    background: white;
    color: #667eea;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
}

.action-btn:hover {
    background: #667eea;
    color: white;
}

.chart-placeholder {
    height: 400px;
    padding: 2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.chart-content {
    text-align: center;
}

.chart-type-indicator {
    font-size: 1.5rem;
    font-weight: 600;
    color: #667eea;
    margin-bottom: 2rem;
}

.chart-data-preview {
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    justify-content: center;
}

.data-point {
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
}

.date {
    font-size: 0.9rem;
    color: #666;
}

.price {
    font-size: 1.1rem;
    font-weight: 600;
    color: #333;
}

/* Market Overview */
.market-overview {
    margin-bottom: 3rem;
}

.section-title {
    font-size: 2rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 2rem;
    text-align: center;
}

.indices-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
}

.index-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease;
    border-top: 4px solid transparent;
}

.index-card:hover {
    transform: translateY(-5px);
}

.index-card.trend-up {
    border-top-color: #28a745;
}

.index-card.trend-down {
    border-top-color: #dc3545;
}

.index-name {
    font-size: 1rem;
    color: #666;
    margin-bottom: 0.5rem;
}

.index-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: #333;
    margin-bottom: 0.5rem;
}

.index-change {
    font-size: 1rem;
    font-weight: 600;
}

.index-change.up {
    color: #28a745;
}

.index-change.down {
    color: #dc3545;
}

/* Portfolio Section */
.portfolio-section {
    margin-bottom: 3rem;
}

.portfolio-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3rem;
    align-items: center;
}

.pie-chart-placeholder {
    display: flex;
    justify-content: center;
}

.pie-chart {
    width: 200px;
    height: 200px;
    border-radius: 50%;
    background: conic-gradient(var(--segment-color) 0% calc(var(--segment-value) * 1%),
            transparent calc(var(--segment-value) * 1%) 100%);
    position: relative;
}

.pie-segment {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 50%;
}

.portfolio-legend {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.legend-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    background: white;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.legend-color {
    width: 20px;
    height: 20px;
    border-radius: 4px;
}

.legend-text {
    display: flex;
    justify-content: space-between;
    flex: 1;
}

.legend-name {
    font-weight: 500;
    color: #333;
}

.legend-value {
    font-weight: 600;
    color: #667eea;
}

/* Metrics Section */
.metrics-section {
    margin-bottom: 3rem;
}

.metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
}

.metric-card {
    background: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
    transition: transform 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
}

.metric-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
}

.metric-value {
    font-size: 2rem;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 0.5rem;
}

.metric-label {
    color: #666;
    font-weight: 500;
}

/* Responsive Design */
@media (max-width: 768px) {
    .controls-grid {
        grid-template-columns: 1fr;
    }

    .indices-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .portfolio-grid {
        grid-template-columns: 1fr;
        gap: 2rem;
    }

    .metrics-grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .chart-header {
        flex-direction: column;
        gap: 1rem;
    }

    .chart-actions {
        justify-content: center;
    }
}

@media (max-width: 480px) {
    .indices-grid {
        grid-template-columns: 1fr;
    }

    .metrics-grid {
        grid-template-columns: 1fr;
    }

    .chart-type-selector,
    .time-range-selector {
        flex-direction: column;
    }

    .chart-type-btn,
    .time-range-btn {
        width: 100%;
        justify-content: center;
    }
}
</style>
