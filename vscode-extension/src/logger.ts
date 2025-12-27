/**
 * Logging utility for Elefante Grounding Extension
 */

import * as vscode from 'vscode';

let outputChannel: vscode.OutputChannel | undefined;

export function initLogger(): vscode.OutputChannel {
    if (!outputChannel) {
        outputChannel = vscode.window.createOutputChannel('Elefante Grounding');
    }
    return outputChannel;
}

export function log(message: string, level: 'INFO' | 'WARN' | 'ERROR' | 'DEBUG' = 'INFO'): void {
    const timestamp = new Date().toISOString();
    const formatted = `[${timestamp}] [${level}] ${message}`;
    
    if (outputChannel) {
        outputChannel.appendLine(formatted);
    }
    
    // Also log to console for debugging
    if (level === 'ERROR') {
        console.error(formatted);
    } else if (level === 'WARN') {
        console.warn(formatted);
    } else {
        console.log(formatted);
    }
}

export function logInfo(message: string): void {
    log(message, 'INFO');
}

export function logWarn(message: string): void {
    log(message, 'WARN');
}

export function logError(message: string, error?: Error): void {
    if (error) {
        log(`${message}: ${error.message}`, 'ERROR');
        if (error.stack) {
            log(error.stack, 'ERROR');
        }
    } else {
        log(message, 'ERROR');
    }
}

export function logDebug(message: string): void {
    log(message, 'DEBUG');
}

export function showOutputChannel(): void {
    outputChannel?.show();
}
