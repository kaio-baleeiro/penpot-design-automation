/* GitHub Kaio v4 cycle 3 — restore the clipped profile navigation. */
const page = penpot.currentFile.pages.find(
  candidate => candidate.id === "b9b9f43f-1dd3-801e-8008-a6725d4e8fbd"
);
await penpot.openPage(page);
const frame = penpotUtils.findShape(
  shape => shape.id === "b9b9f43f-1dd3-801e-8008-a6741a129cb3",
  page.root
);
const tabs = penpotUtils.findShape(
  shape => shape.name === "GitHub / Profile Navigation",
  frame
);

const localPositions = {
  "Profile nav / bottom border": [0, 69],
  "Tab icon / Overview": [444, 39],
  "Tab / Overview": [469, 38],
  "Tab icon / Repositories": [557, 39],
  "Tab / Repositories": [582, 38],
  "Tab icon / Projects": [716, 39],
  "Tab / Projects": [741, 38],
  "Tab icon / Packages": [812, 39],
  "Tab / Packages": [837, 38],
  "Tab icon / Stars": [920, 39],
  "Tab / Stars": [945, 38],
  "Tab / repository count": [671, 38],
  "Tab / stars count": [1001, 38],
  "Tab / active underline": [438, 67]
};

const changed = [];
for (const [name, [x, y]] of Object.entries(localPositions)) {
  const shape = penpotUtils.findShape(candidate => candidate.name === name, tabs);
  if (!shape) continue;
  penpotUtils.setParentXY(shape, x, y);
  shape.hidden = false;
  changed.push({id: shape.id, name, x, y});
}

tabs.clipContent = true;
tabs.setPluginData("cycle_3_fix", "profile-navigation-local-coordinates");
return {page: page.id, frame: frame.id, changed};
