import { useQuery } from '@tanstack/react-query'
import { api, queryKeys } from './api'

// Bio hooks
export const useBio = () => {
  return useQuery({
    queryKey: queryKeys.bio,
    queryFn: api.getBio,
  })
}

// Post hooks
export const usePosts = (tag?: string) => {
  return useQuery({
    queryKey: queryKeys.posts(tag),
    queryFn: () => api.getPosts(tag),
    select: (data) => data.results, // Extract results array
  })
}

export const usePost = (slug: string) => {
  return useQuery({
    queryKey: queryKeys.post(slug),
    queryFn: () => api.getPostBySlug(slug),
    enabled: !!slug, // Only run if slug exists
  })
}

// Video hooks
export const useVideos = () => {
  return useQuery({
    queryKey: queryKeys.videos,
    queryFn: api.getVideos,
    select: (data) => data.results,
  })
}

export const useVideo = (slug: string) => {
  return useQuery({
    queryKey: queryKeys.video(slug),
    queryFn: () => api.getVideoBySlug(slug),
    enabled: !!slug,
  })
}

// Project hooks
export const useProjects = () => {
  return useQuery({
    queryKey: queryKeys.projects,
    queryFn: api.getProjects,
    select: (data) => data.results,
  })
}

export const useProject = (slug: string) => {
  return useQuery({
    queryKey: queryKeys.project(slug),
    queryFn: () => api.getProjectBySlug(slug),
    enabled: !!slug,
  })
}
