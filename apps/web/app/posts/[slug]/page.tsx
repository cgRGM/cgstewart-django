import { api } from '@/lib/api';
import { Post } from '@/lib/types';
import { notFound } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import { Button } from '@workspace/ui/components/button';
import { ArrowLeft } from 'lucide-react';

type PostPageProps = {
  params: {
    slug: string;
  };
};

// This function helps Next.js know which slugs to pre-render at build time.
export async function generateStaticParams() {
  try {
    const postsResponse = await api.getPosts();
    return postsResponse.results.map((post) => ({
      slug: post.slug,
    }));
  } catch (error) {
    console.error('Failed to generate static params for posts:', error);
    return [];
  }
}

export default async function PostPage({ params }: PostPageProps) {
  const { slug } = await params;
  let post: Post;

  try {
    post = await api.getPostBySlug(slug);
  } catch (error) {
    // If the post is not found (404) or another error occurs, show the not-found page.
    console.error(`Failed to fetch post with slug "${slug}":`, error);
    notFound();
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-8">
        <Link href="/" passHref>
          <Button variant="outline">
            <ArrowLeft className="mr-2 h-4 w-4" />
            Back to Home
          </Button>
        </Link>
      </div>

      <article>
        <header className="mb-8 border-b pb-8">
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl mb-4">
            {post.title}
          </h1>
          <div className="text-muted-foreground text-sm">
            <span>Published on {new Date(post.date_published).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</span>
            {post.author_name && <span> by {post.author_name}</span>}
          </div>
        </header>

        {post.image_url && (
          <div className="mb-8 rounded-lg overflow-hidden aspect-video relative">
            <Image
              src={post.image_url}
              alt={post.title}
              fill
              className="object-cover"
              priority
            />
          </div>
        )}

        {/* For security, we are not using dangerouslySetInnerHTML. 
            A library like 'react-markdown' would be ideal for rendering markdown content. 
            For now, we'll display the raw content in a preformatted block. */}
        <div className="prose prose-lg dark:prose-invert max-w-none">
          <pre className="whitespace-pre-wrap font-sans text-base">
            {post.content}
          </pre>
        </div>
      </article>
    </div>
  );
}
