const p=penpot.currentFile.pages.find(x=>x.id==="b9b9f43f-1dd3-801e-8008-a67636574e02");
await penpot.openPage(p);
const f=penpotUtils.findShape(x=>x.id==="b9b9f43f-1dd3-801e-8008-a67636745b0f",p.root);
const news=penpotUtils.findShape(x=>x.name==="News & Updates",f);
const heading=penpotUtils.findShape(x=>x.name==="News / heading",f);heading.y=1729;
for(let i=1;i<=4;i++){
  const card=penpotUtils.findShape(x=>x.name==="News / card "+i,f);
  card.y=i<=2?1829:2329;
  card.fills=[{fillColor:"#08090D",fillOpacity:1}];
}
const seeAll=penpotUtils.findShape(x=>x.name==="News / SEE ALL",f);seeAll.y=2700;
const seeAllLabel=penpotUtils.findShape(x=>x.name==="News / SEE ALL label",f);seeAllLabel.y=2713;
for(let i=1;i<=3;i++){
  const shop=penpotUtils.findShape(x=>x.name==="Shop / product "+i,f);if(shop)shop.fills=[{fillColor:"#08090D",fillOpacity:1}];
  const guide=penpotUtils.findShape(x=>x.name==="Guides / card "+i,f);if(guide)guide.fills=[{fillColor:"#08090D",fillOpacity:1}];
}
const extra=penpotUtils.findShape(x=>x.name==="Instance / Learn More Card",f);if(extra)extra.hidden=true;
async function fillShape(shape,url,name){shape.fills=[{fillImage:await penpot.uploadMediaUrl(name,url),fillOpacity:1}];shape.setPluginData("asset_status","uploaded_to_penpot");}
const socialUrls=[
  "https://www-static.warframe.com/images/icons/material/facebook.svg",
  "https://www-static.warframe.com/images/icons/material/instagram.svg",
  "https://www-static.warframe.com/images/icons/material/twitter.svg",
  "https://www-static.warframe.com/images/icons/material/bluesky.svg",
  "https://www-static.warframe.com/images/icons/material/discord.svg",
  "https://www-static.warframe.com/images/icons/material/twitch.svg",
  "https://www-static.warframe.com/images/icons/material/youtube.svg",
  "https://www-static.warframe.com/images/icons/material/vkontakte.svg"
];
for(let i=0;i<8;i++){const s=penpotUtils.findShape(x=>x.name==="Social icon "+i,f);await fillShape(s,socialUrls[i],"social-"+i+".cycle3");}
const rating=penpotUtils.findShape(x=>x.name==="Asset / rating mark",f);await fillShape(rating,"https://www-static.warframe.com/images/footer/ratings/classind.jpg","classind.cycle3");
return {frame:f.id,newsCards:4,hiddenExtra:!!extra,socialIcons:8,rating:true};
