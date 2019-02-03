module.exports = {
  configureWebpack: {
    devtool: "source-map"
  },
  devServer: {
    proxy: "http://localhost:5000",
    host: "localhost"
  }
};
