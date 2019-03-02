import Vue from "vue";
import Router from "vue-router";
import NotFound from "./views/404.vue";
import Home from "./views/Home.vue";
import About from "./views/About.vue";

import DatasetUpload from "./views/datasets/Upload.vue";
import DatasetList from "./views/datasets/List.vue";
import DatasetDetail from "./views/datasets/Detail.vue";
import DatasetConfigurations from "./views/datasets/Configurations.vue";
import Statistics from "./views/datasets/Statistics.vue";

import Preprocessing from "./views/Preprocessing.vue";
import PreprocessingSplit from "./views/preprocessing/Split.vue";
import PreprocessingModify from "./views/preprocessing/Modify.vue";

import CreateModelSimple from "./views/CreateModelSimple.vue";
import CreateModel from "./views/models/Create.vue";
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
      path: "/datasets/list",
      component: DatasetList
    },
    {
      path: "/datasets/upload",
      component: DatasetUpload
    },
    {
      path: "/datasets/configurations",
      component: DatasetConfigurations
    },
    {
      path: "/datasets/:dataset",
      component: DatasetDetail,
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
      path: "/models/create-simple",
      component: CreateModelSimple
    },
    {
      path: "/models/create",
      component: CreateModel
    },
    {
      path: "/models/list",
      component: Models
    },
    {
      path: "*",
      component: NotFound
    }
  ]
});
