# Scripts

Os scripts da raiz são utilitários determinísticos usados pelas skills:

- `penpot_validation/` captura fontes, deriva frame specs e valida renders;
- `penpot_mcp.py` e `penpot-mcp.sh` fazem o transporte MCP com redação de
  segredos;
- `penpot_inventory.py` extrai o inventário estrutural do design system;
- `validate_skills.py` valida os pacotes Agent Skills do repositório.

Use os wrappers da skill quando existirem; eles resolvem o checkout mesmo se o
comando for iniciado fora da raiz.
