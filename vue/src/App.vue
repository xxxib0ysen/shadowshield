<script>
import { ref, onMounted } from 'vue';
import API from '@/utils/api';

export default {
    setup() {
        const message = ref("");

        onMounted(async () => {
            try {
                const response = await API.get('/hello');
                message.value = response.data.message;  // Flask 返回的 "Hello, World!"
            } catch (error) {
                console.error("API 请求失败", error);
            }
        });

        return { message };
    }
}
</script>

<template>
    <div>
        <h1>Vue + Electron + Flask</h1>
        <p>Flask 返回的内容: {{ message }}</p>
    </div>
</template>
