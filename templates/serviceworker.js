// Cache CSS and javaScript assets with a stale-while-revalidate strategy.
routing.registerRoute(
    ({request}) => request.destination === 'script' ||
        request.destination === 'style',
    new strategies.StaleWhileRevalidate({
        cacheName: 'static-resources',
    })
);

// Cache image files with a cache-first strategy for 30 days.
routing.registerRoute(
    ({request}) => request.destination === 'image',
    new strategies.CacheFirst({
        cacheName: 'images',
        plugins: [
            new expiration.ExpirationPlugin({
                maxEntries: 60,
                maxAgeSeconds: 30 * 24 * 60 * 60,
            }),
        ],
    })
);
