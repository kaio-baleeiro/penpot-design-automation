# Claude Code entrypoint

Read and follow [AGENTS.md](AGENTS.md). On each new session, first run
`./penpot-workflow begin`, ask its exact question, and wait for the user. Record
the verbatim answer with `./penpot-workflow select <mode> --user-answer "..."`.
Use `skills/penpot-design/SKILL.md` as
the workflow entrypoint. Project subagents are available in `.claude/agents/`;
their prompts point to the canonical profiles in `agents/profiles/`.
