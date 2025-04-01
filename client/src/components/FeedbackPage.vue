<template>
  <div class="feedback-container">
    <div class="feedback-card">
      <h1>Оставьте отзыв о собеседовании</h1>

      <div class="rating-section">
        <h3>Оцените собеседование:</h3>
        <div class="stars">
          <span
            v-for="star in 5"
            :key="star"
            @click="setRating(star)"
            :class="{ active: star <= rating }"
            >★</span
          >
        </div>
      </div>

      <div class="form-group">
        <label>Что прошло хорошо?</label>
        <textarea
          v-model="positiveFeedback"
          placeholder="Отметьте сильные стороны собеседования"
        ></textarea>
      </div>

      <div class="form-group">
        <label>Что можно улучшить?</label>
        <textarea
          v-model="improvementFeedback"
          placeholder="Ваши предложения по улучшению"
        ></textarea>
      </div>

      <div class="form-group">
        <label>Общий комментарий</label>
        <textarea
          v-model="generalFeedback"
          placeholder="Дополнительные мысли о собеседовании"
        ></textarea>
      </div>

      <div class="actions">
        <button @click="submitFeedback" :disabled="isSubmitting">
          {{ isSubmitting ? "Отправка..." : "Отправить отзыв" }}
        </button>
        <button @click="skipFeedback" class="skip-btn">Пропустить</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FeedbackPage",
  data() {
    return {
      rating: 0,
      positiveFeedback: "",
      improvementFeedback: "",
      generalFeedback: "",
      isSubmitting: false,
    };
  },
  methods: {
    setRating(star) {
      this.rating = star;
    },
    async submitFeedback() {
      this.isSubmitting = true;

      // Здесь должна быть логика отправки на сервер
      const feedbackData = {
        rating: this.rating,
        positive: this.positiveFeedback,
        improvement: this.improvementFeedback,
        comment: this.generalFeedback,
        date: new Date().toISOString(),
      };

      console.log("Отправка отзыва:", feedbackData);

      // Имитация задержки отправки
      await new Promise((resolve) => setTimeout(resolve, 1000));

      this.isSubmitting = false;
      this.$router.push("/"); // Перенаправление на главную после отправки
      alert("Спасибо за ваш отзыв!");
    },
    skipFeedback() {
      this.$router.push("/");
    },
  },
};
</script>

<style scoped>
.feedback-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
  padding: 20px;
}

.feedback-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 600px;
}

h1 {
  color: #2c3e50;
  text-align: center;
  margin-bottom: 30px;
  font-size: 24px;
}

.rating-section {
  margin-bottom: 25px;
  text-align: center;
}

.rating-section h3 {
  margin-bottom: 15px;
  color: #34495e;
}

.stars {
  font-size: 36px;
  cursor: pointer;
  margin-bottom: 20px;
}

.stars span {
  color: #ddd;
  transition: all 0.2s;
  margin: 0 5px;
}

.stars span.active {
  color: #ffc107;
  text-shadow: 0 0 5px rgba(255, 193, 7, 0.5);
}

.stars span:hover {
  transform: scale(1.2);
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #34495e;
  font-weight: 500;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-family: inherit;
  transition: border 0.3s;
}

textarea:focus {
  outline: none;
  border-color: #42b983;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

button {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background-color: #42b983;
  color: white;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s;
}

button:hover {
  background-color: #3aa876;
  transform: translateY(-2px);
}

button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
  transform: none;
}

.skip-btn {
  background-color: #e74c3c;
}

.skip-btn:hover {
  background-color: #c0392b;
}

@media (max-width: 600px) {
  .feedback-card {
    padding: 20px;
  }

  .actions {
    flex-direction: column;
    gap: 10px;
  }

  button {
    width: 100%;
  }
}
</style>
