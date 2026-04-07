/**
 * Logger com suporte a diferentes níveis
 * Escreve no console do VS Code + arquivo de log
 */

import { appendFileSync, mkdirSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

export class Logger {
    private name: string;
    private level: number;
    private logPath: string;

    private static readonly LEVELS: Record<string, number> = {
        off: 0,
        error: 1,
        warn: 2,
        info: 3,
        debug: 4,
    };

    constructor(name: string, level: string = 'info') {
        this.name = name;
        this.level = Logger.LEVELS[level] || 3;

        // Setup log file path
        const logDir = join(homedir(), '.claw', 'logs');
        mkdirSync(logDir, { recursive: true });
        this.logPath = join(logDir, `vscode-${new Date().toISOString().split('T')[0]}.log`);
    }

    private log(levelName: string, message: string): void {
        if (Logger.LEVELS[levelName] > this.level) {
            return;
        }

        const timestamp = new Date().toISOString();
        const fullMessage = `[${timestamp}] [${this.name}] [${levelName.toUpperCase()}] ${message}`;

        // Console do VS Code
        console.log(fullMessage);

        // Arquivo de log
        try {
            appendFileSync(this.logPath, fullMessage + '\n');
        } catch (e) {
            // Ignorar erro de escrita
        }
    }

    debug(message: string): void {
        this.log('debug', message);
    }

    info(message: string): void {
        this.log('info', message);
    }

    warn(message: string): void {
        this.log('warn', message);
    }

    error(message: string): void {
        this.log('error', message);
    }
}
