<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'

const papers = ref([])
const selectedPaper = ref(null)
const analysisResult = ref(null)
const loading = ref(false)
const search = ref('')

// 页面加载时获取已有论文
onMounted(async () => {
    try {
        const res = await api.get('papers/')
        papers.value = res.data
    } catch (err) {
        console.error('获取论文列表失败:', err)
    }
})

// 选择论文进行分析
const selectPaper = async (paper) => {
    selectedPaper.value = paper
    loading.value = true
    analysisResult.value = null

    try {
        const res = await api.get(`papers/${paper.id}/analyze/`)
        analysisResult.value = res.data.analysis
    } catch (err) {
        console.error('分析论文失败:', err)
        alert('分析论文失败: ' + (err.response?.data?.error || err.message))
    } finally {
        loading.value = false
    }
}

// 返回论文列表
const backToList = () => {
    selectedPaper.value = null
    analysisResult.value = null
}

// 搜索过滤
const filteredPapers = computed(() => {
    if (!search.value) return papers.value
    const searchLower = search.value.toLowerCase()
    return papers.value.filter(paper =>
        paper.title.toLowerCase().includes(searchLower) ||
        paper.author.toLowerCase().includes(searchLower) ||
        (paper.keywords && paper.keywords.toLowerCase().includes(searchLower))
    )
})

// 下载PDF
const downloadPDF = (paper) => {
    if (paper.pdf_file) {
        window.open(paper.pdf_file, '_blank')
    }
}
</script>

<template>
    <div class="paper-analysis-container">
        <h2>论文分析</h2>

        <!-- 论文列表视图 -->
        <div v-if="!selectedPaper" class="paper-list-view">
            <!-- 搜索框 -->
            <div class="search-section">
                <input v-model="search" placeholder="搜索论文标题、作者或关键词" class="search-input" />
            </div>

            <!-- 论文列表 -->
            <div class="papers-list">
                <h3>选择论文进行分析 ({{ filteredPapers.length }})</h3>

                <div v-if="filteredPapers.length === 0" class="empty-state">
                    暂无论文数据
                </div>

                <div v-else class="paper-cards">
                    <div v-for="paper in filteredPapers" :key="paper.id" class="paper-card">
                        <div class="paper-header">
                            <h4 class="paper-title">{{ paper.title }}</h4>
                            <div class="paper-actions">
                                <button @click="downloadPDF(paper)" class="download-btn">📄 查看PDF</button>
                                <button @click="selectPaper(paper)" class="analyze-btn">🔍 分析论文</button>
                            </div>
                        </div>

                        <div class="paper-meta">
                            <span class="author">作者: {{ paper.author || '未知' }}</span>
                            <span class="upload-date">上传时间: {{ new Date(paper.upload_date).toLocaleString() }}</span>
                        </div>

                        <div v-if="paper.keywords" class="keywords">
                            <strong>关键词:</strong> {{ paper.keywords }}
                        </div>

                        <div v-if="paper.abstract" class="abstract">
                            <strong>摘要:</strong> {{ paper.abstract }}
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 分析结果视图 -->
        <div v-else class="analysis-view">
            <div class="analysis-header">
                <button @click="backToList" class="back-btn">← 返回论文列表</button>
                <h3>{{ selectedPaper.title }} - 分析结果</h3>
            </div>

            <div v-if="loading" class="loading">
                正在分析论文...
            </div>

            <div v-else-if="analysisResult" class="analysis-content">
                <!-- 基本信息 -->
                <div class="analysis-section">
                    <h4>基本信息</h4>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>论文标题:</label>
                            <span>{{ analysisResult.title }}</span>
                        </div>
                        <div class="info-item">
                            <label>作者:</label>
                            <span>{{ analysisResult.author }}</span>
                        </div>
                        <div class="info-item">
                            <label>总字数:</label>
                            <span>{{ analysisResult.word_count }} 字</span>
                        </div>
                    </div>
                </div>

                <!-- 关键词分析 -->
                <div class="analysis-section">
                    <h4>关键词分析</h4>
                    <div class="keyword-analysis">
                        <div class="keyword-stats">
                            <span class="stat-item">关键词数量: {{ analysisResult.keyword_analysis.total_keywords }}</span>
                        </div>
                        <div v-if="analysisResult.keyword_analysis.keywords.length > 0" class="keyword-tags">
                            <span v-for="keyword in analysisResult.keyword_analysis.keywords" :key="keyword"
                                class="keyword-tag">
                                {{ keyword.trim() }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- 摘要分析 -->
                <div class="analysis-section">
                    <h4>摘要分析</h4>
                    <div class="abstract-analysis">
                        <div class="abstract-stats">
                            <span class="stat-item">摘要长度: {{ analysisResult.abstract_analysis.length }} 字符</span>
                            <span class="stat-item">句子数量: {{ analysisResult.abstract_analysis.sentences }} 句</span>
                        </div>
                    </div>
                </div>

                <!-- 主题分析 -->
                <div class="analysis-section">
                    <h4>主题分析</h4>
                    <div class="theme-analysis">
                        <div class="theme-tags">
                            <span v-for="theme in analysisResult.themes" :key="theme" class="theme-tag">
                                {{ theme }}
                            </span>
                        </div>
                    </div>
                </div>

                <!-- 建议 -->
                <div class="analysis-section">
                    <h4>研究建议</h4>
                    <div class="recommendations">
                        <ul>
                            <li v-for="(recommendation, index) in analysisResult.recommendations" :key="index"
                                class="recommendation-item">
                                {{ recommendation }}
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.paper-analysis-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.search-section {
    margin-bottom: 2rem;
}

.search-input {
    width: 100%;
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.papers-list h3 {
    margin-bottom: 1rem;
    color: #333;
}

.empty-state {
    text-align: center;
    padding: 3rem;
    color: #666;
    font-style: italic;
}

.paper-cards {
    display: grid;
    gap: 1.5rem;
}

.paper-card {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s, box-shadow 0.2s;
}

.paper-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.paper-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1rem;
}

.paper-title {
    margin: 0;
    color: #333;
    flex: 1;
    margin-right: 1rem;
    font-size: 1.2rem;
}

.paper-actions {
    display: flex;
    gap: 0.5rem;
}

.paper-actions button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 0.9rem;
}

