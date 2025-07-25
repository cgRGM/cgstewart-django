import { api } from '@/lib/api';
import { Video } from '@/lib/types';
import { notFound } from 'next/navigation';
import { Metadata } from 'next';
import Link from 'next/link';
import { Button } from '@workspace/ui/components/button';
import { ArrowLeft } from 'lucide-react';

type VideoPageProps = {
  params: Promise<{
    slug: string;
  }>;
};

// Helper function to convert a YouTube URL to an embeddable URL
function getYouTubeEmbedUrl(url: string): string | null {
  let videoId: string | null = null;
  try {
    const urlObj = new URL(url);
    if (urlObj.hostname === 'youtu.be') {
      videoId = urlObj.pathname.slice(1);
    } else if (urlObj.hostname === 'www.youtube.com' || urlObj.hostname === 'youtube.com') {
      videoId = urlObj.searchParams.get('v');
    }
  } catch (error) {
    console.error('Invalid video URL:', url);
    return null;
  }

  return videoId ? `https://www.youtube.com/embed/${videoId}` : null;
}

// Generate dynamic metadata for SEO
export async function generateMetadata({ params }: VideoPageProps): Promise<Metadata> {
  const { slug } = await params;
  
  try {
    const video = await api.getVideoBySlug(slug);
    return {
      title: `${video.title} by CG Stewart`,
      description: video.description || 'A video by CG Stewart',
      openGraph: {
        title: `${video.title} by CG Stewart`,
        description: video.description || 'A video by CG Stewart',
        type: 'article',
        modifiedTime: video.updated_at,
      },
      twitter: {
        card: 'summary_large_image',
        title: `${video.title} by CG Stewart`,
        description: video.description || 'A video by CG Stewart',
      },
    };
  } catch (error) {
    return {
      title: 'Video Not Found | CG Stewart',
      description: 'The requested video could not be found.',
    };
  }
}

export async function generateStaticParams() {
  try {
    const videosResponse = await api.getVideos();
    return videosResponse.results.map((video) => ({ slug: video.slug }));
  } catch (error) {
    console.error('Failed to generate static params for videos:', error);
    return [];
  }
}

export default async function VideoPage({ params }: VideoPageProps) {
  const { slug } = await params;
  let video: Video;

  try {
    video = await api.getVideoBySlug(slug);
  } catch (error) {
    console.error(`Failed to fetch video with slug "${slug}":`, error);
    notFound();
  }

  const embedUrl = getYouTubeEmbedUrl(video.video_url);

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
          <h1 className="text-4xl font-bold tracking-tight text-foreground sm:text-5xl">
            {video.title}
          </h1>
        </header>

        {embedUrl ? (
          <div className="aspect-video mb-8 rounded-lg overflow-hidden">
            <iframe
              width="100%"
              height="100%"
              src={embedUrl}
              title={video.title}
              frameBorder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            ></iframe>
          </div>
        ) : (
          <div className="mb-8 p-4 bg-destructive/10 text-destructive rounded-md">
            <p>Could not display video. The URL may be invalid or from an unsupported provider.</p>
          </div>
        )}

        {video.description && (
          <div className="prose prose-lg dark:prose-invert max-w-none">
            <p>{video.description}</p>
          </div>
        )}
      </article>
    </div>
  );
}
