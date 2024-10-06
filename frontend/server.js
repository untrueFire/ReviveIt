const webpack = require('webpack');
const WebpackDevServer = require('webpack-dev-server');
const config = require('./webpack.config.js');

const compiler = webpack(config);
const server = new WebpackDevServer(compiler, {
  hot: true,
  open: true,
  port: 80,
  host: 'localhost',
  historyApiFallback: true
});

server.listen(80, 'localhost', (err) => {
  if (err) {
    console.log(err);
    return;
  }
  console.log('Listening at http://localhost');
});