.download-btn {
    background: #28a745;
    color: white;
}

.analyze-btn {
    background: #007bff;
    color: white;
}

.paper-meta {
    display: flex;
    gap: 2rem;
    margin-bottom: 1rem;
    color: #666;
    font-size: 0.9rem;
}

.keywords,
.abstract {
    margin-bottom: 0.5rem;
    color: #555;
}

.abstract {
    line-height: 1.5;
}

/* 分析视图样式 */
.analysis-view {
    background: white;
    border-radius: 8px;
    padding: 2rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.analysis-header {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e9ecef;
}

.back-btn {
    background: #6c757d;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    text-decoration: none;
}

.back-btn:hover {
    background: #5a6268;
}

.analysis-header h3 {
    margin: 0;
    color: #333;
}

.loading {
    text-align: center;
    padding: 3rem;
    color: #666;
    font-size: 1.1rem;
}

.analysis-content {
    display: flex;
    flex-direction: column;
    gap: 2rem;
}

.analysis-section {
    border: 1px solid #e9ecef;
    border-radius: 6px;
    padding: 1.5rem;
}

.analysis-section h4 {
    margin: 0 0 1rem 0;
    color: #495057;
    border-bottom: 1px solid #dee2e6;
    padding-bottom: 0.5rem;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
}

.info-item label {
    font-weight: 600;
    color: #666;
    font-size: 0.9rem;
}

.info-item span {
    color: #333;
    font-size: 1rem;
}

.keyword-analysis,
.abstract-analysis,
.theme-analysis {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.keyword-stats,
.abstract-stats {
    display: flex;
    gap: 2rem;
}

.stat-item {
    background: #e9ecef;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    font-size: 0.9rem;
    color: #495057;
}

.keyword-tags,
.theme-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.keyword-tag,
.theme-tag {
    background: #007bff;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
}

.theme-tag {
    background: #28a745;
}

.recommendations ul {
    margin: 0;
    padding-left: 1.5rem;
}

.recommendation-item {
    margin-bottom: 0.5rem;
    line-height: 1.5;
    color: #495057;
}

@media (max-width: 768px) {
    .paper-analysis-container {
        padding: 1rem;
    }

    .paper-header {
        flex-direction: column;
        gap: 1rem;
    }

    .paper-actions {
        width: 100%;
        justify-content: flex-start;
    }

    .paper-meta {
        flex-direction: column;
        gap: 0.5rem;
    }

    .analysis-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }

    .info-grid {
        grid-template-columns: 1fr;
    }

    .keyword-stats,
    .abstract-stats {
        flex-direction: column;
        gap: 0.5rem;
    }
}
</style>
