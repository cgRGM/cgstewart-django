'use client';

import { useProjects } from '@/lib/hooks';
import { Card, CardContent, CardHeader, CardTitle } from '@workspace/ui/components/card';
import { Button } from '@workspace/ui/components/button';
import { ArrowLeft, ExternalLink, Github } from 'lucide-react';
import { AnimatedElement } from '@/components/animated-element';
import Image from 'next/image';
import Link from 'next/link';

export default function ProjectsPage() {
  const { data: projects, isLoading, error } = useProjects();

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
          <p className="mt-4 text-muted-foreground">Loading projects...</p>
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
          <p className="text-destructive">Failed to load projects. Please try again later.</p>
        </div>
      </div>
    );
  }

  if (!projects || projects.length === 0) {
    return (
      <AnimatedElement>
        <Card className="overflow-hidden">
          <CardHeader>
            <div className="mb-8">
              <Link href="/">
                <Button variant="outline">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back to Home
                </Button>
              </Link>
            </div>
            <CardTitle className="text-4xl font-semibold tracking-tight sm:text-5xl">
              I like to showcase my work here
            </CardTitle>
            <p className="mt-2 text-lg text-muted-foreground">View my development projects and creations</p>
          </CardHeader>
          <CardContent>
            <div className="text-center py-10">No projects available at the moment.</div>
          </CardContent>
        </Card>
      </AnimatedElement>
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
        <h1 className="text-4xl font-bold tracking-tight mb-2">All Projects</h1>
        <p className="text-muted-foreground">
          {projects.length} project{projects.length !== 1 ? 's' : ''} total
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project, index) => (
          <AnimatedElement key={project.id} delay={0.1 + index * 0.1}>
            <Link href={`/projects/${project.slug}`} className="block">
              <Card className="overflow-hidden hover:shadow-lg transition-all duration-300 h-full">
                {project.image_url && (
                  <div className="aspect-video relative overflow-hidden">
                    <Image
                      src={project.image_url}
                      alt={project.title}
                      fill
                      className="object-cover hover:scale-105 transition-transform duration-300"
                    />
                  </div>
                )}
                <CardHeader>
                  <CardTitle className="line-clamp-2 hover:text-primary transition-colors">
                    {project.title}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground line-clamp-3 mb-4">{project.description}</p>
                  
                  {/* Tech Stack */}
                  <div className="flex flex-wrap gap-1 mb-4">
                    {project.stack_list.slice(0, 3).map((tech) => (
                      <span
                        key={tech}
                        className="inline-block bg-secondary text-secondary-foreground px-2 py-1 rounded-full text-xs"
                      >
                        {tech}
                      </span>
                    ))}
                    {project.stack_list.length > 3 && (
                      <span className="inline-block bg-muted text-muted-foreground px-2 py-1 rounded-full text-xs">
                        +{project.stack_list.length - 3} more
                      </span>
                    )}
                  </div>

                  {/* Action buttons */}
                  <div className="flex gap-2">
                    {project.website_url && (
                      <Button 
                        size="sm" 
                        variant="secondary" 
                        asChild
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          window.open(project.website_url, '_blank');
                        }}
                      >
                        <span>
                          <ExternalLink className="h-3 w-3 mr-1" />
                          Live
                        </span>
                      </Button>
                    )}
                    {project.github_url && (
                      <Button 
                        size="sm" 
                        variant="secondary" 
                        asChild
                        onClick={(e) => {
                          e.preventDefault();
                          e.stopPropagation();
                          window.open(project.github_url, '_blank');
                        }}
                      >
                        <span>
                          <Github className="h-3 w-3 mr-1" />
                          Code
                        </span>
                      </Button>
                    )}
                  </div>
                </CardContent>
              </Card>
            </Link>
          </AnimatedElement>
        ))}
      </div>
    </div>
  );
}
