const p=penpot.currentFile.pages.find(x=>x.id==="b9b9f43f-1dd3-801e-8008-a6725d4e8fbd");
await penpot.openPage(p);
const f=penpotUtils.findShape(x=>x.id==="b9b9f43f-1dd3-801e-8008-a6741a129cb3",p.root);
const repos=penpotUtils.findShape(x=>x.name==="GitHub / Popular Repositories",f);
for(const s of penpotUtils.findShapes(x=>x.name.startsWith("Repo Public badge /"),f))s.hidden=true;
const positions=[[780,694],[1226,694],[780,807],[1226,807],[780,918],[1226,918]];
for(let i=0;i<positions.length;i++){
  const [x,y]=positions[i];
  const r=penpot.createRectangle();r.name="Public badge exact / "+(i+1);r.x=x;r.y=y;r.resize(48,22);r.borderRadius=11;r.fills=[{fillColor:"#FFFFFF",fillOpacity:1}];r.strokes=[{strokeColor:"#D0D7DE",strokeOpacity:1,strokeWidth:1}];repos.appendChild(r);
  const t=penpot.createText("Public");t.name="Public badge exact label / "+(i+1);t.x=x+6;t.y=y+4;t.resize(36,16);t.fontFamily="Inter";t.fontSize="12";t.fontWeight="500";t.align="center";t.fills=[{fillColor:"#656D76",fillOpacity:1}];repos.appendChild(t);
}
const side=penpotUtils.findShape(x=>x.name==="GitHub / Profile Sidebar",f);
for(const name of ["Achievement / badge outer","Achievement / badge inner","Achievement / badge icon"]){const s=penpotUtils.findShape(x=>x.name===name,f);if(s)s.hidden=true;}
const badge=penpot.createRectangle();badge.name="Achievement / exact Pull Shark";badge.x=112;badge.y=702;badge.resize(60,60);badge.borderRadius=30;badge.fills=[{fillImage:await penpot.uploadMediaUrl("pull-shark.cycle2","https://github.githubassets.com/assets/pull-shark-bronze-a37accb528d1.png"),fillOpacity:1}];badge.setPluginData("asset_status","uploaded_to_penpot");side.appendChild(badge);
return {frame:f.id,publicBadges:6,achievement:badge.id};
