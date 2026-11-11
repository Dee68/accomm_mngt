'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { useState } from 'react';

export function QueryProvider({ children }: { children: React.ReactNode }) {
  // useState (not useRef) so React Strict Mode + HMR behave; each request gets its own client.
  const [client] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 60_000,          // 1 min — matches RTK Query's default `keepUnusedDataFor` feel
            gcTime: 5 * 60_000,         // 5 min
            refetchOnWindowFocus: false, // we'll opt in per-query where it matters
            retry: 1,
          },
          mutations: {
            retry: 0,
          },
        },
      }),
  );

  return (
    <QueryClientProvider client={client}>
      {children}
      {process.env.NODE_ENV === 'development' && (
        <ReactQueryDevtools initialIsOpen={false} />
      )}
    </QueryClientProvider>
  );
}