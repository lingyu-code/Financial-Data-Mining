<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'

const books = ref([])
const title = ref('')
const author = ref('')
const search = ref('')

// 编辑状态
const editingId = ref(null)
const editTitle = ref('')
const editAuthor = ref('')

// 页面加载时获取已有书籍
onMounted(async () => {
    const res = await api.get('books/')
    books.value = res.data
})

// 添加书籍
const addBook = async () => {
    if (!title.value || !author.value) return
    try {
        const res = await api.post('books/', {
            title: title.value,
            author: author.value
        })
        books.value.push(res.data)
        title.value = ''
        author.value = ''
    } catch (err) {
        console.error('添加失败:', err)
    }
}

// 删除书籍
const deleteBook = async (id) => {
    try {
        await api.delete(`books/${id}/`)
        books.value = books.value.filter(book => book.id !== id)
    } catch (err) {
        console.error('删除失败:', err)
    }
}

// 开始编辑
const startEdit = (book) => {
    editingId.value = book.id
    editTitle.value = book.title
    editAuthor.value = book.author
}

// 保存编辑
const saveEdit = async (id) => {
    try {
        const res = await api.put(`books/${id}/`, {
            title: editTitle.value,
            author: editAuthor.value
        })
        // 更新前端数组
        const index = books.value.findIndex(b => b.id === id)
        if (index !== -1) {
            books.value[index] = res.data
        }
        editingId.value = null
    } catch (err) {
        console.error('更新失败:', err)
    }
}

// 取消编辑
const cancelEdit = () => {
    editingId.value = null
}

// 搜索过滤
const filteredBooks = computed(() => {
    if (!search.value) return books.value
    return books.value.filter(book =>
        book.title.toLowerCase().includes(search.value.toLowerCase()) ||
        book.author.toLowerCase().includes(search.value.toLowerCase())
    )
})
</script>

<template>
    <div>
        <h2>书籍列表</h2>

        <!-- 添加表单 -->
        <form @submit.prevent="addBook">
            <input v-model="title" placeholder="书名" />
            <input v-model="author" placeholder="作者" />
            <button type="submit">添加</button>
        </form>

        <!-- 搜索框 -->
        <input v-model="search" placeholder="搜索书名或作者" />

        <!-- 列表 -->
        <ul>
            <li v-for="book in filteredBooks" :key="book.id">
                <!-- 编辑状态 -->
                <template v-if="editingId === book.id">
                    <input v-model="editTitle" />
                    <input v-model="editAuthor" />
                    <button @click="saveEdit(book.id)">保存</button>
                    <button @click="cancelEdit">取消</button>
                </template>

                <!-- 普通展示 -->
                <template v-else>
                    {{ book.title }} - {{ book.author }}
                    <button @click="startEdit(book)">编辑</button>
                    <button @click="deleteBook(book.id)">删除</button>
                </template>
            </li>
        </ul>
    </div>
</template>
