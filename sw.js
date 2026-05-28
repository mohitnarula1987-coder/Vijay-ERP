// Vijay ERP — minimal service worker
// Purpose: make the app installable (Add to Home Screen) WITHOUT caching,
// so every GitHub push updates the live app immediately (no stale screens).
self.addEventListener('install', function (e) { self.skipWaiting(); });
self.addEventListener('activate', function (e) { self.clients.claim(); });
self.addEventListener('fetch', function (event) {
  // Pass-through: let the browser fetch normally. No caching = always fresh.
});
