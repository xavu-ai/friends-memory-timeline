'use client';

import { UseFormRegister, FieldErrors } from 'react-hook-form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';

interface EventFormFieldsProps {
  register: UseFormRegister<{
    date: string;
    title: string;
    story: string;
    location: string;
    photo_url: string;
  }>;
  errors: FieldErrors<{
    date: string;
    title: string;
    story: string;
    location: string;
    photo_url: string;
  }>;
}

export function EventFormFields({ register, errors }: EventFormFieldsProps) {
  return (
    <div className="space-y-4">
      <div className="space-y-2">
        <label htmlFor="date" className="text-sm font-medium">
          Date <span className="text-destructive">*</span>
        </label>
        <Input
          id="date"
          type="date"
          aria-label="Event date"
          aria-invalid={!!errors.date}
          {...register('date')}
        />
        {errors.date && (
          <p className="text-sm text-destructive" role="alert">{errors.date.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="title" className="text-sm font-medium">
          Title <span className="text-destructive">*</span>
        </label>
        <Input
          id="title"
          type="text"
          placeholder="A memorable title..."
          aria-label="Event title"
          aria-invalid={!!errors.title}
          {...register('title')}
        />
        {errors.title && (
          <p className="text-sm text-destructive" role="alert">{errors.title.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="story" className="text-sm font-medium">
          Story
        </label>
        <Textarea
          id="story"
          placeholder="Tell the story behind this memory..."
          className="min-h-[120px] resize-y"
          aria-label="Event story"
          {...register('story')}
        />
        {errors.story && (
          <p className="text-sm text-destructive" role="alert">{errors.story.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="location" className="text-sm font-medium">
          Location
        </label>
        <Input
          id="location"
          type="text"
          placeholder="Where did this happen?"
          aria-label="Event location"
          {...register('location')}
        />
        {errors.location && (
          <p className="text-sm text-destructive" role="alert">{errors.location.message}</p>
        )}
      </div>

      <div className="space-y-2">
        <label htmlFor="photo_url" className="text-sm font-medium">
          Photo URL
        </label>
        <Input
          id="photo_url"
          type="url"
          placeholder="https://example.com/photo.jpg"
          aria-label="Photo URL"
          {...register('photo_url')}
        />
        {errors.photo_url && (
          <p className="text-sm text-destructive" role="alert">{errors.photo_url.message}</p>
        )}
      </div>
    </div>
  );
}
