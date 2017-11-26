<template>
<div>
  <v-progress-linear class="line-progress" v-model="progress" height="6" color="primary"></v-progress-linear>
  <div class="numeric-progress">{{$route.params.sid}} / {{$store.getters.numSections}}</div>
  <router-view></router-view>
</div>
</template>

<script>
import axios from "axios";

import store from "../store";

export default {
  async beforeRouteEnter(routeTo, routeFrom, next) {
    let resp = await axios.get("/api/experiment");
    if (resp.status === 200) {
      store.commit("setExperiment", resp.data);
      next();
    }
    else {

    }
  },
  computed: {
    progress() {
      return 100 * this.$route.params.sid / this.$store.getters.numSections;
    }
  }
}
</script>

<style>
.line-progress {
  margin: 0 0 20px;
}
.numeric-progress {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 20px;
}
</style>
