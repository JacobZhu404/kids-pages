/* ============================================================
   DFS & BFS 互动教程 - JavaScript
   ============================================================ */

(function () {
'use strict';

var SVG_NS = 'http://www.w3.org/2000/svg';

/* ============================================================
   通用工具
   ============================================================ */
function createSVG(tag, attrs) {
  var el = document.createElementNS(SVG_NS, tag);
  for (var k in attrs) el.setAttribute(k, attrs[k]);
  return el;
}
function $(id) { return document.getElementById(id); }

/* ============================================================
   树数据定义 (共用)
   ============================================================ */
var treeData = {
  nodes: [
    { label: '1', x: 300, y: 50 },
    { label: '2', x: 150, y: 150 },
    { label: '3', x: 450, y: 150 },
    { label: '4', x: 80,  y: 250 },
    { label: '5', x: 220, y: 250 },
    { label: '6', x: 380, y: 250 },
    { label: '7', x: 520, y: 250 },
  ],
  edges: [
    [0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]
  ],
  children: [
    [1, 2], [3, 4], [5, 6], [], [], [], []
  ]
};

/* ============================================================
   树渲染函数
   ============================================================ */
function renderTree(svgId, step, algoType) {
  var svg = $(svgId);
  if (!svg) return;
  svg.innerHTML = '';

  // 构建"已发现"集合 = 已访问 + 在栈/队列中
  var visitedSet = new Set(step.visited);
  var inProgress = new Set(step.stack || step.queue || []);
  var discoveredSet = new Set(visitedSet);
  inProgress.forEach(function (n) { discoveredSet.add(n); });

  // 画边
  treeData.edges.forEach(function (e) {
    var n1 = treeData.nodes[e[0]];
    var n2 = treeData.nodes[e[1]];
    var line = createSVG('line', {
      x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y,
      class: 'edge-line'
    });
    if (discoveredSet.has(e[0]) && discoveredSet.has(e[1])) {
      line.classList.add('active-' + algoType);
    }
    svg.appendChild(line);
  });

  // 画节点
  treeData.nodes.forEach(function (node, i) {
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 26,
      class: 'node-circle'
    });

    if (i === step.current) {
      circle.classList.add('current');
    } else if (inProgress.has(i)) {
      circle.classList.add(algoType === 'dfs' ? 'in-stack' : 'in-queue');
    } else if (visitedSet.has(i)) {
      circle.classList.add('visited-' + algoType);
    }

    svg.appendChild(circle);

    // 文字颜色：未访问用深色，其余用白色
    var isUnvisited = !discoveredSet.has(i) && i !== step.current;
    var textColor = isUnvisited ? '#475569' : '#fff';

    var text = createSVG('text', {
      x: node.x, y: node.y + 5,
      'text-anchor': 'middle',
      fill: textColor,
      class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);
  });
}

/* ============================================================
   DFS 动画
   ============================================================ */

// 预计算 DFS 步骤
var dfsSteps = (function () {
  var steps = [];
  var visited = [];
  var stack = [];
  var order = [];

  steps.push({
    visited: [], current: -1, stack: [], order: [],
    desc: '准备开始 DFS，从根节点 1 出发。点击"播放"或"单步"继续。',
    type: 'init'
  });

  function recordStep(current, desc, type) {
    steps.push({
      visited: visited.slice(),
      current: current,
      stack: stack.slice(),
      order: order.slice(),
      desc: desc,
      type: type
    });
  }

  function dfs(u) {
    visited.push(u);
    order.push(u);
    stack.push(u);
    recordStep(u, '访问节点 ' + treeData.nodes[u].label +
      '，标记已访问并压入栈。栈：[' +
      stack.map(function (s) { return treeData.nodes[s].label; }).join(', ') + ']', 'visit');

    var kids = treeData.children[u];
    for (var i = 0; i < kids.length; i++) {
      var v = kids[i];
      if (visited.indexOf(v) === -1) {
        dfs(v);
      }
    }

    stack.pop();
    if (stack.length > 0) {
      recordStep(u, '节点 ' + treeData.nodes[u].label +
        ' 的所有子节点都访问完了，回溯！弹出栈顶。栈：[' +
        stack.map(function (s) { return treeData.nodes[s].label; }).join(', ') + ']', 'backtrack');
    } else {
      recordStep(u, '节点 ' + treeData.nodes[u].label +
        ' 的所有子节点都访问完了，回溯到根。栈为空，DFS 完成！', 'done');
    }
  }

  dfs(0);
  return steps;
})();

var dfsState = {
  stepIdx: 0,
  playing: false,
  timer: null,
  speed: 900
};

function dfsRender() {
  var step = dfsSteps[dfsState.stepIdx];
  renderTree('dfsTree', step, 'dfs');

  // 渲染栈
  var stackDiv = $('dfsStack');
  stackDiv.innerHTML = '';
  step.stack.forEach(function (s) {
    var item = document.createElement('div');
    item.className = 'ds-item dfs';
    if (s === step.current && step.type === 'visit') item.classList.add('current');
    item.textContent = treeData.nodes[s].label;
    stackDiv.appendChild(item);
  });

  // 渲染已访问
  var visDiv = $('dfsVisited');
  visDiv.innerHTML = '';
  step.visited.forEach(function (v) {
    var item = document.createElement('div');
    item.className = 'ds-item dfs';
    item.style.fontSize = '0.75rem';
    item.style.padding = '0.2rem 0.5rem';
    item.textContent = treeData.nodes[v].label;
    visDiv.appendChild(item);
  });

  // 步骤信息
  $('dfsStepInfo').childNodes[0].nodeValue = step.desc;
  $('dfsCounter').textContent = (dfsState.stepIdx + 1) + ' / ' + dfsSteps.length;

  // 访问顺序
  renderOrder('dfsOrder', step.order, 'dfs');
}

function renderOrder(elId, order, algoType) {
  var div = $(elId);
  div.innerHTML = '';
  order.forEach(function (nodeIdx, i) {
    var item = document.createElement('span');
    item.className = 'order-item ' + algoType;
    item.textContent = treeData.nodes[nodeIdx].label;
    div.appendChild(item);
    if (i < order.length - 1) {
      var arrow = document.createElement('span');
      arrow.className = 'arrow';
      arrow.textContent = '→';
      div.appendChild(arrow);
    }
  });
}

function dfsPlay() {
  if (dfsState.playing) return;
  if (dfsState.stepIdx >= dfsSteps.length - 1) {
    dfsState.stepIdx = 0;
  }
  dfsState.playing = true;
  dfsTimerStep();
}

function dfsTimerStep() {
  if (!dfsState.playing) return;
  dfsRender();
  if (dfsState.stepIdx < dfsSteps.length - 1) {
    dfsState.stepIdx++;
    dfsState.timer = setTimeout(dfsTimerStep, dfsState.speed);
  } else {
    dfsState.playing = false;
  }
}

function dfsPause() {
  dfsState.playing = false;
  if (dfsState.timer) clearTimeout(dfsState.timer);
}

function dfsStepForward() {
  dfsPause();
  if (dfsState.stepIdx < dfsSteps.length - 1) {
    dfsState.stepIdx++;
    dfsRender();
  }
}

function dfsReset() {
  dfsPause();
  dfsState.stepIdx = 0;
  dfsRender();
}

function initDFS() {
  if (!$('dfsTree')) return;
  $('dfsPlay').addEventListener('click', dfsPlay);
  $('dfsPause').addEventListener('click', dfsPause);
  $('dfsStep').addEventListener('click', dfsStepForward);
  $('dfsReset').addEventListener('click', dfsReset);
  $('dfsSpeed').addEventListener('input', function () {
    dfsState.speed = parseInt(this.value);
  });
  dfsRender();
}

/* ============================================================
   BFS 动画
   ============================================================ */

var bfsSteps = (function () {
  var steps = [];
  var visited = [];
  var queue = [];
  var order = [];

  // 初始步：起点入队
  visited.push(0);
  queue.push(0);
  steps.push({
    visited: [], current: -1, queue: [0], order: [],
    desc: '准备开始 BFS：起点 1 入队，标记已访问。队列：[1]',
    type: 'init'
  });

  while (queue.length > 0) {
    var u = queue.shift();
    order.push(u);

    // 收集新入队的邻居
    var newNeighbors = [];
    var kids = treeData.children[u];
    for (var i = 0; i < kids.length; i++) {
      var v = kids[i];
      if (visited.indexOf(v) === -1) {
        visited.push(v);
        queue.push(v);
        newNeighbors.push(v);
      }
    }

    var desc = '节点 ' + treeData.nodes[u].label + ' 出队，访问 ' +
      treeData.nodes[u].label;
    if (newNeighbors.length > 0) {
      desc += '。邻居 ' + newNeighbors.map(function (n) {
        return treeData.nodes[n].label;
      }).join('、') + ' 入队。';
    } else {
      desc += '。没有未访问的新邻居入队。';
    }
    desc += ' 队列：[' + queue.map(function (s) {
      return treeData.nodes[s].label;
    }).join(', ') + ']';
    if (queue.length === 0) desc += '。队列为空，BFS 完成！';

    steps.push({
      visited: visited.slice(),
      current: u,
      queue: queue.slice(),
      order: order.slice(),
      desc: desc,
      type: queue.length === 0 ? 'done' : 'visit'
    });
  }

  return steps;
})();

var bfsState = {
  stepIdx: 0,
  playing: false,
  timer: null,
  speed: 900
};

function bfsRender() {
  var step = bfsSteps[bfsState.stepIdx];
  renderTree('bfsTree', step, 'bfs');

  // 渲染队列
  var queueDiv = $('bfsQueue');
  queueDiv.innerHTML = '';
  step.queue.forEach(function (s, i) {
    var item = document.createElement('div');
    item.className = 'ds-item bfs';
    item.textContent = treeData.nodes[s].label;
    if (i === 0) {
      item.style.boxShadow = '0 0 0 3px rgba(245,158,11,0.3)';
    }
    queueDiv.appendChild(item);
  });

  // 渲染已访问
  var visDiv = $('bfsVisited');
  visDiv.innerHTML = '';
  step.visited.forEach(function (v) {
    var item = document.createElement('div');
    item.className = 'ds-item bfs';
    item.style.fontSize = '0.75rem';
    item.style.padding = '0.2rem 0.5rem';
    item.textContent = treeData.nodes[v].label;
    visDiv.appendChild(item);
  });

  // 步骤信息
  $('bfsStepInfo').childNodes[0].nodeValue = step.desc;
  $('bfsCounter').textContent = (bfsState.stepIdx + 1) + ' / ' + bfsSteps.length;

  // 访问顺序
  renderOrder('bfsOrder', step.order, 'bfs');
}

function bfsPlay() {
  if (bfsState.playing) return;
  if (bfsState.stepIdx >= bfsSteps.length - 1) {
    bfsState.stepIdx = 0;
  }
  bfsState.playing = true;
  bfsTimerStep();
}

function bfsTimerStep() {
  if (!bfsState.playing) return;
  bfsRender();
  if (bfsState.stepIdx < bfsSteps.length - 1) {
    bfsState.stepIdx++;
    bfsState.timer = setTimeout(bfsTimerStep, bfsState.speed);
  } else {
    bfsState.playing = false;
  }
}

function bfsPause() {
  bfsState.playing = false;
  if (bfsState.timer) clearTimeout(bfsState.timer);
}

function bfsStepForward() {
  bfsPause();
  if (bfsState.stepIdx < bfsSteps.length - 1) {
    bfsState.stepIdx++;
    bfsRender();
  }
}

function bfsReset() {
  bfsPause();
  bfsState.stepIdx = 0;
  bfsRender();
}

function initBFS() {
  if (!$('bfsTree')) return;
  $('bfsPlay').addEventListener('click', bfsPlay);
  $('bfsPause').addEventListener('click', bfsPause);
  $('bfsStep').addEventListener('click', bfsStepForward);
  $('bfsReset').addEventListener('click', bfsReset);
  $('bfsSpeed').addEventListener('input', function () {
    bfsState.speed = parseInt(this.value);
  });
  bfsRender();
}

/* ============================================================
   迷宫动画
   ============================================================ */

// 迷宫定义: 0=路, 1=墙, 2=起点, 3=终点
var maze = [
  [2, 0, 0, 1, 0, 0, 0, 0, 0, 0],
  [0, 1, 0, 1, 0, 1, 1, 1, 0, 0],
  [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
  [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
  [0, 0, 0, 0, 0, 0, 0, 1, 0, 3]
];
var mazeRows = maze.length;
var mazeCols = maze[0].length;
var mazeStart = [0, 0];
var mazeEnd = [4, 9];

// DFS 探索顺序
function computeDFSOrder() {
  var visited = {};
  var order = [];
  var parent = {};
  var found = false;

  function key(r, c) { return r + ',' + c; }

  function dfs(r, c, pr) {
    if (found) return;
    if (r < 0 || r >= mazeRows || c < 0 || c >= mazeCols) return;
    if (maze[r][c] === 1 || visited[key(r, c)]) return;
    visited[key(r, c)] = true;
    parent[key(r, c)] = pr;
    order.push([r, c]);
    if (r === mazeEnd[0] && c === mazeEnd[1]) { found = true; return; }
    // 右、下、左、上
    dfs(r, c + 1, [r, c]);
    dfs(r + 1, c, [r, c]);
    dfs(r, c - 1, [r, c]);
    dfs(r - 1, c, [r, c]);
  }

  dfs(mazeStart[0], mazeStart[1], null);

  // 回溯路径
  var path = [];
  var cur = mazeEnd;
  while (cur) {
    path.push(cur);
    cur = parent[key(cur[0], cur[1])];
  }
  path.reverse();

  return { order: order, path: path };
}

// BFS 探索顺序
function computeBFSOrder() {
  var visited = {};
  var parent = {};
  var order = [];
  var queue = [mazeStart.slice()];
  visited[mazeStart[0] + ',' + mazeStart[1]] = true;

  function key(r, c) { return r + ',' + c; }

  while (queue.length > 0) {
    var cur = queue.shift();
    var r = cur[0], c = cur[1];
    order.push([r, c]);

    if (r === mazeEnd[0] && c === mazeEnd[1]) break;

    var dirs = [[0, 1], [1, 0], [0, -1], [-1, 0]];
    for (var i = 0; i < dirs.length; i++) {
      var nr = r + dirs[i][0], nc = c + dirs[i][1];
      if (nr >= 0 && nr < mazeRows && nc >= 0 && nc < mazeCols &&
          maze[nr][nc] !== 1 && !visited[key(nr, nc)]) {
        visited[key(nr, nc)] = true;
        parent[key(nr, nc)] = [r, c];
        queue.push([nr, nc]);
      }
    }
  }

  // 回溯路径
  var path = [];
  var cur2 = mazeEnd;
  while (cur2) {
    path.push(cur2);
    cur2 = parent[key(cur2[0], cur2[1])];
  }
  path.reverse();

  return { order: order, path: path };
}

var dfsMaze = computeDFSOrder();
var bfsMaze = computeBFSOrder();

var mazeState = {
  stepIdx: 0,
  playing: false,
  timer: null,
  speed: 200,
  maxSteps: Math.max(dfsMaze.order.length, bfsMaze.order.length)
};

function buildMazeGrid(elId) {
  var grid = $(elId);
  if (!grid) return;
  grid.style.gridTemplateColumns = 'repeat(' + mazeCols + ', 1fr)';
  grid.innerHTML = '';
  for (var r = 0; r < mazeRows; r++) {
    for (var c = 0; c < mazeCols; c++) {
      var cell = document.createElement('div');
      cell.className = 'maze-cell';
      cell.id = elId + '-' + r + '-' + c;
      if (maze[r][c] === 1) cell.classList.add('wall');
      else if (maze[r][c] === 2) cell.classList.add('start');
      else if (maze[r][c] === 3) cell.classList.add('end');
      else cell.classList.add('empty');
      grid.appendChild(cell);
    }
  }
}

function mazeRender() {
  var idx = mazeState.stepIdx;
  var dfsCells = dfsMaze.order;
  var bfsCells = bfsMaze.order;

  // 重置所有非墙、非起点终点的格子
  for (var r = 0; r < mazeRows; r++) {
    for (var c = 0; c < mazeCols; c++) {
      var dfsCell = $('mazeDFS-' + r + '-' + c);
      var bfsCell = $('mazeBFS-' + r + '-' + c);
      if (dfsCell && !dfsCell.classList.contains('wall') &&
          !dfsCell.classList.contains('start') && !dfsCell.classList.contains('end')) {
        dfsCell.className = 'maze-cell empty';
      }
      if (bfsCell && !bfsCell.classList.contains('wall') &&
          !bfsCell.classList.contains('start') && !bfsCell.classList.contains('end')) {
        bfsCell.className = 'maze-cell empty';
      }
    }
  }

  // DFS 标记已探索
  var dfsDone = false;
  for (var i = 0; i <= idx && i < dfsCells.length; i++) {
    var cr = dfsCells[i][0], cc = dfsCells[i][1];
    var cell = $('mazeDFS-' + cr + '-' + cc);
    if (cell && !cell.classList.contains('start') && !cell.classList.contains('end')) {
      cell.classList.remove('empty');
      cell.classList.add('dfs-visited');
    }
    if (cr === mazeEnd[0] && cc === mazeEnd[1]) dfsDone = true;
  }

  // BFS 标记已探索
  var bfsDone = false;
  for (var j = 0; j <= idx && j < bfsCells.length; j++) {
    var br = bfsCells[j][0], bc = bfsCells[j][1];
    var bcell = $('mazeBFS-' + br + '-' + bc);
    if (bcell && !bcell.classList.contains('start') && !bcell.classList.contains('end')) {
      bcell.classList.remove('empty');
      bcell.classList.add('bfs-visited');
    }
    if (br === mazeEnd[0] && bc === mazeEnd[1]) bfsDone = true;
  }

  // 标记路径（当搜索完成时）
  if (idx >= dfsCells.length - 1) {
    dfsMaze.path.forEach(function (p) {
      var cell = $('mazeDFS-' + p[0] + '-' + p[1]);
      if (cell && !cell.classList.contains('start') && !cell.classList.contains('end')) {
        cell.classList.remove('dfs-visited');
        cell.classList.add('dfs-path');
      }
    });
  }
  if (idx >= bfsCells.length - 1) {
    bfsMaze.path.forEach(function (p) {
      var cell = $('mazeBFS-' + p[0] + '-' + p[1]);
      if (cell && !cell.classList.contains('start') && !cell.classList.contains('end')) {
        cell.classList.remove('bfs-visited');
        cell.classList.add('bfs-path');
      }
    });
  }

  // 更新信息
  var info = $('mazeStepInfo');
  var dfsStep = Math.min(idx + 1, dfsCells.length);
  var bfsStep = Math.min(idx + 1, bfsCells.length);
  if (idx === 0) {
    info.childNodes[0].nodeValue = 'DFS 已探索 ' + dfsStep + ' 格，BFS 已探索 ' + bfsStep + ' 格。观察两种策略的不同探索方式！';
  } else if (dfsDone && bfsDone) {
    info.childNodes[0].nodeValue = '搜索完成！DFS 路径长度 ' + dfsMaze.path.length + ' 步，BFS 路径长度 ' + bfsMaze.path.length + ' 步（最短路径）。';
  } else {
    info.childNodes[0].nodeValue = 'DFS 已探索 ' + dfsStep + ' 格' + (dfsDone ? '（已找到终点）' : '') +
      '，BFS 已探索 ' + bfsStep + ' 格' + (bfsDone ? '（已找到终点）' : '') + '。';
  }
}

function mazePlay() {
  if (mazeState.playing) return;
  if (mazeState.stepIdx >= mazeState.maxSteps - 1) {
    mazeReset();
  }
  mazeState.playing = true;
  mazeTimerStep();
}

function mazeTimerStep() {
  if (!mazeState.playing) return;
  mazeRender();
  if (mazeState.stepIdx < mazeState.maxSteps - 1) {
    mazeState.stepIdx++;
    mazeState.timer = setTimeout(mazeTimerStep, mazeState.speed);
  } else {
    mazeState.playing = false;
  }
}

function mazeStepForward() {
  mazeState.playing = false;
  if (mazeState.timer) clearTimeout(mazeState.timer);
  if (mazeState.stepIdx < mazeState.maxSteps - 1) {
    mazeState.stepIdx++;
    mazeRender();
  }
}

function mazeReset() {
  mazeState.playing = false;
  if (mazeState.timer) clearTimeout(mazeState.timer);
  mazeState.stepIdx = 0;
  mazeRender();
}

function initMaze() {
  if (!$('mazeDFS')) return;
  buildMazeGrid('mazeDFS');
  buildMazeGrid('mazeBFS');
  $('mazePlay').addEventListener('click', mazePlay);
  $('mazeStep').addEventListener('click', mazeStepForward);
  $('mazeReset').addEventListener('click', mazeReset);
  $('mazeSpeed').addEventListener('input', function () {
    mazeState.speed = parseInt(this.value);
  });
  mazeRender();
}

/* ============================================================
   互动练习场
   ============================================================ */

var pg = {
  nodes: [],
  edges: [],
  nextId: 1,
  startNode: null,
  mode: 'node',
  algorithm: 'dfs',
  edgeStart: null,
  isAnimating: false
};

function pgRender() {
  var svg = $('pgCanvas');
  if (!svg) return;
  svg.innerHTML = '';

  // 画边
  pg.edges.forEach(function (e) {
    var n1 = pg.nodes[e.from];
    var n2 = pg.nodes[e.to];
    if (!n1 || !n2) return;
    var line = createSVG('line', {
      x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y,
      class: 'edge-line', stroke: '#94a3b8', 'stroke-width': 2
    });
    line.dataset.edgeIdx = pg.edges.indexOf(e);
    svg.appendChild(line);
  });

  // 画节点
  pg.nodes.forEach(function (node) {
    var g = createSVG('g', {});
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 22,
      class: 'pg-node',
      fill: pg.startNode === node.id ? 'var(--success)' : 'var(--accent)',
      stroke: '#fff', 'stroke-width': 2,
      'data-id': node.id
    });
    circle.style.cursor = 'pointer';
    circle.style.transition = 'all 0.3s';
    g.appendChild(circle);

    var text = createSVG('text', {
      x: node.x, y: node.y + 5,
      'text-anchor': 'middle',
      fill: '#fff', class: 'node-label',
      'font-size': '14px', 'pointer-events': 'none'
    });
    text.textContent = node.label;
    g.appendChild(text);

    // 起点标记
    if (pg.startNode === node.id) {
      var star = createSVG('text', {
        x: node.x + 18, y: node.y - 15,
        'font-size': '16px', 'pointer-events': 'none'
      });
      star.textContent = '\u2B50';
      g.appendChild(star);
    }

    svg.appendChild(g);
  });
}

function pgStatus(msg) {
  $('pgStatus').textContent = msg;
}

function pgHandleClick(e) {
  if (pg.isAnimating) return;
  var svg = $('pgCanvas');
  var rect = svg.getBoundingClientRect();
  var scaleX = 600 / rect.width;
  var scaleY = 400 / rect.height;
  var x = (e.clientX - rect.left) * scaleX;
  var y = (e.clientY - rect.top) * scaleY;

  // 检查是否点击了节点
  var clickedNode = null;
  for (var i = 0; i < pg.nodes.length; i++) {
    var n = pg.nodes[i];
    var dx = x - n.x, dy = y - n.y;
    if (dx * dx + dy * dy <= 24 * 24) {
      clickedNode = n;
      break;
    }
  }

  if (pg.mode === 'node') {
    if (!clickedNode) {
      pg.nodes.push({ id: pg.nextId, label: String(pg.nextId), x: x, y: y });
      pg.nextId++;
      pgRender();
      pgStatus('已添加节点 ' + (pg.nextId - 1) + '。继续点击空白处添加更多节点。');
    } else {
      pgStatus('该位置已有节点，请点击空白处添加新节点。');
    }
  } else if (pg.mode === 'edge') {
    if (clickedNode) {
      if (pg.edgeStart === null) {
        pg.edgeStart = clickedNode.id;
        pgStatus('已选择节点 ' + clickedNode.label + '，再点击另一个节点连线。');
      } else if (pg.edgeStart === clickedNode.id) {
        pg.edgeStart = null;
        pgStatus('取消了选择。请重新点击一个节点开始连线。');
      } else {
        // 检查是否已有边
        var exists = pg.edges.some(function (e) {
          return (e.from === pg.edgeStart && e.to === clickedNode.id) ||
                 (e.from === clickedNode.id && e.to === pg.edgeStart);
        });
        if (!exists) {
          pg.edges.push({ from: pg.edgeStart, to: clickedNode.id });
          pgStatus('已连接节点 ' + pg.nodes.find(function(n){return n.id===pg.edgeStart;}).label +
            ' 和节点 ' + clickedNode.label + '。继续连线或切换模式。');
        } else {
          pgStatus('这两个节点已经连接过了！');
        }
        pg.edgeStart = null;
        pgRender();
      }
    } else {
      pg.edgeStart = null;
      pgStatus('请点击节点（不是空白处）来连线。');
    }
  } else if (pg.mode === 'start') {
    if (clickedNode) {
      pg.startNode = clickedNode.id;
      pgRender();
      pgStatus('已设置节点 ' + clickedNode.label + ' 为搜索起点。选择算法后点击"开始搜索"。');
    } else {
      pgStatus('请点击一个节点来设为起点。');
    }
  } else if (pg.mode === 'delete') {
    if (clickedNode) {
      // 删除节点和相关边
      pg.nodes = pg.nodes.filter(function (n) { return n.id !== clickedNode.id; });
      pg.edges = pg.edges.filter(function (e) {
        return e.from !== clickedNode.id && e.to !== clickedNode.id;
      });
      if (pg.startNode === clickedNode.id) pg.startNode = null;
      pgRender();
      pgStatus('已删除节点 ' + clickedNode.label + '。');
    } else {
      // 检查是否点击了边
      // 简化：不实现边的删除
      pgStatus('请点击一个节点来删除。');
    }
  }
}

function pgBuildAdjList() {
  var adj = {};
  pg.nodes.forEach(function (n) { adj[n.id] = []; });
  pg.edges.forEach(function (e) {
    if (adj[e.from]) adj[e.from].push(e.to);
    if (adj[e.to]) adj[e.to].push(e.from);
  });
  // 排序邻居（按 label 数字大小）
  for (var k in adj) {
    adj[k].sort(function (a, b) { return a - b; });
  }
  return adj;
}

function pgRunAlgorithm() {
  if (pg.isAnimating) return;
  if (pg.nodes.length === 0) {
    pgStatus('请先添加节点！');
    return;
  }
  if (pg.startNode === null) {
    pg.startNode = pg.nodes[0].id;
    pgStatus('未设起点，自动从节点 ' + pg.nodes[0].label + ' 开始。');
    pgRender();
  }

  var adj = pgBuildAdjList();
  var visited = new Set();
  var order = [];

  if (pg.algorithm === 'dfs') {
    function dfs(u) {
      visited.add(u);
      order.push(u);
      var neighbors = adj[u] || [];
      for (var i = 0; i < neighbors.length; i++) {
        if (!visited.has(neighbors[i])) {
          dfs(neighbors[i]);
        }
      }
    }
    dfs(pg.startNode);
  } else {
    var queue = [pg.startNode];
    visited.add(pg.startNode);
    while (queue.length > 0) {
      var u = queue.shift();
      order.push(u);
      var neighbors = adj[u] || [];
      for (var i = 0; i < neighbors.length; i++) {
        if (!visited.has(neighbors[i])) {
          visited.add(neighbors[i]);
          queue.push(neighbors[i]);
        }
      }
    }
  }

  pgAnimateSearch(order);
}

function pgAnimateSearch(order) {
  pg.isAnimating = true;
  $('pgOrder').style.display = 'flex';
  var orderList = $('pgOrderList');
  orderList.innerHTML = '';
  var color = pg.algorithm === 'dfs' ? 'var(--accent)' : 'var(--accent2)';

  var i = 0;
  function step() {
    if (i >= order.length) {
      pg.isAnimating = false;
      pgStatus(pg.algorithm.toUpperCase() + ' 搜索完成！共访问 ' + order.length + ' 个节点。');
      return;
    }
    var nodeId = order[i];
    var node = pg.nodes.find(function (n) { return n.id === nodeId; });
    if (node) {
      // 高亮当前节点
      var circles = $('pgCanvas').querySelectorAll('circle');
      circles.forEach(function (c) {
        if (parseInt(c.getAttribute('data-id')) === nodeId) {
          c.setAttribute('fill', pg.algorithm === 'dfs' ? '#4f46e5' : '#d97706');
          c.setAttribute('r', 26);
        }
      });

      // 添加到访问顺序
      var item = document.createElement('span');
      item.className = 'order-item ' + pg.algorithm;
      item.textContent = node.label;
      item.style.background = pg.algorithm === 'dfs' ? 'var(--accent)' : 'var(--accent2)';
      orderList.appendChild(item);
      if (i < order.length - 1) {
        var arrow = document.createElement('span');
        arrow.className = 'arrow';
        arrow.textContent = '\u2192';
        orderList.appendChild(arrow);
      }

      pgStatus(pg.algorithm.toUpperCase() + ' 正在访问节点 ' + node.label + ' (' + (i + 1) + '/' + order.length + ')');
    }
    i++;
    setTimeout(step, 600);
  }
  step();
}

function pgClear() {
  if (pg.isAnimating) return;
  pg.nodes = [];
  pg.edges = [];
  pg.nextId = 1;
  pg.startNode = null;
  pg.edgeStart = null;
  pgRender();
  $('pgOrder').style.display = 'none';
  pgStatus('画布已清空。模式：添加节点。点击空白处创建节点。');
}

function pgLoadSample() {
  if (pg.isAnimating) return;
  pg.nodes = [
    { id: 1, label: '1', x: 300, y: 60 },
    { id: 2, label: '2', x: 180, y: 150 },
    { id: 3, label: '3', x: 420, y: 150 },
    { id: 4, label: '4', x: 100, y: 250 },
    { id: 5, label: '5', x: 260, y: 250 },
    { id: 6, label: '6', x: 340, y: 250 },
    { id: 7, label: '7', x: 500, y: 250 },
    { id: 8, label: '8', x: 200, y: 340 },
  ];
  pg.edges = [
    { from: 1, to: 2 }, { from: 1, to: 3 },
    { from: 2, to: 4 }, { from: 2, to: 5 },
    { from: 3, to: 6 }, { from: 3, to: 7 },
    { from: 5, to: 8 }, { from: 6, to: 8 }
  ];
  pg.nextId = 9;
  pg.startNode = 1;
  pgRender();
  $('pgOrder').style.display = 'none';
  pgStatus('已加载示例图！起点为节点 1。选择算法后点击"开始搜索"。');
}

function initPlayground() {
  if (!$('pgCanvas')) return;
  $('pgCanvas').addEventListener('click', pgHandleClick);

  document.querySelectorAll('.pg-mode-btn[data-mode]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.pg-mode-btn[data-mode]').forEach(function (b) {
        b.classList.remove('active');
      });
      this.classList.add('active');
      pg.mode = this.dataset.mode;
      pg.edgeStart = null;
      var modeNames = {
        'node': '添加节点',
        'edge': '连线',
        'start': '设起点',
        'delete': '删除'
      };
      pgStatus('模式：' + modeNames[pg.mode] + '。' +
        (pg.mode === 'node' ? '点击空白处创建节点。' :
         pg.mode === 'edge' ? '依次点击两个节点连线。' :
         pg.mode === 'start' ? '点击一个节点设为起点。' :
         '点击一个节点删除。'));
    });
  });

  document.querySelectorAll('.pg-mode-btn[data-algo]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      document.querySelectorAll('.pg-mode-btn[data-algo]').forEach(function (b) {
        b.classList.remove('active');
      });
      this.classList.add('active');
      pg.algorithm = this.dataset.algo;
      pgStatus('已选择 ' + pg.algorithm.toUpperCase() + ' 算法。');
    });
  });

  $('pgRun').addEventListener('click', pgRunAlgorithm);
  $('pgClear').addEventListener('click', pgClear);
  $('pgSample').addEventListener('click', pgLoadSample);
}

