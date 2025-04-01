<template>
  <div class="auth-container">
    <h1>Вход</h1>
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
export default {
  name: "AuthPage",
  data() {
    return {
      email: "",
      password: "",
    };
  },
  methods: {
    handleSubmit() {
      console.log(this.email, this.password);
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
