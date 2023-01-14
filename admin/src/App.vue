<template>
  <router-view/>
</template>

<script setup>

console.log('version: 0.2')

</script>

<style lang="less">
html, body, #app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  min-width: 1200px;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50; 
}
div {
  box-sizing: border-box;
}
.box {
  background-color: #fff;
  border-radius: 12px;
  padding: 22px;
  margin: 12px;
}

</style>
