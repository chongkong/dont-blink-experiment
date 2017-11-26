<template>
  <v-flex class="thankyou-page" md6 offset-md3>
    <div class="fin" >fin</div>
    <h1>실험에 참가해주셔서 감사합니다.</h1>
    <p>모든 실험이 끝났습니다. 제공해주신 개인 정보는 실험이 끝난 뒤에는 모두 폐기됩니다. 감사합니다.</p>
  </v-flex>
</template>

<script>
import axios from "axios";

export default {
  beforeRouteEnter(routeTo, routeFrom, next) {
    axios.post("/api/logout").then(() => next());
  }
}
</script>

<style lang="scss">
.thankyou-page {
  * {
    text-align: center;
  }

  .fin {
    font-family: Tangerine;
    text-shadow: 4px 4px rgba(0, 0, 0, 0.1);
    font-size: 96px;
    margin-top: 160px;
    margin-bottom: 60px;
  }

  h1 {
    margin-bottom: 30px;
  }
}
</style>
