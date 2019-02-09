import Vue from "vue";
import Router from "vue-router";
import NotFound from "./views/404.vue";
import Home from "./views/Home.vue";
import About from "./views/About.vue";
import Datasets from "./views/Datasets.vue";
import Dataset from "./views/Dataset.vue";
import Preprocessing from "./views/Preprocessing.vue";
import PreprocessingSplit from "./views/preprocessing/Split.vue";
import PreprocessingModify from "./views/preprocessing/Modify.vue";
import Statistics from "./views/dataset/Statistics.vue";
import CreateModel from "./views/CreateModel.vue";
import Models from "./views/Models.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      component: Home
    },
    {
      path: "/about",
      component: About
    },
    {
      path: "/datasets",
      component: Datasets
    },
    {
      path: "/dataset/:dataset",
      component: Dataset,
      props: true
    },
    {
      path: "/preprocessing",
      component: Preprocessing
    },
    {
      path: "/preprocessing/split",
      component: PreprocessingSplit
    },
    {
      path: "/preprocessing/modify",
      component: PreprocessingModify
    },
    {
      path: "/statistics",
      component: Statistics
    },
    {
      path: "/create-model",
      component: CreateModel
    },
    {
      path: "/models",
      component: Models
    },
    {
      path: "*",
      component: NotFound
    }
  ]
});
