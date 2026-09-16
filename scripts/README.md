# Scripts

Os scripts da raiz são utilitários determinísticos usados pelas skills:

- `penpot_validation/` captura fontes, deriva frame specs e valida renders;
- `penpot_mcp.py` e `penpot-mcp.sh` fazem o transporte MCP com redação de
  segredos;
- `penpot_inventory.py` extrai o inventário estrutural do design system;
- `rebuild_benchmark_designs.js` é o payload MCP versionado que reconstrói os
  três benchmarks como boards, textos, formas e assets editáveis; a captura
  full-page não é usada como conteúdo visível do frame;
- `apple_cycle{1,2,3}_code.js` e `github_cycle3_code.js` preservam os payloads
  MCP das correções v2 que produziram os exports auditados; eles são histórico
  reproduzível e não devem ser usados para sobrescrever ciclos existentes;
- `validate_skills.py` valida os pacotes Agent Skills do repositório.
- `validate_agent_profiles.py` valida manifesto, frontmatter, modelo Luna e
  README dos perfis portáveis em `agents/`.
- `publish_benchmark_comparisons.py` copia somente side-by-side, overlay e
  heatmap de ciclos já pontuados para `analysis/`, com nomes versionados e sem
  sobrescrever a evidência original.

Use os wrappers da skill quando existirem; eles resolvem o checkout mesmo se o
comando for iniciado fora da raiz.
