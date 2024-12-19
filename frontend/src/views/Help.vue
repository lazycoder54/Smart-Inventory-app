<template>
  <div class="faq-container">
    <h2 class="faq-title">Frequently Asked Questions</h2>

    <div v-for="(faq, index) in faqs" :key="index" class="faq-item">
      <div class="question">
        <button @click="toggleAnswer(index)" class="question-button">
          {{ faq.question }}
        </button>
      </div>
      <div v-if="faq.showAnswer" class="answer">
        <p>{{ faq.answer }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      faqs: [
        {
          question: "What is a smart inventory management system?",
          answer:
            "A smart inventory management system automates and optimizes the tracking, management, and control of inventory using real-time data, IoT devices, and advanced analytics.",
          showAnswer: false,
        },
        {
          question: "How can a smart system improve my inventory management?",
          answer:
            "It can provide real-time tracking, automatic stock updates, alerts for reordering, and predictive analytics to prevent overstocking or stockouts.",
          showAnswer: false,
        },
        {
          question: "Can I integrate this system with my existing software?",
          answer:
            "Yes, most smart inventory management systems offer integration capabilities with popular ERP and accounting software.",
          showAnswer: false,
        },
        {
          question: "Is this system cloud-based or on-premise?",
          answer:
            "It can be either. Many systems are cloud-based for flexibility and ease of access, but some offer on-premise deployment for businesses with specific security requirements.",
          showAnswer: false,
        },
      ],
    };
  },
  methods: {
    toggleAnswer(index) {
      this.faqs[index].showAnswer = !this.faqs[index].showAnswer;
    },
  },
};
</script>

<style scoped>
html,
body {
  height: 100%;
  margin: 0;
}

.faq-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  width: 100%;
  padding: 2rem;
  background-color: #f9fafb;
  overflow-y: auto;
}

.faq-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  color: #333;
}

.faq-item {
  width: 100%;
  max-width: 800px;
  margin-bottom: 1.5rem;
}

.question {
  background-color: #4caf50;
  color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  width: 100%;
  text-align: left;
}

.question-button {
  background: none;
  border: none;
  color: white;
  font-size: 1.25rem;
  font-weight: 600;
  width: 100%;
  text-align: left;
}

.question-button:hover {
  text-decoration: underline;
}

.answer {
  background-color: #e8f5e9;
  padding: 1rem;
  margin-top: 0.5rem;
  border-radius: 0.5rem;
  border-left: 4px solid #4caf50;
}
</style>
