/**
 * webpack.config.js - Bundling e minificação para produção
 */

const path = require('path');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = {
  mode: 'production',
  entry: './dist/extension.js',
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: 'extension.js',
    libraryTarget: 'commonjs2',
  },
  target: 'node',
  externals: {
    vscode: 'commonjs vscode',
  },
  resolve: {
    extensions: ['.js', '.ts', '.json'],
  },
  optimization: {
    minimize: true,
    minimizer: [new TerserPlugin()],
  },
  devtool: 'source-map',
};
