// Define a generic interface for possible API response shapes
export interface ApiResponse<T = any> {
  results?: T[];
  data?: {
    results?: T[];
  };
  popular_tags?: {
    results?: T[];
  };
  top_posts?: {
    results?: T[];
  };
  [key: string]: any; // allow other dynamic keys
}

/**
 * Normalizes RTK Query API responses that may have nested structures
 * like:
 *  - { results: [...] }
 *  - { data: { results: [...] } }
 *  - { popular_tags: { results: [...] } }
 *  - { top_posts: { results: [...] } }
 *
 * @param response - The full API response object
 * @returns The extracted results array (or [])
 */
export function normalizeResults<T = any>(response?: ApiResponse<T>): T[] {
  if (!response) return [];

  if (Array.isArray(response.results)) return response.results;
  if (Array.isArray(response.data?.results)) return response.data.results;
  if (Array.isArray(response.popular_tags?.results)) return response.popular_tags.results;
  if (Array.isArray(response.top_posts?.results)) return response.top_posts.results;
  if (Array.isArray(response as any)) return response as unknown as T[];

  return [];
}
