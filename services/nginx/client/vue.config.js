/**
 * @type {import('@vue/cli-service').ProjectOptions}
 */
module.exports = {
  devServer: {
    proxy: {
      '^/api': {
        target: 'http://web:5000',
        changeOrigin: true
      }
    }
  }
}
