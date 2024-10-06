const path = require('path');
const { VueLoaderPlugin } = require('vue-loader');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const { DefinePlugin } = require('webpack');
const webpack =  require('webpack');
module.exports = {
  mode: 'development',
  entry: './src/main.js',
  output: {
    path: __dirname + '/dist',
    filename: 'bundle.js',
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
    }),
    new DefinePlugin({
      BASE_URL: JSON.stringify('/'),
    }),
    new webpack.DefinePlugin({
      __VUE_OPTIONS_API__: JSON.stringify(true), // 启用 Options API
      __VUE_PROD_DEVTOOLS__: JSON.stringify(true), // 生产环境下的 DevTools
      __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: JSON.stringify(true) // 生产环境下的 hydration 错误详细信息
    })
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
};