/* ============================================================
   知识检测 Quiz
   ============================================================ */

var quizQuestions = [
  {
    q: 'DFS（深度优先搜索）通常使用什么数据结构来实现？',
    options: ['队列（Queue）', '栈（Stack）/ 递归', '数组（Array）', '哈希表（HashMap）'],
    answer: 1,
    explain: 'DFS 的核心是"深入"，递归调用天然形成栈结构。也可以手动用栈来模拟。队列是 BFS 用的。'
  },
  {
    q: 'BFS（广度优先搜索）通常使用什么数据结构来实现？',
    options: ['栈（Stack）', '队列（Queue）', '链表（LinkedList）', '栈和队列都可以'],
    answer: 1,
    explain: 'BFS 需要先进先出（FIFO）的特性，队列正好满足。先发现的节点先处理，保证按层遍历。'
  },
  {
    q: '在无权图中求从起点到终点的最短路径，应该用哪种算法？',
    options: ['DFS', 'BFS', '两个都可以', '两个都不行'],
    answer: 1,
    explain: 'BFS 按距离层层扩展，第一次到达终点时的路径就是最短的。DFS 可能走弯路，不保证最短。'
  },
  {
    q: '在 BFS 中，应该在什么时候将节点标记为"已访问"？',
    options: ['节点出队时', '节点入队时', '处理完节点的所有邻居后', '不需要标记'],
    answer: 1,
    explain: '入队时就标记！如果等出队才标记，同一个节点可能被多次加入队列，导致效率降低甚至出错。'
  },
  {
    q: 'DFS 遍历下图（从节点 1 开始，邻居按编号从小到大），adj[1]={2,3}, adj[2]={1,4}, adj[3]={1}, adj[4]={2}。访问顺序是？',
    options: ['1 2 3 4', '1 2 4 3', '1 3 2 4', '1 3 4 2'],
    answer: 1,
    explain: 'DFS：访问1→走2→访问2→走4→访问4→4无邻居→回溯到2→2无其他邻居→回溯到1→走3→访问3。顺序：1 2 4 3。'
  }
];

