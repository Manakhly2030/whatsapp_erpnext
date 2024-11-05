<template>
  <div :class="isActive ? 'bg-gray-200' : ''">
    <div class="flex w-full px-4 py-3 items-center cursor-pointer">
      <img class="rounded-full mr-4 w-12" :src="chat.user.picture || ''" />

      <div class="w-full">
        <div class="flex justify-between items-center">
          <div class="text-[15px] text-gray-600">
            {{ chat.user.firstName }}
          </div>
          <div class="text-[12px] text-gray-600">
            {{ lastCreatedAt }}
          </div>
        </div>
        <MagnifyIcon fillColor="#515151" :size="18" class="ml-2" />
        <DotsVerticalIcon @click="logout" fillColor="#515151" class="cursor-pointer" />
        <div class="flex items-center">
          <CheckAllIcon :size="18" :fillColor="tickColor" class="mr-1" />
          <div class="text-[15px] w-full text-gray-500 flex items-center justify-between">
            {{ lastChatMessage }}...
          </div>
        </div>
      </div>
    </div>

    <div class="border-b w-[calc(100%-80px)] float-right"></div>
  </div>
</template>

<script>
import CheckAllIcon from '../../../node_modules/vue-material-design-icons/CheckAll.vue'
import MagnifyIcon from '../../../node_modules/vue-material-design-icons/Magnify.vue';
import DotsVerticalIcon from '../../../node_modules/vue-material-design-icons/DotsVertical.vue';

import { computed } from 'vue'
import moment from 'moment'

export default {
  name: 'ChatListItem',
  components: {
    CheckAllIcon,
    MagnifyIcon,
    DotsVerticalIcon,
  },
  props: {
    chat: {
      type: Object,
      required: true,
      default: () => ({
        user: { firstName: 'John', picture: 'https://example.com/profile.jpg' },
        messages: [
          { content: 'Hello!', createdAt: new Date(), seen: false },
        ],
      }),
    },
    isActive: {
      type: Boolean,
      default: false,
    },
  },
  setup(props) {
    const lastCreatedAt = computed(() => {
      const lastMessage = props.chat.messages[props.chat.messages.length - 1]
      return lastMessage ? moment(lastMessage.createdAt).fromNow() : ''
    })

    const lastChatMessage = computed(() => {
      const lastMessage = props.chat.messages[props.chat.messages.length - 1]
      return lastMessage ? lastMessage.content : ''
    })

    const tickColor = computed(() => {
      const lastMessage = props.chat.messages[props.chat.messages.length - 1]
      return lastMessage && lastMessage.seen ? '#4FC3F7' : '#B0BEC5'
    })

    return { lastCreatedAt, lastChatMessage, tickColor }
  },
}
</script>

<style scoped>
.border-b {
  border-bottom-width: 1px;
}
img {
  max-width: 10%;
}
</style>
