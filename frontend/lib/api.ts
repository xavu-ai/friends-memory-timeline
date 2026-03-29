import type { Friend, Event, CreateEventPayload, UpdateEventPayload, ApiError as ApiErrorInterface } from './types';
import { authStore } from './auth';

const API_BASE = '';

class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public fieldErrors?: Record<string, string>
  ) {
    super(message);
    this.name = 'ApiError';
  }
}

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = authStore.getToken();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Only add Content-Type for non-FormData requests
  const isFormData = options?.body instanceof FormData;
  if (isFormData) {
    delete headers['Content-Type'];
  }

  const res = await fetch(`${API_BASE}/api/v1${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({ code: 'UNKNOWN', detail: 'Unknown error' })) as ApiErrorInterface;
    throw new ApiError(res.status, err.code, err.detail, err.field_errors);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  return res.json();
}

export const api = {
  auth: {
    verify: (password: string): Promise<Friend> => {
      return request<Friend>('/auth/verify', {
        method: 'POST',
        body: JSON.stringify({ password }),
      });
    },
  },
  events: {
    list: (): Promise<{ events: Event[] }> => {
      return request<{ events: Event[] }>('/events');
    },
    get: (id: string): Promise<Event> => {
      return request<Event>(`/events/${id}`);
    },
    create: (data: CreateEventPayload): Promise<Event> => {
      const { photo, ...rest } = data;
      if (photo) {
        const formData = new FormData();
        formData.append('date', rest.date);
        formData.append('title', rest.title);
        if (rest.story) formData.append('story', rest.story);
        if (rest.location) formData.append('location', rest.location);
        formData.append('photo', photo);
        return request<Event>('/events', {
          method: 'POST',
          body: formData,
        });
      }
      return request<Event>('/events', {
        method: 'POST',
        body: JSON.stringify(data),
      });
    },
    update: (id: string, data: UpdateEventPayload): Promise<Event> => {
      const { photo, ...rest } = data;
      if (photo) {
        const formData = new FormData();
        if (rest.date) formData.append('date', rest.date);
        if (rest.title) formData.append('title', rest.title);
        if (rest.story !== undefined) formData.append('story', rest.story);
        if (rest.location) formData.append('location', rest.location);
        formData.append('photo', photo);
        return request<Event>(`/events/${id}`, {
          method: 'PUT',
          body: formData,
        });
      }
      return request<Event>(`/events/${id}`, {
        method: 'PUT',
        body: JSON.stringify(data),
      });
    },
    delete: (id: string): Promise<void> => {
      return request<void>(`/events/${id}`, { method: 'DELETE' });
    },
  },
};

export { ApiError };
