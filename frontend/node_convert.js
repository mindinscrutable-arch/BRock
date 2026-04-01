const fs = require('fs');
const HTMLtoJSX = require('htmltojsx');

const html = fs.readFileSync('../finalindex.html', 'utf-8');
const bodyMatch = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
let bodyHtml = bodyMatch ? bodyMatch[1] : html;

// Remove script tags and comments
bodyHtml = bodyHtml.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
bodyHtml = bodyHtml.replace(/<!--[\s\S]*?-->/g, '');
// For some reason htmltojsx might fail on some complex things, we will just use it and see
const converter = new HTMLtoJSX({
  createClass: false
});

let jsxOutput = converter.convert(bodyHtml);
// Remove window quotes from event bindings manually just in case
jsxOutput = jsxOutput.replace(/onClick="selectDemoTab\((\d+)\)"/g, 'onClick={() => window.selectDemoTab($1)}');
jsxOutput = jsxOutput.replace(/onClick="executeDemoScenario\(\)"/g, 'onClick={() => window.executeDemoScenario()}');
jsxOutput = jsxOutput.replace(/onClick="replayDemo\(\)"/g, 'onClick={() => window.replayDemo()}');

const finalComponent = `import React, { useEffect } from 'react';
import { useMigrationDemo } from '../hooks/useMigrationDemo';

export default function LandingPage() {
  useMigrationDemo();

  return (
    <>
      ${jsxOutput}
    </>
  );
}
`;

fs.writeFileSync('src/pages/LandingPage.jsx', finalComponent, 'utf-8');
console.log('Successfully generated LandingPage.jsx');
