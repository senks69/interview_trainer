<template>
  <div class="main-page">
    <header class="header">
      <h1>Interview Trainer</h1>
      <p>Подготовка к техническим собеседованиям</p>
    </header>

    <section class="features">
      <div
        class="feature-card"
        v-for="(feature, index) in features"
        :key="index"
      >
        <h3>{{ feature.title }}</h3>
        <p>{{ feature.description }}</p>
      </div>
    </section>

    <button @click="startTraining" class="cta-button">Начать тренировку</button>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  data() {
    return {
      features: [
        {
          title: "Вопросы и ответы",
          description: "Банк вопросов с проверенными ответами",
        },
        {
          title: "Симуляция собеседования",
          description: "Режим имитации реального интервью",
        },
        {
          title: "Прогресс",
          description: "Отслеживание вашего прогресса",
        },
      ],
    };
  },
  methods: {
    startTraining() {
      // Навигация к тренировке
      this.$router.push("/interview");
    },
  },
};
</script>

<style scoped>
.main-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}

.header {
  margin-bottom: 3rem;
}

.features {
  display: flex;
  justify-content: space-between;
  margin: 3rem 0;
}

.feature-card {
  flex: 1;
  padding: 1.5rem;
  margin: 0 1rem;
  border: 1px solid #eaeaea;
  border-radius: 8px;
}

.cta-button {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>
