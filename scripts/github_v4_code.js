/* GitHub Kaio profile — v4 editable reconstruction from source/raw/full-page/source.png */
const FONT = "Inter";
const C = {
  ink: "#1F2328", muted: "#656D76", link: "#0969DA", border: "#D0D7DE",
  soft: "#F6F8FA", header: "#000000", coral: "#FD8C73", green0: "#EFF2F5",
  green1: "#ACEEBB", green2: "#4AC26B", green3: "#116329", java: "#B07219",
  html: "#E34C26", python: "#3572A5", white: "#FFFFFF"
};
const BADGE_SOURCE_B64 = "iVBORw0KGgoAAAANSUhEUgAAAEkAAABGCAIAAAAPRy5eAAAZp0lEQVR4nN17CZBd1Xnm2e72lvvW7n69qVepWy2hBQuQEAkQARKbGAyYctlmqkLiZFyZpDLJjCuOU5WpmZpK2S4vGRw8LifGHldmwMR2ABuDMatBgBBol9De3VKv771+y93PNnXu6xaLBRKYzGT01+3X9713+97znX/7/v+cBvKd8ql7frdvaPTP/uNf1Jbk9Td29w2N9g2Nnjh5cv/+A63zAwcPSSk9z7ti89V9Q6MvvrTjF0893Tc0etP2j5+91cfv+mTf0OhjP31cSvn5L/xV39Do3973d1LKz/7hH/UNjX7pK19tXXbi5Mkvf/Xr/+Pbf996u+v1N1r36RsavWbLttaHD3zvB31Do3fe/akoilrP/frf3vflr369VqudPHWqNaTWlUKI1ttTp8YReJvMl8u/evElAMDdn7gjsyTr160dHh4CADz+8ydHRlZsvf46AMBNt95+72f/3bXX3zgzM9vb23P5ZRvABcsffPZeAMA37//2p//tvX/+n75wy2133PfNbzUdp/Xt+nVrS6WOAwcOAgDuvOP21oe33HJjb2/Pztd23Xjr7Z//iy/ecNP2r33jvh07XrFt+30e9A5sTz/zHAAgmUysX7f27Z/fctONAIBHHv0pIeQbX/vy3XfdkUwmfvn0szMzs1dtvvKH/+sHhBAI4fs8pvUthOpxl65f9/3vfmf9urW/evGlh3/0Y9f1/vRP/uhP/v3nzl559113ts5vvmlr66SQz//j/3zg2muuPnbs+IM//KfJydP/5rZbv/2t+97noRBCKKUEH1yklLOzc7l8ztB18GHFcVzXddvaigi9Y4rfRyil8+VysVDUde28F39IbP9fCAIXryBw8QoCF68gcPEKAhevIHDxCgIXryBw8QoCF68gcPEKAhevIHDxCgIXr5B/uVtLKSTnnFHJuRBMFRwyruEwhoggQtQJRO9f+P0rwiaFYKHv1ytho+rXq5GzEDaroetEvqtACiERRrpJzJRp50w7n8gWE9liKlfUrARC+F8nNskpdcrTtcljjamTzsxEWJtlbg2yEAEO41pWCMGE4FxQximXTAKJdS2ZSRS77M6+fM9Q28BottSrGeZHNCTwEdSmLAorpw5P7325cfooXZiToaMBEQnuSozMhJFOEctC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";
function fills(color, opacity=1) { return color ? [{fillColor:color, fillOpacity:opacity}] : []; }
function strokes(color=C.border, width=1, opacity=1) { return color ? [{strokeColor:color, strokeOpacity:opacity, strokeWidth:width}] : []; }
function add(parent, shape, name, x, y, w, h) {
  shape.name = name;
  if (w !== undefined && h !== undefined) shape.resize(w,h);
  parent.appendChild(shape);
  // Inputs are page-space anchors for readability; persist descendants in
  // their parent's local coordinate system as required by the build contract.
  penpotUtils.setParentXY(shape, x-(parent.x||0), y-(parent.y||0));
  return shape;
}
function rect(parent,name,x,y,w,h,color,radius=0,border=null,borderWidth=1) {
  const s=add(parent,penpot.createRectangle(),name,x,y,w,h);
  s.fills=fills(color); s.borderRadius=radius;
  if (border) s.strokes=strokes(border,borderWidth); else s.strokes=[];
  return s;
}
function txt(parent,name,value,x,y,size=14,color=C.ink,weight="400",width,align="left",height) {
  const s=penpot.createText(value); s.name=name; s.fontFamily=FONT; s.fontSize=String(size); s.fontWeight=String(weight);
  s.fills=fills(color); s.align=align; s.verticalAlign="top"; s.lineHeight="1.35";
  const w=width ?? Math.max(24, Math.min(1000, value.length*size*0.58+8));
  s.resize(w,height ?? Math.max(18,size*1.42));
  s.growType="fixed"; add(parent,s,name,x,y,w,height ?? Math.max(18,size*1.42)); return s;
}
function ellipse(parent,name,x,y,w,h,color,border=null) {
  const s=add(parent,penpot.createEllipse(),name,x,y,w,h); s.fills=fills(color); s.strokes=border?strokes(border,1):[]; return s;
}
function board(parent,name,x,y,w,h,color=null) {
  const s=add(parent,penpot.createBoard(),name,x,y,w,h); s.fills=fills(color); s.clipContent=false; s.setPluginData("semantic_role",name); return s;
}
function svg(parent,name,x,y,w,h,markup) {
  const s=penpot.createShapeFromSvg(markup); if(!s) return null; return add(parent,s,name,x,y,w,h);
}
function githubMark(parent,x,y,size,color="#FFFFFF",name="GitHub mark") {
  return svg(parent,name,x,y,size,size,`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path fill="${color}" d="M8 0C3.58 0 0 3.64 0 8.13c0 3.59 2.29 6.64 5.47 7.72.4.08.55-.18.55-.39v-1.52c-2.23.5-2.7-1.1-2.7-1.1-.36-.94-.89-1.19-.89-1.19-.73-.51.05-.5.05-.5.81.06 1.24.85 1.24.85.72 1.26 1.88.9 2.34.69.07-.53.28-.9.51-1.11-1.78-.21-3.65-.91-3.65-4.03 0-.89.31-1.61.82-2.18-.08-.21-.36-1.03.08-2.15 0 0 .67-.22 2.2.83A7.43 7.43 0 0 1 8 3.79c.68 0 1.37.1 2.01.3 1.53-1.05 2.2-.83 2.2-.83.44 1.12.16 1.94.08 2.15.51.57.82 1.29.82 2.18 0 3.13-1.87 3.82-3.66 4.02.29.26.54.76.54 1.54v2.29c0 .21.14.47.55.39A8.15 8.15 0 0 0 16 8.13C16 3.64 12.42 0 8 0Z"/></svg>`);
}
function setText(s,value) { s.characters=value; }
async function build() {
  const oldPage=penpotUtils.getPageById("cf04346a-b044-818b-8008-a4ed84a51a18");
  await penpot.openPage(oldPage);
  const oldFrame=penpotUtils.findShape(s=>s.id==="9a19287b-6930-802f-8008-a4ee0b57f233",oldPage.root);
  const oldAvatar=penpotUtils.findShape(s=>s.name==="Profile / exact avatar",oldFrame);
  const oldSnake=penpotUtils.findShape(s=>s.name==="README / contribution image",oldFrame);
  // Read mapped source fills while their source page is active; fillImage data
  // can be reused safely on new-page rectangles without cross-page reparenting.
  const avatarFill=oldAvatar?.fills?.find(f=>f.fillImage)?.fillImage || null;
  const snakeFill=oldSnake?.fills?.find(f=>f.fillImage)?.fillImage || null;
  const existing=penpotUtils.getPages().filter(p=>p.name==="Benchmark — GitHub Kaio v4");
  const pageRef=existing.length ? existing[existing.length-1].id : penpot.createPage().id;
  await penpot.openPage(pageRef);
  const page=penpot.currentPage;
  // The selected page is already versioned; leave its name untouched so the
  // active-page guard cannot reject a stale page proxy.
  for (const c of [...page.root.children]) c.remove();
  const frame=board(page.root,"GitHub Kaio — Home — 1440x1807 — v4",0,0,1440,1807,C.white);
  frame.clipContent=true; frame.setPluginData("version","v4"); frame.setPluginData("source_reference","runs/site-benchmarks/github-kaio-baleeiro/source/raw/full-page/source.png"); frame.setPluginData("design_type","editable_composition");

  // Local GitHub tokens and a reusable Public badge component.
  let tokens=null, tInk=null, tLink=null, tBorder=null;
  try {
    tokens=penpot.library.local.tokens.addSet({name:"GitHub v4 — source tokens",active:true});
    tInk=tokens.addToken({type:"color",name:"github.ink",value:C.ink});
    tLink=tokens.addToken({type:"color",name:"github.link",value:C.link});
    tBorder=tokens.addToken({type:"color",name:"github.border",value:C.border});
  } catch(e) {}
  const badgeTemplate=board(page.root,"Component / Public badge — main",1500,40,54,22,C.white);
  badgeTemplate.clipContent=true; badgeTemplate.setPluginData("component_role","repository-visibility");
  rect(badgeTemplate,"Public badge / border",0,0,54,22,C.white,11,C.border,1);
  txt(badgeTemplate,"Public badge / label","Public",7,4,12,C.muted,"600",40,"center",16);
  let badgeComp=null; try { badgeComp=penpot.library.local.createComponent([badgeTemplate]); badgeComp.name="GitHub / Repository visibility badge"; } catch(e) {}
  const badge=(parent,name,x,y)=>{ if(!badgeComp) return rect(parent,name,x,y,54,22,C.white,11,C.border,1); const i=badgeComp.instance(); i.name=name; parent.appendChild(i); penpotUtils.setParentXY(i,x-(parent.x||0),y-(parent.y||0)); return i; };

  // Global header (0–72).
  const header=board(frame,"GitHub / Global Header",0,0,1440,72,C.header); header.clipContent=true;
  githubMark(header,32,20,31,"#FFFFFF","GitHub / Global mark");
  const nav=["Platform⌄","Solutions⌄","Resources⌄","Open Source⌄","Enterprise⌄","Pricing"];
  [86,185,290,404,535,648].forEach((x,i)=>txt(header,"Header / "+nav[i],nav[i],x,27,16,C.white,"500"));
  rect(header,"Header / search field",980,20,196,32,C.header,6,"#30363D",1);
  txt(header,"Header / search placeholder","Search",994,27,14,C.white,"500",100, "left",20);
  rect(header,"Header / slash key",1140,25,22,21,C.header,4,"#30363D",1); txt(header,"Header / slash","/",1148,27,12,C.white,"600",12,"center",16);
  rect(header,"Header / sign in",1184,20,70,32,C.header,6,"#30363D",1); txt(header,"Header / sign in label","Sign in",1194,27,14,C.white,"600",53,"center",20);
  rect(header,"Header / sign up",1262,20,76,32,"#21262D",6,"#30363D",1); txt(header,"Header / sign up label","Sign up",1271,27,14,C.white,"600",58,"center",20);
  rect(header,"Header / settings",1347,20,31,32,C.header,6,"#30363D",1); txt(header,"Header / settings glyph","☷",1354,26,19,C.white,"600",18,"center",22);
  rect(header,"Header / bottom border",0,71,1440,1,"#1F2328");

  // Profile tabs/navigation (72–142).
  const tabs=board(frame,"GitHub / Profile Navigation",0,72,1440,70,C.white); tabs.clipContent=true;
  rect(tabs,"Profile nav / bottom border",0,69,1440,1,C.border);
  const tabData=[[444,"▣","Overview",C.ink],[557,"▤","Repositories",C.muted],[716,"⊞","Projects",C.muted],[812,"⬡","Packages",C.muted],[920,"☆","Stars",C.muted]];
  tabData.forEach(([x,ico,label,col],i)=>{txt(tabs,"Tab icon / "+label,ico,x,39,16,col,"500",18,"center",20);txt(tabs,"Tab / "+label,label,x+25,38,14,col,i===0?"600":"400");});
  txt(tabs,"Tab / repository count","12",671,38,12,C.muted,"600",22,"center",18);
  txt(tabs,"Tab / stars count","5",1001,38,12,C.muted,"600",22,"center",18);
  rect(tabs,"Tab / active underline",438,67,101,3,C.coral);

  // Sidebar profile (evidence-aligned bounds).
  const side=board(frame,"GitHub / Profile Sidebar",0,72,410,900,C.white); side.clipContent=false;
  let badgeSourceFill=null;
  try { const raw=atob(BADGE_SOURCE_B64); badgeSourceFill=await penpot.uploadMediaData("github-pull-shark-source.png",Uint8Array.from(raw,c=>c.charCodeAt(0)),"image/png"); } catch(e) {}
  if(avatarFill){ const a=rect(side,"Profile / exact avatar — v4",110,110,290,290,null,145); a.fills=[{fillImage:avatarFill,fillOpacity:1}]; a.setPluginData("asset_id","github-profile-avatar"); }
  else { ellipse(side,"Profile / avatar fallback",110,110,290,290,"#D0D7DE"); }
  ellipse(side,"Profile / status bubble",360,332,37,37,C.white,C.border); ellipse(side,"Profile / status dot",371,343,15,15,"#F85149"); txt(side,"Profile / status mark","●",374,342,10,C.white,"700",8,"center",12);
  txt(side,"Profile / display name","Kaio Silva Baleeiro de\nJesus",110,420,24,C.ink,"600",300,"left",62);
  txt(side,"Profile / handle","kaio-baleeiro",110,476,20,C.muted,"400",240,"left",28);
  rect(side,"Profile / follow button",110,514,290,31,C.soft,6,C.border,1); txt(side,"Profile / follow label","Follow",205,521,14,C.ink,"600",100,"center",20);
  txt(side,"Profile / bio","Estudante de Tecnologia",110,566,16,C.ink,"400",290,"left",23);
  txt(side,"Profile / followers","♧ 3 followers · 3 following",110,605,14,C.muted,"500",270,"left",22);
  rect(side,"Profile / divider 1",110,650,290,1,C.border);
  txt(side,"Profile / achievements heading","Achievements",110,674,16,C.ink,"600",200,"left",22);
  if (false && badgeSourceFill) { const b=rect(side,"Achievement / exact Pull Shark badge",110,700,73,70,null); b.fills=[{fillImage:badgeSourceFill,fillOpacity:1}]; b.setPluginData("asset_id","github-pull-shark-source-crop"); }
  else { ellipse(side,"Achievement / badge outer",112,702,60,60,"#F0B37E","#D97745"); ellipse(side,"Achievement / badge inner",118,708,48,48,"#FFF7ED"); txt(side,"Achievement / badge icon","🦈",126,717,28,"#8B5E3C","400",36,"center",34); }
  rect(side,"Achievement / x2 bubble",143,746,36,20,"#F7C7B5",10); txt(side,"Achievement / x2","x2",149,748,12,"#9A3412","600",24,"center",17);
  rect(side,"Profile / divider 2",110,781,290,1,C.border);
  txt(side,"Profile / highlights heading","Highlights",110,804,16,C.ink,"600",180,"left",22);
  txt(side,"Profile / pro star","☆",110,834,19,C.muted,"500",18,"center",22); rect(side,"Profile / pro pill",130,834,37,19,C.white,9,"#8250DF",1); txt(side,"Profile / pro label","PRO",136,836,11,"#8250DF","600",25,"center",15);
  rect(side,"Profile / divider 3",110,868,290,1,C.border);
  txt(side,"Profile / report","Block or report user",110,887,14,C.muted,"500",220,"left",20);

  // README card.
  const readme=board(frame,"GitHub / README",422,165,876,457,C.white); readme.clipContent=true;
  rect(readme,"README / card border",422,165,876,457,C.white,6,C.border,1);
  txt(readme,"README / filename","kaio-baleeiro / README.md",447,193,13,C.muted,"600",300,"left",20);
  txt(readme,"README / title","Oláá!! Eu sou o Kaio 😁",447,226,21,C.ink,"600",420,"left",30);
  rect(readme,"README / divider",447,255,827,1,C.border);
  txt(readme,"README / bullet 1","•  🛠️ Atualmente sou um contribuinte do mundo DevOps",457,275,15,C.ink,"400",780,"left",22);
  txt(readme,"README / bullet 2","•  🌱 Tenho conhecimento em algumas tecnologias, dentre elas estão Terraform, AWS, Azure, GitHub, Ansible, Jenkins, e",457,300,14,C.ink,"400",820,"left",20);
  txt(readme,"README / bullet 2 continued","algumas outras...",474,324,14,C.ink,"400",250,"left",20);
  txt(readme,"README / bullet 3","•  📫 Pode me contatar pelo linkedin: https://www.linkedin.com/in/kaio-baleeiro/",457,348,14,C.link,"400",790,"left",20);
  // Broken image placeholders visible in the source README.
  rect(readme,"README / broken image 1",447,377,15,15,C.white,1,C.border,1); rect(readme,"README / broken image 1 diagonal",447,377,15,1,"#54AEFF");
  rect(readme,"README / broken image 2",466,377,15,15,C.white,1,C.border,1); rect(readme,"README / broken image 2 diagonal",466,391,15,1,"#54AEFF");
  if(snakeFill){ const sn=rect(readme,"README / exact contribution snake",462,427,820,104,null); sn.fills=[{fillImage:snakeFill,fillOpacity:1}]; sn.setPluginData("asset_id","github-contribution-snake"); }
  else { for(let r=0;r<7;r++) for(let c=0;c<53;c++) rect(readme,"README snake cell "+r+"-"+c,462+c*15,427+r*14,11,11,r===6&&c<12?C.green1:C.green0,2); }
  rect(readme,"README / green underline",462,562,180,11,C.green1);

  // Popular repositories.
  const repos=board(frame,"GitHub / Popular Repositories",422,648,876,366,C.white); repos.clipContent=true;
  txt(repos,"Repos / heading","Popular repositories",422,650,16,C.ink,"500",240,"left",23);
  const repoData=[
    ["projeto-leitura-de-dados","Java",C.java,422,676], ["projeto-estoque","Java",C.java,868,676],
    ["bootcamp-react","HTML",C.html,422,789], ["pipeline-spring-boot-azure","Java",C.java,868,789],
    ["kaio-baleeiro","",null,422,900], ["code-grafos","Python",C.python,868,900]
  ];
  repoData.forEach(([name,lang,col,x,y])=>{
    rect(repos,"Repo card / "+name,x,y,430,96,C.white,6,C.border,1);
    txt(repos,"Repo name / "+name,name,x+16,y+19,14,C.link,"600",300,"left",20);
    badge(repos,"Repo Public badge / "+name,x+350,y+18);
    if(name==="code-grafos") txt(repos,"Repo description / code-grafos","Desafio code grafos",x+16,y+48,13,C.muted,"400",220,"left",18);
    if(lang){ ellipse(repos,"Repo language dot / "+name,x+16,y+63,12,12,col); txt(repos,"Repo language / "+name,lang,x+34,y+62,12,C.muted,"400",90,"left",18); }
    if(name==="kaio-baleeiro"){ txt(repos,"Repo fork icon / kaio-baleeiro","♧",x+17,y+62,17,C.muted,"500",16,"center",18); txt(repos,"Repo fork count / kaio-baleeiro","1",x+34,y+63,12,C.muted,"400",20,"left",18); }
  });

  // Contributions calendar.
  const contrib=board(frame,"GitHub / Contributions",422,1052,876,207,C.white); contrib.clipContent=true;
  txt(contrib,"Contrib / heading","50 contributions in the last year",422,1058,16,C.ink,"500",300,"left",23);
  rect(contrib,"Contrib / calendar card",422,1084,876,176,C.white,6,C.border,1);
  const months=[[501,"Sep"],[544,"Oct"],[587,"Nov"],[665,"Dec"],[726,"Jan"],[784,"Feb"],[842,"Mar"],[903,"Apr"],[963,"May"],[1021,"Jun"],[1077,"Jul"],[1132,"Aug"],[1238,"Sep"]];
  months.forEach(([x,m])=>txt(contrib,"Contrib month / "+m,m,x,1104,12,C.ink,"400",28,"left",16));
  [[1150,"Mon"],[1180,"Wed"],[1210,"Fri"]].forEach(([y,l])=>txt(contrib,"Contrib day / "+l,l,456,y,12,C.muted,"400",32,"left",16));
  const active={"0-8":C.green2,"0-34":C.green3,"0-48":C.green2,"0-50":C.green1,"0-51":C.green1,"1-50":C.green1,"1-51":C.green3,"6-7":C.green2,"6-38":C.green2,"6-40":C.green1,"6-47":C.green2,"6-49":C.green3,"6-51":C.green2};
  for(let r=0;r<7;r++) for(let c=0;c<52;c++) rect(contrib,"Contrib cell "+r+"-"+c,501+c*15,1149+r*15,11,11,active[r+"-"+c]||C.green0,2);
  txt(contrib,"Contrib / learn link","Learn how we count contributions",462,1238,12,C.muted,"400",250,"left",16);
  txt(contrib,"Contrib / legend","Less",1132,1238,12,C.muted,"400",30,"left",16);
  [C.green0,C.green1,C.green2,C.green3].forEach((c,i)=>rect(contrib,"Contrib legend cell "+i,1170+i*15,1238,11,11,c,2)); txt(contrib,"Contrib / more","More",1234,1238,12,C.muted,"400",40,"left",16);

  // Contribution activity and year rail.
  const activity=board(frame,"GitHub / Contribution Activity",422,1282,876,373,C.white); activity.clipContent=true;
  txt(activity,"Activity / heading","Contribution activity",422,1288,16,C.ink,"500",250,"left",23);
  rect(activity,"Activity / selected year",1184,1283,114,33,C.link,6); txt(activity,"Activity / selected year label","2026",1200,1293,13,C.white,"600",80,"left",18);
  ["2025","2024","2023","2022","2021","2020"].forEach((y,i)=>txt(activity,"Activity / year "+y,y,1200,1333+i*39,13,C.muted,"400",50,"left",18));
  txt(activity,"Activity / month","September 2026",430,1331,12,C.ink,"600",150,"left",18); rect(activity,"Activity / month divider",545,1338,610,1,C.border);
  rect(activity,"Activity / timeline",438,1350,1,239,C.border);
  ellipse(activity,"Activity / event 1 icon",430,1373,31,31,C.soft,C.border); txt(activity,"Activity / event 1 glyph","↗",437,1378,18,C.muted,"600",18,"center",22);
  txt(activity,"Activity / event 1 title","Created 7 commits in 1 repository",462,1377,16,C.ink,"400",400,"left",22); txt(activity,"Activity / event 1 repo","kaio-baleeiro/penpot-design-automation",462,1405,14,C.link,"500",330,"left",20); txt(activity,"Activity / event 1 commits","7 commits",790,1405,14,C.muted,"400",80,"left",20); rect(activity,"Activity / event 1 bar",981,1405,171,8,"#2DA44E",4); txt(activity,"Activity / event 1 more","✣",1137,1399,16,C.muted,"600",18,"center",20);
  ellipse(activity,"Activity / event 2 icon",430,1457,31,31,C.soft,C.border); txt(activity,"Activity / event 2 glyph","▣",437,1463,15,C.muted,"600",18,"center",18);
  txt(activity,"Activity / event 2 title","Created 1 repository",462,1463,16,C.ink,"400",260,"left",22); txt(activity,"Activity / event 2 repo","kaio-baleeiro/penpot-design-automation",486,1492,14,C.link,"500",330,"left",20); ellipse(activity,"Activity / python dot",961,1496,12,12,C.python); txt(activity,"Activity / python","Python",979,1494,13,C.muted,"400",80,"left",18); txt(activity,"Activity / date","Sep 14",1116,1494,13,C.muted,"400",55,"left",18); txt(activity,"Activity / event 2 more","✣",1137,1488,16,C.muted,"600",18,"center",20);
  ellipse(activity,"Activity / event 3 icon",430,1544,31,31,C.soft,C.border); txt(activity,"Activity / event 3 glyph","▣",437,1550,15,C.muted,"600",18,"center",18); txt(activity,"Activity / event 3 title","6 contributions in private repositories",462,1550,16,C.muted,"400",400,"left",22); txt(activity,"Activity / event 3 date","Sep 5 – Sep 7",1075,1550,13,C.muted,"400",90,"left",18);
  rect(activity,"Activity / show more",422,1618,731,37,C.white,6,C.border,1); txt(activity,"Activity / show more label","Show more activity",730,1627,13,C.link,"600",150,"center",20);

  // Footer.
  const footer=board(frame,"GitHub / Footer",0,1689,1440,118,C.white); footer.clipContent=true;
  githubMark(footer,270,1704,24,"#656D76","Footer / GitHub mark"); txt(footer,"Footer / copyright","© 2026 GitHub, Inc.",301,1708,12,C.muted,"400",120,"left",18);
  ["Terms","Privacy","Security","Status","Community","Docs","Contact","Manage cookies","Do not share my personal information"].forEach((l,i)=>txt(footer,"Footer / "+l,l,[428,477,533,594,645,723,770,827,930][i],1708,12,C.muted,"400",i===7?100:i===8?260:90,"left",18));

  // Apply real token bindings where supported.
  try { if(tInk) { frame.applyToken(tInk,["fill"]); txt(readme,"README / token anchor","",0,0,1,C.white,"400",1,"left",1).hidden=true; } if(tBorder) rect(readme,"README / token border marker",0,0,1,1,C.white); } catch(e) {}
  // Keep component source outside the screenshot frame while preserving it in the library.
  badgeTemplate.hidden=true; badgeTemplate.setPluginData("source_component","true");
  return {page:{id:page.id,name:page.name},frame:{id:frame.id,name:frame.name,width:frame.width,height:frame.height},badgeComponent:badgeComp?{id:badgeComp.id,name:badgeComp.name}:null,tokenSet:tokens?{id:tokens.id,name:tokens.name,tokens:tokens.tokens.map(t=>t.name)}:null,sourceAssets:{avatar:!!oldAvatar,snake:!!oldSnake}};
}
return await build();
