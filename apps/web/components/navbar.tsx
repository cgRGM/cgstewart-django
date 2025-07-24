import Link from "next/link";

export default function Navbar() {
  return (
    <header className="border-b">
      <div className="container mx-auto px-4 py-6">
        <nav className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold">
            CG Stewart
          </Link>
          <div className="flex items-center gap-6">
            <Link
              href="/posts"
              className="hover:text-primary transition-colors"
            >
              Posts
            </Link>
            <Link
              href="/projects"
              className="hover:text-primary transition-colors"
            >
              Projects
            </Link>
            <Link
              href="/videos"
              className="hover:text-primary transition-colors"
            >
              Videos
            </Link>
          </div>
        </nav>
      </div>
    </header>
  );
}
