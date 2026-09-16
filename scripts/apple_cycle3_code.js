const page = penpotUtils.getPageByName("Benchmark — Apple BR v2");
await penpot.openPage(page);
const frame = penpotUtils.findShape(s => s.id === "9a19287b-6930-802f-8008-a4f18603c814", page.root);
const heroes = [
  ["Apple / iPhone 18 Pro", "Apple / exact iPhone 18 Pro hero"],
  ["Apple / iPhone Duo", "Apple / exact iPhone Duo hero"],
  ["Apple / Apple Watch Series 12", "Apple / exact Watch Series 12 hero"]
];
for (const [boardName, assetName] of heroes) {
  const board = frame.children.find(s => s.name === boardName);
  const asset = board && board.children.find(s => s.name === assetName);
  if (board && asset) {
    asset.resize(1800, 1000);
    asset.x = board.x - 180;
    asset.y = board.y - 154;
    asset.setPluginData("image_fit", "cover_crop");
  }
}
const tv = frame.children.find(s => s.name === "Apple / TV+ Gallery");
if (tv) {
  const cards = tv.children.filter(s => s.name && s.name.indexOf("TV / card") === 0);
  const positions = [[0, 280, 300], [255, 930, 330], [1200, 280, 300]];
  for (let i = 0; i < cards.length; i++) {
    if (i < 3) {
      cards[i].hidden = false;
      cards[i].x = positions[i][0];
      cards[i].y = tv.y + 84;
      cards[i].resize(positions[i][1], positions[i][2]);
    } else {
      cards[i].hidden = true;
    }
  }
}
return {
  frame: frame.id,
  heroes: heroes.map(([b,a]) => ({board:b, asset:a, crop:"1800x1000"})),
  tvCarousel: "main 930px Mayday card with 280px side previews",
  status: "cycle-3-build"
};
