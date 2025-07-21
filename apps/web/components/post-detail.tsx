"use client"

import { usePost } from "@/lib/hooks"
import { Card, CardContent, CardHeader, CardTitle } from "@workspace/ui/components/card"
import { Badge } from "@workspace/ui/components/badge"
import { Button } from "@workspace/ui/components/button"
import { CalendarDays, User, ArrowLeft } from "lucide-react"
import Image from "next/image"
import Link from "next/link"

interface PostDetailProps {
  slug: string
}

export default function PostDetail({ slug }: PostDetailProps) {
  const { data: post, isLoading, error } = usePost(slug)

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardContent className="p-8">
            <div className="animate-pulse space-y-4">
              <div className="h-8 bg-gray-200 rounded w-3/4"></div>
              <div className="h-64 bg-gray-200 rounded"></div>
              <div className="space-y-2">
                <div className="h-4 bg-gray-200 rounded"></div>
                <div className="h-4 bg-gray-200 rounded"></div>
                <div className="h-4 bg-gray-200 rounded w-2/3"></div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <Card>
          <CardContent className="p-8">
            <div className="text-center space-y-4">
              <p className="text-red-500">Error loading post: {error.message}</p>
              <Button asChild>
                <Link href="/posts">
                  <ArrowLeft className="h-4 w-4 mr-2" />
                  Back to Posts
                </Link>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  if (!post) return null

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <Button variant="ghost" asChild>
          <Link href="/posts">
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Posts
          </Link>
        </Button>
      </div>

      <Card>
        <CardHeader className="space-y-4">
          <div className="space-y-2">
            <CardTitle className="text-3xl">{post.title}</CardTitle>
            <p className="text-lg text-muted-foreground">{post.excerpt}</p>
          </div>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-1">
                <User className="h-4 w-4" />
                {post.author}
              </div>
              <div className="flex items-center gap-1">
                <CalendarDays className="h-4 w-4" />
                {new Date(post.date_published).toLocaleDateString()}
              </div>
            </div>
            
            <Badge variant="secondary">
              {post.tags.replace('_', ' ')}
            </Badge>
          </div>

          {post.image && (
            <div className="w-full">
              <Image
                src={post.image}
                alt={post.title}
                width={800}
                height={400}
                className="rounded-lg object-cover w-full"
              />
            </div>
          )}
        </CardHeader>
        
        <CardContent className="prose prose-gray dark:prose-invert max-w-none">
          <div 
            dangerouslySetInnerHTML={{ __html: post.content }}
            className="whitespace-pre-wrap"
          />
        </CardContent>
      </Card>
    </div>
  )
}
