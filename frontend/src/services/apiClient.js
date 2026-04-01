const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

/**
 * A tiny wrapper around native fetch() to maintain the Axios-like 
 * return shape (e.g. { data: ... }) so we don't have to rewrite 
 * the LandingPage.jsx component.
 */
async function fetchPost(endpoint, payload) {
  const url = `${API_BASE}${endpoint}`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(`HTTP Error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json();
  return { data };
}

/**
 * Sends original payload to FastAPI to be structurally parsed and mapped
 * to the automatically determined target Bedrock format based on the sourceModel.
 */
export const translatePrompt = async ({ sourcePrompt, sourceModel }) => {
  try {
    return await fetchPost('/translate', {
      source_payload: sourcePrompt,
      source_model: sourceModel
    });
  } catch (error) {
    // Return a mocked success object if backend is offline to test UI
    return new Promise(resolve => setTimeout(() => resolve({
      data: {
        converted_schema: {
          messages: [
            { role: "user", content: [{ text: "Simulated Bedrock Translation of your prompt" }] }
          ],
          system: "Simulated System Rules",
          anthropic_version: "bedrock-2023-05-31",
          max_tokens: 4096,
        },
        // The backend KI determines this mapping automatically!
        target_model: "anthropic.claude-3-5-sonnet-20240620-v1:0"
      }
    }), 1500));
  }
};

/**
 * Triggers dual execution on the backend (executing both source OpenAI and Bedrock concurrently).
 */
export const executeComparison = async ({ translatedPrompt, targetModel }) => {
  try {
    return await fetchPost('/compare', {
      payload: translatedPrompt,
      model: targetModel
    });
  } catch (error) {
    // Return a mocked success object if backend is offline to test UI
    return new Promise(resolve => setTimeout(() => resolve({
      data: {
        latency: 1240,
        sourceOutput: "This is a streamed simulation response from your selected OpenAI source model. In a live environment, this will stream the actual tokens from OpenAI.",
        targetOutput: "This is a simulated execution from Amazon Bedrock returning via the dual-invoke execution engine. Look closely: the payload structure was successfully converted!",
        metrics: {
          qualityScore: "98.4",
          sourceQuality: "96.1",
          latencyDiff: "-0.4s",
          sourceLatency: "1.6s",
          targetLatency: "1.2s",
          tokenDiff: "-18%",
          sourceTokens: "381",
          targetTokens: "312",
          savingsAmount: "$4,200",
          sourceCost: "$10,000/mo",
          targetCost: "$5,800/mo",
          verdict: "SAFE TO MIGRATE",
          confidence: "96%"
        }
      }
    }), 3000));
  }
};

/**
 * Fire-and-forget metrics save endpoint to funnel execution data
 * into the AWS DynamoDB table via your backend.
 */
export const saveComparisonMetrics = async ({ source, destination, comparisonData }) => {
  try {
    await fetchPost('/report/save', {
      source_model: source,
      destination_model: destination,
      metrics: comparisonData,
      timestamp: new Date().toISOString()
    });
    console.log("DynamoDB Payload Sent Successfully.");
  } catch (error) {
    console.warn("Could not save to DynamoDB. Backend /report/save likely offline.", error);
  }
};