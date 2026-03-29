'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';
import { PasswordForm } from '@/components/auth/PasswordForm';
import type { Friend } from '@/lib/types';
import { useAuth } from '@/hooks/useAuth';

export default function HomePage() {
  const router = useRouter();
  const { isAuthenticated, isLoading } = useAuth();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted && !isLoading && isAuthenticated) {
      router.replace('/timeline');
    }
  }, [mounted, isLoading, isAuthenticated, router]);

  const handleSuccess = (friend: Friend) => {
    router.push('/timeline');
  };

  if (!mounted || isLoading) {
    return null;
  }

  if (isAuthenticated) {
    return null;
  }

  return <PasswordForm onSuccess={handleSuccess} />;
}
