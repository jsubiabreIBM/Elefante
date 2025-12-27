/**
 * Grounding Service
 * 
 * Core logic for intercepting chat messages and injecting Elefante context.
 * This is the heart of the extension.
 */

import * as vscode from 'vscode';
import { ElefanteClient } from './client';
import { SearchCache } from './cache';
import { ContextFormatter } from './formatter';
import { getConfig, onConfigChange } from './config';
import { logInfo, logWarn, logError, logDebug } from './logger';
import { MemoryResult, ExtensionConfig } from './types';

export class GroundingService {
    private client: ElefanteClient;
    private cache: SearchCache;
    private formatter: ContextFormatter;
    private config: ExtensionConfig;
    private disposables: vscode.Disposable[] = [];

    constructor() {
        this.config = getConfig();
        this.client = new ElefanteClient(this.config.serverUrl);
        this.cache = new SearchCache(this.config.cacheTtlSeconds);
        this.formatter = new ContextFormatter();

        // Listen for config changes
        this.disposables.push(
            onConfigChange((newConfig) => {
                this.config = newConfig;
                this.client.setServerUrl(newConfig.serverUrl);
                this.cache.setDefaultTtl(newConfig.cacheTtlSeconds);
                logInfo('Configuration updated');
            })
        );

        // Prune cache periodically
        const pruneInterval = setInterval(() => this.cache.prune(), 60000);
        this.disposables.push({
            dispose: () => clearInterval(pruneInterval),
        });
    }

    /**
     * Ground a user message with relevant Elefante memories
     * 
     * This is the main entry point called before every chat message.
     * Returns the context to prepend, or empty string if no relevant memories.
     */
    async ground(userMessage: string): Promise<string> {
        if (!this.config.enabled) {
            logDebug('Grounding disabled');
            return '';
        }

        if (!userMessage || userMessage.trim().length === 0) {
            return '';
        }

        try {
            // Check cache first
            const cached = this.cache.get(userMessage);
            if (cached !== undefined) {
                return this.formatter.format(cached);
            }

            // Search Elefante
            const memories = await this.client.search(userMessage, {
                limit: this.config.maxResults,
                minSimilarity: this.config.minSimilarity,
                mode: 'hybrid',
            });

            // Cache the results (even if empty, to avoid repeated searches)
            this.cache.set(userMessage, memories);

            // Format and return context
            const context = this.formatter.format(memories);

            // Show notification if configured
            if (this.config.showNotifications && memories.length > 0) {
                vscode.window.showInformationMessage(
                    this.formatter.formatNotification(memories)
                );
            }

            return context;

        } catch (error) {
            logError('Grounding failed', error instanceof Error ? error : new Error(String(error)));
            // Never block the user - return empty on error
            return '';
        }
    }

    /**
     * Get memories without formatting (for inspection)
     */
    async getMemories(query: string): Promise<MemoryResult[]> {
        return this.client.search(query, {
            limit: this.config.maxResults,
            minSimilarity: this.config.minSimilarity,
            mode: 'hybrid',
        });
    }

    /**
     * Test server connection
     */
    async testConnection(): Promise<boolean> {
        return this.client.isServerAvailable();
    }

    /**
     * Toggle grounding on/off
     */
    async toggle(): Promise<boolean> {
        const newState = !this.config.enabled;
        const config = vscode.workspace.getConfiguration('elefante.grounding');
        await config.update('enabled', newState, vscode.ConfigurationTarget.Global);
        logInfo(`Grounding ${newState ? 'enabled' : 'disabled'}`);
        return newState;
    }

    /**
     * Clear the search cache
     */
    clearCache(): void {
        this.cache.clear();
    }

    /**
     * Get current status
     */
    getStatus(): { enabled: boolean; cacheSize: number; serverUrl: string } {
        return {
            enabled: this.config.enabled,
            cacheSize: this.cache.size,
            serverUrl: this.config.serverUrl,
        };
    }

    /**
     * Dispose of resources
     */
    dispose(): void {
        this.disposables.forEach(d => d.dispose());
    }
}

// Singleton instance
let groundingService: GroundingService | undefined;

export function getGroundingService(): GroundingService {
    if (!groundingService) {
        groundingService = new GroundingService();
    }
    return groundingService;
}

export function disposeGroundingService(): void {
    groundingService?.dispose();
    groundingService = undefined;
}
