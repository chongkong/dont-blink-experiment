<template>
  <v-flex class="prepare-page" md6 offset-md3>
    <h1>{{ koreanSid }} 번째 이야기</h1>
    <p>문제에 집중할 수 있도록 충분히 쉰 다음에 <kbd :class="{blue: pressed}">space</kbd> 를 눌러주세요.</p>
  </v-flex>
</template>

<script>
import {keyEvent} from "../events";

export default {
  created() {
    keyEvent.$on("space", this.proceed);
  },

  beforeDestroy() {
    keyEvent.$off("space", this.proceed);
  },

  data() {
    return {
      pressed: false,
      keyEventListener: null
    }
  },

  computed: {
    koreanSid() {
      const translations = [
        "첫", "두", "세", "네", "다섯", "여섯", "일곱", "여덟", "아홉", "열",
        "열한", "열두", "열세", "열네", "열다섯", "열여섯", "열일곱", "열여덟", "열아홉", "스무"
      ]
      if (this.$route.params.sid <= 20)
        return translations[this.$route.params.sid - 1];
      return "여러";
    }
  },

  methods: {
    proceed() {
      this.pressed = true;
      let sid = this.$route.params.sid;
      this.$router.push({name: "text", params: {sid}});
    }
  }
}
</script>

<style lang="scss">
.prepare-page {
  h1 {
    margin-bottom: 40px;
  }
}
</style>
