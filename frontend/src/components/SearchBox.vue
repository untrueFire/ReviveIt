<template>
  <div>
    <input
      type="text"
      v-model="query"
      @input="handleInput"
      placeholder="搜索..."
    />
    <table v-if="results.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>物品名称</th>
          <th>物品描述</th>
          <th>联系方式</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="result in results" :key="result.id">
          <td>{{ result.id }}</td>
          <td>{{ result.name }}</td>
          <td>{{ result.description }}</td>
          <td>{{ result.contact_info }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

const query = ref("");
const results = ref([]);

const handleInput = async () => {
  try {
    const response = await axios.get(
      `http://localhost:8000/api/search/?q=${encodeURIComponent(query.value)}`
    );
    results.value = response.data;
  } catch (error) {
    console.log("Error fetching data:", error);
  }
};

onMounted(() => {
  handleInput();
});
</script>

<style scoped src="@/assets/css/styles.css"></style>