'use client';

import { useState } from 'react';
import { usePosts } from '@/lib/hooks';
import { Card, CardContent, CardHeader, CardTitle } from '@workspace/ui/components/card';
import { Button } from '@workspace/ui/components/button';
import { ArrowLeft } from 'lucide-react';
import { AnimatedElement } from '@/components/animated-element';
import Image from 'next/image';
import Link from 'next/link';

const categories = ['All', 'General', 'Tech', 'Book Reviews'];

export default function PostsPage() {
  const { data: posts, isLoading, error } = usePosts();
  const [activeCategory, setActiveCategory] = useState('All');

  // Filter posts based on selected category
  const filteredPosts = posts ? posts.filter(post => {
    if (activeCategory === 'All') return true;
    return post.tags.replace('_', ' ').toLowerCase() === activeCategory.toLowerCase();
  }) : [];

  if (isLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Link href="/">
            <Button variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </Link>
        </div>
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 ">Loading posts...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Link href="/">
            <Button variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </Link>
        </div>
        <div className="text-center py-12">
          <p className="text-destructive">Failed to load posts. Please try again later.</p>
        </div>
      </div>
    );
  }

  if (!posts || posts.length === 0) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <Link href="/">
            <Button variant="outline">
              <ArrowLeft className="mr-2 h-4 w-4" />
              Back to Home
            </Button>
          </Link>
        </div>
        <div className="text-center py-12">
          <p className="">No posts found.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="mb-8">
        <Link href="/">
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Home
          </Button>
        </Link>
      </div>

      <div className="mb-12 text-center">
        <h1 className="text-4xl font-bold tracking-tight mb-2">All Posts</h1>
        <p className="">
          {filteredPosts.length} post{filteredPosts.length !== 1 ? 's' : ''} {activeCategory !== 'All' ? `in ${activeCategory}` : 'total'}
        </p>
      </div>

      {/* Filter Tabs */}
      <div className="flex justify-center mb-8">
        <div className="flex space-x-1 rounded-lg bg-muted p-1">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setActiveCategory(category)}
              className={`px-4 py-2 text-sm font-medium rounded-md transition-colors ${
                activeCategory === category
                  ? 'bg-background text-foreground shadow-sm'
                  : ' hover:text-foreground'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      {filteredPosts.length === 0 ? (
        <div className="text-center py-12">
          <p className="">No posts found for this category.</p>
        </div>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredPosts.map((post, index) => (
            <AnimatedElement key={post.id} delay={0.1 + index * 0.05}>
              <Card className="overflow-hidden hover:shadow-lg transition-shadow">
                <Link href={`/posts/${post.slug}`}>
                  {post.image_url && (
                    <div className="aspect-video relative overflow-hidden">
                      <Image
                        src={post.image_url}
                        alt={post.title}
                        fill
                        className="object-cover hover:scale-105 transition-transform duration-300"
                      />
                    </div>
                  )}
                  <CardHeader>
                    <CardTitle className="line-clamp-2 hover:text-primary transition-colors">
                      {post.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className=" line-clamp-3 mb-4">{post.excerpt}</p>
                    <div className="flex items-center justify-between text-xs">
                      <time dateTime={post.date_published} className="">
                        {new Date(post.date_published).toLocaleDateString()}
                      </time>
                      <span className="rounded-full bg-muted px-3 py-1.5 font-medium">
                        {post.tags.replace('_', ' ')}
                      </span>
                    </div>
                  </CardContent>
                </Link>
              </Card>
            </AnimatedElement>
          ))}
        </div>
      )}
    </div>
  );
}
