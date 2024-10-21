const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { DefinePlugin } = require('webpack');
const AutoImport = require('unplugin-auto-import/webpack');
const Components = require('unplugin-vue-components/webpack');
const { NaiveUiResolver } = require('unplugin-vue-components/resolvers');
const webpack = require('webpack');
module.exports = {
  mode: 'development',
  entry: './src/main.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'bundle.js',
    publicPath: '/'
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
      },
      {
        test: /\.css$/,
        use: ['style-loader', 'css-loader'],
      },
    ],
  },
  plugins: [
    new VueLoaderPlugin(),
    new HtmlWebpackPlugin({
      template: './public/index.html',
      title: 'ReviveIt'
    }),
    new DefinePlugin({
      BASE_URL: JSON.stringify('/'),
    }),
    new webpack.DefinePlugin({
      __VUE_OPTIONS_API__: JSON.stringify(false),
      __VUE_PROD_DEVTOOLS__: JSON.stringify(false),
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(false)
    }),
    AutoImport.default({
      resolvers: [NaiveUiResolver()],
    }),
    Components.default({
      resolvers: [NaiveUiResolver()],
    }),
  ],
  devServer: {
    static: {
      directory: __dirname + '/dist',
    },
    hot: true,
    port: 80,
    proxy: [
      {
        context: ['/api'],
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      {
        context: ['/accounts'],
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    ],
    historyApiFallback: true,
  },
  resolve: {
    alias: {
      vue: '@vue/runtime-dom',
      '@': path.resolve(__dirname, 'src')
    },
  },
  optimization: {
    usedExports: true,
  },
  profile: true,
};