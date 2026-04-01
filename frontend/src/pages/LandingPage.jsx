import React, { useState } from 'react';
import { useMigrationDemo } from '../hooks/useMigrationDemo';
import PromptInput from '../components/upload/PromptInput';
import TranslationDiff from '../components/translate/TranslationDiff';
import ExecutionPanel from '../components/compare/ExecutionPanel';
import MigrationReport from '../components/report/MigrationReport';
import { translatePrompt, executeComparison, saveComparisonMetrics } from '../services/apiClient';

export default function LandingPage() {
  useMigrationDemo();

  const [sourceModel, setSourceModel] = useState('llama-3.1-8b-instant');
  const [targetModel, setTargetModel] = useState(null); 
  const [inputPrompt, setInputPrompt] = useState('');
  
  const [translatedPrompt, setTranslatedPrompt] = useState(null);
  const [isTranslating, setIsTranslating] = useState(false);
  const [translationError, setTranslationError] = useState(null);

  const [executionResult, setExecutionResult] = useState(null);
  const [isExecuting, setIsExecuting] = useState(false);

  const handleTranslate = async () => {
    if (!inputPrompt) return;
    setIsTranslating(true);
    setTranslationError(null);
    try {
      const res = await translatePrompt({ sourcePrompt: inputPrompt, sourceModel });
      setTranslatedPrompt(res.data.converted_schema);
      setTargetModel(res.data.target_model);
      
      // Auto-scroll slightly to show result if on mobile
      setTimeout(() => {
        document.getElementById('migration-workspace')?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }, 100);
    } catch (err) {
      setTranslationError('Error connecting to backend translation engine.');
      console.error(err);
    } finally {
      setIsTranslating(false);
    }
  };

  const handleExecute = async () => {
    if (!translatedPrompt || !targetModel) return;
    setIsExecuting(true);
    try {
      const res = await executeComparison({ translatedPrompt, targetModel });
      setExecutionResult(res.data);
      await saveComparisonMetrics({ source: sourceModel, destination: targetModel, comparisonData: res.data });
    } catch (err) {
      console.error('Execution Failed:', err);
    } finally {
      setIsExecuting(false);
    }
  };

  const scrollToApp = (e) => {
    e.preventDefault();
    document.getElementById('migration-workspace').scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <>
      {/* Custom cursor */}
      <div className="cursor" id="cursor"></div>
      <div className="cursor-ring" id="cursor-ring"></div>

      {/* NAV */}
      <nav>
        <div className="nav-logo">BRIDGEROCK<span></span> <div className="nav-badge" style={{marginLeft: "12px"}}>GOOGLE VERTEX / GEMINI</div></div>
        <div className="nav-links">
          <a href="#cta" onClick={scrollToApp}>Migration Studio</a>
        </div>
        <a href="#migration-workspace" className="nav-cta" onClick={scrollToApp}>Start Migrating →</a>
      </nav>

      {/* HERO */}
      <section className="hero">
        <div className="hero-grid-bg"></div>
        <div className="hero-glow"></div>
        <div className="hero-glow2"></div>

        <div className="hero-tag">🏗 HACKATHON PROJECT · HACK'A'WAR 2026</div>

        <div className="hero-brand-wrap">
          <div style={{fontFamily: "'Bebas Neue',sans-serif", fontSize: "clamp(4rem,10vw,9rem)", lineHeight: ".92", letterSpacing: ".02em"}}>
            <div className="hero-brand-line" id="brand-line1">BRIDGEROCK</div>
            <div className="hero-brand-line line-factory" id="brand-line2" style={{fontFamily: "'Instrument Serif',serif", fontStyle: "italic", fontSize: "clamp(3rem,8vw,7rem)"}}></div>
          </div>
          <div className="hero-brand-sub">MIGRATION FACTORY FOR GOOGLE VERTEX AI</div>
        </div>

        <p className="hero-desc">
          Move your AI applications from Groq (LLaMA), Google Vertex AI, or Azure to Google Vertex — without rebuilding
          from scratch. Intelligent translation. Zero vendor lock-in.
        </p>

        <div className="hero-actions">
          <button onClick={scrollToApp} className="btn-primary">Start Migrating Workspace →</button>
        </div>

        <div className="hero-stat-strip">
          <div className="hero-stat">
            <div className="num">3×</div>
            <div className="label">FASTER MIGRATION</div>
          </div>
          <div className="hero-stat">
            <div className="num">60%</div>
            <div className="label">COST REDUCTION</div>
          </div>
          <div className="hero-stat">
            <div className="num">100%</div>
            <div className="label">BEHAVIOR PRESERVED</div>
          </div>
          <div className="hero-stat">
            <div className="num">5</div>
            <div className="label">AI PROVIDERS SUPPORTED</div>
          </div>
        </div>
      </section>

      {/* MARQUEE */}
      <div className="marquee-wrap">
        <div className="marquee-inner">
          <div className="marquee-item"><span>◆</span> PROMPT TRANSLATION</div>
          <div className="marquee-item"><span>◆</span> MODEL MAPPING ENGINE</div>
          <div className="marquee-item"><span>◆</span> SIDE-BY-SIDE BENCHMARKING</div>
          <div className="marquee-item"><span>◆</span> COST ANALYSIS</div>
          <div className="marquee-item"><span>◆</span> LLM-AS-JUDGE EVALUATION</div>
          <div className="marquee-item"><span>◆</span> GOOGLE VERTEX NATIVE</div>
          <div className="marquee-item"><span>◆</span> ZERO VENDOR LOCK-IN</div>
          <div className="marquee-item"><span>◆</span> ENTERPRISE READY</div>
          <div className="marquee-item"><span>◆</span> PROMPT TRANSLATION</div>
          <div className="marquee-item"><span>◆</span> MODEL MAPPING ENGINE</div>
          <div className="marquee-item"><span>◆</span> SIDE-BY-SIDE BENCHMARKING</div>
          <div className="marquee-item"><span>◆</span> COST ANALYSIS</div>
          <div className="marquee-item"><span>◆</span> LLM-AS-JUDGE EVALUATION</div>
          <div className="marquee-item"><span>◆</span> GOOGLE VERTEX NATIVE</div>
          <div className="marquee-item"><span>◆</span> ZERO VENDOR LOCK-IN</div>
          <div className="marquee-item"><span>◆</span> ENTERPRISE READY</div>
        </div>
      </div>

      {/* CTA SECTION - Ready to break free? */}
      <section className="cta-section" id="cta" style={{ minHeight: 'auto', padding: '6rem 10%', paddingBottom: '3rem' }}>
        <div className="cta-glow"></div>
        <div className="reveal">
          <div className="section-label" style={{justifyContent: "center"}}>LLM MIGRATION STUDIO</div>
          <h2 className="section-title">Ready to<br /><em>break free?</em></h2>
          <p className="cta-sub">
            Paste your original AI Prompt below and allow BridgeRock to intelligently translate it to Google Vertex syntax, completely handling system roles, tool calling, and JSON schemas.
          </p>
        </div>
      </section>

      {/* ===================== THE REAL FUNCTIONAL WORKSPACE ===================== */}
      <section id="migration-workspace" style={{ background: 'var(--bg)', padding: '2rem 5%', paddingBottom: '8rem', position: 'relative', zIndex: 2 }}>
        
        {/* Workspace Container */}
        <div className="max-w-[1600px] mx-auto border border-gray-800 bg-[#0d1326] rounded-xl overflow-hidden shadow-2xl">
          
          <div className="border-b border-gray-800 bg-[#151c33] px-6 py-4 flex items-center justify-between">
            <div className="font-bold text-sm tracking-widest text-[#00c8ff] flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-[#00c8ff] animate-pulse"></span>
              LIVE ENVIRONMENT
            </div>
            <div className="text-sm font-mono text-slate-400">
              Source: {sourceModel} {targetModel ? `→ Target: ${targetModel}` : `→ Mapping...`}
            </div>
          </div>

          <div className="p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Left Column: Input Panel */}
            <div className="lg:col-span-4 flex flex-col gap-6">
              <PromptInput 
                sourceModel={sourceModel}
                setSourceModel={setSourceModel}
                inputPrompt={inputPrompt}
                setInputPrompt={setInputPrompt}
                onTranslate={handleTranslate}
                isTranslating={isTranslating}
              />
            </div>

            {/* Right Column: Diff + Execution */}
            <div className="lg:col-span-8 flex flex-col gap-6">
              <TranslationDiff 
                originalPrompt={inputPrompt} 
                translatedPrompt={translatedPrompt} 
                isLoading={isTranslating} 
                error={translationError}
              />
              
              {translatedPrompt && targetModel && (
                <ExecutionPanel 
                  onExecute={handleExecute}
                  isExecuting={isExecuting}
                  executionResult={executionResult}
                  targetModel={targetModel}
                  sourceModel={sourceModel}
                />
              )}
            </div>
          </div>
        </div>

      </section>

      {/* DYNAMIC POST-EXECUTION METRICS REPORT */}
      <MigrationReport metrics={executionResult?.metrics} />

      {/* FOOTER */}
      <footer>
        <div className="footer-logo">BRIDGEROCK<span>_</span>MIGRATOR</div>
        <div className="footer-right">HACKATHON PROJECT · GOOGLE VERTEX MIGRATION FACTORY · 2026</div>
      </footer>
    </>
  );
}
