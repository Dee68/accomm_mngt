import type { Metadata } from "next";
import "./globals.css";
import React from "react";
import { QueryProvider } from '@/providers/query-provider';
import { openSans, robotoSlab } from "@/lib/fonts";
import { ThemeProvider } from "@/components/theme-provider";
import Toast from "@/components/shared/Toast";
import { PersistAuth } from "@/utils";

export const metadata: Metadata = {
  title: "Home | Accommodation Center",
  description: "Welcome home",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${openSans.variable} ${robotoSlab.variable}`}>
        <Toast />
        <QueryProvider>
          <PersistAuth />
        {/* ThemeProvider inside body, but modifies <html> since attribute="class" */}
        <ThemeProvider 
        attribute="class" 
        defaultTheme="system" 
        enableSystem
        disableTransitionOnChange>
          {children}
        </ThemeProvider>
        </QueryProvider>
      </body>
    </html>
  );
}

