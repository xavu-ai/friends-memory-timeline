'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState, useCallback } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { useEvents } from '@/hooks/useEvents';
import { Header } from '@/components/layout/Header';
import { LoadingState } from '@/components/layout/LoadingState';
import { Timeline } from '@/components/timeline/Timeline';
import { EventForm } from '@/components/event/EventForm';
import { DeleteConfirmation } from '@/components/event/DeleteConfirmation';
import type { Event } from '@/lib/types';

export default function TimelinePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading: authLoading, friendId, friendName } = useAuth();
  const { events, isLoading: eventsLoading, error, fetchEvents, createEvent, updateEvent, deleteEvent } = useEvents();

  const [mounted, setMounted] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<Event | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [editTarget, setEditTarget] = useState<Event | null>(null);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !authLoading && !isAuthenticated) {
      router.replace('/');
    }
  }, [mounted, authLoading, isAuthenticated, router]);

  const handleCreateEvent = useCallback(async (data: { date: string; title: string; story?: string; location?: string; photo_url?: string }) => {
    await createEvent({
      date: data.date,
      title: data.title,
      story: data.story,
      location: data.location,
    });
  }, [createEvent]);

  const handleEditEvent = useCallback(async (id: string, data: { date?: string; title?: string; story?: string; location?: string; photo_url?: string }) => {
    await updateEvent(id, {
      date: data.date,
      title: data.title,
      story: data.story,
      location: data.location,
    });
    setEditTarget(null);
  }, [updateEvent]);

  const handleDeleteConfirm = useCallback(async () => {
    if (!deleteTarget) return;
    try {
      setIsDeleting(true);
      await deleteEvent(deleteTarget.id);
      setDeleteTarget(null);
    } finally {
      setIsDeleting(false);
    }
  }, [deleteTarget, deleteEvent]);

  if (!mounted || authLoading) {
    return (
      <div className="min-h-screen">
        <LoadingState />
      </div>
    );
  }

  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-retro-50 to-modern-100">
      <Header friendName={friendName} />

      <main className="container mx-auto px-4 py-8">
        {eventsLoading ? (
          <LoadingState />
        ) : (
          <Timeline
            events={events}
            isLoading={false}
            error={error}
            onRefresh={fetchEvents}
            onCreateEvent={handleCreateEvent}
            onEditEvent={handleEditEvent}
            onDeleteEvent={setDeleteTarget}
            isOwner={true}
          />
        )}
      </main>

      {editTarget && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="w-full max-w-lg">
            <EventForm
              mode="edit"
              event={editTarget}
              onSubmit={async (data) => {
                await handleEditEvent(editTarget.id, data);
              }}
              onCancel={() => setEditTarget(null)}
              isLoading={false}
            />
          </div>
        </div>
      )}

      <DeleteConfirmation
        open={deleteTarget !== null}
        onOpenChange={(open) => !open && setDeleteTarget(null)}
        eventTitle={deleteTarget?.title || ''}
        onConfirm={handleDeleteConfirm}
        isLoading={isDeleting}
      />
    </div>
  );
}
