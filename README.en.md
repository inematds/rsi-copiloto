# RSI Copiloto

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

[![RSI Copiloto](guia/assets/banner.jpg)](https://inematds.github.io/rsi-copiloto/guia/en/)

A local AI assistant with memory, tasks, and supervised improvement cycles for individuals, independent professionals, and small businesses. **A separate project from the [RSI research (in Portuguese)](https://inematds.github.io/rsi/guia/)**.

**[Try the demo](https://inematds.github.io/rsi-copiloto/app/en/)** · **[User guide](https://inematds.github.io/rsi-copiloto/guia/en/)**

The demo uses scripted examples and browser storage. The local version calls real AI through OpenRouter and persists data in SQLite. The public demo interface is now available in PT/EN/ES; the guide and README are also translated.

## Run

Python 3.11+ and Git. No additional Python dependencies.

```bash
git clone https://github.com/inematds/rsi-copiloto.git
cd rsi-copiloto
python3 -m rsi.server
```

Open **http://127.0.0.1:8765/app/**. The server listens only on loopback, for individual use.

The `OPENROUTER_API_KEY` credential is read from the environment or the file specified by `RSI_ENV_FILE`. On the author's machine, it also checks `~/projetos/openpcbotv2/.env` and `~/projetos/wifi/.env`. Do not copy keys into this repository.

```bash
RSI_ENV_FILE="$HOME/.config/minhas-credenciais.env" python3 -m rsi.server
```

The specified file must contain `OPENROUTER_API_KEY`. Optional configuration: `RSI_MODEL` (default `openai/gpt-5.4-nano`), `RSI_DAILY_CALLS` (50 attempts per UTC day), `RSI_DB`, `--port`, `--db`, `--no-scheduler`. Up to 2,400 output tokens per call. A call limit is not a spending cap.

## What works

- Three workspaces: personal, freelance, and small business; nine ready-to-use routines.
- Deliverables with gaps, memory sources, next steps, tokens, and reported cost.
- Tasks, knowledge by profile, and context retrieved through word matching.
- Feedback, instruction proposals, current/candidate comparison on three cases, human review, promotion, and rollback.
- Optional daily routines while the server is running; a failure pauses the routine.
- History, JSON backup/restore, CSV tasks, and `.ics` calendar export.

The cycle improves instructions and processes, **not model weights**. Checks are structural and do not prove truth or business gains. The active instruction applies to all three workspaces. AI does not send messages, move money, or execute commands. External integrations and multiple users are future steps.

## Data

SQLite is stored at `~/.local/share/rsi-copiloto/state.sqlite3`, outside the published directory. The API receives the request, profile, instruction, and up to five relevant memories. Backups contain data from all three workspaces: keep them private. Importing pauses recurring routines and requires a fresh evaluation before promoting instructions; the local daily usage limit is preserved.

## Verify

```bash
python3 -m unittest discover -s tests -v
# Optional: paid live test, up to eight calls, fictional data only.
python3 -m scripts.smoke_live
```

[Plan (in Portuguese)](docs/PLANO-IMPLEMENTACAO.md) · [Operations (in Portuguese)](docs/OPERACAO.md) · [Validation (in Portuguese)](docs/VALIDACAO.md) · [Changelog (in Portuguese)](CHANGELOG.md)

A free, open research and education project by [INEMA.CLUB](https://inema.club).

## Missions and LOOP-R: two connected cycles.

You define the mission. The AI proposes one to five steps. Review the plan and click “Aprovar plano e executar primeira etapa” (approve the plan and run the first step). The result appears inside the mission for your review.

Click “Aprovar e executar próxima etapa” (approve and run the next step) to continue using the approved result and your feedback. “Corrigir esta etapa” revises the current work. You can pause, reload and resume. Saving to memory is optional: mission history is already preserved.

**Execute → Measure → Critique → Propose → Test → Validate → Promote → Repeat**

After completion, view your average rating and revision count. Click “Iniciar LOOP-R desta missão” (start this mission’s LOOP-R). The AI receives this evidence, critiques failures and proposes a candidate instruction. In the lab, compare both versions, read the answers, record your assessment and only then promote.

New missions use the promoted instruction. Missions already started retain their original version. This is supervised improvement of instructions and procedures, without training model weights. The three general tests check structure; they do not prove better quality or financial results.

The public demo uses programmed examples. The full workflow operates; use the local version to generate actual mission content with AI.
