# Pack Wix Velo - Rumba Reader

## Fichiers

- `public/commonWords.js`
- `public/readerCore.js`
- `backend/readerEngine.jsw`
- `page_code/readerPage.js`

## IDs Wix attendus

- `#inputText` (TextInput multiline)
- `#fontDropdown` (Dropdown)
- `#sizeDropdown` (Dropdown)
- `#formatButton` (Button)
- `#outputRich` (RichText)
- `#markdownOutput` (TextBox multiline, optionnel)
- `#metricsText` (Text)

## Contraintes appliquées

- Police de sortie: `Avenir Next`, `Arial`, `OpenDyslexic`
- Taille de sortie: `11`, `12`, `13`, `14`, `15`
- Interligne: `1.5` (fixe)

## API principale

```js
import { formatForDyslexia } from 'public/readerCore';

const result = formatForDyslexia({
  text,
  fontFamily: 'Arial',
  fontSize: 13,
  seed: 42,
  targetMin: 74,
  targetMax: 82,
});
```

Retour:

- `result.styledHtml`
- `result.markdownText`
- `result.metrics`
