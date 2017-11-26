import Vue from "vue";
import Router from "vue-router";
import IntroPage from "./pages/IntroPage";
import InstructionPage from "./pages/InstructionPage";
import PreparePage from "./pages/PreparePage";
import ExperimentPage from "./pages/ExperimentPage";
import TextPage from "./pages/TextPage";
import QuestionPage from "./pages/QuestionPage";
import ThankYouPage from "./pages/ThankYouPage";

Vue.use(Router);

export default new Router({
  routes: [
    {path: "/", name: "intro", component: IntroPage},
    {path: "/instruction", name: "instruction", component: InstructionPage},
    {path: "/experiment/:sid", name: "experiment", component: ExperimentPage, children: [
      {path: "text", name: "text", component: TextPage},
      {path: "prepare", name: "prepare", component: PreparePage},
      {path: ":qid", name: "question", component: QuestionPage}
    ]},
    {path: "/thankyou", name: "thankyou", component: ThankYouPage}
  ]
});
