import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Not Found",
  robots: {
    index: false,
    follow: false,
  },
};

export default function NotFound() {
  return (
    <div className="min-h-screen bg-white text-black flex flex-col items-center justify-center p-6 text-center select-none">
      <h1 className="text-4xl md:text-6xl font-medium tracking-tight mb-4">Page not found</h1>
      <p className="text-neutral-600 mb-8 max-w-md">
        The page you are looking for does not exist or has been moved.
      </p>
      <Link
        href="/"
        className="px-6 py-2.5 rounded-full bg-black text-white font-medium text-sm hover:bg-neutral-800 transition-colors"
      >
        Back to Home
      </Link>
    </div>
  );
}
