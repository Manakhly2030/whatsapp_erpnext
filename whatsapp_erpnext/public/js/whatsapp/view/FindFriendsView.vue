<template>
  <div id="FindFriends" class="overflow-auto fixed h-[100vh] w-full">
    <!-- User List -->
    <div
      v-for="user in filteredUsers"
      :key="user.sub"
      @click="selectUser(user)"
      class="flex w-[420px] p-4 items-center cursor-pointer hover:bg-gray-100"
    >
      <img class="rounded-full mr-4 w-12 h-12" :src="user.picture || ''" alt="User Picture" />
      <div class="w-full">
        <div class="flex justify-between items-center">
          <div class="text-[15px] text-gray-600 font-semibold">
            {{ user.firstName }} {{ user.lastName }}
          </div>
        </div>
        <div class="flex items-center">
          <div class="text-[15px] text-gray-500">Hi, I'm using WhatsApp!</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineEmits } from 'vue';

const emit = defineEmits();

// Sample data for users
const users = ref([
  { sub: 'user1', firstName: 'Alice', lastName: 'Green', picture: 'https://website.finbyz.com/files/download%20(2).jfif' },
  { sub: 'user2', firstName: 'Bob', lastName: 'Brown', picture: 'https://website.finbyz.com/files/download.jfif' },
  { sub: 'user3', firstName: 'Charlie', lastName: 'Smith', picture: 'https://website.finbyz.com/files/download%20(1).jfif' },
  { sub: 'user4', firstName: 'David', lastName: 'Johnson', picture: 'https://website.finbyz.com/files/download%20(2).jfif' },
  { sub: 'user5', firstName: 'Eva', lastName: 'Adams', picture: 'https://website.finbyz.com/files/download.jfif' },
  { sub: 'user6', firstName: 'Frank', lastName: 'Clark', picture: 'https://website.finbyz.com/files/download%20(1).jfif' },
  { sub: 'user7', firstName: 'Grace', lastName: 'Wilson', picture: 'https://website.finbyz.com/files/download%20(2).jfif' },
  { sub: 'user8', firstName: 'Hannah', lastName: 'Lee', picture: 'https://website.finbyz.com/files/download.jfif' },
  { sub: 'user9', firstName: 'Ian', lastName: 'Taylor', picture: 'https://website.finbyz.com/files/download%20(1).jfif' },
  { sub: 'user10', firstName: 'Jack', lastName: 'Anderson', picture: 'https://website.finbyz.com/files/download%20(2).jfif' },
  { sub: 'user12', firstName: 'Kira', lastName: 'Thomas', picture: 'https://website.finbyz.com/files/download.jfif' },
  { sub: 'user13', firstName: 'Liam', lastName: 'White', picture: 'https://website.finbyz.com/files/download%20(1).jfif' },
]);

const searchTerm = ref(''); // For search functionality

// Computed property to filter users based on searchTerm
const filteredUsers = computed(() => {
  return users.value.filter(user => {
    const fullName = `${user.firstName} ${user.lastName}`.toLowerCase();
    return fullName.includes(searchTerm.value.toLowerCase());
  });
});

const selectUser = (user) => {
  emit('user-selected', user);
};
</script>

<style scoped>
img {
  max-width: 10%;
}
</style>
