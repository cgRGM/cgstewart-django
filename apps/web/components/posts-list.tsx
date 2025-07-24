"use client";

import { usePosts } from "@/lib/hooks";
import { AnimatedElement } from "@/components/animated-element";
import Image from "next/image";
import Link from "next/link";

export default function PostsList() {
  const { data: posts, isLoading, error } = usePosts();

  if (isLoading) {
    return (
      <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-20 lg:mx-0 lg:max-w-none lg:grid-cols-3">
        {[...Array(3)].map((_, i) => (
          <div key={i} className="animate-pulse">
            <div className="aspect-[16/9] w-full rounded-2xl bg-gray-200 mb-8"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-1/2"></div>
          </div>
        ))}
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-10">
        <p className="text-destructive">Error loading posts: {error.message}</p>
      </div>
    );
  }

  if (!posts || posts.length === 0) {
    return (
      <div className="text-center py-10">
        <p className="">No posts available at the moment.</p>
      </div>
    );
  }

  return (
    <div className="mx-auto mt-16 grid max-w-2xl grid-cols-1 gap-x-8 gap-y-20 lg:mx-0 lg:max-w-none lg:grid-cols-3">
      {posts.slice(0, 3).map((post, index) => (
        <AnimatedElement key={post.id} delay={0.1 + index * 0.1}>
          <article className="flex flex-col items-start justify-between">
            <div className="relative w-full">
              {post.image_url ? (
                <Image
                  src={post.image_url}
                  alt={post.title}
                  width={800}
                  height={400}
                  className="aspect-[16/9] w-full rounded-2xl bg-gray-100 object-cover sm:aspect-[2/1] lg:aspect-[3/2]"
                />
              ) : (
                <div className="aspect-[16/9] w-full rounded-2xl bg-gray-100 sm:aspect-[2/1] lg:aspect-[3/2]"></div>
              )}
              <div className="absolute inset-0 rounded-2xl ring-1 ring-inset ring-gray-900/10" />
            </div>
            <div className="max-w-xl">
              <div className="mt-8 flex items-center gap-x-4 text-xs">
                <time dateTime={post.date_published} className="text-gray-500">
                  {new Date(post.date_published).toLocaleDateString()}
                </time>
                <span className="relative z-10 rounded-full bg-gray-50 px-3 py-1.5 font-medium text-gray-600 hover:bg-gray-100">
                  {post.tags.replace('_', ' ')}
                </span>
              </div>
              <div className="group relative">
                <h3 className="mt-3 text-lg font-semibold leading-6 text-foreground group-hover:text-gray-600">
                  <Link href={`/posts/${post.slug}`}>
                    <span className="absolute inset-0" />
                    {post.title}
                  </Link>
                </h3>
                <p className="mt-5 line-clamp-3 text-sm leading-6 ">
                  {post.excerpt}
                </p>
              </div>

            </div>
          </article>
        </AnimatedElement>
      ))}
    </div>
  );
}
