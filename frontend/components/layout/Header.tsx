'use client';

import { Heart } from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/button';

interface HeaderProps {
  friendName: string | null;
}

export function Header({ friendName }: HeaderProps) {
  const { logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-2">
          <Heart className="h-6 w-6 text-retro-500 fill-retro-500" />
          <span className="font-serif text-xl font-semibold">
            {friendName ? `${friendName}'s Memories` : 'Memory Timeline'}
          </span>
        </div>
        <Button variant="ghost" size="sm" onClick={logout} aria-label="Log out">
          Log out
        </Button>
      </div>
    </header>
  );
}
