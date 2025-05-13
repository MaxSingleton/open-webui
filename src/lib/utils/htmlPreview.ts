export interface PreviewBlock {
  /** 'iframe' for HTML/CSS/JS previews, 'svg' for raw SVG content */
  type: 'iframe' | 'svg';
  /** The full HTML document (for iframe) or SVG markup */
  content: string;
}

/**
 * Extracts previewable HTML/CSS/JS or SVG blocks from a sequence of chat messages.
 * Similar logic to Artifacts.svelte#getContents, but returns a simple list of blocks.
 */
export function extractPreviewBlocks(
  messages: Array<{ role: string; content: string }>
): PreviewBlock[] {
  const blocks: PreviewBlock[] = [];
  for (const message of messages) {
    if (message.role === 'user' || !message.content) continue;
    // Find fenced code blocks of form ```lang\n...```  
    const fenceRegex = /```[\s\S]*?```/g;
    const fences = message.content.match(fenceRegex) || [];
    // Parse each fence into lang + code
    const codeBlocks: Array<{ lang: string; code: string }> = fences.map((fence) => {
      const lines = fence.split('\n');
      const first = (lines[0] || '').replace(/^```/, '').trim().toLowerCase();
      const body = lines.slice(1).join('\n').replace(/```$/, '');
      return { lang: first, code: body };
    });
    // Also detect inline <html>, <style>, <script> blocks
    const inlineHtml = Array.from(message.content.match(/<html>[\s\S]*?<\/html>/gi) || []).map(b => b.replace(/<\/?html>/gi, ''));
    const inlineCss  = Array.from(message.content.match(/<style>[\s\S]*?<\/style>/gi) || []).map(b => b.replace(/<\/?style>/gi, ''));
    const inlineJs   = Array.from(message.content.match(/<script>[\s\S]*?<\/script>/gi) || []).map(b => b.replace(/<\/?script>/gi, ''));

    // Aggregate code by type
    let html = inlineHtml.join('\n');
    let css  = inlineCss.join('\n');
    let js   = inlineJs.join('\n');
    for (const cb of codeBlocks) {
      if (cb.lang === 'html') {
        html += cb.code + '\n';
      } else if (cb.lang === 'css') {
        css += cb.code + '\n';
      } else if (cb.lang === 'javascript' || cb.lang === 'js') {
        js += cb.code + '\n';
      } else if (cb.lang === 'svg' || (cb.lang === 'xml' && cb.code.includes('<svg'))) {
        // Raw SVG block
        blocks.push({ type: 'svg', content: cb.code });
      }
    }
    // If we have any HTML/CSS/JS, wrap into a full document
    if (html.trim() || css.trim() || js.trim()) {
      const doc = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    body { margin:0; padding:0; background:white; }
    ${css}
  </style>
</head>
<body>
  ${html}
  <script>
    ${js}
  </script>
</body>
</html>`;
      blocks.push({ type: 'iframe', content: doc });
    }
  }
  return blocks;
}