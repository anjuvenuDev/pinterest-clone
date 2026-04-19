export type PinItem = {
  id: string;
  image: string;
  title: string;
  source_url?: string | null;
  creator_id?: string;
  tags?: string[];
};

export type FeedResponse = {
  items: PinItem[];
  total: number;
};

export type UserProfile = {
  id: string;
  name: string;
  email: string;
  roles: string[];
  onboarding_completed: boolean;
  bookmarks: number;
  likes: number;
};

export type CreatorIngestResponse = {
  success: boolean;
  message: string;
  recipe: PinItem;
};
