<template>
  <div class="ml-[420px] w-full relative">
    <div class="border-l border-gray-500 w-full relative bg-cover bg-center h-screen"
      style="background-image: url('https://website.finbyz.com/files/message-bg%20(1).png');">
      <div class="bg-[#F0F0F0] fixed z-10 min-w-[calc(100vw-420px)] flex justify-between items-center px-2 py-2">
        <div class="flex items-center">
          <img v-if="user?.picture" class="rounded-full mx-1 w-10" :src="user.picture" />
          <div v-if="user?.firstName" class="text-gray-900 ml-1 font-semibold">
            {{ user.firstName }}
          </div>
        </div>
      </div>

      <div id="MessagesSection"
        class="pt-20 pb-8 h-[calc(100vh-65px)] w-[calc(100vw-420px)] overflow-auto fixed touch-auto">
        <div v-if="messages.length" class="px-20 text-sm">
          <div v-for="msg in messages" :key="msg.message">
            <div v-if="msg.sub === currentUserSub" class="flex justify-end w-full">
              <div class="inline-block p-2 rounded-md my-1" :class="msg.type === 'text' ? 'bg-green-200' : ''">
                <span v-if="msg.type === 'text'">{{ msg.message }}</span>
                <a v-if="msg.type === 'file'" :href="msg.message" download
                  class="text-blue-500 underline cursor-pointer">{{ msg.fileName || 'Download File' }}</a>
                <img v-if="msg.type === 'image'" :src="msg.message" alt="Uploaded Image"
                  class="max-w-200px max-h-200px rounded-md" />
              </div>
            </div>

            <div v-else class="flex justify-start w-full">
              <div class="inline-block bg-white p-2 rounded-md my-1">
                <span v-if="msg.type === 'text'">{{ msg.message }}</span>
                <a v-if="msg.type === 'file'" :href="msg.message" download
                  class="text-blue-500 underline">{{ msg.fileName || 'Download File' }}</a>
                <img v-if="msg.type === 'image'" :src="msg.message" alt="Uploaded Image"
                  class="max-w-200px max-h-200px rounded-md" />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="w-[calc(100vw-420px)] p-2.5 bg-[#F0F0F0] fixed bottom-0 z-10">
        <div class="flex items-center justify-center">
          <label for="file-upload" class="ml-3 cursor-pointer">
            <span class="plus-icon mr-3">+</span>
            <input id="file-upload" type="file" class="hidden" multiple @change="handleFileUpload" />
          </label>
          <input v-model="messageInput" @keyup.enter="sendMessage"
            class="mr-1 shadow appearance-none rounded-lg w-full py-3 px-4 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
            type="input" placeholder="Message" />
          <button @click="sendMessage" class="ml-3 p-2 w-12 flex items-center justify-center">
            Send
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue';

export default {
  name: 'MessageView',
  props: {
    user: {
      type: Object,
      required: true,
    },
  },
  setup(props) {
    const currentUserSub = 'currentUser';
    const messages = ref([]);
    const messageInput = ref('');

    const localStorageKey = () => `messages_${props.user?.sub}`;

    const loadMessages = () => {
      if (props.user) {
        const savedMessages = localStorage.getItem(localStorageKey());
        messages.value = savedMessages ? JSON.parse(savedMessages) : [];
      }
    };

    watch(
      () => props.user,
      loadMessages,
      { immediate: true }
    );

    const sendMessage = () => {
      if (messageInput.value && props.user) {
        messages.value.push({ sub: currentUserSub, message: messageInput.value, type: 'text' });
        messageInput.value = '';

        localStorage.setItem(localStorageKey(), JSON.stringify(messages.value));

        setTimeout(() => {
          const objDiv = document.getElementById('MessagesSection');
          objDiv.scrollTop = objDiv.scrollHeight;
        }, 50);
      }
    };

    const handleFileUpload = (event) => {
      const files = Array.from(event.target.files);
      files.forEach((file) => {
        const reader = new FileReader();
        reader.onload = (e) => {
          const fileType = file.type.startsWith('image/') ? 'image' : 'file';
          const fileName = file.name || `file_${Date.now()}`; // Use file name or fallback

          // Create a Blob URL for the file
          const blobUrl = URL.createObjectURL(file);

          messages.value.push({
            sub: currentUserSub,
            message: blobUrl, // Store Blob URL for display
            type: fileType,
            fileName: fileName, // Store file name for download link
          });

          localStorage.setItem(localStorageKey(), JSON.stringify(messages.value));

          setTimeout(() => {
            const objDiv = document.getElementById('MessagesSection');
            objDiv.scrollTop = objDiv.scrollHeight;
          }, 50);
        };
        reader.readAsDataURL(file);
      });
    };

    return {
      currentUserSub,
      messages,
      messageInput,
      sendMessage,
      handleFileUpload,
    };
  },
};
</script>

<style scoped>
.fixed {
  position: fixed;
}

.relative {
  position: relative;
}

.max-w-200px {
  max-width: 200px;
}

.max-h-200px {
  max-height: 200px;
}

.plus-icon {
  font-size: 2.5rem;
  line-height: 1;
}
</style>
