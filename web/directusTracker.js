const DIRECTUS_URL = (typeof window !== "undefined" && window.PLI_DIRECTUS_URL) || "";

let sessionId = null;

function createSessionId() {
  if (globalThis.crypto && typeof globalThis.crypto.randomUUID === "function") {
    return globalThis.crypto.randomUUID();
  }

  const bytes = new Uint8Array(16);
  if (globalThis.crypto && typeof globalThis.crypto.getRandomValues === "function") {
    globalThis.crypto.getRandomValues(bytes);
  } else {
    for (let i = 0; i < bytes.length; i += 1) {
      bytes[i] = Math.floor(Math.random() * 256);
    }
  }

  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  const hex = Array.from(bytes, (byte) => byte.toString(16).padStart(2, "0"));
  return `${hex.slice(0, 4).join("")}-${hex.slice(4, 6).join("")}-${hex.slice(6, 8).join("")}-${hex.slice(8, 10).join("")}-${hex.slice(10, 16).join("")}`;
}

function getSessionId() {
  if (!sessionId) {
    sessionId = createSessionId();
  }
  return sessionId;
}

function nullableString(value) {
  if (value === undefined || value === null || value === "") return null;
  return String(value);
}

function nullableInteger(value) {
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) ? parsed : null;
}

function normalizeFormat(format) {
  const normalized = nullableString(format);
  return ["html", "pdf", "docx"].includes(normalized) ? normalized : null;
}

function postEvent(payload) {
  if (typeof window === "undefined" || window.RUMBA_TELEMETRY_ENABLED !== true) return;
  const baseUrl = String(DIRECTUS_URL || "").replace(/\/+$/, "");
  if (!baseUrl) {
    console.warn("RUMBA.RD tracker: usage server URL is missing.");
    return;
  }

  fetch(`${baseUrl}/items/rumba_rd_events`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      ...payload,
      session_id: getSessionId(),
    }),
    keepalive: true,
  }).catch((error) => {
    console.warn("RUMBA.RD tracker: usage event could not be sent.", error);
  });
}

/**
 * Initializes the in-memory RUMBA.RD analytics session.
 * The generated UUID is intentionally not persisted and changes on reload.
 *
 * @returns {string} The current session UUID.
 */
export function initTracker() {
  sessionId = createSessionId();
  return sessionId;
}

/**
 * Tracks a text submission without sending any user text.
 *
 * @param {{ wordCount?: number, fontFamily?: string, fontSize?: number }} options
 * @returns {void}
 */
export function trackInput({ wordCount, fontFamily, fontSize } = {}) {
  postEvent({
    event_type: "input_submitted",
    input_word_count: nullableInteger(wordCount),
    font_family: nullableString(fontFamily),
    font_size: nullableInteger(fontSize),
    download_format: null,
  });
}

/**
 * Tracks a download action without sending any user text.
 *
 * @param {{ format?: "html" | "pdf" | "docx" | string, fontFamily?: string, fontSize?: number }} options
 * @returns {void}
 */
export function trackDownload({ format, fontFamily, fontSize } = {}) {
  postEvent({
    event_type: "download",
    input_word_count: null,
    font_family: nullableString(fontFamily),
    font_size: nullableInteger(fontSize),
    download_format: normalizeFormat(format),
  });
}
