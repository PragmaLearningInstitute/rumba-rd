import { formatForDyslexia, ALLOWED_FONTS, ALLOWED_SIZES } from 'public/readerCore';

$w.onReady(() => {
  $w('#fontDropdown').options = ALLOWED_FONTS.map((font) => ({ label: font, value: font }));
  $w('#sizeDropdown').options = ALLOWED_SIZES.map((size) => ({ label: String(size), value: String(size) }));

  $w('#fontDropdown').value = 'Arial';
  $w('#sizeDropdown').value = '13';

  $w('#formatButton').onClick(() => {
    const text = ($w('#inputText').value || '').trim();
    if (!text) {
      $w('#metricsText').text = 'Collez un texte avant de lancer le formatage.';
      return;
    }

    const fontFamily = $w('#fontDropdown').value;
    const fontSize = Number($w('#sizeDropdown').value);

    const result = formatForDyslexia({
      text,
      fontFamily,
      fontSize,
      seed: 42,
      targetMin: 74,
      targetMax: 82,
    });

    // Rich text element required
    $w('#outputRich').html = result.styledHtml;
    $w('#markdownOutput').value = result.markdownText;

    $w('#metricsText').text =
      `FRE: ${result.metrics.fleschScore} | Mots communs: ${(result.metrics.zipfCommonRatio * 100).toFixed(1)}% | Langue: ${result.metrics.language.toUpperCase()}`;
  });
});