var quizAnswers = {};

function initQuiz() {
  var container = $('quizContainer');
  if (!container) return;

  quizQuestions.forEach(function (item, qi) {
    var div = document.createElement('div');
    div.className = 'quiz-q';

    var num = document.createElement('div');
    num.className = 'q-num';
    num.textContent = '第 ' + (qi + 1) + ' 题';
    div.appendChild(num);

    var text = document.createElement('div');
    text.className = 'q-text';
    text.textContent = item.q;
    div.appendChild(text);

    var opts = document.createElement('div');
    opts.className = 'quiz-options';
    item.options.forEach(function (opt, oi) {
      var btn = document.createElement('div');
      btn.className = 'quiz-opt';
      btn.textContent = String.fromCharCode(65 + oi) + '. ' + opt;
      btn.addEventListener('click', function () {
        if (quizAnswers[qi] !== undefined) return; // 已答过
        quizAnswers[qi] = oi;
        if (oi === item.answer) {
          btn.classList.add('correct');
        } else {
          btn.classList.add('wrong');
          // 显示正确答案
          opts.children[item.answer].classList.add('correct');
        }
        var feedback = div.querySelector('.quiz-feedback');
        feedback.classList.add('show');
        feedback.classList.add(oi === item.answer ? 'correct' : 'wrong');
        feedback.innerHTML = (oi === item.answer ? '\u2705 ' : '\u274C ') + item.explain;

        // 检查是否全部答完
        checkQuizComplete();
      });
      opts.appendChild(btn);
    });
    div.appendChild(opts);

    var feedback = document.createElement('div');
    feedback.className = 'quiz-feedback';
    div.appendChild(feedback);

    container.appendChild(div);
  });
}

