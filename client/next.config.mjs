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
};

export default nextConfig;
