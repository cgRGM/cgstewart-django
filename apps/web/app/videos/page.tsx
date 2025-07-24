'use client';

import { useVideos } from '@/lib/hooks';
import { Card, CardContent, CardHeader, CardTitle } from '@workspace/ui/components/card';
import { Button } from '@workspace/ui/components/button';
import { ArrowLeft, Play } from 'lucide-react';
import Link from 'next/link';

// Helper function to get YouTube thumbnail
function getYouTubeThumbnail(url: string): string | null {
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

  return videoId ? `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg` : null;
}

export default function VideosPage() {
  const { data: videos, isLoading, error } = useVideos();

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
          <p className="mt-4 ">Loading videos...</p>
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
          <p className="text-destructive">Failed to load videos. Please try again later.</p>
        </div>
      </div>
    );
  }

  if (!videos || videos.length === 0) {
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
          <p className="">No videos found.</p>
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

      <div className="mb-8">
        <h1 className="text-4xl font-bold tracking-tight">All Videos</h1>
        <p className=" mt-2">
          {videos.length} video{videos.length !== 1 ? 's' : ''} found
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {videos.map((video) => {
          const thumbnailUrl = getYouTubeThumbnail(video.video_url);
          
          return (
            <Card key={video.id} className="overflow-hidden hover:shadow-lg transition-shadow">
              <Link href={`/videos/${video.slug}`}>
                <div className="aspect-video relative overflow-hidden bg-muted">
                  {thumbnailUrl ? (
                    <>
                      <img
                        src={thumbnailUrl}
                        alt={video.title}
                        className="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
                      />
                      <div className="absolute inset-0 flex items-center justify-center bg-black/20 hover:bg-black/30 transition-colors">
                        <div className="bg-primary text-primary-foreground rounded-full p-3">
                          <Play className="h-6 w-6 fill-current" />
                        </div>
                      </div>
                    </>
                  ) : (
                    <div className="w-full h-full flex items-center justify-center">
                      <div className="bg-primary text-primary-foreground rounded-full p-3">
                        <Play className="h-6 w-6 fill-current" />
                      </div>
                    </div>
                  )}
                </div>
                <CardHeader>
                  <CardTitle className="line-clamp-2 hover:text-primary transition-colors">
                    {video.title}
                  </CardTitle>
                </CardHeader>
                {video.description && (
                  <CardContent>
                    <p className=" line-clamp-3">{video.description}</p>
                  </CardContent>
                )}
              </Link>
            </Card>
          );
        })}
      </div>
    </div>
  );
}
