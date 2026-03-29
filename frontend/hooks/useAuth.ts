'use client';

import { useState, useEffect, useCallback } from 'react';
import type { AuthState } from '@/lib/types';
import { authStore } from '@/lib/auth';
import { api } from '@/lib/api';

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    friendId: null,
    friendName: null,
    token: null,
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setState(authStore.getState());
    setIsLoading(false);
  }, []);

  const login = useCallback(async (password: string) => {
    const friend = await api.auth.verify(password);
    authStore.setAuth(friend.friend_id, friend.friend_name, password);
    setState(authStore.getState());
    return friend;
  }, []);

  const logout = useCallback(() => {
    authStore.clearAuth();
    setState({ friendId: null, friendName: null, token: null });
  }, []);

  return {
    ...state,
    isAuthenticated: state.token !== null,
    isLoading,
    login,
    logout,
  };
}
