<template>
  <div id="app">
    <nav v-if="isAuthenticated">
      <router-link to="/home">Главная</router-link> |
      <router-link to="/about">О проекте</router-link>
    </nav>
    <router-view />
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      isAuthenticated: false,
    };
  },
  created() {},
};
</script>

<style>
@import url('https://fonts.cdnfonts.com/css/sf-compact-display');

html,body{
  padding: 0;
  margin: 0;
  height: 100%;
  width: 100%;
}
#app {
  height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
  margin: 0 10px;
}

nav a.router-link-exact-active {
  color: #42b983;
  text-decoration: underline;
}
</style>
