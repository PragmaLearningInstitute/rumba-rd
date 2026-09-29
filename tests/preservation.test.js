import test from 'node:test';
import assert from 'node:assert/strict';
import { gaussReformulator } from '../web/rumbaEngine.js';
test('formatting preserves digits, underscores, Unicode and escaped markup', () => {
 const text = "123_45 € 漢字 😀 <script>alert(1)</script> & lecture";
 const result = gaussReformulator(text);
 assert.equal(result.plainText, text);
 const restored = result.htmlText.replace(/<strong>|<\/strong>|<p>|<\/p>/g, '').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#x27;|&#39;/g, "'").replace(/&quot;/g, '"').replace(/&amp;/g, '&');
 assert.equal(restored, text);
 assert.ok(!result.htmlText.includes('<script>'));
});
