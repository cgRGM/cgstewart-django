"use client";

import { useVideos } from "@/lib/hooks";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import { Button } from "@workspace/ui/components/button";
import { ExternalLink } from "lucide-react";
import Link from "next/link";

// Helper function to convert YouTube URL to thumbnail URL
function getYouTubeThumbnail(url: string): string | null {
  try {
    const urlObj = new URL(url);
    let videoId: string | null = null;

    if (urlObj.hostname === 'youtu.be') {
      videoId = urlObj.pathname.slice(1);
    } else if (urlObj.hostname === 'www.youtube.com' || urlObj.hostname === 'youtube.com') {
      videoId = urlObj.searchParams.get('v');
    }

    return videoId ? `https://img.youtube.com/vi/${videoId}/maxresdefault.jpg` : null;
  } catch {
    return null;
  }
}

// Helper function to get platform name from URL
function getPlatformName(url: string): string {
  try {
    const urlObj = new URL(url);
    if (urlObj.hostname.includes('youtube.com') || urlObj.hostname.includes('youtu.be')) {
      return 'YouTube';
    } else if (urlObj.hostname.includes('twitch.tv')) {
      return 'Twitch';
    }
    return 'Video';
  } catch {
    return 'Video';
  }
}

interface VideosListProps {
  limit?: number;
  showViewAll?: boolean;
}

export default function VideosList({ limit, showViewAll = true }: VideosListProps) {
  const { data: videos, isLoading, error } = useVideos();

  if (isLoading) {
    return (
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: limit || 6 }).map((_, i) => (
          <Card key={i} className="animate-pulse">
            <div className="aspect-video bg-muted rounded-t-lg" />
            <CardHeader>
              <div className="h-6 bg-muted rounded" />
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                <div className="h-4 bg-muted rounded" />
                <div className="h-4 bg-muted rounded w-3/4" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (error || !videos || videos.length === 0) {
    return (
      <Card>
        <CardContent className="p-6">
          <p className="">No videos found.</p>
        </CardContent>
      </Card>
    );
  }

  const displayVideos = limit ? videos.slice(0, limit) : videos;

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {displayVideos.map((video) => {
          const thumbnail = getYouTubeThumbnail(video.video_url);
          const platform = getPlatformName(video.video_url);

          return (
            <Card key={video.id} className="group hover:shadow-md transition-shadow">
              <Link href={`/videos/${video.slug}`}>
                <div className="aspect-video relative overflow-hidden rounded-t-lg bg-muted">
                  {thumbnail ? (
                    <img
                      src={thumbnail}
                      alt={video.title}
                      className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-300"
                    />
                  ) : (
                    <div className="flex items-center justify-center h-full">
                      <ExternalLink className="h-8 w-8 text-muted-foreground" />
                    </div>
                  )}
                  
                  {/* Platform badge */}
                  <div className="absolute top-2 right-2">
                    <span className="inline-block bg-black/80 text-white px-2 py-1 rounded text-xs font-medium">
                      {platform}
                    </span>
                  </div>
                </div>

                <CardHeader>
                  <CardTitle className="line-clamp-2 group-hover:text-primary transition-colors">
                    {video.title}
                  </CardTitle>
                </CardHeader>

                {video.description && (
                  <CardContent className="space-y-4">
                    <p className="line-clamp-3 text-sm">{video.description}</p>
                  </CardContent>
                )}
              </Link>

              <CardContent className="pt-0">
                <div className="flex items-center justify-between">
                  <Button size="sm" asChild>
                    <Link href={`/videos/${video.slug}`}>Watch</Link>
                  </Button>
                  
                  <Button size="sm" variant="outline" asChild>
                    <a href={video.video_url} target="_blank" rel="noopener noreferrer">
                      <ExternalLink className="h-4 w-4 mr-1" />
                      {platform}
                    </a>
                  </Button>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {showViewAll && videos.length > (limit || 0) && (
        <div className="text-center">
          <Button asChild>
            <Link href="/videos">View All Videos</Link>
          </Button>
        </div>
      )}
    </div>
  );
}
