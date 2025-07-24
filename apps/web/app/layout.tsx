import { Geist, Geist_Mono } from "next/font/google";
import { Metadata } from "next";

import "@workspace/ui/globals.css";
import { Providers } from "@/components/providers";
import Navbar from "@/components/navbar";

const fontSans = Geist({
  subsets: ["latin"],
  variable: "--font-sans",
});

const fontMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
});

export const metadata: Metadata = {
  title: 'CG Stewart - Full-stack Developer & Content Creator',
  description: 'Full-stack developer, content creator, and tech enthusiast sharing insights on web development, programming, and digital innovation.',
  openGraph: {
    title: 'CG Stewart - Full-stack Developer & Content Creator',
    description: 'Full-stack developer, content creator, and tech enthusiast sharing insights on web development, programming, and digital innovation.',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'CG Stewart - Full-stack Developer & Content Creator',
    description: 'Full-stack developer, content creator, and tech enthusiast sharing insights on web development, programming, and digital innovation.',
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body
        className={`${fontSans.variable} ${fontMono.variable} font-sans antialiased `}
      >
        <Providers>
          <Navbar />
          {children}
        </Providers>
      </body>
    </html>
  );
}
