/**
 * A small language model that runs in the page, on WebGPU, for the manuals' playgrounds.
 *
 * Adapted from the chat demo of jax-js (https://github.com/ekzhang/jax-js, website/src/routes/chat), which is MIT
 * licensed, Copyright (c) Eric Zhang. The model definitions (Gemma 3 270M, LFM2.5 350M), the tokenizers and the
 * sampling loop are theirs; this file wraps them as `load(id)` and `chat(messages)` with no UI. The weights are
 * fetched from Hugging Face (ekzhang/jax-js-models) and cached by the browser.
 */
import { defaultDevice, init, numpy as np } from "@jax-js/jax";
import { cachedFetch } from "@jax-js/loaders";

import { CHAT_MODELS, type ChatMessage, type ChatModelId, type ChatTokenizer, type LoadedChatModel } from "./chat-model";

export type Progress = { loaded: number; total: number };
export type Options = { backend?: "webgpu" | "wasm"; onProgress?: (what: string, p: Progress) => void; onStatus?: (text: string) => void };
export type ChatOptions = { maxTokens?: number; temperature?: number; topK?: number; topP?: number; repetitionPenalty?: number; onToken?: (text: string) => void; signal?: AbortSignal };

export const MODELS = Object.values(CHAT_MODELS).map((m) => ({ id: m.id as string, label: m.label, size: m.downloadSize }));

/** The devices this browser offers, best first. */
export async function devices(): Promise<string[]> {
  const found = await init("webgpu", "wasm");
  return (["webgpu", "wasm"] as const).filter((d) => found.includes(d));
}

function sampleLogits(logits: Float32Array, o: { temperature: number; topK: number; topP: number; repetitionPenalty: number; previous: number[] }): number {
  const k = Math.max(1, Math.min(o.topK, logits.length));
  const candidates: { id: number; logit: number }[] = [];
  const previous = new Set(o.previous);
  for (let id = 0; id < logits.length; id++) {
    let logit = logits[id];
    if (Number.isNaN(logit)) continue;
    if (o.repetitionPenalty !== 1 && previous.has(id)) logit = logit < 0 ? logit * o.repetitionPenalty : logit / o.repetitionPenalty;
    if (candidates.length < k || logit > candidates[candidates.length - 1].logit) {
      let at = 0;
      while (at < candidates.length && logit < candidates[at].logit) at++;
      candidates.splice(at, 0, { id, logit });
      if (candidates.length > k) candidates.pop();
    }
  }
  if (!candidates.length) throw new Error("The model returned all-NaN logits.");
  if (o.temperature <= 0) return candidates[0].id;
  const max = candidates[0].logit;
  if (!Number.isFinite(max)) return candidates[0].id;
  const probs = candidates.map((c) => Math.exp((c.logit - max) / o.temperature));
  const total = probs.reduce((a, b) => a + b, 0);
  if (!Number.isFinite(total) || total <= 0) return candidates[0].id;
  let kept = 0, keptTotal = 0;
  for (; kept < candidates.length; kept++) { keptTotal += probs[kept]; if (keptTotal / total >= o.topP) { kept++; break; } }
  if (kept === 0) kept = 1;
  let r = Math.random() * keptTotal;
  for (let i = 0; i < kept; i++) { r -= probs[i]; if (r <= 0) return candidates[i].id; }
  return candidates[kept - 1].id;
}

export class LocalModel {
  constructor(private model: LoadedChatModel, private tokenizer: ChatTokenizer, readonly label: string, readonly backend: string) {}

  /** A reply to `messages` (roles "user" and "assistant"; a "system" message is folded into the first user turn). */
  async chat(messages: { role: string; content: string }[], opts: ChatOptions = {}): Promise<string> {
    const def = this.model.definition, d = def.defaults;
    const system = messages.filter((m) => m.role === "system").map((m) => m.content).join("\n\n");
    let history: ChatMessage[] = messages.filter((m) => m.role !== "system").map((m, i) => ({ id: i, role: m.role === "assistant" ? "assistant" : "user", content: m.content }));
    if (system && history.length) history = [{ ...history[0], content: system + "\n\n" + history[0].content }, ...history.slice(1)];
    const promptTokens = def.encodePrompt(this.tokenizer, history);
    const generated: number[] = [];
    const session = this.model.createSession();
    const stop = def.stopTokens(this.tokenizer);
    const sampling = { temperature: opts.temperature ?? 0, topK: opts.topK ?? d.topK, topP: opts.topP ?? d.topP, repetitionPenalty: opts.repetitionPenalty ?? d.repetitionPenalty };
    let logits: np.Array | null = null;
    try {
      logits = session.prefill(np.array(promptTokens, { dtype: np.uint32 }));
      const max = opts.maxTokens ?? 512;
      for (let i = 0; i < max; i++) {
        if (opts.signal?.aborted) break;
        const current = logits;
        logits = null; // data() consumes the array
        const next = sampleLogits((await current.data()) as Float32Array, { ...sampling, previous: [...promptTokens, ...generated] });
        if (stop.includes(next)) break;
        generated.push(next);
        opts.onToken?.(this.tokenizer.decodeGenerated(generated));
        if (i === max - 1) break;
        logits = session.step(next);
      }
    } finally {
      logits?.dispose();
      session.dispose();
    }
    return this.tokenizer.decodeGenerated(generated);
  }

  dispose() { this.model.dispose(); }
}

/** Download (or read from the browser's cache) and load a model. */
export async function load(id: string, opts: Options = {}): Promise<LocalModel> {
  const def = CHAT_MODELS[id as ChatModelId];
  if (!def) throw new Error(`Unknown model ${id}`);
  const available = await devices();
  const backend = opts.backend && available.includes(opts.backend) ? opts.backend : available[0];
  if (!backend) throw new Error("Neither WebGPU nor WebAssembly is available in this browser.");
  defaultDevice(backend as Parameters<typeof defaultDevice>[0]);
  opts.onStatus?.("Downloading the tokenizer…");
  const tokenizerData = await cachedFetch(def.tokenizerUrl, {}, (p) => opts.onProgress?.("tokenizer", { loaded: p.loadedBytes, total: p.totalBytes ?? 0 }));
  const tokenizer = def.createTokenizer(tokenizerData);
  opts.onStatus?.(`Downloading ${def.label} (${def.downloadSize}, cached in this browser after the first time)…`);
  const weights = await cachedFetch(def.weightsUrl, {}, (p) => opts.onProgress?.("weights", { loaded: p.loadedBytes, total: p.totalBytes ?? 0 }));
  opts.onStatus?.(backend === "wasm" ? "Preparing the weights for WebAssembly…" : "Uploading the weights to the GPU…");
  const model = await def.loadCheckpoint(weights, backend === "wasm" ? np.float32 : np.float16);
  opts.onStatus?.("Ready.");
  return new LocalModel(model, tokenizer, def.label, backend);
}
