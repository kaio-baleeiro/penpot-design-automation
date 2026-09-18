/*
 * Rebuild benchmark pages as editable Penpot compositions.
 * This file is executed through the Penpot MCP execute_code tool. It intentionally
 * creates boards, rectangles, text and image fills instead of using a full-page
 * screenshot as the frame content.
 */

const FONT = "sourcesanspro";

function fill(color, opacity = 1) {
  return color ? [{ fillColor: color, fillOpacity: opacity }] : [];
}

function put(parent, shape, name, x, y, w, h) {
  shape.name = name;
  // Penpot stores child coordinates in page space; translate the local
  // section coordinates so the editable content lands inside its board.
  shape.x = x + (parent.x || 0);
  shape.y = y + (parent.y || 0);
  if (w !== undefined && h !== undefined) shape.resize(w, h);
  parent.appendChild(shape);
  return shape;
}

function rect(parent, name, x, y, w, h, color, radius = 0, opacity = 1) {
  const shape = put(parent, penpot.createRectangle(), name, x, y, w, h);
  shape.fills = fill(color, opacity);
  shape.borderRadius = radius;
  return shape;
}

function text(parent, name, value, x, y, size, color, weight = "400", align = "left") {
  const shape = penpot.createText(value);
  shape.name = name;
  shape.fontFamily = FONT;
  shape.fontSize = String(size);
  shape.fontWeight = String(weight);
  shape.fills = fill(color);
  shape.align = align;
  shape.verticalAlign = "top";
  shape.growType = "auto-height";
  // Give every text node an editable, readable box. Without an explicit
  // width Penpot leaves a newly-created text shape at 1px and it disappears
  // from exports even though the characters are present.
  shape.resize(Math.max(60, Math.min(1000, value.length * size * 0.62 + 16)), Math.max(22, size * 1.45));
  shape.x = x + (parent.x || 0);
  shape.y = y + (parent.y || 0);
  parent.appendChild(shape);
  return shape;
}

async function image(parent, name, x, y, w, h, url, opacity = 1) {
  const shape = penpot.createRectangle();
  shape.name = name;
  shape.x = x + (parent.x || 0);
  shape.y = y + (parent.y || 0);
  shape.resize(w, h);
  try {
    const data = await penpot.uploadMediaUrl(name + ".asset", url);
    shape.fills = [{ fillImage: data, fillOpacity: opacity }];
  } catch (error) {
    shape.fills = fill("#303846", opacity);
    shape.setPluginData("asset_status", "unavailable");
  }
  parent.appendChild(shape);
  return shape;
}

function section(frame, name, y, h, color) {
  const board = penpot.createBoard();
  board.name = name;
  board.x = 0;
  board.y = y;
  board.resize(1440, h);
  board.fills = fill(color);
  board.clipContent = true;
  board.setPluginData("semantic_role", name);
  frame.appendChild(board);
  return board;
}

async function clearPage(pageName, frameName, width, height, background) {
  const page = penpotUtils.getPageByName(pageName);
  if (!page) throw new Error("Missing page: " + pageName);
  await penpot.openPage(page);
  const frame = penpotUtils.findShape(s => s.name === frameName, page.root);
  if (!frame) throw new Error("Missing frame: " + frameName);
  for (const child of [...page.root.children]) {
    if (child.id !== frame.id) child.remove();
  }
  for (const child of [...frame.children]) child.remove();
  frame.x = 0;
  frame.y = 0;
  frame.resize(width, height);
  frame.name = frameName;
  frame.fills = fill(background);
  frame.clipContent = true;
  frame.setPluginData("design_type", "editable-composition");
  frame.setPluginData("reference_only", "false");
  return { page, frame };
}

