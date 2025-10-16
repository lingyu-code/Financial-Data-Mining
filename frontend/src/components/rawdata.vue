<template>
    <div>
        <h2>股票数据管理</h2>

        <!-- 上传 CSV -->
        <div style="margin-bottom: 20px;">
            <input type="file" @change="onFileChange" accept=".csv" />
            <button @click="uploadFile">上传CSV</button>
        </div>

        <!-- 上传进度条 -->
        <div v-if="progress > 0" style="margin-top:10px; width:300px; background:#eee;">
            <div :style="{ width: progress + '%', background: '#4caf50', height: '20px' }"></div>
        </div>
        <p v-if="progress > 0">{{ progress }}%</p>

        <!-- 股票数据表格 -->
        <table border="1" cellspacing="0" cellpadding="8">
            <thead>
                <tr>
                    <th>股票代码</th>
                    <th>交易日期</th>
                    <th>开盘价</th>
                    <th>最高价</th>
                    <th>最低价</th>
                    <th>收盘价</th>
                    <th>成交量</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="stock in stocks" :key="stock.id">
                    <td>{{ stock.ts_code }}</td>
                    <td>{{ stock.trade_date }}</td>
                    <td>{{ stock.open }}</td>
                    <td>{{ stock.high }}</td>
                    <td>{{ stock.low }}</td>
                    <td>{{ stock.close }}</td>
                    <td>{{ stock.volume }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'   // 你封装的 axios 实例

const stocks = ref([])
const file = ref(null)
const progress = ref(0)   // ✅ 定义进度条变量

// 获取股票数据
async function fetchStocks() {
    try {
        const response = await api.get('/stocks/')
        stocks.value = response.data
    } catch (error) {
        console.error('获取股票数据失败:', error)
    }
}

// 选择文件
function onFileChange(e) {
    file.value = e.target.files[0]
}

// 上传文件
async function uploadFile() {
    if (!file.value) {
        alert("请先选择文件")
        return
    }
    const formData = new FormData()
    formData.append("file", file.value)

    try {
        const response = await api.post('/stocks/upload_csv/', formData, {
            onUploadProgress: (event) => {
                if (event.total) {
                    progress.value = Math.round((event.loaded * 100) / event.total)
                }
            }
        })
        alert(response.data.message || "上传成功！")
        progress.value = 0
        fetchStocks()
    } catch (error) {
        console.error("上传失败:", error.response?.data || error.message)
        progress.value = 0
    }
}

onMounted(() => {
    fetchStocks()
})
</script>
