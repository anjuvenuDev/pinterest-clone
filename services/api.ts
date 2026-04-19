import { Platform } from 'react-native';
import Constants from 'expo-constants';

import type { CreatorIngestResponse, FeedResponse, PinItem, UserProfile } from '@/types/pin';

const defaultBaseUrl = Platform.select({
  android: 'http://10.0.2.2:8000/api',
  ios: 'http://127.0.0.1:8000/api',
  default: 'http://127.0.0.1:8000/api',
});

function normalizeBaseUrl(url: string): string {
  return url.replace(/\/+$/, '');
}

function inferExpoHostBaseUrl(): string | null {
  const hostUri = Constants.expoConfig?.hostUri;
  if (!hostUri) return null;
  const host = hostUri.split(':')[0];
  if (!host || host === 'localhost' || host === '127.0.0.1') return null;
  return `http://${host}:8000/api`;
}

const configuredBaseUrl = process.env.EXPO_PUBLIC_API_BASE_URL?.trim();
const API_BASE_URL = normalizeBaseUrl(
  configuredBaseUrl || inferExpoHostBaseUrl() || defaultBaseUrl || 'http://127.0.0.1:8000/api'
);
const DEMO_TOKEN = process.env.EXPO_PUBLIC_DEMO_TOKEN ?? 'demo-token';

type FeedQuery = {
  query?: string;
  limit?: number;
  bookmarked?: boolean;
};

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 8000);
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${DEMO_TOKEN}`,
        ...(init?.headers ?? {}),
      },
      signal: controller.signal,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Network request failed';
    throw new Error(`API request failed to ${API_BASE_URL}${path}: ${message}`);
  } finally {
    clearTimeout(timeout);
  }

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`API ${response.status}: ${body}`);
  }

  return response.json() as Promise<T>;
}

export async function fetchFeed(options: FeedQuery = {}): Promise<FeedResponse> {
  const params = new URLSearchParams();
  if (options.query) params.set('query', options.query);
  if (options.limit) params.set('limit', String(options.limit));
  if (options.bookmarked) params.set('bookmarked', 'true');

  const queryString = params.toString();
  return request<FeedResponse>(`/feed${queryString ? `?${queryString}` : ''}`);
}

export async function fetchRecipeById(recipeId: string): Promise<PinItem> {
  return request<PinItem>(`/feed/${recipeId}`);
}

export async function toggleLike(recipeId: string): Promise<void> {
  await request(`/feed/${recipeId}/like`, { method: 'POST' });
}

export async function toggleBookmark(recipeId: string): Promise<void> {
  await request(`/feed/${recipeId}/bookmark`, { method: 'POST' });
}

export async function fetchMyProfile(): Promise<UserProfile> {
  return request<UserProfile>('/users/me');
}

export async function ingestRecipe(sourceUrl: string, creatorNotes: string): Promise<CreatorIngestResponse> {
  return request<CreatorIngestResponse>('/creator/ingest', {
    method: 'POST',
    body: JSON.stringify({
      source_url: sourceUrl,
      consent_accepted: true,
      creator_notes: creatorNotes || null,
    }),
  });
}

export async function createRemix(recipeId: string, ingredientSwaps: Record<string, string>): Promise<unknown> {
  return request('/remix', {
    method: 'POST',
    body: JSON.stringify({
      recipe_id: recipeId,
      ingredient_swaps: ingredientSwaps,
      goal: 'lighter version',
    }),
  });
}

export function getBackendBaseUrl(): string {
  return API_BASE_URL;
}