async function buildApple() {
  const { page, frame } = await clearPage(
    "Benchmark — Apple BR",
    "Apple BR — Home — 1440x5261",
    1440, 5261, "#F5F5F7"
  );


  const nav = section(frame, "Apple / Global Navigation", 0, 52, "#FFFFFF");
  text(nav, "Apple mark", "", 76, 15, 22, "#1D1D1F", "600");
  ["Store", "Mac", "iPad", "iPhone", "Watch", "AirPods", "TV & Home", "Entertainment", "Accessories", "Support"].forEach((item, i) => text(nav, "Nav / " + item, item, 144 + i * 104, 19, 12, "#1D1D1F"));
  text(nav, "Search", "⌕", 1265, 15, 20, "#1D1D1F");
  text(nav, "Bag", "⌑", 1322, 15, 19, "#1D1D1F");

  const hero = section(frame, "Apple / Hero / iPhone 16 Pro", 52, 760, "#000000");
  text(hero, "Hero eyebrow", "iPhone 16 Pro", 0, 86, 46, "#F5F5F7", "600", "center").resize(1440, 64);
  text(hero, "Hero subtitle", "Titanium. So strong. So light. So Pro.", 0, 150, 22, "#D2D2D7", "400", "center").resize(1440, 36);
  text(hero, "Hero primary CTA", "Learn more  ›", 600, 208, 17, "#2997FF", "400");
  text(hero, "Hero secondary CTA", "Buy  ›", 790, 208, 17, "#2997FF", "400");
  rect(hero, "Hero / gradient glow", 390, 250, 660, 440, "#1B1B1F", 220, 0.55);
  rect(hero, "Apple / Hero / editable product silhouette", 505, 318, 430, 285, "#3A3A3C", 38);
  rect(hero, "Apple / Hero / editable product screen", 540, 350, 360, 210, "#121214", 24);
  rect(hero, "Apple / Hero / editable product highlight", 600, 380, 240, 16, "#68686E", 8);

  const iphone = section(frame, "Apple / Promo / iPhone 16", 812, 720, "#FFFFFF");
  text(iphone, "iPhone heading", "iPhone 16", 0, 72, 42, "#1D1D1F", "600", "center").resize(1440, 56);
  text(iphone, "iPhone subtitle", "Hello, Apple Intelligence.", 0, 132, 21, "#424245", "400", "center").resize(1440, 32);
  text(iphone, "iPhone CTA", "Learn more  ›     Buy  ›", 0, 182, 16, "#0066CC", "400", "center").resize(1440, 26);
  rect(iphone, "Apple / Promo / editable iPhone silhouette", 548, 248, 344, 365, "#2B2B2E", 42);
  rect(iphone, "Apple / Promo / editable iPhone screen", 570, 270, 300, 320, "#DCE8F5", 28);
  rect(iphone, "Apple / Promo / editable iPhone camera", 642, 286, 156, 18, "#73869A", 9);

  const mac = section(frame, "Apple / Promo / MacBook Air", 1532, 720, "#DDEBFA");
  text(mac, "Mac heading", "MacBook Air", 0, 72, 42, "#1D1D1F", "600", "center").resize(1440, 56);
  text(mac, "Mac subtitle", "Supercharged by the M4 chip.", 0, 132, 21, "#424245", "400", "center").resize(1440, 32);
  text(mac, "Mac CTA", "Learn more  ›     Buy  ›", 0, 182, 16, "#0066CC", "400", "center").resize(1440, 26);
  rect(mac, "Mac / laptop silhouette", 270, 310, 900, 280, "#B7CBE1", 32);
  rect(mac, "Mac / display", 312, 338, 816, 215, "#F5F5F7", 18);
  rect(mac, "Mac / display highlight", 360, 375, 720, 130, "#D7E9FF", 10);
  text(mac, "Mac / display label", "M4", 0, 426, 48, "#5B77A0", "600", "center").resize(1440, 56);

  const ipad = section(frame, "Apple / Promo / iPad Air", 2252, 720, "#F7F7F7");
  text(ipad, "iPad heading", "iPad Air", 0, 72, 42, "#1D1D1F", "600", "center").resize(1440, 56);
  text(ipad, "iPad subtitle", "Fresh air. Fresh colors. Fresh possibilities.", 0, 132, 21, "#424245", "400", "center").resize(1440, 32);
  text(ipad, "iPad CTA", "Learn more  ›     Buy  ›", 0, 182, 16, "#0066CC", "400", "center").resize(1440, 26);
  ["#9CC7E8", "#D9A8CB", "#E3B98A", "#B5D8C3"].forEach((c, i) => rect(ipad, "iPad / color card " + i, 225 + i * 250, 292 + (i % 2) * 34, 188, 306, c, 26));
  text(ipad, "iPad / color label", "A15", 0, 430, 30, "#FFFFFF", "600", "center").resize(1440, 40);

  const watch = section(frame, "Apple / Promo / Apple Watch", 2972, 720, "#000000");
  text(watch, "Watch heading", " WATCH", 0, 74, 38, "#FFFFFF", "600", "center").resize(1440, 48);
  text(watch, "Watch subtitle", "Thinstant classic.", 0, 134, 22, "#D2D2D7", "400", "center").resize(1440, 32);
  text(watch, "Watch CTA", "Learn more  ›     Buy  ›", 0, 182, 16, "#2997FF", "400", "center").resize(1440, 26);
  rect(watch, "Watch / case", 585, 270, 270, 270, "#6C6C70", 72);
  rect(watch, "Watch / screen", 618, 303, 204, 204, "#111111", 54);
  text(watch, "Watch / time", "10:09", 0, 375, 34, "#FFFFFF", "400", "center").resize(1440, 44);

  const airpods = section(frame, "Apple / Promo / AirPods", 3692, 720, "#FFFFFF");
  text(airpods, "AirPods heading", "AirPods Pro 2", 0, 72, 42, "#1D1D1F", "600", "center").resize(1440, 56);
  text(airpods, "AirPods subtitle", "Hearing health features built in.", 0, 132, 21, "#424245", "400", "center").resize(1440, 32);
  text(airpods, "AirPods CTA", "Learn more  ›     Buy  ›", 0, 182, 16, "#0066CC", "400", "center").resize(1440, 26);
  rect(airpods, "AirPods / case", 520, 300, 400, 240, "#E9E9EB", 110);
  rect(airpods, "AirPods / lid", 542, 320, 356, 80, "#FFFFFF", 36);
  rect(airpods, "AirPods / left bud", 600, 405, 70, 120, "#FFFFFF", 35);
  rect(airpods, "AirPods / right bud", 770, 405, 70, 120, "#FFFFFF", 35);

  const services = section(frame, "Apple / Services and Stories", 4412, 650, "#F5F5F7");
  text(services, "Services heading", "The Apple experience.", 80, 72, 36, "#1D1D1F", "600");
  text(services, "Services intro", "Discover services, entertainment and support designed around you.", 80, 132, 20, "#424245");
  ["Apple TV+", "Apple Music", "Apple Arcade", "iCloud+"].forEach((item, i) => {
    const x = 80 + (i % 4) * 320;
    rect(services, "Service card / " + item, x, 240, 280, 250, ["#1D1D1F", "#EAC9D6", "#CFE6D3", "#BFD9F5"][i], 24);
    text(services, "Service title / " + item, item, x + 22, 275, 22, i === 0 ? "#FFFFFF" : "#1D1D1F", "600");
  text(services, "Service link / " + item, "Explore  ›", x + 22, 437, 15, i === 0 ? "#2997FF" : "#0066CC", "400");
  });

  const footer = section(frame, "Apple / Footer", 5062, 199, "#E8E8ED");
  text(footer, "Footer note", "Copyright © 2026 Apple Inc. Todos os direitos reservados.", 80, 36, 12, "#6E6E73");
  text(footer, "Footer links", "Privacidade     Termos de uso     Vendas e suporte", 80, 80, 12, "#6E6E73");
  return { page: page.name, frame: frame.id, width: frame.width, height: frame.height };
}

