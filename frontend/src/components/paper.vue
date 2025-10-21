<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'

const papers = ref([])
const title = ref('')
const author = ref('')
const abstract = ref('')
const keywords = ref('')
const pdfFile = ref(null)
const search = ref('')

// 编辑状态
const editingId = ref(null)
const editTitle = ref('')
const editAuthor = ref('')
const editAbstract = ref('')
const editKeywords = ref('')

// 页面加载时获取已有论文
onMounted(async () => {
    const res = await api.get('papers/')
    papers.value = res.data
})

// 处理文件选择
const handleFileSelect = (event) => {
    pdfFile.value = event.target.files[0]
}

// 上传论文
const uploadPaper = async () => {
    if (!title.value || !pdfFile.value) {
        alert('请填写论文标题并选择PDF文件')
        return
    }

    try {
        const formData = new FormData()
        formData.append('title', title.value)
        formData.append('author', author.value)
        formData.append('abstract', abstract.value)
        formData.append('keywords', keywords.value)
        formData.append('pdf_file', pdfFile.value)

        const res = await api.post('papers/upload_pdf/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        papers.value.unshift(res.data.paper)

        // 重置表单
        title.value = ''
        author.value = ''
        abstract.value = ''
        keywords.value = ''
        pdfFile.value = null
        document.getElementById('pdf-file').value = ''

        alert('论文上传成功！')
    } catch (err) {
        console.error('上传失败:', err)
        alert('上传失败: ' + (err.response?.data?.error || err.message))
    }
}

// 删除论文
const deletePaper = async (id) => {
    if (!confirm('确定要删除这篇论文吗？')) return

    try {
        await api.delete(`papers/${id}/`)
        papers.value = papers.value.filter(paper => paper.id !== id)
    } catch (err) {
        console.error('删除失败:', err)
        alert('删除失败: ' + err.message)
    }
}

// 开始编辑
const startEdit = (paper) => {
    editingId.value = paper.id
    editTitle.value = paper.title
    editAuthor.value = paper.author
    editAbstract.value = paper.abstract || ''
    editKeywords.value = paper.keywords || ''
}

// 保存编辑
const saveEdit = async (id) => {
    try {
        const res = await api.put(`papers/${id}/`, {
            title: editTitle.value,
            author: editAuthor.value,
            abstract: editAbstract.value,
            keywords: editKeywords.value
        })

        const index = papers.value.findIndex(p => p.id === id)
        if (index !== -1) {
            papers.value[index] = res.data
        }
        editingId.value = null
    } catch (err) {
        console.error('更新失败:', err)
        alert('更新失败: ' + err.message)
    }
}

// 取消编辑
const cancelEdit = () => {
    editingId.value = null
}

// 下载PDF
const downloadPDF = (paper) => {
    if (paper.pdf_file) {
        window.open(paper.pdf_file, '_blank')
    }
}

// 搜索过滤
const filteredPapers = computed(() => {
    if (!search.value) return papers.value
    const searchLower = search.value.toLowerCase()
    return papers.value.filter(paper =>
        paper.title.toLowerCase().includes(searchLower) ||
        paper.author.toLowerCase().includes(searchLower) ||
        (paper.keywords && paper.keywords.toLowerCase().includes(searchLower)) ||
        (paper.abstract && paper.abstract.toLowerCase().includes(searchLower))
    )
})
</script>

<template>
    <div class="paper-container">
        <h2>金融论文管理</h2>

        <!-- 上传表单 -->
        <div class="upload-form">
            <h3>上传新论文</h3>
            <form @submit.prevent="uploadPaper" class="form-grid">
                <div class="form-group">
                    <label>论文标题 *</label>
                    <input v-model="title" placeholder="请输入论文标题" required />
                </div>

                <div class="form-group">
                    <label>作者</label>
                    <input v-model="author" placeholder="请输入作者姓名" />
                </div>

                <div class="form-group">
                    <label>关键词</label>
                    <input v-model="keywords" placeholder="请输入关键词，用逗号分隔" />
                </div>

                <div class="form-group full-width">
                    <label>摘要</label>
                    <textarea v-model="abstract" placeholder="请输入论文摘要" rows="3"></textarea>
                </div>

                <div class="form-group full-width">
                    <label>PDF文件 *</label>
                    <input type="file" id="pdf-file" @change="handleFileSelect" accept=".pdf" required />
                    <small>仅支持PDF格式文件</small>
                </div>

                <div class="form-group full-width">
                    <button type="submit" class="upload-btn">上传论文</button>
                </div>
            </form>
        </div>

        <!-- 搜索框 -->
        <div class="search-section">
            <input v-model="search" placeholder="搜索论文标题、作者、关键词或摘要" class="search-input" />
        </div>

        <!-- 论文列表 -->
        <div class="papers-list">
            <h3>论文列表 ({{ filteredPapers.length }})</h3>

            <div v-if="filteredPapers.length === 0" class="empty-state">
                暂无论文数据
            </div>

            <div v-else class="paper-cards">
                <div v-for="paper in filteredPapers" :key="paper.id" class="paper-card">
                    <!-- 编辑状态 -->
                    <template v-if="editingId === paper.id">
                        <div class="edit-form">
                            <input v-model="editTitle" class="edit-input" />
                            <input v-model="editAuthor" class="edit-input" />
                            <textarea v-model="editAbstract" class="edit-textarea" placeholder="摘要"></textarea>
                            <input v-model="editKeywords" class="edit-input" placeholder="关键词" />
                            <div class="edit-actions">
                                <button @click="saveEdit(paper.id)" class="save-btn">保存</button>
                                <button @click="cancelEdit" class="cancel-btn">取消</button>
                            </div>
                        </div>
                    </template>

                    <!-- 普通展示 -->
                    <template v-else>
                        <div class="paper-header">
                            <h4 class="paper-title">{{ paper.title }}</h4>
                            <div class="paper-actions">
                                <button @click="downloadPDF(paper)" class="download-btn">📄 查看PDF</button>
                                <button @click="startEdit(paper)" class="edit-btn">✏️ 编辑</button>
                                <button @click="deletePaper(paper.id)" class="delete-btn">🗑️ 删除</button>
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
                    </template>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.paper-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

.upload-form {
    background: #f8f9fa;
    padding: 2rem;
    border-radius: 8px;
    margin-bottom: 2rem;
}

.form-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
}

.form-group {
    display: flex;
    flex-direction: column;
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    margin-bottom: 0.5rem;
    font-weight: 500;
}

.form-group input,
.form-group textarea {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 1rem;
}

.form-group textarea {
    resize: vertical;
    min-height: 80px;
}

.upload-btn {
    background: #007bff;
    color: white;
    padding: 0.75rem 2rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
}

.upload-btn:hover {
    background: #0056b3;
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

.edit-btn {
    background: #ffc107;
    color: black;
}

.delete-btn {
    background: #dc3545;
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

.edit-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.edit-input,
.edit-textarea {
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
}

.edit-textarea {
    resize: vertical;
    min-height: 60px;
}

.edit-actions {
    display: flex;
    gap: 0.5rem;
}

.save-btn {
    background: #28a745;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.cancel-btn {
    background: #6c757d;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

@media (max-width: 768px) {
    .paper-container {
        padding: 1rem;
    }

    .form-grid {
        grid-template-columns: 1fr;
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
}
</style>
