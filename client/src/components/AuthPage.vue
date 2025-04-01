<template>
  <div class="auth-wrapper">
    <div
      v-for="(window, index) in windows"
      :key="index"
      class="auth-container"
      ref="authContainer"
      :style="{ left: window.x + 'px', top: window.y + 'px' }"
      @mousedown="startDrag(index, $event)"
    >
      <div class="title-text">
        <img src="./../assets/key_gray.png" alt="" />Вход
      </div>
      <div v-if="error_msg" class="error">{{ error_msg }}</div>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Логин:</label>
          <input v-model="email" required />
        </div>
        <div class="form-group">
          <label>Пароль:</label>
          <input v-model="password" type="password" required />
        </div>
        <button class="enter-btn" type="submit">Войти</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AuthPage",
  data() {
    return {
      windows: [{ x: 100, y: 100 }],
      dragging: false,
      email: "",
      password: "",
      draggedWindow: null,
      offsetX: 0,
      error_msg: "",
      offsetY: 0,
    };
  },
  methods: {
    handleSubmit() {
      console.log(this.windows.email, this.windows.password);
      axios
        .post("http://localhost:8000/login", {
          login: this.email,
          password: this.password,
        })
        .then((response) => {
          console.log(response);
          if (response.status == 200) {
            this.$router.push("/home");
          }
        })
        .catch((error) => {
          this.error_msg = "Не верный логин или пароль";
        });
    },
    startDrag(index, event) {
      this.dragging = true;
      this.draggedWindow = index;
      this.offsetX = event.clientX - this.windows[index].x;
      this.offsetY = event.clientY - this.windows[index].y;
      document.addEventListener("mousemove", this.onDrag);
      document.addEventListener("mouseup", this.stopDrag);
    },
    onDrag(event) {
      if (!this.dragging || this.draggedWindow === null) return;
      this.windows[this.draggedWindow].x = event.clientX - this.offsetX;
      this.windows[this.draggedWindow].y = event.clientY - this.offsetY;
      this.createGhostWindows(
        this.windows[this.draggedWindow].x,
        this.windows[this.draggedWindow].y
      );
    },
    stopDrag() {
      this.dragging = false;
      this.draggedWindow = null;
      document.removeEventListener("mousemove", this.onDrag);
      document.removeEventListener("mouseup", this.stopDrag);
      this.cleanupOldWindows();
    },
    createGhostWindows(x, y) {
      this.windows.push({ x: x + 10, y: y + 10, email: "", password: "" });
      if (this.windows.length > 10) {
        this.windows.shift();
      }
    },
    cleanupOldWindows() {
      if (this.windows.length > 10) {
        this.windows.splice(0, this.windows.length - 10);
      }
    },
  },
};
</script>

<style scoped>
.auth-wrapper {
  position: relative;
  background-color: #0077ff54;
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
  font-family: "SF Compact Display", sans-serif;
}
.title-text {
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
.auth-container {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 35px;

  width: 545px;
  height: 290px;
  background-color: #c0c0c0;
  border-bottom: 1px solid black;
  border-right: 1px solid black;
  border-top: 1px solid #ffffff;
  border-left: 1px solid #ffffff;
}
form {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 35px;
}
.form-group {
  display: flex;
  flex-direction: column;
  color: #0026ff;
  font-weight: 900;
  align-items: flex-start;
  width: 425px;
}
.form-group input {
  width: 100%;
}
.enter-btn {
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
}
</style>