async function buildGithub() {
  const { page, frame } = await clearPage(
    "Benchmark — GitHub Kaio",
    "GitHub Kaio — Home — 1440x1807",
    1440, 1807, "#FFFFFF"
  );

  const avatar = "https://github.com/fluidicon.png";
  const header = section(frame, "GitHub / Global Header", 0, 72, "#25292E");
  text(header, "GitHub mark", "◉", 72, 18, 30, "#FFFFFF", "600");
  rect(header, "Header / search field", 125, 16, 370, 40, "#3A4048", 7);
  text(header, "Header / search placeholder", "Search or jump to...", 145, 29, 14, "#C8D1DB");
  ["Pull requests", "Issues", "Marketplace", "Explore"].forEach((item, i) => text(header, "Header / " + item, item, 535 + i * 140, 29, 14, "#FFFFFF"));
  text(header, "Header / avatar", "kaio-baleeiro", 1190, 29, 14, "#FFFFFF");

  const profile = section(frame, "GitHub / Profile Header", 72, 250, "#FFFFFF");
  await image(profile, "GitHub / first-party profile image", 100, 52, 132, 132, avatar);
  text(profile, "Profile / display name", "Kaio Baleeiro", 270, 58, 30, "#1F2328", "600");
  text(profile, "Profile / handle", "@kaio-baleeiro", 270, 104, 20, "#656D76");
  text(profile, "Profile / bio", "Building useful products, data workflows and delightful interfaces.", 270, 145, 16, "#1F2328");
  text(profile, "Profile / location", "São Paulo, Brazil", 270, 184, 14, "#656D76");
  rect(profile, "Profile / follow button", 1150, 58, 180, 42, "#F6F8FA", 7);
  text(profile, "Profile / follow label", "Follow", 1207, 72, 14, "#1F2328", "600");

  const tabs = section(frame, "GitHub / Profile Tabs", 322, 62, "#FFFFFF");
  ["Overview", "Repositories", "Projects", "Packages"].forEach((item, i) => {
    text(tabs, "Tab / " + item, item, 110 + i * 170, 22, 15, i === 0 ? "#1F2328" : "#656D76", i === 0 ? "600" : "400");
    if (i === 0) rect(tabs, "Tab / active underline", 100, 58, 120, 4, "#FD8C73");
  });

  const content = section(frame, "GitHub / Repository Content", 384, 1220, "#F6F8FA");
  text(content, "Content / repositories heading", "Popular repositories", 90, 54, 20, "#1F2328", "600");
  text(content, "Content / repository action", "Customize your pins", 1150, 58, 14, "#0969DA", "400");
  const repos = [
    ["penpot-design-automation", "Automação de designs editáveis no Penpot", "TypeScript", "#3178C6", "12"],
    ["kaio-baleeiro", "Perfil, experimentos e documentação", "HTML", "#E34C26", "8"],
    ["projeto-leitura-de-dados", "Projeto público de leitura e tratamento de dados", "Java", "#B07219", "6"],
    ["design-system", "Tokens e componentes para produtos digitais", "CSS", "#563D7C", "24"],
    ["data-workflows", "Pipelines e validações reproduzíveis", "Jupyter", "#DA5B0B", "15"],
    ["product-notes", "Notas de produto e decisões", "Markdown", "#083FA1", "4"]
  ];
  repos.forEach((repo, i) => {
    const col = i % 2;
    const row = Math.floor(i / 2);
    const x = col === 0 ? 90 : 750;
    const y = 120 + row * 250;
    rect(content, "Repository card / " + repo[0], x, y, 600, 205, "#FFFFFF", 8);
    text(content, "Repository name / " + repo[0], repo[0], x + 24, y + 24, 17, "#0969DA", "600");
    rect(content, "Repository visibility / " + repo[0], x + 330, y + 20, 74, 25, "#FFFFFF", 12);
    text(content, "Repository visibility label / " + repo[0], "Public", x + 348, y + 27, 11, "#656D76", "600");
    text(content, "Repository description / " + repo[0], repo[1], x + 24, y + 72, 14, "#656D76");
    rect(content, "Repository language dot / " + repo[0], x + 24, y + 153, 12, 12, repo[3], 6);
    text(content, "Repository language / " + repo[0], repo[2], x + 44, y + 151, 12, "#656D76");
    text(content, "Repository stars / " + repo[0], "★ " + repo[4], x + 190, y + 151, 12, "#656D76");
    text(content, "Repository updated / " + repo[0], "Updated recently", x + 310, y + 151, 12, "#656D76");
  });
  rect(content, "Repository / pagination divider", 90, 900, 1260, 1, "#D0D7DE");
  text(content, "Contribution heading", "Contribution activity", 90, 952, 20, "#1F2328", "600");
  for (let r = 0; r < 5; r++) for (let c = 0; c < 52; c++) {
    const intensity = (r * 7 + c * 3) % 5;
    const colors = ["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"];
    rect(content, "Contribution cell " + r + "-" + c, 180 + c * 18, 1025 + r * 18, 13, 13, colors[intensity], 2);
  }
  text(content, "Contribution legend", "Less     More", 1095, 1144, 12, "#656D76");

  const footer = section(frame, "GitHub / Footer", 1604, 203, "#F6F8FA");
  text(footer, "Footer brand", "© 2026 GitHub, Inc.", 90, 60, 13, "#656D76");
  ["Terms", "Privacy", "Security", "Status", "Docs", "Contact"].forEach((item, i) => text(footer, "Footer / " + item, item, 300 + i * 120, 60, 13, "#0969DA"));
  text(footer, "Footer context", "Designed as an editable reconstruction from the public profile source.", 90, 112, 13, "#656D76");
  return { page: page.name, frame: frame.id, width: frame.width, height: frame.height };
}

