import Vue from "vue";
import axios from "axios";

Vue.prototype.$http = axios;

// if (process.env.NODE_ENV === "production") {
//   Vue.prototype.$http = axios;
// } else {
//   Vue.prototype.$http = axios.create({
//     baseURL: "http://localhost:5000" // Development only
//   });
// }
