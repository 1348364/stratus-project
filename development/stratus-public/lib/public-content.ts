// Release feeds contain approved showcase copy, never feedback or owner configuration.
export function containsPrivateContent(value: unknown, env: Record<string, any>) {
  const text = JSON.stringify(value) || '';
  if (/[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\/(?:Users|home|private|var\/folders)\/|[A-Z]:\\Users\\|(?:re_|ghp_|sk-)[A-Za-z0-9_-]{20,}|-----BEGIN [^-]*PRIVATE KEY-----/i.test(text)) return true;
  const lower = text.toLowerCase();
  return [env.STUDIO_OWNER_EMAIL, env.STUDIO_OWNER_NAME, env.STUDIO_URL]
    .filter((s): s is string => typeof s === 'string' && s.length > 3)
    .some(s => lower.includes(s.toLowerCase().replace(/\/#home$/, '')));
}
