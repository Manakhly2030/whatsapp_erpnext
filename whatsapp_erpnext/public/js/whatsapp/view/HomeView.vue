<template>
  <div class="flex">
    <div id="Header" class="fixed w-[420px] z-10">
      <div class="bg-gray-100 w-full flex justify-between items-center px-3 py-2">
        <img
          class="rounded-full ml-1 w-10 h-10"
          :src="'https://website.finbyz.com/files/download (1).jfif'"
          alt=""
        />
        <div class="flex items-center justify-center">
          <AccountGroupIcon fillColor="#515151" class="mr-6" />
          <DotsVerticalIcon @click="logout" fillColor="#515151" class="cursor-pointer" />
        </div>
      </div>
      <div id="Search" class="bg-white px-2 border-b shadow-sm w-[420px]">
        <div class="px-1 m-2 bg-[#F0F0F0] flex items-center justify-center rounded-md">
          <MagnifyIcon fillColor="#515151" :size="18" class="ml-2" />
          <input
          v-model="searchTerm" 
            @click="showFindFriends = true"
            class="ml-5 appearance-none w-full bg-[#F0F0F0] py-1.5 px-2.5 text-gray-700 leading-tight focus:outline-none focus:shadow-outline placeholder:text-sm placeholder:text-gray-500"
            autocomplete="off"
            type="text"
            placeholder="Search chats..."
          />
        </div>
      </div>

    
      <FindFriendsView v-if="showFindFriends" @user-selected="startChat" />
    </div>

    <MessageView v-if="userDataForChat.length" :user="userDataForChat[0]" />
    <div v-else>
      <div class="ml-[420px] fixed w-[calc(100vw-420px)] h-[100vh] bg-gray-100 text-center">
        <div class="grid h-screen place-items-center">
          <div>
            <div class="w-full flex items-center justify-center">
              <img width="375" src="w-web-not-loaded-chat.png" alt="" />
            </div>
            <div class="text-[32px] text-gray-500 font-light mt-10">WhatsApp Web</div>
            <div class="text-[14px] text-gray-600 mt-2">
              <div>Send and receive messages without keeping your phone online.</div>
              <div>Use WhatsApp on up to 4 linked devices and 1 phone at the same time.</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import DotsVerticalIcon from '../../../node_modules/vue-material-design-icons/DotsVertical.vue';
import AccountGroupIcon from '../../../node_modules/vue-material-design-icons/AccountGroup.vue';
import ChatsView from './ChatsView.vue';
import MessageView from './MessageView.vue';
import FindFriendsView from './FindFriendsView.vue';
import MagnifyIcon from '../../../node_modules/vue-material-design-icons/Magnify.vue';

export default {
  name: "HomeView",
  components: {
    AccountGroupIcon,
    DotsVerticalIcon,
    ChatsView,
    MessageView,
    FindFriendsView,
    MagnifyIcon,
  },
  data() {
    return {
      showFindFriends: true,
      userDataForChat: [],
      searchTerm: '', // For search functionality
      chats: [], // This should contain your chat data
    };
  },
  computed: {
    filteredChats() {
      // Filter chats based on the search term
      return this.chats.filter(chat => {
        const userName = `${chat.user.firstName} ${chat.user.lastName}`.toLowerCase();
        const lastMessage = chat.messages[chat.messages.length - 1]?.content.toLowerCase() || '';
        return userName.includes(this.searchTerm.toLowerCase()) || lastMessage.includes(this.searchTerm.toLowerCase());
      });
    },
  },
  methods: {
    logout() {
      console.log("Logout clicked");
    },
    startChat(user) {
      this.userDataForChat = [user];
      this.showFindFriends = true;
    },
    setChat(chatData) {
      this.userDataForChat = [chatData];
      this.showFindFriends = false;
    },
  },
};

</script>

<style lang="scss" scoped>
img {
  max-width: 10%;
}
</style>
