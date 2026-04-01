import React, { useState, useEffect } from 'react';

// Reusable hook to simulate a generative AI typing stream
function useTypewriter(text, active, speed = 8) {
  const [displayedText, setDisplayedText] = useState('');

  useEffect(() => {
    if (!active || !text) {
      if (!text) setDisplayedText('');
      return;
    }
    setDisplayedText(''); // Reset on new stream
    let i = 0;
    const interval = setInterval(() => {
      setDisplayedText((prev) => prev + text.charAt(i));
      i++;
      if (i >= text.length) clearInterval(interval);
    }, speed);
    return () => clearInterval(interval);
  }, [text, active, speed]);

  return active ? displayedText : text;
}

export default function ExecutionPanel({ onExecute, isExecuting, executionResult, targetModel, sourceModel }) {
  
  // Custom states to handle the local reveal animations
  const [streamActive, setStreamActive] = useState(false);

  // When execution finishes (result arrives and isExecuting flips to false), start streaming!
  useEffect(() => {
    if (!isExecuting && executionResult) {
      setStreamActive(true);
    } else {
      setStreamActive(false);
    }
  }, [isExecuting, executionResult]);

  const animatedSource = useTypewriter(executionResult?.sourceOutput || '', streamActive, 6);
  const animatedTarget = useTypewriter(executionResult?.targetOutput || '', streamActive, 5);

  return (
    <div className="bg-[#111827] border border-gray-800 rounded-lg p-5 flex flex-col gap-4 shadow-lg flex-1">
      <div className="flex justify-between items-center">
        <h2 className="text-lg font-semibold text-gray-100 flex items-center gap-2">
           <span className="text-[#00c8ff]">3.</span> Execution Engine
        </h2>
        {executionResult && !isExecuting && (
           <span className="text-[10px] tracking-widest text-green-400 uppercase bg-green-500/10 px-2.5 py-1 rounded-full border border-green-500/30 animate-pulse">
             DYNAMODB SAVE QUEUED ✓
           </span>
        )}
      </div>

      <p className="text-xs text-gray-400 leading-relaxed mb-1">
        Run the fully mapped prompt against Amazon Bedrock ({targetModel}). This action invokes the backend dual-execution engine, triggering LLM inference and streaming evaluation metrics.
      </p>

      <button 
        onClick={onExecute}
        disabled={isExecuting}
        className="w-full flex items-center justify-center gap-2 bg-gradient-to-r hover:from-blue-500 hover:to-cyan-400 from-blue-600 to-cyan-500 text-white font-bold tracking-wider rounded-md text-sm px-5 py-3.5 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_15px_rgba(0,200,255,0.2)]"
      >
        {isExecuting ? 'INVOKING CLOUD APIS...' : '▶ RUN BEDROCK EXECUTION'}
      </button>

      {/* Execution Results Data View */}
      {executionResult && (
        <div className="mt-4 flex flex-col gap-3">
          <div className="grid grid-cols-2 gap-4">
             {/* Source Side Output */}
             <div className="border border-gray-800 rounded bg-[#0f1524] p-4 text-xs font-mono text-gray-300 min-h-[150px] shadow-inner">
                <div className="border-b border-gray-800 pb-2 mb-3 text-[10px] text-gray-500 uppercase tracking-widest flex items-center gap-2">
                  <span className={`w-2 h-2 rounded-full ${isExecuting ? 'bg-orange-500 animate-pulse' : 'bg-green-500'}`}></span>
                  {sourceModel} Output
                </div>
                {isExecuting ? (
                  <span className="opacity-50 blur-[1px]">Awaiting First Token...</span>
                ) : (
                  <span className="whitespace-pre-wrap leading-relaxed">{animatedSource}<span className={animatedSource.length < executionResult.sourceOutput.length ? "inline-block w-1.5 h-3.5 bg-gray-400 animate-pulse ml-0.5" : "hidden"}></span></span>
                )}
             </div>
             {/* Target Bedrock Output */}
             <div className="border border-[#00c8ff]/20 rounded bg-[#0b1724] p-4 text-xs font-mono text-cyan-50 min-h-[150px] shadow-[inset_0_0_15px_rgba(0,200,255,0.03)] relative">
                <div className="border-b border-[#00c8ff]/20 pb-2 mb-3 text-[10px] text-[#00c8ff] uppercase tracking-widest flex justify-between items-center">
                  <div className="flex items-center gap-2">
                     <span className={`w-2 h-2 rounded-full ${isExecuting ? 'bg-cyan-500 animate-pulse' : 'bg-cyan-400'}`}></span>
                     <span>{targetModel}</span>
                  </div>
                  {!isExecuting && <span className="opacity-80 drop-shadow">{executionResult.latency} ms</span>}
                </div>
                {isExecuting ? (
                  <span className="text-cyan-800 blur-[1px]">Awaiting First Token...</span>
                ) : (
                  <span className="whitespace-pre-wrap leading-relaxed">{animatedTarget}<span className={animatedTarget.length < executionResult.targetOutput.length ? "inline-block w-1.5 h-3.5 bg-cyan-400 animate-pulse ml-0.5 drop-shadow-[0_0_5px_rgba(0,200,255,1)]" : "hidden"}></span></span>
                )}
             </div>
          </div>
        </div>
      )}

    </div>
  );
}
