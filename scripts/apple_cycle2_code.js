const page = penpotUtils.getPageByName("Benchmark — Apple BR v2");
await penpot.openPage(page);
const frame = penpotUtils.findShape(s => s.id === "9a19287b-6930-802f-8008-a4f18603c814", page.root);
const promos = penpotUtils.findShapes(s => s.name && s.name.indexOf("Apple / Promo /") === 0, frame);
const tilePairs = [
  ["Apple / Promo / Apple Watch Ultra 4", 0, "https://www.apple.com/br/homepage/built/promos/26_apple-watch-ultra-4_09/images/promo_apple_watch_ultra_4_preorder__fvnta8sy0wa6_large.jpg"],
  ["Apple / Promo / AirPods 5", 738, "https://www.apple.com/v/homepage/images/airpods-5/a/promo_airpods_5_preorder__lydvte0llb6i_large.jpg"],
  ["Apple / Promo / MacBook Air", 0, "https://www.apple.com/v/homepage/images/macbook-air-m5/a/promo_macbook_air_m5__e5xk2yysqiie_large.jpg"],
  ["Apple / Promo / AirPods Pro 3", 738, "https://www.apple.com/v/homepage/images/airpods-pro-3/a/promo_airpods_pro_3__e4755qofhnyq_large.jpg"],
  ["Apple / Promo / iPad Air", 0, "https://www.apple.com/v/homepage/images/ipad-air-m4/a/promo_ipad_air_m4__bgcv7t286k8y_large.jpg"],
  ["Apple / Promo / MacBook Pro", 738, "https://www.apple.com/v/homepage/images/macbook-air-m5/a/promo_macbook_air_m5__e5xk2yysqiie_large.jpg"]
];
for (const [name, x, url] of tilePairs) {
  const board = promos.find(s => s.name === name);
  if (!board) continue;
  board.x = x;
  board.resize(702, 580);
  const asset = board.children.find(s => s.name && s.name.indexOf("Apple / exact") === 0);
  if (asset) {
    try {
      const data = await penpot.uploadMediaUrl(name + ".asset", url);
      asset.resize(702, 580);
      asset.x = board.x;
      asset.y = board.y;
      asset.fills = [{fillImage: data, fillOpacity: 1}];
      asset.setPluginData("source_asset_url", url);
    } catch (e) {
      asset.setPluginData("asset_status", "unavailable");
    }
  }
}
const tv = penpotUtils.findShape(s => s.name === "Apple / TV+ Gallery", frame);
const tvUrls = [
  "https://is1-ssl.mzstatic.com/image/thumb/0VbaTTVC5_5511h5ESrOLw/1960x1044sr.jpg",
  "https://is1-ssl.mzstatic.com/image/thumb/1IEuXkMS1Hdhs7bES88SAg/1960x1044sr.jpg",
  "https://is1-ssl.mzstatic.com/image/thumb/ZUCp6pyyffalTQpg4UESLQ/1960x1044sr.jpg",
  "https://is1-ssl.mzstatic.com/image/thumb/hRaOrIKahRFcNlKt6UV4Ow/1960x1044sr.jpg",
  "https://is1-ssl.mzstatic.com/image/thumb/plPQbHn4gzuGfTN4BEEX0Q/1960x1044sr.jpg",
  "https://is1-ssl.mzstatic.com/image/thumb/rWbGmWMxHKMgE2w-Xi_1Ag/1960x1044sr.jpg"
];
if (tv) {
  const cards = tv.children.filter(s => s.name && s.name.indexOf("TV / card") === 0);
  for (let i = 0; i < cards.length; i++) {
    try {
      const data = await penpot.uploadMediaUrl("apple-tv-" + i + ".jpg", tvUrls[i]);
      cards[i].fills = [{fillImage: data, fillOpacity: 1}];
      cards[i].setPluginData("source_asset_url", tvUrls[i]);
      cards[i].setPluginData("asset_id", ["apple-tv-mayday","apple-tv-silo","apple-tv-materia-escura","apple-tv-desaparecida","apple-tv-slow-horses","apple-tv-widows-bay"][i]);
    } catch (e) {
      cards[i].setPluginData("asset_status", "unavailable");
    }
  }
}
return {frame: frame.id, promoBoards: promos.map(s => ({name:s.name,x:s.x,width:s.width,height:s.height})), tvCards: tv ? tv.children.filter(s=>s.name && s.name.indexOf("TV / card")===0).length : 0, status:"cycle-2-build"};
