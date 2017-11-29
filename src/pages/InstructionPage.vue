<template>
  <v-flex class="instruction-page" md6 offset-md3>
    <h1>Instructions</h1>
    <p>실험자는 앞으로 지문을 읽고 지문에 관련된 문제에 답변하게 됩니다. 지문은 <em>평범하지 않은 형태</em>로도 제공될 수 있으니 당황하지 마세요. 또한 지문을 읽는 과정에서 오디오가 재생되는 경우가 있으니 컴퓨터의 소리가 잘 들리는지 확인해주세요.</p>
    <div class="audio-wrapper">
      <audio src="//storage.googleapis.com/snu-dont-blink-experiment.appspot.com/data/p231_023.wav" controls></audio>
    </div>
    <h2>실험 시 유의사항</h2>
    <ul>
      <li>모든 조작은 키보드로 이루어지며 마우스는 사용하지 않도록 합니다. </li>
      <li>실험 진행 중에 새로 고침, 뒤로 가기 등의 동작은 하지 마십시오.</li>
    </ul>
    <p>실험을 계속하려면 <kbd :class="{blue: pressed}">space</kbd>를 눌러주세요.</p>
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
  h1, h2 {
    margin: 20px 0;
  }

  .audio-wrapper {
    text-align: center;
  }

  p, ul {
    margin-bottom: 16px;
  }

  ul {
    padding-left: 20px;
  }
}
</style>

