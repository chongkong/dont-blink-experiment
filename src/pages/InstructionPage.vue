<template>
  <v-flex class="instruction-page" md6 offset-md3>
    <h1>Instructions</h1>
    <p>실험자는 앞으로 지문을 읽고 지문에 관련된 문제에 답변하게 됩니다. </p>
    <ul>
      <li>모든 조작은 키보드로 이루어지며 마우스는 사용하지 않도록 합니다. </li>
      <li>실험 진행 중에 새로 고침, 뒤로 가기 등의 동작은 하지 마십시오.</li>
    </ul>
    <p>실험을 계속하려면 <kbd :class="{blue: pressed}">space</kbd>를 눌러주세요.</p>
  </v-flex>
</template>

<script>
export default {
  created() {
    this.keyEventListener = window.addEventListener("keydown", (event) => {
      if (event.isTrusted && event.code === "Space")
        this.proceed();
    });
  },

  destroyed() {
    window.removeEventListener(this.keyEventListener, window);
  },

  data() {
    return {
      pressed: false,
      keyEventListener: null
    }
  },

  methods: {
    proceed() {
      this.pressed = true;
      this.$router.push({name: "prepare", params: {sid: 1}});
    }
  }
}
</script>

<style lang="scss">
.instruction-page {
  h1 {
    margin: 20px 0;
  }

  p, ul {
    margin-bottom: 16px;
  }

  ul {
    padding-left: 20px;
  }
}
</style>

