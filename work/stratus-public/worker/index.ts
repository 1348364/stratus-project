import handler from "vinext/server/fetch-handler";
import { runWithConnectorBinding } from "../lib/connector-context";
import type { ConnectorBinding } from "../lib/connector-contract.mjs";
import { deliverFeedback, serverMailEnabled } from "../lib/feedback-mail";

const worker = {
  fetch(request: Request, env: Cloudflare.Env, ctx: ExecutionContext<{ CONNECTORS?: ConnectorBinding }>) {
    let binding = ctx.props?.CONNECTORS;
    // Local preview emulates the same request-scoped capability. This branch and
    // the auxiliary service binding are absent from production builds.
    if (import.meta.env.DEV && !binding && env.CONNECTORS) {
      const preview = env.CONNECTORS;
      const expiresAt = Date.now() + 60_000;
      binding = {
        async getContext() {
          if (Date.now() >= expiresAt) return { status: "request_context_expired" };
          return preview.getContext?.() ?? { status: "binding_unavailable" };
        },
        async invoke(connectorId, actionName, args) {
          if (Date.now() >= expiresAt) {
            return { status: "request_context_expired", message: "This request has expired. Please try again." };
          }
          return preview.invoke(connectorId, actionName, args);
        },
      };
    }
    const response = runWithConnectorBinding(binding, () => handler.fetch(request, env, ctx));
    const path = new URL(request.url).pathname;
    if (serverMailEnabled(env as any) &&
        ((request.method === 'POST' && path === '/api/feedback') ||
         (request.method === 'GET' && ['/api/release', '/api/updates'].includes(path)))) {
      // After the submission commits; delivery continues after returning the page/form response.
      // Public feed refreshes also retry saved records while visitors have the site open.
      ctx.waitUntil(Promise.resolve(response).then(() => deliverFeedback(env as any))
        .catch(() => console.warn('Feedback queue retained; delivery needs another attempt.')));
    }
    return response;
  },
};

export default worker;
