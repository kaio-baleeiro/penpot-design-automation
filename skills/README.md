# Skills

Cada subpasta é um pacote Agent Skills independente. O `SKILL.md` é a entrada;
`agents/` contém metadados de interface, `scripts/` wrappers executáveis,
`references/` instruções sob demanda, `assets/` configuração reutilizável e
`lessons-learned/` memória operacional versionada da skill.

As sete skills trabalham em conjunto, mas não dependem de cópias globais. Os
perfis especializados que operam cada fase ficam em [`../agents/`](../agents/)
e seguem um contrato de handoff comum para funcionar em outros CLIs. O
instalador cria apenas um vínculo global para `penpot-design`.
