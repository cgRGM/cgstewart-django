import { api } from "@/lib/api";
import { Project } from "@/lib/types";
import { notFound } from "next/navigation";
import { Metadata } from "next";
import Image from "next/image";
import Link from "next/link";
import { Button } from "@workspace/ui/components/button";
import { ArrowLeft, ExternalLink } from "lucide-react";

type ProjectPageProps = {
  params: {
    slug: string;
  };
};

// Generate dynamic metadata for SEO
export async function generateMetadata({ params }: ProjectPageProps): Promise<Metadata> {
  const { slug } = await params;
  
  try {
    const project = await api.getProjectBySlug(slug);
    return {
      title: `${project.title} by CG Stewart`,
      description: project.description || 'A project by CG Stewart',
      openGraph: {
        title: `${project.title} by CG Stewart`,
        description: project.description || 'A project by CG Stewart',
        type: 'article',
        images: project.image_url ? [{ url: project.image_url }] : [],
        modifiedTime: project.updated_at,
      },
      twitter: {
        card: 'summary_large_image',
        title: `${project.title} by CG Stewart`,
        description: project.description || 'A project by CG Stewart',
        images: project.image_url ? [project.image_url] : [],
      },
    };
  } catch (error) {
    return {
      title: 'Project Not Found | CG Stewart',
      description: 'The requested project could not be found.',
    };
  }
}

export async function generateStaticParams() {
  try {
    const projectsResponse = await api.getProjects();
    return projectsResponse.results.map((project) => ({
      slug: project.slug,
    }));
  } catch (error) {
    console.error("Failed to generate static params for projects:", error);
    return [];
  }
}

export default async function ProjectPage({ params }: ProjectPageProps) {
  const { slug } = await params;
  let project: Project;

  try {
    project = await api.getProjectBySlug(slug);
  } catch (error) {
    console.error(`Failed to fetch project with slug "${slug}":`, error);
    notFound();
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-4xl">
      <div className="mb-12">
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
            {project.title}
          </h1>
          <div className="flex flex-wrap gap-4 items-center">
            {project.website_url && (
              <Button asChild variant="secondary">
                <a
                  href={project.website_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <ExternalLink className="mr-2 h-4 w-4" />
                  Live Site
                </a>
              </Button>
            )}
            {project.github_url && (
              <Button asChild variant="secondary">
                <a
                  href={project.github_url}
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <ExternalLink className="mr-2 h-4 w-4" />
                  GitHub
                </a>
              </Button>
            )}
          </div>
        </header>

        {project.image_url && (
          <div className="mb-8 rounded-lg overflow-hidden aspect-video relative">
            <Image
              src={project.image_url}
              alt={project.title}
              fill
              className="object-cover"
              priority
            />
          </div>
        )}

        <div className="prose prose-lg dark:prose-invert max-w-none">
          <p className="lead mb-6 text-xl text-muted-foreground">
            {project.description}
          </p>
          <h3 className="text-2xl font-semibold mt-8 mb-4">Tech Stack</h3>
          <div className="flex flex-wrap gap-2 mb-8">
            {project.stack_list.map((tech) => (
              <div
                key={tech}
                className="bg-secondary text-secondary-foreground px-3 py-1 rounded-full text-sm mb-4"
              >
                {tech}
              </div>
            ))}
          </div>
          <h3 className="text-2xl font-semibold mt-8 mb-4">
            About this Project
          </h3>
          <pre className="whitespace-pre-wrap font-sans text-base">
            {project.content}
          </pre>
        </div>
      </article>
    </div>
  );
}
