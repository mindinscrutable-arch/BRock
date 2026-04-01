import React from 'react';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import json from 'react-syntax-highlighter/dist/esm/languages/hljs/json';
import { nightOwl } from 'react-syntax-highlighter/dist/esm/styles/hljs';

// Register specific language for bundle size efficiency
SyntaxHighlighter.registerLanguage('json', json);

export default function TranslationDiff({ originalPrompt, translatedPrompt, isLoading, error }) {
  if (error) {
    return (
      <div className="bg-red-500/10 border border-red-500/50 p-6 rounded-lg text-red-400">
        <h3 className="font-bold flex items-center gap-2">⚠️ Translation Error</h3>
        <p className="text-sm mt-2">{error}</p>
      </div>
    );
  }

  // Placeholder while empty
  if (!translatedPrompt && !isLoading) {
    return (
      <div className="bg-[#111827] border border-gray-800 rounded-lg p-10 flex flex-col items-center justify-center text-center opacity-60 shadow-lg min-h-[300px]">
        <span className="text-4xl mb-4">🔁</span>
        <h3 className="text-gray-400 font-medium tracking-wide">WAITING FOR PAYLOAD</h3>
        <p className="text-sm text-gray-500 max-w-sm mt-2">Paste a Groq (LLaMA) or Vertex AI payload on the left and click translate to visually map the Amazon Bedrock equivalent JSON structure.</p>
      </div>
    );
  }

  const formatOutput = (payload) => {
    if (!payload) return '';
    try {
      return typeof payload === 'object' ? JSON.stringify(payload, null, 2) : payload;
    } catch {
      return payload;
    }
  };

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-lg p-5 flex flex-col gap-4 shadow-lg min-h-[450px]">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold text-gray-100 flex items-center gap-2">
           <span className="text-blue-500">2.</span> Translation Engine Output
        </h2>
        {translatedPrompt && !isLoading && (
          <span className="text-[10px] tracking-widest text-[#00c8ff] uppercase bg-[#00c8ff]/10 px-2.5 py-1 rounded-full border border-[#00c8ff]/30 shadow-[0_0_10px_rgba(0,200,255,0.2)]">
            BEDROCK SCHEMA COMPLETE ⚡
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4 mt-2 h-full flex-1">
        {/* Source Payload Viewer */}
        <div className="flex flex-col gap-2 relative">
          <label className="text-[11px] uppercase tracking-wider text-gray-400 font-bold">Original Source</label>
          <div className="bg-[#0b0f19] rounded border border-gray-800 overflow-auto max-h-[450px] shadow-inner text-xs flex-1">
            <SyntaxHighlighter 
              language="json" 
              style={nightOwl} 
              customStyle={{ background: 'transparent', padding: '1rem', margin: 0, overflow: 'visible' }}
            >
              {originalPrompt || '{}'}
            </SyntaxHighlighter>
          </div>
        </div>

        {/* Translation Output Viewer */}
        <div className="flex flex-col gap-2 relative">
          <label className="text-[11px] uppercase tracking-wider text-green-400 font-bold drop-shadow-[0_0_4px_rgba(34,211,160,0.4)]">Translated Bedrock Schema</label>
          <div className="bg-[#0b1219] rounded border border-gray-800 overflow-auto max-h-[450px] shadow-[inset_0_0_20px_rgba(34,211,160,0.03)] text-xs flex-1 relative">
            {isLoading && (
              <div className="absolute inset-0 z-10 flex flex-col items-center justify-center bg-[#0b1219]/90 backdrop-blur-[2px]">
                <div className="w-6 h-6 border-2 border-green-500 border-t-transparent rounded-full animate-spin mb-3 shadow-[0_0_10px_rgba(34,211,160,0.5)]"></div>
                <span className="text-green-400 animate-pulse tracking-widest text-[10px] font-bold">RE-MAPPING TOKENS...</span>
              </div>
            )}
            
            <SyntaxHighlighter 
              language="json" 
              style={nightOwl} 
              customStyle={{ background: 'transparent', padding: '1rem', margin: 0, overflow: 'visible', opacity: isLoading ? 0.3 : 1, transition: 'opacity 0.3s ease' }}
            >
              {formatOutput(translatedPrompt)}
            </SyntaxHighlighter>
          </div>
        </div>
      </div>
    </div>
  );
}
