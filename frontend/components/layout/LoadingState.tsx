'use client';

import { Spinner } from '@/components/ui/spinner';

export function LoadingState() {
  return (
    <div className="flex min-h-[50vh] flex-col items-center justify-center gap-4">
      <Spinner />
      <p className="text-muted-foreground">Loading memories...</p>
    </div>
  );
}
