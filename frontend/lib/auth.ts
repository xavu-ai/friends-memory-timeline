import type { AuthState } from './types';

const AUTH_STORAGE_KEY = 'friends-memory-auth';

class AuthStore {
  private state: AuthState = {
    friendId: null,
    friendName: null,
    token: null,
  };

  constructor() {
    this.hydrate();
  }

  private hydrate(): void {
    if (typeof window === 'undefined') return;
    try {
      const stored = localStorage.getItem(AUTH_STORAGE_KEY);
      if (stored) {
        this.state = JSON.parse(stored);
      }
    } catch {
      // Invalid stored data, use default
    }
  }

  private persist(): void {
    if (typeof window === 'undefined') return;
    localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(this.state));
  }

  getState(): AuthState {
    return { ...this.state };
  }

  getToken(): string | null {
    return this.state.token;
  }

  setAuth(friendId: string, friendName: string, token: string): void {
    this.state = { friendId, friendName, token };
    this.persist();
  }

  clearAuth(): void {
    this.state = { friendId: null, friendName: null, token: null };
    this.persist();
  }

  isAuthenticated(): boolean {
    return this.state.token !== null;
  }
}

export const authStore = new AuthStore();
