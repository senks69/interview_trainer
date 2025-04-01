<template>
  <div class="auth-container">
    <h1>Вход</h1>
    <div v-if="error_msg" class="error">{{ error_msg }}</div>
    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>Email</label>
        <input v-model="email" type="email" required />
      </div>
      <div class="form-group">
        <label>Пароль</label>
        <input v-model="password" type="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "AuthPage",
  data() {
    return {
      email: "",
      password: "",
      error_msg: "",
    };
  },
  methods: {
    handleSubmit() {
      console.log(this.email, this.password);
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
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
.form-group {
  margin-bottom: 15px;
}
</style>
