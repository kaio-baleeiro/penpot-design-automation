# Infraestrutura

`infra/penpot/` contém a composição Docker local compartilhada, seus scripts de
operação e a configuração pública sem segredos. O arquivo `.env` real é local,
ignorado e nunca deve ser commitado.

Em um clone novo, execute `./setup.sh` na raiz. Ele cria segredos e volumes
neutros automaticamente. Uma instalação migrada continua usando seus volumes
históricos definidos apenas no `.env` e nas lições locais ignoradas.

Consulte [`penpot/README.md`](penpot/README.md) para subir, validar, fazer
backup, restaurar ou atualizar os sete serviços.
