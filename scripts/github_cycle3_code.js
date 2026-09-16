const page = penpotUtils.getPageByName("Benchmark — GitHub Kaio");
await penpot.openPage(page);
const frame = penpotUtils.findShape(s => s.id === "9a19287b-6930-802f-8008-a4ee0b57f233", page.root);
const sections = penpotUtils.findShapes(s => s.type === "board", frame);
for (const board of sections) {
  if (board.name !== "GitHub / Global Header" && board.name !== "GitHub / Profile Overview") {
    board.fills = [];
  }
}
const readme = sections.find(s => s.name === "GitHub / README");
if (readme) {
  const ref = penpotUtils.findShape(s => s.name === "README / contribution image", readme);
  if (ref) {
    try {
      const data = await penpot.uploadMediaUrl("github-contribution-snake.svg", "https://github.com/kaio-baleeiro/kaio-baleeiro/raw/output/github-contribution-grid-snake.svg");
      ref.fills = [{fillImage: data, fillOpacity: 1}];
      ref.setPluginData("asset_id", "github-contribution-snake");
    } catch (e) {
      ref.setPluginData("asset_status", "unavailable");
    }
  }
}
return {
  page: page.name,
  frame: frame.id,
  boards: sections.map(s => ({name:s.name, y:s.y, height:s.height, fillCount:s.fills.length})),
  status: "cycle-3-build"
};
