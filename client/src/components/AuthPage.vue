<template>
  <div class="auth-wrapper">
    <div class="auth-container">
      <div class="title-text"><img src="./../assets/key_gray.png" alt="">Вход</div>
      <div v-if="error_msg" class="error">{{ error_msg }}</div>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Логин:</label>
          <input v-model="email" type="email" required />
        </div>
        <div class="form-group">
          <label>Пароль:</label>
          <input v-model="password" type="password" required />
        </div>
        <button class="enter-btn" type="submit"><img src="./../assets/internet_connection_wiz-2.png" alt="">Войти</button>
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
.auth-wrapper{
  background-color: #0077FF54;
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;

  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'SF Compact Display', sans-serif;
}
.title-text{
  width: 100%;
  background: rgb(0,0,128);
  background: linear-gradient(90deg, rgba(0,0,128,1) 0%, rgba(16,132,208,1) 100%);
  margin: 0;
  color: #fff;
  font-family: 'SF Compact Display', sans-serif;
  font-size: 32px;
  font-weight: 900;
  display: flex;
  align-items: center;
  justify-content: center;
}
.auth-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 35px;

  width: 545px;
  height: 290px;
  background-color: #C0C0C0;
  border-bottom: 1px solid black;
  border-right: 1px solid black;
  border-top: 1px solid #ffffff;
  border-left: 1px solid #ffffff;
}
form{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 35px;
}
.form-group {
  display: flex;
  flex-direction: column;
  color: #0026FF;
  font-weight: 900;
  align-items: flex-start;
  width: 425px;
}
.form-group input{
  width: 100%;
}
.enter-btn{
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

  color: #0026FF;
  font-family: 'SF Compact Display', sans-serif;
  font-weight: 900;
  font-size: 16px;

}
</style>
