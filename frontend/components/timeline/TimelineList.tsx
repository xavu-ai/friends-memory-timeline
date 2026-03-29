'use client';

import type { Event } from '@/lib/types';
import { TimelineCard } from './TimelineCard';

interface TimelineListProps {
  events: Event[];
  onEdit: (event: Event) => void;
  onDelete: (event: Event) => void;
  isOwner: boolean;
}

export function TimelineList({ events, onEdit, onDelete, isOwner }: TimelineListProps) {
  return (
    <div role="list" className="space-y-8" aria-label="Memory events">
      {events.map((event) => (
        <div key={event.id} role="listitem">
          <TimelineCard
            event={event}
            onEdit={onEdit}
            onDelete={onDelete}
            isOwner={isOwner}
          />
        </div>
      ))}
    </div>
  );
}
