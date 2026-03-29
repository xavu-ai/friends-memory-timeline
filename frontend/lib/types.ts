// API Types
export interface Friend {
  friend_id: string;
  friend_name: string;
  created_at: string;
}

export interface Event {
  id: string;
  date: string;
  title: string;
  story: string | null;
  photo_url: string | null;
  location: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
  theme_era: 'retro' | 'modern';
}

export interface CreateEventPayload {
  date: string;
  title: string;
  story?: string;
  photo?: File;
  location?: string;
}

export interface UpdateEventPayload {
  date?: string;
  title?: string;
  story?: string;
  photo?: File;
  location?: string;
}

export interface ApiError {
  code: string;
  detail: string;
  field_errors?: Record<string, string>;
}

// Auth State
export interface AuthState {
  friendId: string | null;
  friendName: string | null;
  token: string | null;
}

// Form Types
export type EventFormMode = 'create' | 'edit';

export interface EventFormValues {
  date: string;
  title: string;
  story: string;
  location: string;
  photo_url: string;
}
