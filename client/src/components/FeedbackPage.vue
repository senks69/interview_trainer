<template>
  <div class="feedback-wrapper">
    <div
      v-for="(feedbackWindow, index) in feedbackWindows"
      :key="index"
      class="feedback-container"
      ref="feedbackContainer"
      :style="{ left: feedbackWindow.x + 'px', top: feedbackWindow.y + 'px' }"
      @mousedown="startDrag(index, $event)"
    >
      <div class="title-text">Вы прошли</div>
    </div>
  </div>
</template>

<script>
export default {
  name: "FeedbackPage",
  data() {
    return {
      feedbackWindows: [{ x: 100, y: 100 }],
    };
  },
  methods: {
    startDrag(index, event) {
      // Здесь будет логика перетаскивания окна
    },
  },
};
</script>

<style scoped>
.feedback-wrapper {
  position: relative;
  background-color: #0077ff54;
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "SF Compact Display", sans-serif;
}

.feedback-title {
  width: 100%;
  background: rgb(0, 0, 128);
  background: linear-gradient(
    90deg,
    rgba(0, 0, 128, 1) 0%,
    rgba(16, 132, 208, 1) 100%
  );
  margin: 0;
  color: #fff;
  font-family: "SF Compact Display", sans-serif;
  font-size: 32px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feedback-container {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 35px;
  width: 545px;
  height: 290px;
  background-color: #c0c0c0;
  border-bottom: 1px solid black;
  border-right: 1px solid black;
  border-top: 1px solid #ffffff;
  border-left: 1px solid #ffffff;
  box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.2);
  color: #0026ff;
  font-weight: 900;
  font-size: 24px;
}

.feedback-form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 35px;
}

.feedback-group {
  display: flex;
  flex-direction: column;
  color: #0026ff;
  font-weight: 900;
  align-items: flex-start;
  width: 425px;
}

.feedback-group input {
  width: 100%;
}

.feedback-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  width: 167px;
  height: 36px;
  border-bottom: 1px solid black;
  border-right: 1px solid black;
  border-top: 1px solid #ffffff;
  border-left: 1px solid #ffffff;
  color: #0026ff;
  font-family: "SF Compact Display", sans-serif;
  font-weight: 900;
  font-size: 16px;
  cursor: pointer;
  background-color: #c0c0c0;
}

.feedback-btn:hover {
  background-color: #b0b0b0;
}
</style>
