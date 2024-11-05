import { createApp } from "vue"; // Ensure you are using Vue 3
import WhatsappComponent from "./App.vue"; 
import './style.css'


class WhatsappApp {
  constructor({ wrapper }) {
    this.$wrapper = $(wrapper);

    // Log to ensure wrapper element is being passed correctly
    console.log("Initializing WhatsappApp with wrapper:", this.$wrapper);

    // Check if the wrapper element exists
    if (this.$wrapper.length === 0) {
      console.error("Wrapper element not found!");
      return;
    }

    // Mount the Vue app to the wrapper element
    const app = createApp(WhatsappComponent);
    app.mount(this.$wrapper.get(0));
  }
}

// Expose the class globally using window
window.Whatsapp = WhatsappApp;
