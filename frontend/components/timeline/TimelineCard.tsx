'use client';

import Image from 'next/image';
import type { Event } from '@/lib/types';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Pencil, Trash2, MapPin, Calendar } from 'lucide-react';
import { formatDate, getDecade } from '@/lib/utils';

interface TimelineCardProps {
  event: Event;
  onEdit: (event: Event) => void;
  onDelete: (event: Event) => void;
  isOwner: boolean;
}

export function TimelineCard({ event, onEdit, onDelete, isOwner }: TimelineCardProps) {
  const isRetro = event.theme_era === 'retro';

  return (
    <article
      className={`relative animate-fade-in animate-slide-up ${
        isRetro ? 'theme-retro' : 'theme-modern'
      } rounded-xl p-6`}
    >
      {/* Timeline dot */}
      <div
        className={`absolute left-1/2 top-8 h-4 w-4 -translate-x-1/2 rounded-full ${
          isRetro ? 'bg-retro-500' : 'bg-blue-500'
        } ring-4 ring-background`}
        aria-hidden="true"
      />

      <div className="ml-0 md:ml-[calc(50%+2rem)]">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-2 flex-1">
            <div className="flex items-center gap-2 flex-wrap">
              <Badge
                variant="secondary"
                className={isRetro ? 'bg-retro-200 text-retro-800' : 'bg-modern-100 text-modern-700'}
              >
                {getDecade(event.date)}
              </Badge>
              <span className="flex items-center gap-1 text-sm text-muted-foreground">
                <Calendar className="h-3 w-3" aria-hidden="true" />
                <time dateTime={event.date}>{formatDate(event.date)}</time>
              </span>
            </div>

            <h3 className={`font-serif text-2xl font-semibold ${isRetro ? 'text-retro-900' : 'text-modern-900'}`}>
              {event.title}
            </h3>

            {event.photo_url && (
              <div className="relative mt-4 aspect-video w-full overflow-hidden rounded-lg">
                <Image
                  src={event.photo_url}
                  alt={`Photo for ${event.title}`}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, 50vw"
                />
              </div>
            )}

            {event.story && (
              <p className={`text-base leading-relaxed ${isRetro ? 'text-retro-800' : 'text-modern-700'}`}>
                {event.story}
              </p>
            )}

            {event.location && (
              <span className={`flex items-center gap-1 text-sm ${isRetro ? 'text-retro-600' : 'text-modern-500'}`}>
                <MapPin className="h-3 w-3" aria-hidden="true" />
                {event.location}
              </span>
            )}
          </div>

          {isOwner && (
            <div className="flex gap-2">
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onEdit(event)}
                aria-label={`Edit ${event.title}`}
              >
                <Pencil className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => onDelete(event)}
                aria-label={`Delete ${event.title}`}
                className="text-destructive hover:text-destructive"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          )}
        </div>
      </div>
    </article>
  );
}