async function buildWarframe() {
  const { page, frame } = await clearPage(
    "Benchmark — Warframe EN",
    "Warframe EN — Home — 1440x5953",
    1440, 5953, "#10131A"
  );

  const warframeMeta = "https://www-static.warframe.com/images/landing/warframe-metacard.png";
  const logo = "https://www-static.warframe.com/images/logoWhite.png";

  const header = section(frame, "Warframe / Header", 0, 82, "#0C0F14");
  await image(header, "Warframe / first-party logo", 62, 22, 142, 34, logo);
  ["GAME", "NEWS", "COMMUNITY", "ABOUT", "SUPPORT"].forEach((item, i) => text(header, "Warframe nav / " + item, item, 270 + i * 124, 34, 13, "#D8DDE5", "600"));
  rect(header, "Warframe / download button", 1130, 18, 220, 46, "#E85D3F", 4);
  text(header, "Warframe / download label", "DOWNLOAD NOW", 1172, 34, 13, "#FFFFFF", "700");

  const hero = section(frame, "Warframe / Hero", 82, 940, "#171B25");
  await image(hero, "Warframe / hero first-party image", 0, 0, 1440, 940, warframeMeta, 0.52);
  rect(hero, "Warframe / hero color wash", 0, 0, 1440, 940, "#1B1520", 0, 0.45);
  text(hero, "Warframe / hero kicker", "THE ORIGIN SYSTEM", 0, 222, 18, "#F5B89F", "700", "center").resize(1440, 28);
  text(hero, "Warframe / hero title", "WARFRAME", 0, 272, 78, "#FFFFFF", "700", "center").resize(1440, 90);
  text(hero, "Warframe / hero subtitle", "Awaken as an ancient warrior and fight across a living universe.", 0, 390, 22, "#E0E4EA", "400", "center").resize(1440, 34);
  rect(hero, "Warframe / hero primary CTA", 540, 465, 360, 56, "#E85D3F", 4);
  text(hero, "Warframe / hero primary label", "PLAY FREE NOW", 0, 485, 15, "#FFFFFF", "700", "center").resize(1440, 24);
  text(hero, "Warframe / hero secondary CTA", "WATCH TRAILER  ›", 0, 555, 14, "#FFFFFF", "600", "center").resize(1440, 22);
  rect(hero, "Warframe / hero bottom gradient", 0, 820, 1440, 120, "#0F1118", 0, 0.85);

  const news = section(frame, "Warframe / News and Updates", 1022, 760, "#121721");
  text(news, "Warframe / news heading", "LATEST FROM THE ORIGIN SYSTEM", 72, 72, 30, "#FFFFFF", "700");
  text(news, "Warframe / news link", "VIEW ALL NEWS  ›", 1170, 82, 13, "#E85D3F", "600");
  const newsCards = ["The Old Peace", "Update 41.0", "Community Stories"];
  newsCards.forEach((item, i) => {
    const x = 72 + i * 438;
    rect(news, "News card / " + item, x, 150, 400, 470, "#232A35", 6);
    rect(news, "News image / " + item, x, 150, 400, 250, ["#5A2E38", "#344A63", "#536340"][i], 6);
    text(news, "News image mark / " + item, ["01", "02", "03"][i], x + 28, 235, 44, "#FFFFFF", "700");
    text(news, "News title / " + item, item, x + 28, 438, 22, "#FFFFFF", "700");
    text(news, "News description / " + item, "Read the latest dispatch from Digital Extremes.", x + 28, 486, 14, "#B8C0CC");
    text(news, "News link / " + item, "READ MORE  ›", x + 28, 572, 13, "#E85D3F", "600");
  });

  const arsenal = section(frame, "Warframe / Arsenal Feature", 1782, 890, "#0E1219");
  text(arsenal, "Arsenal / heading", "BUILD YOUR ARSENAL", 72, 86, 34, "#FFFFFF", "700");
  text(arsenal, "Arsenal / intro", "Master the Warframes, weapons and companions that define your playstyle.", 72, 146, 18, "#B8C0CC");
  ["WARFRAMES", "WEAPONS", "COMPANIONS"].forEach((item, i) => {
    const x = 72 + i * 438;
    rect(arsenal, "Arsenal card / " + item, x, 270, 400, 440, ["#273D54", "#563A3D", "#384F43"][i], 8);
    rect(arsenal, "Arsenal card accent / " + item, x + 28, 300, 90, 8, "#E85D3F", 4);
    text(arsenal, "Arsenal card title / " + item, item, x + 28, 590, 22, "#FFFFFF", "700");
    text(arsenal, "Arsenal card link / " + item, "EXPLORE  ›", x + 28, 644, 13, "#F5B89F", "600");
  });

  const universe = section(frame, "Warframe / Universe Stories", 2672, 970, "#171B25");
  text(universe, "Universe / heading", "A LIVING UNIVERSE", 72, 86, 34, "#FFFFFF", "700");
  text(universe, "Universe / intro", "There is always more to discover beyond the next relay.", 72, 146, 18, "#B8C0CC");
  rect(universe, "Universe / large media", 72, 240, 1296, 500, "#283347", 8);
  rect(universe, "Universe / media highlight", 110, 280, 520, 420, "#5A2E38", 8, 0.8);
  rect(universe, "Universe / media highlight 2", 675, 280, 650, 180, "#344A63", 8, 0.8);
  rect(universe, "Universe / media highlight 3", 675, 500, 650, 200, "#536340", 8, 0.8);
  text(universe, "Universe / feature title", "THE STORY NEVER ENDS", 110, 570, 32, "#FFFFFF", "700");
  text(universe, "Universe / feature body", "Explore quests, factions and worlds shaped by the choices of the Tenno.", 110, 628, 16, "#E0E4EA");

  const community = section(frame, "Warframe / Community", 3642, 890, "#11151D");
  text(community, "Community / heading", "JOIN THE COMMUNITY", 72, 82, 34, "#FFFFFF", "700");
  text(community, "Community / intro", "Connect with Tenno around the world.", 72, 140, 18, "#B8C0CC");
  ["Forums", "Creators", "Events", "Support"].forEach((item, i) => {
    const x = 72 + i * 320;
    rect(community, "Community card / " + item, x, 260, 280, 410, "#242B36", 6);
    text(community, "Community icon / " + item, ["◌", "◈", "◇", "◎"][i], x + 105, 330, 60, "#E85D3F", "700");
    text(community, "Community title / " + item, item, x + 28, 480, 22, "#FFFFFF", "700");
    text(community, "Community link / " + item, "VISIT  ›", x + 28, 600, 13, "#F5B89F", "600");
  });

  const cta = section(frame, "Warframe / Call To Action", 4532, 930, "#1C202A");
  text(cta, "CTA / kicker", "THE SYSTEM NEEDS YOU", 0, 148, 16, "#F5B89F", "700", "center").resize(1440, 24);
  text(cta, "CTA / title", "BECOME A TENNO", 0, 205, 52, "#FFFFFF", "700", "center").resize(1440, 66);
  text(cta, "CTA / body", "Begin your journey today. Free to play on all platforms.", 0, 295, 20, "#D8DDE5", "400", "center").resize(1440, 32);
  rect(cta, "CTA / button", 540, 370, 360, 58, "#E85D3F", 4);
  text(cta, "CTA / button label", "DOWNLOAD WARFRAME", 0, 390, 15, "#FFFFFF", "700", "center").resize(1440, 24);
  text(cta, "CTA / secondary", "Available now for PC, PlayStation, Xbox, Nintendo Switch and more.", 0, 470, 14, "#B8C0CC", "400", "center").resize(1440, 22);

  const footer = section(frame, "Warframe / Footer", 5462, 491, "#0A0D12");
  await image(footer, "Warframe / footer logo", 72, 90, 150, 36, logo);
  text(footer, "Footer / legal", "© 2026 Digital Extremes Ltd. All rights reserved.", 72, 178, 13, "#7D8794");
  ["Privacy", "Terms", "Cookies", "Accessibility", "Contact"].forEach((item, i) => text(footer, "Footer / " + item, item, 72 + i * 120, 230, 13, "#B8C0CC"));
  text(footer, "Footer / source note", "Editable reconstruction • full-page source was dynamic and remains marked NEEDS_REVIEW.", 72, 310, 13, "#7D8794");
  return { page: page.name, frame: frame.id, width: frame.width, height: frame.height };
}

return { apple: await buildApple(), github: await buildGithub(), warframe: await buildWarframe() };
