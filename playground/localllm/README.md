# local-llm

A small language model that runs in the page on WebGPU, for the manuals' playgrounds (`pg.js` loads `local-llm.js` on demand).

Adapted from the chat demo of [jax-js](https://github.com/ekzhang/jax-js) (`website/src/routes/chat`, MIT, Copyright (c) Eric Zhang): the model definitions in `src/gemma.ts`, `src/lfm.ts`, `src/chat-model.ts`, and the tokenizer in `src/huggingface-tokenizer.ts` are theirs; `src/index.ts` wraps them as `load(id)` and `chat(messages)` with no UI. The weights (Gemma 3 270M, LFM2.5 350M) are fetched from Hugging Face (`ekzhang/jax-js-models`) at run time and cached by the browser; nothing is committed here.

```bash
npm install && npm run build      # writes local-llm.js (about 410 KB)
cp local-llm.js ../../../hermes-docs/ ../../../kroma-docs/ ../../../agentic-ontologist-docs/
```
