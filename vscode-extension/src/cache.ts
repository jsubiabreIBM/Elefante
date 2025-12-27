/**
 * Simple in-memory cache with TTL support
 */

import { CacheEntry, MemoryResult } from './types';
import { logDebug } from './logger';

export class SearchCache {
    private cache: Map<string, CacheEntry<MemoryResult[]>> = new Map();
    private defaultTtlMs: number;

    constructor(defaultTtlSeconds: number = 300) {
        this.defaultTtlMs = defaultTtlSeconds * 1000;
    }

    /**
     * Generate a cache key from query string
     * Normalizes the query to improve cache hit rate
     */
    private generateKey(query: string): string {
        return query.toLowerCase().trim();
    }

    /**
     * Get cached results if they exist and haven't expired
     */
    get(query: string): MemoryResult[] | undefined {
        const key = this.generateKey(query);
        const entry = this.cache.get(key);

        if (!entry) {
            return undefined;
        }

        if (Date.now() > entry.expiresAt) {
            // Entry has expired, remove it
            this.cache.delete(key);
            logDebug(`Cache expired for query: "${query.substring(0, 50)}..."`);
            return undefined;
        }

        logDebug(`Cache hit for query: "${query.substring(0, 50)}..."`);
        return entry.value;
    }

    /**
     * Store results in cache with optional custom TTL
     */
    set(query: string, results: MemoryResult[], ttlMs?: number): void {
        const key = this.generateKey(query);
        const expiresAt = Date.now() + (ttlMs ?? this.defaultTtlMs);

        this.cache.set(key, {
            value: results,
            expiresAt,
        });

        logDebug(`Cached ${results.length} results for query: "${query.substring(0, 50)}..."`);
    }

    /**
     * Clear all cached entries
     */
    clear(): void {
        const size = this.cache.size;
        this.cache.clear();
        logDebug(`Cleared ${size} cached entries`);
    }

    /**
     * Remove expired entries (call periodically for memory management)
     */
    prune(): number {
        const now = Date.now();
        let pruned = 0;

        for (const [key, entry] of this.cache.entries()) {
            if (now > entry.expiresAt) {
                this.cache.delete(key);
                pruned++;
            }
        }

        if (pruned > 0) {
            logDebug(`Pruned ${pruned} expired cache entries`);
        }

        return pruned;
    }

    /**
     * Get current cache size
     */
    get size(): number {
        return this.cache.size;
    }

    /**
     * Update default TTL
     */
    setDefaultTtl(ttlSeconds: number): void {
        this.defaultTtlMs = ttlSeconds * 1000;
    }
}
