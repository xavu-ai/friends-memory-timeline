'use client';

import { useState, useEffect } from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Spinner } from '@/components/ui/spinner';
import { EventFormFields } from './EventFormFields';
import type { Event, EventFormMode } from '@/lib/types';
import { isValidUrl } from '@/lib/utils';

const eventSchema = z.object({
  date: z.string().min(1, 'Date is required'),
  title: z.string().min(1, 'Title is required').max(200, 'Title must be 200 characters or less'),
  story: z.string().max(5000, 'Story must be 5000 characters or less').optional().default(''),
  location: z.string().max(200, 'Location must be 200 characters or less').optional().default(''),
  photo_url: z.string().optional().default('').refine((val) => !val || isValidUrl(val), {
    message: 'Please enter a valid URL',
  }),
});

type EventFormValues = z.infer<typeof eventSchema>;

interface EventFormProps {
  mode: EventFormMode;
  event?: Event;
  onSubmit: (data: EventFormValues) => Promise<void>;
  onCancel?: () => void;
  isLoading?: boolean;
}

export function EventForm({ mode, event, onSubmit, onCancel, isLoading = false }: EventFormProps) {
  const [error, setError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<EventFormValues>({
    resolver: zodResolver(eventSchema),
    defaultValues: {
      date: event?.date.split('T')[0] || '',
      title: event?.title || '',
      story: event?.story || '',
      location: event?.location || '',
      photo_url: event?.photo_url || '',
    },
  });

  useEffect(() => {
    if (event) {
      reset({
        date: event.date.split('T')[0],
        title: event.title,
        story: event.story || '',
        location: event.location || '',
        photo_url: event.photo_url || '',
      });
    }
  }, [event, reset]);

  const onFormSubmit = async (data: EventFormValues) => {
    try {
      setError(null);
      await onSubmit(data);
      if (mode === 'create') {
        reset();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save event');
    }
  };

  return (
    <Card className="border-retro-200 bg-retro-50/50">
      <CardHeader>
        <CardTitle className="font-serif text-xl">
          {mode === 'create' ? 'Add a New Memory' : 'Edit Memory'}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit(onFormSubmit)} className="space-y-6" noValidate>
          {error && (
            <Alert variant="destructive" role="alert">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          <EventFormFields register={register} errors={errors} />

          <div className="flex gap-3">
            <Button type="submit" disabled={isLoading} aria-label={mode === 'create' ? 'Add memory' : 'Save changes'}>
              {isLoading ? <Spinner className="mr-2 h-4 w-4" /> : null}
              {isLoading ? 'Saving...' : mode === 'create' ? 'Add Memory' : 'Save Changes'}
            </Button>
            {onCancel && (
              <Button type="button" variant="outline" onClick={onCancel} disabled={isLoading}>
                Cancel
              </Button>
            )}
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
