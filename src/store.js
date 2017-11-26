import Vue from "vue";
import Vuex from "vuex";
import axios from "axios";

import router from "./router";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    me: null,
    experimentFut: null,
    experiment: {
      sections: [1, 2, 3, 4]
    },
    docs: {}
  },

  getters: {
    numSections(state) {
      return state.experiment.sections.length;
    },

    currentSectionIndex(state) {
      return state.experiment.sections.filter(s => s.completed).length;
    },

    currentSection(state, getters) {
      return state.experiment.sections[getters.currentSectionIndex];
    }
  },

  mutations: {
    login(state, participant) {
      state.me = participant;
    },

    logout(state) {
      state.me = null;
    },

    setExperimentFut(state, fut) {
      state.experimentFut = fut;
    },

    setExperiment(state, exp) {
      state.experiment = exp;
    },

    recordAnswer(state, {sec_idx, ans_idx, choice, responseTime}) {
      let ans = {
        choice: choice,
        response_time: responseTime
      }
      let sec = state.experiment.sections[sec_idx];
      sec.answers[ans_idx] = ans;

      if (sec.answers.length === sec.doc.questions.length) {
        sec.completed = true;
        sec.completed_at = Date.now();
      }
    },

    setDocs(state, docId, doc) {
      state.docs[docId] = doc;
    }
  },

  actions: {
    async register(ctx, participant) {
      let resp = await axios.post("/api/participants", participant);
      if (resp.status !== 200)
        return;
      ctx.commit("login", resp.data);
      router.push("instruction");
    },

    loadExperiment(ctx) {
      if (ctx.state.experimentFut !== null)
        return ctx.state.experimentFut;
      ctx.commit("setExperimentFut", axios.get("/api/experiment").then(resp => {
        if (resp.status === 200)
          ctx.commit("setExperiment", resp.data);
        return ctx.state.experiment;
      }));
      return ctx.state.experimentFut;
    },

    recordAnswer(ctx, {sid, qid, choice, responseTime}) {
      let sec_idx = sid - 1;
      let ans_idx = qid - 1;
      ctx.commit("recordAnswer", {sec_idx, ans_idx, choice, responseTime});
      return axios.post(`/api/experiment/${sec_idx}/${ans_idx}`, {choice, responseTime});
    }
  }
});
