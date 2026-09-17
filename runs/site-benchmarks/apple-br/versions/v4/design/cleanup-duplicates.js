/* Run only after reviewing the result of the inventory below. This removes
   only empty duplicate Apple BR v4 pages; it never touches v2/v3. */
const pages = penpotUtils.getPages().filter(p => p.name === 'Benchmark — Apple BR v4');
const target = pages.find(p => p.id === 'b9b9f43f-1dd3-801e-8008-a6714b37dc3b');
if (!target) throw new Error('Final Apple BR v4 page not found');
const duplicates = pages.filter(p => p.id !== target.id);
const inventory = duplicates.map(p => ({id: p.id, child_count: p.root.children?.length || 0}));
for (const p of duplicates) {
  if ((p.root.children?.length || 0) === 0) p.remove();
}
return {kept: {id: target.id, name: target.name}, inspected: inventory, removed: inventory.filter(x => x.child_count === 0)};
