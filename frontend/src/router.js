import Vue from "vue";
import Router from "vue-router";
import NotFound from "./views/404.vue";
import Home from "./views/Home.vue";
import About from "./views/About.vue";

import DatasetUpload from "./views/datasets/Upload.vue";
import DatasetImport from "./views/datasets/Import.vue";
import DatasetGenerate from "./views/datasets/Generate.vue";
import DatasetList from "./views/datasets/List.vue";
import DatasetDetail from "./views/datasets/Detail.vue";
import DatasetConfigurations from "./views/datasets/Configurations.vue";
import Statistics from "./views/datasets/Statistics.vue";

import Preprocessing from "./views/Preprocessing.vue";
import PreprocessingSplit from "./views/preprocessing/Split.vue";
import PreprocessingModify from "./views/preprocessing/Modify.vue";

import CreateClassificationModel from "./views/models/CreateClassification.vue";
import ModelList from "./views/models/List.vue";
import ModelDetail from "./views/models/Detail.vue";
import ModelPredict from "./views/models/Predict.vue";

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
      path: "/datasets/import",
      component: DatasetImport
    },
    {
      path: "/datasets/generate",
      component: DatasetGenerate
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
      path: "/models/create-classification",
      component: CreateClassificationModel
    },
    {
      path: "/models/list",
      component: ModelList
    },
    {
      path: "/models/predict",
      component: ModelPredict
    },
    {
      path: "/models/:model",
      component: ModelDetail,
      props: true
    },
    {
      path: "*",
      component: NotFound
    }
  ]
});
