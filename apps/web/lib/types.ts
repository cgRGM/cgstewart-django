// API Response Types
export interface Bio {
  id: number
  image?: string
  image_url?: string
  about: string
  x_url?: string
  linkedin_url?: string
  github_url?: string
  youtube_url?: string
  twitch_url?: string
  resume?: string
  resume_url?: string
  updated_at: string
}

export interface Post {
  id: number
  title: string
  image?: string
  image_url?: string
  excerpt: string
  content: string
  author: number
  author_name: string
  date_published: string
  slug: string
  tags: 'general' | 'tech' | 'book_reviews'
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface PostListItem {
  id: number
  title: string
  image?: string
  image_url?: string
  excerpt: string
  author: number
  author_name: string
  date_published: string
  slug: string
  tags: 'general' | 'tech' | 'book_reviews'
}

export interface Video {
  id: number
  title: string
  video_url: string
  slug: string
  description?: string
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface Project {
  id: number
  title: string
  description: string
  stack: string
  stack_list: string[]
  website_url?: string
  github_url?: string
  slug: string
  content?: string
  image?: string
  image_url?: string
  is_published: boolean
  created_at: string
  updated_at: string
}

export interface ProjectListItem {
  id: number
  title: string
  description: string
  stack_list: string[]
  website_url?: string
  github_url?: string
  slug: string
  image?: string
  image_url?: string
}
