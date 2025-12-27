/**
 * Configuration management for Elefante Grounding Extension
 */

import * as vscode from 'vscode';
import { ExtensionConfig } from './types';

const CONFIG_SECTION = 'elefante.grounding';

export function getConfig(): ExtensionConfig {
    const config = vscode.workspace.getConfiguration(CONFIG_SECTION);
    
    return {
        enabled: config.get<boolean>('enabled', true),
        serverUrl: config.get<string>('serverUrl', 'http://localhost:8000'),
        minSimilarity: config.get<number>('minSimilarity', 0.5),
        maxResults: config.get<number>('maxResults', 5),
        cacheTtlSeconds: config.get<number>('cacheTtlSeconds', 300),
        showNotifications: config.get<boolean>('showNotifications', false),
    };
}

export async function setEnabled(enabled: boolean): Promise<void> {
    const config = vscode.workspace.getConfiguration(CONFIG_SECTION);
    await config.update('enabled', enabled, vscode.ConfigurationTarget.Global);
}

export function onConfigChange(callback: (config: ExtensionConfig) => void): vscode.Disposable {
    return vscode.workspace.onDidChangeConfiguration((event) => {
        if (event.affectsConfiguration(CONFIG_SECTION)) {
            callback(getConfig());
        }
    });
}
