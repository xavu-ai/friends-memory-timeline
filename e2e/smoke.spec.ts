import { test, expect } from '@playwright/test';

const BASE_URL = process.env.E2E_BASE_URL || 'http://localhost:8100';
const API_URL = process.env.API_BASE_URL || 'http://localhost:6100';

test.describe('Auth Flow', () => {
  test('correct password grants access', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('[name="password"]', 'secret1');
    await page.click('[type="submit"]');
    // Should redirect to timeline after login
    await expect(page).toHaveURL(/\/timeline/);
  });

  test('wrong password shows 401 error', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    await page.fill('[name="password"]', 'wrongpassword');
    await page.click('[type="submit"]');
    // Should show error
    await expect(page.locator('text=/401|Invalid/i')).toBeVisible();
  });
});

test.describe('Timeline Load', () => {
  test.beforeEach(async ({ page }) => {
    // Login first
    await page.goto(`${BASE_URL}/login`);
    await page.fill('[name="password"]', 'secret1');
    await page.click('[type="submit"]');
    await page.waitForURL(/\/timeline/);
  });

  test('timeline page loads', async ({ page }) => {
    await page.goto(`${BASE_URL}/timeline`);
    await expect(page.locator('h1, h2, [data-testid="timeline"]')).toBeVisible();
  });
});

test.describe('API Direct Tests', () => {
  test('health endpoint returns ok', async () => {
    const res = await fetch(`${API_URL}/healthz`);
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.status).toBe('ok');
  });

  test('auth verify with correct password returns token', async () => {
    const res = await fetch(`${API_URL}/api/v1/auth/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: 'secret1' }),
    });
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.token).toBeDefined();
    expect(data.expires_in).toBeGreaterThan(0);
  });

  test('auth verify with wrong password returns 401', async () => {
    const res = await fetch(`${API_URL}/api/v1/auth/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: 'wrongpassword' }),
    });
    expect(res.status).toBe(401);
  });

  test('events list requires auth', async () => {
    const res = await fetch(`${API_URL}/api/v1/events`);
    expect(res.status).toBe(401);
  });

  test('events list with auth returns array', async () => {
    // Get token
    const authRes = await fetch(`${API_URL}/api/v1/auth/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: 'secret1' }),
    });
    const { token } = await authRes.json();

    const res = await fetch(`${API_URL}/api/v1/events`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    expect(res.status).toBe(200);
    const data = await res.json();
    expect(data.events).toBeDefined();
    expect(Array.isArray(data.events)).toBe(true);
  });
});

test.describe('Mobile Viewport', () => {
  test('375px width renders without horizontal overflow', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(`${BASE_URL}/timeline`);
    const scrollWidth = await page.evaluate(() => document.body.scrollWidth);
    const clientWidth = await page.evaluate(() => document.body.clientWidth);
    expect(scrollWidth).toBeLessThanOrEqual(clientWidth);
  });
});
