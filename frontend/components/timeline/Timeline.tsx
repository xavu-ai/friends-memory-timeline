'use client';

import type { Event } from '@/lib/types';
import { TimelineList } from './TimelineList';
import { EmptyTimeline } from './EmptyTimeline';
import { EventForm } from '@/components/event/EventForm';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Button } from '@/components/ui/button';
import { RefreshCw } from 'lucide-react';

interface TimelineProps {
  events: Event[];
  isLoading: boolean;
  error: Error | null;
  onRefresh: () => void;
  onCreateEvent: (data: { date: string; title: string; story?: string; location?: string; photo_url?: string }) => Promise<void>;
  onEditEvent: (id: string, data: { date?: string; title?: string; story?: string; location?: string; photo_url?: string }) => Promise<void>;
  onDeleteEvent: (event: Event) => void;
  isOwner: boolean;
}

export function Timeline({
  events,
  isLoading,
  error,
  onRefresh,
  onCreateEvent,
  onEditEvent,
  onDeleteEvent,
  isOwner,
}: TimelineProps) {
  if (error) {
    return (
      <Alert variant="destructive" className="mx-auto max-w-4xl">
        <AlertDescription className="flex items-center justify-between">
          <span aria-live="polite">{error.message}</span>
          <Button variant="outline" size="sm" onClick={onRefresh}>
            <RefreshCw className="mr-2 h-4 w-4" />
            Retry
          </Button>
        </AlertDescription>
      </Alert>
    );
  }

  const handleEdit = (event: Event) => {
    // This will be handled by the parent via the edit modal
    onEditEvent(event.id, { date: event.date.split('T')[0], title: event.title, story: event.story || undefined, location: event.location || undefined });
  };

  const handleDelete = (event: Event) => {
    onDeleteEvent(event);
  };

  return (
    <div className="mx-auto max-w-4xl space-y-8 px-4 py-8">
      {isOwner && (
        <section aria-label="Add new memory">
          <EventForm mode="create" onSubmit={onCreateEvent} isLoading={isLoading} />
        </section>
      )}

      <section aria-label="Memory timeline" className="relative">
        <div className="absolute left-1/2 top-0 h-full w-0.5 -translate-x-1/2 bg-gradient-to-b from-amber-400 via-amber-500 to-blue-500" aria-hidden="true" />

        {events.length === 0 ? (
          <EmptyTimeline />
        ) : (
          <TimelineList
            events={events}
            onEdit={handleEdit}
            onDelete={handleDelete}
            isOwner={isOwner}
          />
        )}
      </section>
    </div>
  );
}
