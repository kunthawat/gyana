const path = require("path");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const VueLoaderPlugin = require("vue-loader/lib/plugin");

module.exports = {
  resolve: {
    extensions: [".js", ".jsx"],
  },
  entry: {
    "site-base": "./assets/site-base.js", // base styles shared between frameworks
    "site-tailwind": "./assets/site-tailwind.js", // required for tailwindcss styles
    app: "./assets/javascript/app.js",
    teams: "./assets/javascript/teams/teams.js",
    pegasus: "./assets/javascript/pegasus/pegasus.js",
    "react-object-lifecycle":
      "./assets/javascript/pegasus/examples/react/react-object-lifecycle.js",
    "vue-object-lifecycle":
      "./assets/javascript/pegasus/examples/vue/vue-object-lifecycle.js",
    stimulus: "./assets/javascript/stimulus.js",
    dataflow: "./apps/dataflows/javascript/app.jsx",
  },
  output: {
    path: path.resolve(__dirname, "./static"),
    filename: "js/[name]-bundle.js",
    library: ["SiteJS", "[name]"],
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader",
      },
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: ["@babel/env", "@babel/preset-react"],
          plugins: [
            "@babel/plugin-proposal-class-properties",
            "@babel/plugin-transform-runtime",
          ],
        },
      },
      {
        test: /\.scss$/,
        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"],
      },
      {
        test: /\.css$/i,
        use: [MiniCssExtractPlugin.loader, "css-loader", "postcss-loader"],
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: "css/[name].css",
    }),
    new VueLoaderPlugin(),
  ],
};
