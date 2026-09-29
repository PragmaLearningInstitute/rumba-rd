import { COMMON_WORDS } from 'public/commonWords';

export const ALLOWED_FONTS = ['Avenir Next', 'Arial', 'OpenDyslexic'];
export const ALLOWED_SIZES = [11, 12, 13, 14, 15];

const WORD_RE = /[A-Za-zÀ-ÖØ-öø-ÿ'’\-]+/g;
const TOKEN_RE = /[A-Za-zÀ-ÖØ-öø-ÿ'’\-]+|\s+|[^\s]/gu;
const VOWELS = 'aeiouyàâäæéèêëîïôœùûüÿ';

function mulberry32(seed) {
  let t = seed >>> 0;
  return function rng() {
    t += 0x6d2b79f5;
    let x = Math.imul(t ^ (t >>> 15), 1 | t);
    x ^= x + Math.imul(x ^ (x >>> 7), 61 | x);
    return ((x ^ (x >>> 14)) >>> 0) / 4294967296;
  };
}

function gaussRandom(rng) {
  let u = 0;
  let v = 0;
  while (u === 0) u = rng();
  while (v === 0) v = rng();
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(2.0 * Math.PI * v);
}

function normalizeToken(token) {
  return token.toLowerCase().replace(/[’]/g, "'").replace(/^['’-]+|['’-]+$/g, '');
}

function tokenizeWords(text) {
  const matches = text.match(WORD_RE);
  return matches || [];
}

function countSyllables(word) {
  const cleaned = word.toLowerCase().replace(/[^a-zàâäæéèêëîïôœùûüÿ]/g, '');
  if (!cleaned) return 1;
  const groups = cleaned.match(/[aeiouyàâäæéèêëîïôœùûüÿ]+/g) || [];
  return Math.max(1, groups.length);
}

function detectLanguage(text) {
  const words = tokenizeWords(text).map(normalizeToken);
  if (words.length === 0) return 'fr';

  const frMarkers = new Set(['le', 'la', 'les', 'des', 'que', 'qui', 'dans', 'pour', 'avec', 'une', 'est', 'pas', 'vous', 'nous', 'sur']);
  const enMarkers = new Set(['the', 'and', 'that', 'with', 'for', 'you', 'your', 'this', 'from', 'have', 'are', 'was', 'were', 'they', 'their']);

  let frCount = 0;
  let enCount = 0;
  for (const w of words) {
    if (frMarkers.has(w)) frCount += 1;
    if (enMarkers.has(w)) enCount += 1;
  }
  return enCount > frCount ? 'en' : 'fr';
}

export function fleschReadingEase(text, language = 'auto') {
  const sentences = text.split(/[.!?]+/).map((s) => s.trim()).filter(Boolean);
  const words = tokenizeWords(text);

  const wordCount = Math.max(1, words.length);
  const sentenceCount = Math.max(1, sentences.length);
  let syllableCount = 0;
  for (const w of words) syllableCount += countSyllables(w);

  const asl = wordCount / sentenceCount;
  const asw = syllableCount / wordCount;

  const lang = language === 'auto' ? detectLanguage(text) : language;
  const score = lang === 'fr'
    ? 207.0 - 1.015 * asl - 73.6 * asw
    : 206.835 - 1.015 * asl - 84.6 * asw;

  return {
    score: Number(score.toFixed(2)),
    asl,
    asw,
    language: lang,
  };
}

export function zipfCommonRatio(text) {
  const allowed = new Set(COMMON_WORDS);
  const tokens = tokenizeWords(text).map(normalizeToken);
  if (!tokens.length) {
    return { ratio: 1, commonCount: 0, totalWords: 0 };
  }
  let commonCount = 0;
  for (const t of tokens) {
    if (allowed.has(t)) commonCount += 1;
  }
  return {
    ratio: commonCount / tokens.length,
    commonCount,
    totalWords: tokens.length,
  };
}

function isVowel(ch) {
  return VOWELS.includes(ch.toLowerCase());
}

function splitWordSyllables(word) {
  const letters = [...word];
  if (letters.length <= 3) return [word];

  const chunks = [];
  let current = letters[0];

  for (let i = 1; i < letters.length; i += 1) {
    const prev = letters[i - 1];
    const curr = letters[i];
    const nxt = i + 1 < letters.length ? letters[i + 1] : '';

    let boundary = false;
    if (isVowel(prev) && !isVowel(curr) && nxt && isVowel(nxt)) {
      boundary = true;
    } else if (!isVowel(prev) && isVowel(curr) && current.length >= 2) {
      boundary = true;
    }

    if (boundary) {
      chunks.push(current);
      current = curr;
    } else {
      current += curr;
    }
  }

  chunks.push(current);
  return chunks.filter(Boolean);
}

function brownianBlockSizes(totalSyllables, rng, bMin = 4, bMax = 11, b0 = 7, sigma = 1.3) {
  if (totalSyllables <= 0) return [];

  const clamp = (v) => Math.max(bMin, Math.min(bMax, v));
  const sizes = [];
  let current = clamp(b0);
  let consumed = 0;

  while (consumed < totalSyllables) {
    const remaining = totalSyllables - consumed;
    if (remaining <= bMax) {
      sizes.push(Math.max(1, remaining));
      break;
    }

    const size = Math.min(current, remaining);
    sizes.push(size);
    consumed += size;

    const epsilon = Math.round(gaussRandom(rng) * sigma);
    current = clamp(current + epsilon);
  }

  return sizes;
}

function gaussianWeight(u, sigmaLeft, sigmaRight) {
  const sigma = u >= 0 ? sigmaRight : sigmaLeft;
  return Math.exp(-((u * u) / (2 * sigma * sigma)));
}

function escapeHtml(value) {
  return value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

function syllableEntries(text) {
  const rawTokens = text.match(TOKEN_RE) || [];
  const syllables = [];
  const syllCountPerToken = new Array(rawTokens.length).fill(0);

  rawTokens.forEach((token, idx) => {
    if (token.match(/^[A-Za-zÀ-ÖØ-öø-ÿ'’\-]+$/u)) {
      const parts = splitWordSyllables(token);
      const use = parts.length ? parts : [token];
      syllCountPerToken[idx] = use.length;
      for (const part of use) {
        syllables.push({ tokenIdx: idx, text: part });
      }
    }
  });

  return { syllables, rawTokens, syllCountPerToken };
}

function formatTextBrownian(text, options = {}) {
  const {
    seed = 42,
    bMin = 4,
    bMax = 11,
    b0 = 7,
    sigmaBlock = 1.3,
    sigmaLeft = 2.4,
    sigmaRight = 3.7,
    tau0 = 0.14,
  } = options;

  if (!text || !text.trim()) {
    return { markdownText: '', htmlText: '' };
  }

  const rng = mulberry32(seed);
  const { syllables, rawTokens, syllCountPerToken } = syllableEntries(text);
  if (!syllables.length) {
    const esc = escapeHtml(text);
    return { markdownText: text, htmlText: `<p>${esc}</p>` };
  }

  const blockSizes = brownianBlockSizes(syllables.length, rng, bMin, bMax, b0, sigmaBlock);
  const blockMap = [];
  blockSizes.forEach((size, blockId) => {
    for (let i = 0; i < size; i += 1) blockMap.push(blockId);
  });
  while (blockMap.length < syllables.length) blockMap.push(blockSizes.length - 1);

  const blockStarts = [];
  let acc = 0;
  for (const size of blockSizes) {
    blockStarts.push(acc);
    acc += size;
  }

  const styledMd = [];
  const styledHtml = [];
  const blockMean = (bMin + bMax) / 2;

  for (let k = 0; k < syllables.length; k += 1) {
    const blockId = blockMap[k];
    const blockSize = blockSizes[blockId];
    const localPos = k - blockStarts[blockId];

    const u = blockSize <= 1 ? 0 : (2 * localPos / (blockSize - 1)) - 1;
    const weight = gaussianWeight(u, sigmaLeft, sigmaRight);

    const tauI = Math.min(0.98, tau0 * blockSize);
    const cadence = blockSize >= blockMean ? 3 : 2;
    const cadenceHit = localPos % cadence === 0;
    const centerWindow = Math.abs(u) <= (cadence === 3 ? 0.42 : 0.52);

    const makeBold = (weight > tauI) || (cadenceHit && centerWindow && weight > (tauI * 0.92));
    const txt = syllables[k].text;

    if (makeBold) {
      styledMd.push(`**${txt}**`);
      styledHtml.push(`<strong>${escapeHtml(txt)}</strong>`);
    } else {
      styledMd.push(txt);
      styledHtml.push(escapeHtml(txt));
    }
  }

  const tokenToMd = new Map();
  const tokenToHtml = new Map();

  syllables.forEach((item, i) => {
    if (!tokenToMd.has(item.tokenIdx)) {
      tokenToMd.set(item.tokenIdx, []);
      tokenToHtml.set(item.tokenIdx, []);
    }
    tokenToMd.get(item.tokenIdx).push(styledMd[i]);
    tokenToHtml.get(item.tokenIdx).push(styledHtml[i]);
  });

  const outMdParts = [];
  const outHtmlParts = [];

  rawTokens.forEach((token, idx) => {
    if (syllCountPerToken[idx] > 0) {
      outMdParts.push(tokenToMd.get(idx).join(''));
      outHtmlParts.push(tokenToHtml.get(idx).join(''));
    } else {
      outMdParts.push(token);
      outHtmlParts.push(escapeHtml(token));
    }
  });

  const markdownText = outMdParts.join('');
  const htmlText = `<p>${outHtmlParts.join('').replaceAll('\n', '<br>')}</p>`;

  return { markdownText, htmlText };
}

function normalizeFont(value) {
  return ALLOWED_FONTS.includes(value) ? value : 'Arial';
}

function normalizeSize(value) {
  return ALLOWED_SIZES.includes(value) ? value : 13;
}

export function formatForDyslexia({
  text,
  seed = 42,
  targetMin = 74,
  targetMax = 82,
  fontFamily = 'Arial',
  fontSize = 13,
} = {}) {
  const safeText = text || '';
  const readability = fleschReadingEase(safeText, 'auto');
  const zipf = zipfCommonRatio(safeText);

  let b0 = 7;
  if (readability.score < targetMin) b0 = 6;
  else if (readability.score > targetMax) b0 = 8;

  const { markdownText, htmlText } = formatTextBrownian(safeText, { seed, b0 });

  const safeFont = normalizeFont(fontFamily);
  const safeSize = normalizeSize(fontSize);

  return {
    markdownText,
    htmlText,
    styledHtml: `<div style="font-family:'${safeFont}',Arial,sans-serif;font-size:${safeSize}pt;line-height:1.5;font-weight:400;">${htmlText}</div>`,
    metrics: {
      language: readability.language,
      fleschScore: readability.score,
      asl: readability.asl,
      asw: readability.asw,
      zipfCommonRatio: zipf.ratio,
      commonWordsCount: zipf.commonCount,
      totalWords: zipf.totalWords,
    },
  };
}
