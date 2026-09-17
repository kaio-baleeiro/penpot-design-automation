# Serial MCP build

`warframe-v4.js` is the Penpot plugin-context body. Execute it only after the
active Penpot page is isolated from concurrent builds. It creates the page and
frame itself, uses all approved section bounds, applies local coordinates for
nested boards, adds exact first-party media, and creates real tokens plus a
visible component instance.

After execution, append the MCP request/response to
`../penpot-mcp-log.jsonl`, export the frame to `../exports/cycle-1.png`, and
fill `../structure-inventory.json` from the actual Penpot tree.
