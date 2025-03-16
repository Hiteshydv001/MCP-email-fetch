import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import axios from 'axios';

console.log = () => {};
console.error = () => {};

const server = new McpServer({
  name: 'email-assistant',
  description: 'MCP server for email management with Claude',
  version: '1.0.0'
});

const api = axios.create({ baseURL: 'http://localhost:5000/api' });

server.tool(
  'get_emails',
  {},
  async () => {
    try {
      const response = await api.get('/emails');
      if (!response.data) throw new Error("No data returned from /emails");
      return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
    } catch (error) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: (error as Error).message }) }] };
    }
  }
);

server.tool(
  'get_thread',
  { thread_id: z.string() },
  async ({ thread_id }) => {
    try {
      const response = await api.get(`/thread?thread_id=${thread_id}`);
      return { content: [{ type: 'text', text: JSON.stringify(response.data) }] };
    } catch (error) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: (error as Error).message }) }] };
    }
  }
);

server.tool(
  'send_reply',
  { 
    email_id: z.string(), 
    thread_id: z.string(), 
    reply_text: z.string().optional()
  },
  async ({ email_id, thread_id, reply_text }) => {
    try {
      const response = await api.post('/reply', { email_id, thread_id, reply_text });
      const data = response.data;
      if (!data.success) {
        return { 
          content: [{ 
            type: 'text', 
            text: JSON.stringify({
              message: "Please choose a reply option: positive, neutral, or negative",
              options: data.reply_options,
              action: `Use send_reply with email_id '${email_id}', thread_id '${thread_id}', and reply_text '[chosen reply]'`
            })
          }]
        };
      }
      return { content: [{ type: 'text', text: JSON.stringify(data) }] };
    } catch (error) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: (error as Error).message }) }] };
    }
  }
);

const transport = new StdioServerTransport();
(async () => {
  await server.connect(transport);
})();