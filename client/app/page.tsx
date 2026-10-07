import type { Metadata } from 'next'
import Image from "next/image";
import buildings from "@/./public/assets/images/buildings1.webp"
import Link from "next/link";
import { ArrowRightIcon } from "@heroicons/react/24/solid";

export const metadata: Metadata = {
  title: "Home | Accommodation Center",
  description: "Accommodation Center Home Page. Create an account to get started"
}

export default function HomePage() {
  return (
    <div className="relative h-screen">
      <div className="absolute inset-0 z-0">
        <Image
          src={buildings}
          alt="Accommodation Center"
          fill
          style={{ objectFit: "cover", objectPosition: "center" }}
          priority
        />
      </div>
      <main className="flex-center relative z-10 h-full bg-black/50">
        <div className="mx-auto max-w-4xl px-6 text-center">
          <p className="mb-8 text-sm font-medium uppercase tracking-[0.3em] text-teal-300 sm:text-base">
            Welcome to
          </p>
          <h1 className="font-robotoSlab text-4xl font-semibold text-cyan-400 antialiased sm:text-6xl md:text-8xl">
            Accommodation Center
          </h1>
          <p className="my-8 text-2xl text-teal-300 sm:text-4xl">
            Are you a tenant or a technician?
          </p>
          <Link href="/register" prefetch={false}>
            <button className="bg-asparagus rounded-3xl px-4 py-2 text-lg font-semibold text-white hover:bg-lime-700 sm:px-6 sm:text-2xl">
              <span className="inline-flex items-center">
                Create Your Account
                <ArrowRightIcon className="ml-2 size-6" />
              </span>
            </button>
          </Link>
        </div>
      </main>
    </div>
  );
}