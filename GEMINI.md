# Gemini CLI entrypoint

@./AGENTS.md

On each new session, run `./penpot-workflow begin`, ask its exact question and
wait for the user. Record the verbatim answer with
`./penpot-workflow select <mode> --user-answer "..."`. Use
`skills/penpot-design/SKILL.md` as the workflow entrypoint. Project
subagents are available in `.gemini/agents/`; their prompts point to the
canonical profiles in `agents/profiles/`.
