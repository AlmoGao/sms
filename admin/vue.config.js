const { defineConfig } = require('@vue/cli-service')
var publicPath = ''
var outputDir = 'dist'
var assetsDir = ''
console.log('???????????????>>>>>>>>>', process.env.NODE_ENV)
if (process.env.NODE_ENV === 'production') {
  publicPath = '././'
  outputDir = '../templates'
  assetsDir = '../static'
}
module.exports = defineConfig({
  publicPath: publicPath,
  lintOnSave: false,
  outputDir: outputDir,
  assetsDir: assetsDir,
  productionSourceMap: false,
})
