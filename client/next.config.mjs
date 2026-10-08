/** @type {import('next').NextConfig} */
const nextConfig = {
    images:{
        remotePatterns: [
            {hostname: "res.cloudinary.com"},
        ],
    },
     eslint: {
        ignoreDuringBuilds: true,
    },
    async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: "https://api-production-e0b80.up.railway.app/api/:path*",
      },
    ];
  },
};

export default nextConfig;