function checkQuizComplete() {
  var answered = Object.keys(quizAnswers).length;
  if (answered === quizQuestions.length) {
    var correct = 0;
    for (var k in quizAnswers) {
      if (quizAnswers[k] === quizQuestions[k].answer) correct++;
    }
    var score = $('quizScore');
    score.classList.add('show');
    var pct = Math.round(correct / quizQuestions.length * 100);
    var msg = '';
    if (pct === 100) msg = '\uD83C\uDF89 满分！你完全掌握了 DFS 和 BFS！';
    else if (pct >= 60) msg = '\uD83D\uDC4D 不错！答对了 ' + correct + '/' + quizQuestions.length + ' 道。再复习一下错题吧！';
    else msg = '\uD83D\uDCDA 还需加油！答对了 ' + correct + '/' + quizQuestions.length + ' 道。建议重新学习相关章节。';
    score.innerHTML = msg + '<br>得分：' + correct + ' / ' + quizQuestions.length + '（' + pct + '%）';
  }
}

/* ============================================================
   导航高亮
   ============================================================ */
function initNav() {
  var links = document.querySelectorAll('.nav-bar a');
  var sections = [];
  links.forEach(function (link) {
    var target = document.querySelector(link.getAttribute('href'));
    if (target) sections.push({ link: link, el: target });
  });

  window.addEventListener('scroll', function () {
    var scrollY = window.scrollY + 100;
    var current = null;
    sections.forEach(function (s) {
      if (s.el.offsetTop <= scrollY) current = s;
    });
    links.forEach(function (l) { l.classList.remove('active'); });
    if (current) current.link.classList.add('active');
  });

  // 平滑滚动
  links.forEach(function (link) {
    link.addEventListener('click', function (e) {
      e.preventDefault();
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        window.scrollTo({ top: target.offsetTop - 60, behavior: 'smooth' });
      }
    });
  });
}

/* ============================================================
   初始化
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {
  initNav();
  initDFS();
  initBFS();
  initMaze();
  initPlayground();
  initQuiz();
});

})();
