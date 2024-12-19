<template>
  <div class="container">
    <h1 class="title">Notifications</h1>
    <p class="description">View your notifications.</p>

    <!-- Notification List -->
    <div v-if="notifications.length" class="notification-list">
      <div
        v-for="(notification, index) in notifications.slice().reverse()"
        :key="index"
        class="notification-item"
      >
        {{ notification.message }}
      </div>
    </div>
    <div v-else class="no-notifications">No notifications yet.</div>
    <div>
      <button @click="clearNotifications" class="clear-notifications-btn">
        Clear All Notifications
      </button>
    </div>
  </div>
</template>

<script>
import { useToast } from "vue-toastification";
import notificationSound from "../assets/notification.mp3";

export default {
  name: "Notifications",
  data() {
    return {
      notifications: JSON.parse(localStorage.getItem("notifications")) || [],
      audio: new Audio(notificationSound),
    };
  },
  methods: {
    handleRealTimeUpdate(data) {
      const toast = useToast();
      let message = "";

      if (data.action === "move") {
        message = `ID: ${data.item.id} Item ${data.item.name} moved from ${data.source_location} to ${data.destination_location}. Quantity Change: ${data.change}. New Quantity: ${data.new_quantity}`;
      } else if (data.action === "add") {
        message = `ID: ${data.item.id} Item ${data.item.name} added to inventory. Initial Quantity: ${data.item.quantity}`;
      } else if (data.action === "update") {
        message = `ID: ${data.item.id} Item ${data.item.name}  updated. New Quantity: ${data.item.quantity}`;
      }

      this.notifications.push({ message });

      if (this.notifications.length > 20) {
        this.notifications.shift();
      }

      localStorage.setItem("notifications", JSON.stringify(this.notifications));

      toast.info(message, {
        timeout: false,
        closeOnClick: true,
        draggable: true,
      });

      this.playNotificationSound();
    },
    playNotificationSound() {
      this.audio.play().catch((error) => {
        
      });
    },
    clearNotifications() {
      this.notifications = [];
      localStorage.removeItem("notifications");
    },
  },
  mounted() {
    this.$socket.off("inventory_update");
    this.$socket.on("inventory_update", this.handleRealTimeUpdate);
  },
  beforeDestroy() {
    this.$socket.off("inventory_update", this.handleRealTimeUpdate);
  },
};
</script>

<style scoped>
.container {
  padding: 2rem;
  background-color: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 2rem auto;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #0284c7;
  margin-bottom: 1rem;
}

.description {
  font-size: 1rem;
  color: #0369a1;
}

.notification-list {
  margin-top: 1rem;
}

.notification-item {
  background-color: #e0f2fe;
  padding: 1rem;
  border: 1px solid #7dd3fc;
  border-radius: 0.25rem;
  margin-bottom: 0.5rem;
  color: #0369a1;
}

.no-notifications {
  color: #64748b;
  margin-top: 1rem;
}

.clear-notifications-btn {
  background-color: #0284c7;
  color: white;
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  margin-top: 1rem;
}

.clear-notifications-btn:hover {
  background-color: #0369a1;
}
</style>
