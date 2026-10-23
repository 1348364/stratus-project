// Server-only delivery. No credentials, recipients or visitor feedback reach the browser.
type MailEnv = { DB: D1Database; RESEND_API_KEY?: string; FEEDBACK_TO?: string; FEEDBACK_FROM?: string; FEEDBACK_DELIVERY?: string };
const email = /^[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+$/;
export function serverMailEnabled(env: MailEnv) {
  return env.FEEDBACK_DELIVERY === 'server' && !!env.RESEND_API_KEY && email.test(env.FEEDBACK_TO || '');
}

export async function deliverFeedback(env: MailEnv) {
  if (!serverMailEnabled(env)) return;
  // A request can drain three records. Other visitors/workers use the same durable leases.
  for (let i = 0; i < 3; i++) {
    const now = Date.now(), lease = now + 60_000;
    const row: any = await env.DB.prepare(`UPDATE feedback SET status='cloud-sending',mail_lease=?,
      mail_attempts=mail_attempts+1 WHERE id=(SELECT id FROM feedback
      WHERE status IN ('pending','cloud-pending','cloud-retry','cloud-sending')
      AND mail_next<=? AND mail_lease<=? ORDER BY created LIMIT 1)
      RETURNING *`).bind(lease, now, now).first();
    if (!row) return;
    const update = (sql: string, ...args: any[]) => env.DB.prepare(sql + ' WHERE id=? AND mail_lease=?')
      .bind(...args, row.id, lease).run();
    // Resend retains idempotency keys for 24 hours. Never replay an old uncertain send.
    if (row.mail_first && now - row.mail_first >= 23 * 60 * 60 * 1000) {
      await update("UPDATE feedback SET status='unknown',mail_error=?,mail_lease=0", 'Delivery window expired; inspect provider receipts before retrying.');
      continue;
    }
    const payload = row.mail_payload || JSON.stringify({
      from: env.FEEDBACK_FROM || 'Stratus feedback <onboarding@resend.dev>',
      to: [env.FEEDBACK_TO],
      subject: `[Stratus feedback ${row.id}] ${row.topic}`,
      text: `Stratus public feedback\n\nTopic: ${row.topic}\nSubmitted: ${row.created}\n\n${row.message}\n\nOptional reply address: ${row.reply || 'not provided'}\n\nVisitor feedback only. No shader or website changes were triggered.`,
    });
    // Freeze the exact request before contacting the provider, including its private target.
    await update('UPDATE feedback SET mail_payload=?,mail_first=?', payload, row.mail_first || now);
    let failure = 'Network response unconfirmed', delay = Math.min(3_600_000, 60_000 * 2 ** Math.min(row.mail_attempts, 6));
    let accepted = false;
    try {
      const response = await fetch('https://api.resend.com/emails', {
        method: 'POST', headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`,
          'Content-Type': 'application/json', 'Idempotency-Key': `stratus-feedback/${row.id}` },
        body: payload, signal: AbortSignal.timeout(12_000),
      });
      if (response.ok) {
        const result: any = await response.json();
        if (typeof result.id === 'string' && /^[a-f0-9-]{36}$/.test(result.id)) {
          // Keep database failures outside transport retries: replaying this same key is safe.
          await update("UPDATE feedback SET status='sent',receipt=?,mail_error=NULL,mail_lease=0", `resend:${result.id}`);
          accepted = true;
        } else failure = 'Provider receipt unconfirmed';
      } else {
        // Do not log provider bodies: they may include private addresses or feedback.
        failure = `Provider HTTP ${response.status}`;
        const retry = Number(response.headers.get('Retry-After'));
        if (Number.isFinite(retry) && retry > 0) delay = Math.max(delay, Math.min(retry * 1000, 3_600_000));
        if (response.status === 401 || response.status === 403 || response.status === 422) delay = 3_600_000;
      }
    } catch { /* Same durable payload/key may be retried within the safety window. */ }
    if (!accepted) {
      await update("UPDATE feedback SET status='cloud-retry',mail_error=?,mail_next=?,mail_lease=0", failure, now + delay);
      // Avoid hammering an unavailable provider for the remaining queue.
      return;
    }
  }
}
