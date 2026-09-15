# Scripts

Os scripts da raiz são utilitários determinísticos usados pelas skills:

- `penpot_validation/` captura fontes, deriva frame specs e valida renders;
- `penpot_mcp.py` e `penpot-mcp.sh` fazem o transporte MCP com redação de
  segredos;
- `penpot_inventory.py` extrai o inventário estrutural do design system;
- `rebuild_benchmark_designs.js` é o payload MCP versionado que reconstrói os
  três benchmarks como boards, textos, formas e assets editáveis; a captura
  full-page não é usada como conteúdo visível do frame;
- `validate_skills.py` valida os pacotes Agent Skills do repositório.

Use os wrappers da skill quando existirem; eles resolvem o checkout mesmo se o
comando for iniciado fora da raiz.
