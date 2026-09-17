const p=penpot.currentFile.pages.find(x=>x.id==="b9b9f43f-1dd3-801e-8008-a6714b37dc3b");
await penpot.openPage(p);
const f=penpotUtils.findShape(x=>x.id==="b9b9f43f-1dd3-801e-8008-a67202c01eef",p.root);
const assets=[
  ["Apple / iPhone 18 Pro / exact source asset","https://www.apple.com/v/homepage/images/iphone-18-pro/a/hero_iphone_18_pro_preorder__dd68unjbzswi_large.jpg"],
  ["Apple / iPhone Duo / exact source asset","https://www.apple.com/br/homepage/built/heroes/26_iphone-duo_09/images/hero_iphone_duo_announce__fh4u8yzndpe2_large.jpg"],
  ["Apple / Apple Watch Series 12 / exact source asset","https://www.apple.com/br/homepage/built/heroes/26_apple-watch-series-12_09/images/hero_apple_watch_series_12_preorder__cv2wd7ow8926_large.jpg"],
  ["TV / card Mayday","https://is1-ssl.mzstatic.com/image/thumb/0VbaTTVC5_5511h5ESrOLw/1960x1044sr.jpg"],
  ["TV / card Silo","https://is1-ssl.mzstatic.com/image/thumb/1IEuXkMS1Hdhs7bES88SAg/1960x1044sr.jpg"],
  ["TV / card Matéria Escura","https://is1-ssl.mzstatic.com/image/thumb/ZUCp6pyyffalTQpg4UESLQ/1960x1044sr.jpg"]
];
for(const [name,url] of assets){
  const s=penpotUtils.findShape(q=>q.name===name,f);
  if(!s) throw new Error("missing asset shape: "+name);
  const media=await penpot.uploadMediaUrl(name+".v4-cycle3",url);
  s.fills=[{fillImage:media,fillOpacity:1}];
  s.setPluginData("asset_status","uploaded_to_penpot");
}
for(const [name,x,y] of [
  ["Apple / iPhone 18 Pro / exact source asset",-180,-110],
  ["Apple / iPhone Duo / exact source asset",-180,594],
  ["Apple / Apple Watch Series 12 / exact source asset",-180,1298]
]){
  const s=penpotUtils.findShape(q=>q.name===name,f);
  s.x=x; s.y=y; s.resize(1800,1000);
}
for(const board of penpotUtils.findShapes(q=>q.type==="board",f)){
  for(const child of [...(board.children||[])].filter(q=>q.type==="text")) board.appendChild(child);
}
return {frame:f.id,refreshed:assets.map(a=>a[0])};
