import { Bio, Post, PostListItem, Video, Project, ProjectListItem } from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Generic fetcher function
async function fetcher<T>(url: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${url}`)
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status} ${response.statusText}`)
  }
  
  return response.json()
}

// API functions
export const api = {
  // Bio
  getBio: () => fetcher<Bio>('/bio/'),
  
  // Posts
  getPosts: (tag?: string) => {
    const url = tag ? `/posts/?tag=${tag}` : '/posts/'
    return fetcher<{ results: PostListItem[] }>(url)
  },
  getPostBySlug: (slug: string) => fetcher<Post>(`/posts/${slug}/`),
  
  // Videos
  getVideos: () => fetcher<{ results: Video[] }>('/videos/'),
  getVideoBySlug: (slug: string) => fetcher<Video>(`/videos/${slug}/`),
  
  // Projects
  getProjects: () => fetcher<{ results: ProjectListItem[] }>('/projects/'),
  getProjectBySlug: (slug: string) => fetcher<Project>(`/projects/${slug}/`),
}

// Query keys for TanStack Query
export const queryKeys = {
  bio: ['bio'] as const,
  posts: (tag?: string) => ['posts', tag] as const,
  post: (slug: string) => ['post', slug] as const,
  videos: ['videos'] as const,
  video: (slug: string) => ['video', slug] as const,
  projects: ['projects'] as const,
  project: (slug: string) => ['project', slug] as const,
}
