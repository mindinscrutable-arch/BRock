import React, { useState, useEffect } from 'react';

export default function PromptInput({ sourceModel, setSourceModel, inputPrompt, setInputPrompt, onTranslate, isTranslating }) {

  // Smart Badges State
  const [detectedFeatures, setDetectedFeatures] = useState([]);

  useEffect(() => {
    if (!inputPrompt || inputPrompt.trim().length === 0) {
      setDetectedFeatures([]);
      return;
    }
    
    // Naive front-end regex mapping to dynamically "detect" what the user is throwing at us. 
    // This is purely for the "cool factor" UI presentation without touching the backend at all!
    const text = inputPrompt.toLowerCase();
    const flags = [];
    
    if (text.includes('"tools"') || text.includes('"function"')) {
      flags.push({ id: 'features', label: '⚙️ Tool Calling', color: 'text-purple-400 bg-purple-500/10 border-purple-500/30' });
    }
    if (text.includes('"response_format"') || text.includes('json_object')) {
      flags.push({ id: 'json', label: '📊 JSON Mode', color: 'text-orange-400 bg-orange-500/10 border-orange-500/30' });
    }
    if (text.includes('"role": "system"') || text.includes('systeminstruction')) {
      flags.push({ id: 'system', label: '🤖 System Context', color: 'text-cyan-400 bg-cyan-500/10 border-cyan-500/30' });
    }
    if (text.includes('"stream": true')) {
      flags.push({ id: 'stream', label: '🌊 Streaming', color: 'text-blue-400 bg-blue-500/10 border-blue-500/30' });
    }

    setDetectedFeatures(flags);
  }, [inputPrompt]);

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-lg p-5 flex flex-col gap-4 shadow-lg">
      <h2 className="text-lg font-semibold text-gray-100 flex items-center gap-2">
        <span className="text-orange-500">1.</span> Configuration & Payload
      </h2>
      
      {/* Source Model Dropdowns placed above input */}
      <div className="flex flex-col gap-3">
        <div className="flex flex-col gap-1">
          <label className="text-xs uppercase tracking-wider text-gray-500 font-medium">Source Model (Groq LLaMA)</label>
          <select 
            value={sourceModel}
            onChange={(e) => setSourceModel(e.target.value)}
            className="bg-[#1f2937] border border-gray-700 text-gray-200 text-sm rounded focus:ring-orange-500 focus:border-orange-500 block w-full p-2.5 transition-colors cursor-pointer"
          >
            <option value="llama-3.1-8b-instant">llama-3.1-8b-instant</option>
            <option value="llama3-70b-8192">llama3-70b-8192</option>
            <option value="mixtral-8x7b-32768">mixtral-8x7b-32768</option>
          </select>
        </div>
      </div>

      <hr className="border-gray-800 my-2" />

      {/* Input Textarea */}
      <div className="flex flex-col gap-1 flex-1 relative">
        <label className="text-xs uppercase tracking-wider text-gray-500 font-medium flex justify-between items-center">
          <span>Source Payload (JSON or Raw Text)</span>
          <span 
            className="text-orange-400 cursor-pointer hover:underline text-[10px]"
            onClick={() => setInputPrompt(`{\n  "model": "llama-3.1-8b-instant",\n  "messages": [\n    {\n      "role": "system",\n      "content": "You are a helpful assistant."\n    }\n  ],\n  "tools": [],\n  "response_format": {"type": "json_object"}\n}`)}
          >
            Load Example JSON
          </span>
        </label>
        
        <textarea
          value={inputPrompt}
          onChange={(e) => setInputPrompt(e.target.value)}
          placeholder="Paste your original system prompts, user messages, or entirely raw JSON request body here..."
          className="bg-[#0f1524] border border-gray-800 text-gray-300 text-sm rounded focus:ring-orange-500 focus:border-gray-600 block w-full p-3 font-mono mt-1 flex-1 min-h-[300px] resize-y"
          style={{ lineHeight: '1.6' }}
        />

        {/* Feature Parsing Badges Layer */}
        <div className="mt-3 min-h-[28px] flex items-center gap-2 flex-wrap">
          {detectedFeatures.length > 0 ? (
            detectedFeatures.map(f => (
              <span key={f.id} className={`text-[10px] tracking-widest uppercase px-2 py-1 rounded-sm border ${f.color} shadow-sm transition-all animate-in fade-in zoom-in duration-300`}>
                {f.label}
              </span>
            ))
          ) : (
            <span className="text-[10px] uppercase text-gray-600 tracking-wider">
              {inputPrompt.length > 5 ? "NO COMPLEX SCHEMA FLAGS DETECTED" : "AWAITING PAYLOAD INPUT..."}
            </span>
          )}
        </div>
      </div>

      <button 
        onClick={onTranslate}
        disabled={isTranslating || inputPrompt.trim().length === 0}
        className="mt-2 w-full flex items-center justify-center gap-2 bg-gradient-to-r from-orange-500 to-orange-600 hover:from-orange-400 hover:to-orange-500 text-white font-medium rounded-md text-sm px-5 py-3 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(255,107,26,0.15)]"
      >
        {isTranslating ? (
           <span className="animate-pulse">Analyzing Payload Geometry...</span>
        ) : (
          <>
            <span>⚡ Parse & Translate to Bedrock</span>
          </>
        )}
      </button>

    </div>
  );
}
