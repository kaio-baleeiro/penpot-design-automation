# Scripts da composição Penpot

Scripts para `up`, `down`, `healthcheck`, `wait-ready`, `provision`, `validate`,
`logs`, `backup`, `restore` e `update`. O provisionador cria/reutiliza a conta
local e MCP, salvando segredos somente no `.env` ignorado da raiz. Os scripts
operam volumes externos; `down` não remove volumes e `restore` exige
confirmação explícita.
