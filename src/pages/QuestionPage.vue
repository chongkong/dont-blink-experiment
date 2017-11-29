<template>
  <v-flex class="question-page" md6 offset-md3>
    <h2>{{statement}}</h2>
    <div class="ul-wrapper">
      <ul>
        <li v-for="(choice, i) in choices" :key="choice">
          <kbd :class="{'blue': selected === i}">{{i + 1}}</kbd>
          {{choice}}
        </li>
      </ul>
    </div>
    <div class="giveup">
      <kbd :class="{'blue': selected === -1}">space</kbd>모르겠어요 😢😢
    </div>
  </v-flex>
</template>

<script>
import store from "../store";
import util from "../util";
import {keyEvent} from "../events";

export default {
  beforeRouteEnter(curr, prev, next) {
    let {sid, qid} = curr.params;
    store.dispatch("loadExperiment").then(exp => {
      let question = exp.sections[sid - 1].doc.questions[qid - 1];
      next(vm => vm.setQuestion(question));
    })
  },

  beforeRouteUpdate(curr, prev, next) {
    this.selected = null;
    let {sid, qid} = curr.params;
    store.dispatch("loadExperiment").then(exp => {
      let question = exp.sections[sid - 1].doc.questions[qid - 1];
      this.setQuestion(question);
      next();
    });
  },

  created() {
    keyEvent.$on("digit", this.recordAndProceed);
    keyEvent.$on("space", this.recordAndProceed);
  },

  beforeDestroy() {
    keyEvent.$off("digit", this.recordAndProceed);
    keyEvent.$off("space", this.recordAndProceed);
  },

  data() {
    return {
      selected: null,
      askedAt: 0,
      statement: "",
      choices: [],
      keyEventListener: null
    }
  },

  methods: {
    setQuestion(question) {
      this.askedAt = Date.now();
      this.statement = question.statement;
      this.choices = question.choices;
    },
    giveupAndProceed() {
      this.recordAndProceed(-1);
    },
    recordAndProceed(choice) {
      const WAIT_MILLIS = 2000;
      if (this.selected !== null || choice > this.choices.length)
        return;

      let answeredAt = Date.now();
      this.selected = choice - 1;
      let responseTime = answeredAt - this.askedAt;
      let sid = this.$route.params.sid - 0;
      let qid = this.$route.params.qid - 0;
      this.$store.dispatch("recordAnswer", {sid, qid, choice, responseTime}).then(() => {
        let timeLeft = Math.max(0, WAIT_MILLIS - (Date.now() - answeredAt));
        return util.waitForMillis(timeLeft);
      }).then(() => {
        let sec = this.$store.state.experiment.sections[sid - 1];
        if (sec.answers.length < sec.doc.questions.length)
          this.$router.push({name: "question", params: {sid, qid: qid + 1}});
        else if (sid < this.$store.getters.numSections)
          this.$router.push({name: "prepare", params: {sid: sid + 1}});
        else
          this.$router.push({name: "thankyou"});
      });
    },
    getColor(choiceIndex) {
      return this.selected === choiceIndex ? "primary" : "";
    }
  }
}
</script>

<style lang="scss">
.question-page {
  h2 {
    margin: 40px 0;
    padding: 0 20px;
  }

  .ul-wrapper {
    text-align: center;

    ul {
      list-style-type: none;
      padding: 0;
      display: inline-block;
      text-align: left;

      li {
        display: inline-block;
        margin: 0 20px;
        font-size: 20px;
      }
    }
  }

  .giveup {
    margin: 40px auto;
    text-align: center;
  }
}
</style>
