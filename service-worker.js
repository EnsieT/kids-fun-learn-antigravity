const CACHE_NAME = 'kids-fun-learn-v1';
const ASSETS = [
  './',
  './index.html',
  './css/style.css',
  './css/home.css',
  './js/common.js',
  './js/home.js',
  'https://fonts.googleapis.com/css2?family=Baloo+2:wght@400;700;800;900&family=Noto+Sans+Devanagari:wght@400;700;900&display=swap'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
