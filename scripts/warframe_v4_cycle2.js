const p=penpot.currentFile.pages.find(x=>x.id==="b9b9f43f-1dd3-801e-8008-a67636574e02");
await penpot.openPage(p);
const f=penpotUtils.findShape(x=>x.id==="b9b9f43f-1dd3-801e-8008-a67636745b0f",p.root);
const hero=penpotUtils.findShape(x=>x.name==="Hero",f);
async function media(url,name){return await penpot.uploadMediaUrl(name,url);}
async function replace(name,url){const s=penpotUtils.findShape(x=>x.name===name,f);if(!s)throw new Error("missing "+name);s.fills=[{fillImage:await media(url,name+".cycle2"),fillOpacity:1}];s.setPluginData("asset_status","uploaded_to_penpot");return s;}
await replace("Asset / hero red key art","https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/mainframe/dynamic-config/homepage/11/conversions/19bb4c95-23f8-4ac0-b5c4-17f1923c19a3-webp.webp");
const overlay=penpotUtils.findShape(x=>x.name==="Hero / red overlay",f);if(overlay)overlay.hidden=true;
for(const name of ["Hero / title","Hero / subtitle"]){const s=penpotUtils.findShape(x=>x.name===name,f);if(s)s.hidden=true;}
let logo=penpotUtils.findShape(x=>x.name==="Hero / exact masthead logo",f);
if(!logo){logo=penpot.createRectangle();logo.name="Hero / exact masthead logo";logo.x=130;logo.y=116;logo.resize(430,180);hero.appendChild(logo);}
logo.fills=[{fillImage:await media("https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/mainframe/dynamic-config/homepage/11/conversions/cc1706f7-36bc-4bd9-8f40-d8f06d663e1f-webp.webp","warframe-masthead-logo.cycle2"),fillOpacity:1}];
logo.setPluginData("asset_status","uploaded_to_penpot");
let cookie=penpotUtils.findShape(x=>x.name==="Cookie consent",f);
if(!cookie){
  cookie=penpot.createBoard();cookie.name="Cookie consent";cookie.x=0;cookie.y=826;cookie.resize(1440,84);cookie.fills=[{fillColor:"#FFFFFF",fillOpacity:1}];hero.appendChild(cookie);
  const t=penpot.createText("Ao clicar em ‘Aceitar todos os cookies’, concordo com o armazenamento de cookies no seu dispositivo para melhorar a navegação no site, analisar a utilização do site e ajustar nas nossas iniciativas de marketing.");t.name="Cookie / copy";t.x=25;t.y=844;t.resize(760,34);t.fontFamily="Inter";t.fontSize="11";t.fills=[{fillColor:"#20242A",fillOpacity:1}];cookie.appendChild(t);
  for(const [label,x,w,c] of [["Definições de cookies",860,160,"#FFFFFF"],["Rejeitar Todos",1030,130,"#174E73"],["Aceitar todos os cookies",1170,190,"#174E73"]]){const b=penpot.createRectangle();b.name="Cookie / "+label;b.x=x;b.y=846;b.resize(w,32);b.fills=[{fillColor:c,fillOpacity:1}];b.strokes=[{strokeColor:"#174E73",strokeOpacity:1,strokeWidth:1}];cookie.appendChild(b);const l=penpot.createText(label);l.name="Cookie / "+label+" label";l.x=x;l.y=854;l.resize(w,18);l.fontFamily="Inter";l.fontSize="10";l.fontWeight="600";l.align="center";l.fills=[{fillColor:c==="#FFFFFF"?"#174E73":"#FFFFFF",fillOpacity:1}];cookie.appendChild(l);}
}
await replace("Asset / prime banner","https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/mainframe/dynamic-config/homepage/11/conversions/bf9e06af-a756-4214-b03f-7f78dcc3685b-webp.webp");
await replace("Asset / Guides / card 1","https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/mainframe/dynamic-config/homepage/11/conversions/586d1969-5352-4910-a01d-38ca38623fe0-webp.webp");
await replace("Asset / Guides / card 2","https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/mainframe/dynamic-config/homepage/11/conversions/5802a9f7-0b49-4969-aaff-32f0f5c1a2de-webp.webp");
await replace("Asset / Guides / card 3","https://warframe-web-assets.nyc3.cdn.digitaloceanspaces.com/mainframe/dynamic-config/homepage/11/conversions/45141a5f-a834-485f-af5d-ee574fe3a3ea-webp.webp");
return {frame:f.id,heroPoster:true,logo:logo.id,cookie:cookie.id,prime:true,guides:3};
