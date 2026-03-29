'use client';

import { useMemo } from 'react';
import type { Event } from '@/lib/types';

export function useTimelineTheme(events: Event[]) {
  const themeClasses = useMemo(() => {
    const decadesArray: string[] = [];
    const decadeSet = new Set<string>();
    events.forEach((event) => {
      const year = new Date(event.date).getFullYear();
      const decade = Math.floor(year / 10) * 10;
      const decadeStr = `${decade}s`;
      if (!decadeSet.has(decadeStr)) {
        decadeSet.add(decadeStr);
        decadesArray.push(decadeStr);
      }
    });

    const hasRetro = decadesArray.some((d) => d.endsWith('s') && parseInt(d) < 2000);
    const hasModern = decadesArray.some((d) => parseInt(d) >= 2000);

    return {
      hasRetro,
      hasModern,
      decades: decadesArray.sort(),
    };
  }, [events]);

  const getEraClasses = (themeEra: 'retro' | 'modern') => {
    if (themeEra === 'retro') {
      return {
        container: 'bg-retro-50',
        card: 'theme-retro relative rounded-xl',
        text: 'text-retro-900',
        accent: 'bg-retro-400',
        badge: 'bg-retro-200 text-retro-800',
        border: 'border-retro-300',
      };
    }
    return {
      container: 'bg-modern-50',
      card: 'theme-modern relative rounded-lg',
      text: 'text-modern-900',
      accent: 'bg-blue-500',
      badge: 'bg-modern-200 text-modern-800',
      border: 'border-modern-200',
    };
  };

  return {
    themeClasses,
    getEraClasses,
  };
}
