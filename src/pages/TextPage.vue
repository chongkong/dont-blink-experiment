<template>
<v-flex class="text-page" md6 offset-md3>
  <div v-if="displayMode === 'full'">
    <div style="text-align: center">
      <v-progress-circular class="progress" v-model="progress" size="60" :rotate="270"
          :color="progressColor">
        {{ Math.ceil(duration - (Date.now() - startedAt) / 1000) }}
      </v-progress-circular>
    </div>
    <div class="full" v-html="fullText"></div>
  </div>

  <div class="blink" v-else-if="displayMode === 'blink'">
    <transition-group name="blink">
      <div class="blink-item" 
           v-for="word in frame" 
           v-bind:key="word"
           v-html="word">
      </div>
    </transition-group>
  </div>

  <audio autoplay :src="audioSource" v-if="audioSource"></audio>

</v-flex>
</template>

<script>
import store from "../store";
import util from "../util";

const BLINK_MILLIS = 360;

export default {
  beforeRouteEnter(curr, prev, next) {
    let sid = curr.params.sid;
    store.dispatch("loadExperiment").then(exp => {
      let sec = exp.sections[sid - 1];
      next(vm => vm.composeView(sec));
    })
  },

  data() {
    return {
      displayMode: "blink",
      fullText: "",
      audioSource: "",
      startedAt: Date.now(),
      progress: 0,
      progressColor: "primary",
      duration: 1.0,
      frame: []
    };
  },

  methods: {
    composeView(section) {
      this.startedAt = Date.now();
      if (section.audio_file)
        this.audioSource = section.audio_file;
      this.displayMode = section.disp_type;
      if (section.disp_type === "blink") {
        this.runBlink(util.magicSplit(section.doc.content))
      }
      else {
        this.fullText = util.cleanText(section.doc.content);
        this.runProgress();
      }
      this.duration = section.doc.duration;
    },

    async runProgress() {
      this.progressColor = "primary";
      while (true) {
        this.progress = 100 * (Date.now() - this.startedAt) / (this.duration * 1000);
        await util.waitForMillis(300);
        if (this.progress >= 90)
          this.progressColor = "error";
        else if (this.progress >= 70)
          this.progressColor = "warning";
        if (this.progress >= 100)
          break;
      }
      await util.waitForMillis(1000);
      this.proceed();
    },
    
    async runBlink(frames) {
      for (let frame of frames) {
        this.frame.splice(0, this.frame.length);
        for (let word of frame) {
          this.frame.push(word);
          await util.waitForMillis(BLINK_MILLIS);
        }
      }
      await util.waitForMillis(1000);
      this.proceed();
    },

    proceed() {
      let sid = this.$route.params.sid;
      this.$router.push({name: "question", params: {sid, qid: 1}});
    }
  }
}
</script>

<style lang="scss">
.text-page {
  .blink {
    padding-top: 80px;
    text-align: center;

    .blink-item {
      display: inline-block;
      font-size: 48px;
      padding-right: 0.3em;
      transition: 180ms;

      &.blink-enter-active {
        transition-duration: 150ms;
        opacity: 0;
      }
      &.blink-leave-active {
        opacity: 0;
        transform: translateX(-100px);
      }
    }
  }

  .progress {
    font-size: 20px;
  }

  .full {
    padding: 20px;
    font-size: 20px;
    text-align: left;
    white-space: pre-wrap;
    line-height: 1.6;
  }
}
</style>