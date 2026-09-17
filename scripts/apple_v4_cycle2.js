const p=penpot.currentFile.pages.find(x=>x.id==="b9b9f43f-1dd3-801e-8008-a6714b37dc3b");
await penpot.openPage(p);
const f=penpotUtils.findShape(x=>x.id==="b9b9f43f-1dd3-801e-8008-a67202c01eef",p.root);
const updates=[
  ["Apple / iPhone 18 Pro / exact source asset",0,44,1440,692],
  ["Apple / iPhone Duo / exact source asset",0,748,1440,692],
  ["Apple / Apple Watch Series 12 / exact source asset",0,1452,1440,692]
];
for(const [name,x,y,w,h] of updates){const s=penpotUtils.findShape(q=>q.name===name,f);if(s){s.x=x;s.y=y;s.resize(w,h);}}
for(const name of ["TV / card Desaparecida","TV / card Slow Horses","TV / card O Segredo de Widow's Bay"]){const s=penpotUtils.findShape(q=>q.name===name,f);if(s)s.hidden=true;}
for(const board of penpotUtils.findShapes(q=>q.type==="board",f)){
  for(const child of [...(board.children||[])].filter(q=>q.type==="text")) board.appendChild(child);
}
return {frame:f.id,updates:updates.length,hidden:3};
