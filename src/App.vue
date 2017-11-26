<template>
  <v-app>
    <v-content>
      <transition class="page-transition" name="page-fade" mode="out-in">
        <router-view class="child-view"></router-view>
      </transition>
    </v-content>
    
    <v-footer>
      <v-spacer></v-spacer>
      <div>2017 말과 마음</div>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  name: 'app',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: sans-serif;
  color: #2c3e50;
}

body {
  font-size: 20px;
}

h1 {
  font-weight: normal;
  font-size: 48px;
  margin-top: 40px;
}

h2 {
  font-weight: normal;
  font-size: 28px;
}

.footer {
  padding: 12px;
  font-size: 16px;  
}

* {
  word-break: keep-all;
  overflow-wrap: break-word;
}

.page-fade-enter-active,
.page-fade-leave-active {
  transition: 200ms ease;
  
}

.page-fade-enter,
.page-leave-active {
  opacity: 0;
}

.child-view {
  width: 100%;
  position: absolute;
}
</style>
