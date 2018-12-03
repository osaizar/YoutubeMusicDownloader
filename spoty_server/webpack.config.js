const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: "./dev/index.js",
  mode: "development",
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /(node_modules|bower_components)/,
        loader: "babel-loader",
        options: { presets: ["@babel/env"] }
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
  },
  resolve: { extensions: ["*", ".js", ".jsx"] },
  output: {
    path: path.resolve(__dirname, "static/js"),
    filename: "main.js"
  },
  plugins: [new webpack.HotModuleReplacementPlugin()]
};
