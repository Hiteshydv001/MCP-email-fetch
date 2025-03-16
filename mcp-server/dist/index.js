import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import axios from 'axios';
// Suppress all console output
console.log = () => { };
console.error = () => { };
const server = new McpServer({
    name: 'email-assistant',
    description: 'MCP server for email management with Claude',
    version: '1.0.0'
});
const api = axios.create({ baseURL: 'http://localhost:5000/api' });
// Tool to fetch all emails
server.tool('get_emails', {}, async () => {
    try {
        const response = await api.get('/emails');
        return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
    }
    catch (error) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: error.message }) }] };
    }
});
// Tool to fetch dashboard stats
server.tool('get_dashboard', {}, async () => {
    try {
        const response = await api.get('/dashboard');
        return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
    }
    catch (error) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: error.message }) }] };
    }
});
// Tool to send a reply
server.tool('send_reply', { email_id: z.string(), thread_id: z.string() }, async ({ email_id, thread_id }) => {
    try {
        const response = await api.post('/reply', { email_id, thread_id });
        return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
    }
    catch (error) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: error.message }) }] };
    }
});
// Tool to fetch a thread
server.tool('get_thread', { thread_id: z.string() }, async ({ thread_id }) => {
    try {
        const response = await api.get(`/thread?thread_id=${thread_id}`);
        return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
    }
    catch (error) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: error.message }) }] };
    }
});
// Start server with stdio transport
const transport = new StdioServerTransport();
(async () => {
    await server.connect(transport);
})();
