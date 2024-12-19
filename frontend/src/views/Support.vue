<template>
  <div class="container">
    <h1 class="title">Support</h1>
    <p class="description">
      Need help? Contact support or explore our resources below.
    </p>

    <!-- Contact Form -->
    <div class="form-container">
      <h2 class="form-title">Contact Us</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="name">Your Name</label>
          <input
            type="text"
            id="name"
            v-model="formData.name"
            placeholder="Enter your name"
            required
          />
        </div>
        <div class="form-group">
          <label for="email">Your Email</label>
          <input
            type="email"
            id="email"
            v-model="formData.email"
            placeholder="Enter your email"
            required
          />
        </div>
        <div class="form-group">
          <label for="message">Message</label>
          <textarea
            id="message"
            v-model="formData.message"
            rows="5"
            placeholder="Write your message here..."
            required
          ></textarea>
        </div>
        <button type="submit" class="submit-button">Submit</button>
      </form>
    </div>

    <!-- Additional Support Options -->
    <div class="support-options">
      <h2 class="options-title">Explore More Support Options</h2>
      <ul class="options-list">
        <li><a href="/help" class="link">FAQs</a></li>
        <li><a href="/help-desk" class="link">Help Desk</a></li>
        <li><a href="/resources" class="link">Resource Library</a></li>
      </ul>
    </div>
  </div>

  <!-- Footer Section -->
  <footer class="bg-gray-800 text-white p-4 mt-6 text-center">
    <p>© 2024 Pranjit Das. All Rights Reserved.</p>
  </footer>
</template>

<script>
import { useToast } from "vue-toastification";
import "vue-toastification/dist/index.css";

export default {
  name: "Support",
  data() {
    return {
      formData: {
        name: "",
        email: "",
        message: "",
      },
    };
  },
  methods: {
    handleSubmit() {
      const toast = useToast();
      toast.success(
        "Thank you for contacting support. We'll get back to you shortly!"
      );

      this.formData = { name: "", email: "", message: "" };
    },
  },
};
</script>

<style scoped>
.container {
  padding: 2rem;
  background-color: #faf5ff;
  border: 1px solid #e9d5ff;
  border-radius: 0.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 2rem auto;
}

.title {
  font-size: 2rem;
  font-weight: 700;
  color: #7c3aed;
  margin-bottom: 1rem;
}

.description {
  font-size: 1rem;
  color: #6b21a8;
}

.form-container {
  margin-top: 2rem;
}

.form-title {
  font-size: 1.5rem;
  color: #7c3aed;
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #e9d5ff;
  border-radius: 0.25rem;
  font-size: 1rem;
  color: #4a5568;
  background-color: #ffffff;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #7c3aed;
  box-shadow: 0 0 0 2px rgba(124, 58, 237, 0.3);
}

.submit-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  color: #ffffff;
  background-color: #7c3aed;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #6b21a8;
}

.support-options {
  margin-top: 3rem;
}

.options-title {
  font-size: 1.5rem;
  color: #7c3aed;
  margin-bottom: 1rem;
}

.options-list {
  list-style: none;
  padding: 0;
}

.options-list li {
  margin-bottom: 0.5rem;
}

.options-list .link {
  color: #6b21a8;
  text-decoration: none;
  font-weight: 600;
}

.options-list .link:hover {
  text-decoration: underline;
}
</style>
