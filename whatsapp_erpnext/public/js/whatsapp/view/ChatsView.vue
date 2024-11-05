<template>
  <div id="Messages" class="pt-1 z-0 overflow-auto fixed h-[calc(100vh-100px)] w-[420px]">
    <div v-for="chat in chats" :key="chat.user.firstName" @click="openChat(chat)" class="hover:bg-gray-100">
      <MessageRowComponent :chat="chat" />
    </div>
  </div>
</template>

<script>
import MessageRowComponent from '../components/MessageRowComponent.vue';

export default {
  name: "ChatsView",
  components: {
    MessageRowComponent,
  },
  props: {
    chats: {
      type: Array,
      required: true,
    },
  },
  methods: {
    openChat(chat) {
      this.$emit("open-chat", chat);
    },
  },
};
</script>
