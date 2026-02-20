const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'wafilife-media.wafilife.com',
      },
      {
        protocol: 'http',
        hostname: '127.0.0.1',
      }
    ],
  },
}

module.exports = nextConfig
