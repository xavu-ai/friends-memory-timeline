'use client';

import { useState, useEffect, useCallback } from 'react';
import type { Event, CreateEventPayload, UpdateEventPayload } from '@/lib/types';
import { api } from '@/lib/api';

export function useEvents() {
  const [events, setEvents] = useState<Event[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  const fetchEvents = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const { events: fetchedEvents } = await api.events.list();
      setEvents(fetchedEvents.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()));
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to fetch events'));
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEvents();
  }, [fetchEvents]);

  const createEvent = useCallback(async (data: CreateEventPayload) => {
    const newEvent = await api.events.create(data);
    setEvents((prev) => [newEvent, ...prev].sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime()));
    return newEvent;
  }, []);

  const updateEvent = useCallback(async (id: string, data: UpdateEventPayload) => {
    const updatedEvent = await api.events.update(id, data);
    setEvents((prev) =>
      prev.map((e) => (e.id === id ? updatedEvent : e)).sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    );
    return updatedEvent;
  }, []);

  const deleteEvent = useCallback(async (id: string) => {
    await api.events.delete(id);
    setEvents((prev) => prev.filter((e) => e.id !== id));
  }, []);

  return {
    events,
    isLoading,
    error,
    fetchEvents,
    createEvent,
    updateEvent,
    deleteEvent,
  };
}
