'use client';

import { Heart } from 'lucide-react';

export function EmptyTimeline() {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <div className="rounded-full bg-retro-100 p-6">
        <Heart className="h-12 w-12 text-retro-400" aria-hidden="true" />
      </div>
      <h3 className="mt-4 font-serif text-2xl font-semibold">No memories yet</h3>
      <p className="mt-2 text-muted-foreground max-w-sm">
        Start preserving your precious memories by adding your first moment above.
      </p>
    </div>
  );
}
