import Bio from "@/components/bio";
import PostsList from "@/components/posts-list";
import ProjectsList from "@/components/projects-list";
import VideosList from "@/components/videos-list";
import { Button } from "@workspace/ui/components/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import Link from "next/link";

export default function Page() {
  return (
    <div className="min-h-screen bg-background">
      {/* Header */}

      {/* Main Content */}
      <main className="container mx-auto px-4 py-12">
        <div className="space-y-16">
          {/* Bio Section */}
          <section className="flex justify-center">
            <Bio />
          </section>

          {/* Recent Posts Section */}
          <section className="space-y-8">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">
                I write about tech and books here
              </h2>
              <Button asChild variant="outline">
                <Link href="/posts">View All Posts</Link>
              </Button>
            </div>
            <PostsList />
          </section>

          {/* Featured Projects Section */}
          <section className="space-y-8">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">
                I like to showcase my art here
              </h2>

              <Button asChild variant="outline">
                <Link href="/projects">View All Projects</Link>
              </Button>
            </div>
            <ProjectsList />
          </section>

          {/* Featured Videos Section */}
          <section className="space-y-8">
            <div className="flex items-center justify-between">
              <h2 className="text-3xl font-bold">
                I like to build in public here
              </h2>

              <Button asChild variant="outline">
                <Link href="/videos">View All Videos</Link>
              </Button>
            </div>
            <VideosList limit={6} />
          </section>
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center ">
            <p>
              &copy; {new Date().getFullYear()} CG Stewart. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
