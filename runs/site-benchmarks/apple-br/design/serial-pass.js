/* Serial MCP pass for Apple BR v4. Run only while this page is active and no
   other benchmark worker is mutating the shared Penpot connection. */
const PAGE_ID = 'b9b9f43f-1dd3-801e-8008-a6714b37dc3b';
const FRAME_ID = 'b9b9f43f-1dd3-801e-8008-a67202c01eef';

await penpot.openPage(PAGE_ID);
const frame = penpotUtils.findShape(s => s.id === FRAME_ID);
if (!frame) throw new Error('Apple BR v4 frame not found');

// Preserve the rendered page coordinates while making every nested child
// explicit in its parent's local coordinate system.
function normalize(parent) {
  for (const child of [...(parent.children || [])]) {
    const localX = child.bounds.x - parent.bounds.x;
    const localY = child.bounds.y - parent.bounds.y;
    penpotUtils.setParentXY(child, localX, localY);
    if (child.children?.length) normalize(child);
  }
}
normalize(frame);

// Apply a font actually present in this file; do not leave unresolved text
// glyphs in the export. SF Pro remains the source reference, while Inter is
// the available runtime fallback recorded in visual-spec.json.
const font = (penpot.fonts.all || []).find(f => f.name === 'Inter') ||
  (penpot.fonts.all || []).find(f => f.name === 'Inter Tight');
if (font) {
  for (const text of penpotUtils.findShapes(s => s.type === 'text', frame)) {
    font.applyToText(text);
  }
}

// Create real local-library component masters and instances out of clones,
// kept off-canvas/hidden so the source-faithful visible composition remains
// unchanged. The visible boards remain editable content descendants.
const componentNames = [
  'Apple / Global Navigation — v4',
  'Apple / Hero Product — v4',
  'Apple / Promo Tile — v4',
  'Apple / TV Card — v4',
  'Apple / Footer — v4'
];
const sourceBoards = [frame.children[0], frame.children[1], frame.children[4], frame.children[10], frame.children[11]];
const componentRecords = [];
for (let i = 0; i < sourceBoards.length; i++) {
  const clone = sourceBoards[i].clone();
  clone.x = 1700;
  clone.y = i * 760;
  clone.hidden = true;
  penpot.root.appendChild(clone);
  const component = penpot.library.local.createComponent([clone]);
  component.name = componentNames[i];
  const instance = component.instance();
  instance.name = componentNames[i] + ' / Instance';
  instance.x = 1700;
  instance.y = i * 760 + 420;
  instance.hidden = true;
  penpot.root.appendChild(instance);
  componentRecords.push({name: component.name, main_id: component.mainInstance()?.id || null, instance_id: instance.id});
}

// Add real tokens once, preserving a rerunnable serial pass.
let tokenSet = (penpot.library.local.tokens.sets || []).find(s => s.name === 'Apple BR v4');
if (!tokenSet) tokenSet = penpot.library.local.tokens.addSet({name: 'Apple BR v4'});
if (!tokenSet.active) tokenSet.toggleActive();
const tokenDefs = [
  {type: 'color', name: 'color.apple.black', value: '#000000'},
  {type: 'color', name: 'color.apple.surface', value: '#F5F5F7'},
  {type: 'color', name: 'color.apple.link', value: '#0071E3'},
  {type: 'dimension', name: 'space.section', value: '12px'},
  {type: 'borderRadius', name: 'radius.tile', value: '24px'}
];
const tokenRecords = [];
for (const def of tokenDefs) {
  let token = (tokenSet.tokens || []).find(t => t.name === def.name);
  if (!token) token = tokenSet.addToken(def);
  tokenRecords.push({name: token.name, type: token.type, value: token.value});
}

return {page_id: PAGE_ID, frame_id: FRAME_ID, componentRecords, tokenRecords};
