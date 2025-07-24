"use client";

import { useBio } from "@/lib/hooks";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@workspace/ui/components/card";
import { Button } from "@workspace/ui/components/button";
import { Badge } from "@workspace/ui/components/badge";
import { ExternalLink, Github, Linkedin, Youtube, Twitch } from "lucide-react";
import Image from "next/image";

const socialIcons = {
  x_url: ExternalLink,
  linkedin_url: Linkedin,
  github_url: Github,
  youtube_url: Youtube,
  twitch_url: Twitch,
};

const socialLabels = {
  x_url: "X (Twitter)",
  linkedin_url: "LinkedIn",
  github_url: "GitHub",
  youtube_url: "YouTube",
  twitch_url: "Twitch",
};

export default function Bio() {
  const { data: bio, isLoading, error } = useBio();

  if (isLoading) {
    return (
      <Card className="w-full max-w-2xl">
        <CardContent className="p-6">
          <div className="animate-pulse">
            <div className="h-32 w-32 bg-gray-200 rounded-full mx-auto mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded w-3/4"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="w-full max-w-2xl">
        <CardContent className="p-6">
          <p className="text-red-500">Error loading bio: {error.message}</p>
        </CardContent>
      </Card>
    );
  }

  if (!bio) return null;

  const socialLinks = Object.entries(socialIcons).filter(
    ([key]) => bio[key as keyof typeof bio]
  );

  return (
    <Card className="w-full max-w-2xl">
      <CardHeader className="text-center">
        {bio.image_url && (
          <div className="flex justify-center mb-6">
            <Image
              src={bio.image_url}
              alt="Profile"
              width={150}
              height={150}
              className="rounded-full object-cover"
            />
          </div>
        )}
        <CardTitle className="text-2xl">CG Stewart</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <p className=" leading-relaxed">{bio.about}</p>
        </div>

        {socialLinks.length > 0 && (
          <div>
            <h3 className="font-semibold mb-3">Connect with me</h3>
            <div className="flex flex-wrap gap-2">
              {socialLinks.map(([key, Icon]) => {
                const url = bio[key as keyof typeof bio] as string;
                const label = socialLabels[key as keyof typeof socialLabels];
                return (
                  <Button key={key} variant="outline" size="sm" asChild>
                    <a
                      href={url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="flex items-center gap-2"
                    >
                      <Icon className="h-4 w-4" />
                      {label}
                    </a>
                  </Button>
                );
              })}
            </div>
          </div>
        )}

        {bio.resume_url && (
          <div>
            <Button asChild>
              <a
                href={bio.resume_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-2"
              >
                <ExternalLink className="h-4 w-4" />
                View Resume
              </a>
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
