/**
 * Elefante Grounding Extension
 * 
 * Automatically injects relevant memories from Elefante into AI chat context.
 * 
 * Architecture:
 * 1. Registers a ChatParticipant that intercepts chat requests
 * 2. For each request, searches Elefante for relevant memories
 * 3. Injects found memories into the prompt context
 * 4. The AI then sees both the context and the user's message
 */

import * as vscode from 'vscode';
import { initLogger, logInfo, logError, showOutputChannel } from './logger';
import { getGroundingService, disposeGroundingService } from './grounding';

export function activate(context: vscode.ExtensionContext) {
    // Initialize logger
    const outputChannel = initLogger();
    context.subscriptions.push(outputChannel);

    logInfo('Elefante Grounding extension activating...');

    // Get grounding service
    const groundingService = getGroundingService();

    // Register chat participant
    // This is the key integration point with VS Code's chat API
    const participant = vscode.chat.createChatParticipant('elefante.grounding', async (request, context, response, token) => {
        // The user invoked @elefante directly
        // We'll search for relevant memories and display them
        
        logInfo(`Chat request received: "${request.prompt.substring(0, 50)}..."`);

        try {
            // Ground the message
            const groundedContext = await groundingService.ground(request.prompt);

            if (groundedContext) {
                response.markdown('**Elefante Context Loaded**\n\n');
                response.markdown(groundedContext);
                response.markdown('\n---\n\n');
            } else {
                response.markdown('*No relevant memories found in Elefante.*\n\n');
            }

            // Forward to the default chat handler
            response.markdown('_Forwarding your question with context..._');

        } catch (error) {
            logError('Chat participant error', error instanceof Error ? error : new Error(String(error)));
            response.markdown('*Error loading Elefante context. Proceeding without grounding.*');
        }
    });

    participant.iconPath = vscode.Uri.joinPath(context.extensionUri, 'icon.png');
    context.subscriptions.push(participant);

    // Register commands
    context.subscriptions.push(
        vscode.commands.registerCommand('elefante.grounding.toggle', async () => {
            const newState = await groundingService.toggle();
            vscode.window.showInformationMessage(
                `Elefante Grounding ${newState ? 'enabled' : 'disabled'}`
            );
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('elefante.grounding.clearCache', () => {
            groundingService.clearCache();
            vscode.window.showInformationMessage('Elefante cache cleared');
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('elefante.grounding.testConnection', async () => {
            const available = await groundingService.testConnection();
            if (available) {
                vscode.window.showInformationMessage('✓ Elefante server is available');
            } else {
                vscode.window.showWarningMessage(
                    '✗ Cannot reach Elefante server. Check that the MCP server is running.'
                );
            }
        })
    );

    context.subscriptions.push(
        vscode.commands.registerCommand('elefante.grounding.showLogs', () => {
            showOutputChannel();
        })
    );

    logInfo('Elefante Grounding extension activated');
}

export function deactivate() {
    logInfo('Elefante Grounding extension deactivating...');
    disposeGroundingService();
}
