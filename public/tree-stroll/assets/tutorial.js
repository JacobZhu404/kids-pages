/* ============================================================
   树上漫步 P11962 - JavaScript 互动教程
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

function getVisitedList(visited) {
  var list = [];
  for (var i = 0; i < visited.length; i++) {
    if (visited[i]) list.push(i);
  }
  return list;
}

/* ============================================================
   1. 样例 1 树渲染 (静态)
   ============================================================ */
function initExample1() {
  var svg = $('example1Tree');
  if (!svg) return;

  var nodes = [
    { label: '1', x: 80, y: 60, depth: 0 },
    { label: '3', x: 250, y: 60, depth: 1 },
    { label: '2', x: 420, y: 60, depth: 2 }
  ];
  var edges = [[0, 1], [1, 2]];

  edges.forEach(function (e) {
    svg.appendChild(createSVG('line', {
      x1: nodes[e[0]].x, y1: nodes[e[0]].y,
      x2: nodes[e[1]].x, y2: nodes[e[1]].y,
      class: 'edge-line active'
    }));
  });

  var answers = [2, 1, 2];
  nodes.forEach(function (node, i) {
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 26,
      class: 'node-circle ' + (node.depth % 2 === 0 ? 'even-depth' : 'odd-depth')
    });
    svg.appendChild(circle);

    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: '#fff', class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);

    var dlabel = createSVG('text', {
      x: node.x, y: node.y - 35, 'text-anchor': 'middle', class: 'depth-label'
    });
    dlabel.textContent = '深度:' + node.depth;
    svg.appendChild(dlabel);

    var ansLabel = createSVG('text', {
      x: node.x, y: node.y + 48, 'text-anchor': 'middle',
      fill: '#10b981', 'font-family': 'JetBrains, monospace',
      'font-weight': '700', 'font-size': '14px',
      'pointer-events': 'none', 'user-select': 'none'
    });
    ansLabel.textContent = '答案:' + answers[i];
    svg.appendChild(ansLabel);
  });
}

/* ============================================================
   2. 偶数步动画 - 路径图
   ============================================================ */
var pathNodes = [
  { label: '1', x: 80, y: 100 },
  { label: '2', x: 230, y: 100 },
  { label: '3', x: 380, y: 100 },
  { label: '4', x: 530, y: 100 },
  { label: '5', x: 680, y: 100 }
];
var pathEdges = [[0, 1], [1, 2], [2, 3], [3, 4]];

var esSteps = (function () {
  var steps = [];
  var visited = [];
  var queue = [];
  var depths = [];
  var cntEven = 0, cntOdd = 0;

  var adj = [[], [], [], [], []];
  pathEdges.forEach(function (e) {
    adj[e[0]].push(e[1]);
    adj[e[1]].push(e[0]);
  });

  queue.push(0);
  depths[0] = 0;
  steps.push({
    current: -1, visited: [], queue: [0], depths: [0],
    cntEven: 0, cntOdd: 0,
    desc: '准备开始 BFS。从节点 1 出发，观察每一步能到达哪些节点。',
  });

  while (queue.length > 0) {
    var u = queue.shift();
    visited[u] = true;
    if (depths[u] % 2 === 0) cntEven++; else cntOdd++;

    var newNodes = [];
    for (var i = 0; i < adj[u].length; i++) {
      var v = adj[u][i];
      if (!visited[v] && depths[v] === undefined) {
        depths[v] = depths[u] + 1;
        queue.push(v);
        newNodes.push(v);
      }
    }

    var desc = '第 ' + depths[u] + ' 步到达节点 ' + pathNodes[u].label +
      '（深度=' + depths[u] + '，' + (depths[u] % 2 === 0 ? '偶数' : '奇数') + '）。';
    if (newNodes.length > 0) {
      desc += '走一步可到达节点 ' + newNodes.map(function (n) { return pathNodes[n].label; }).join('、') + '。';
    }
    desc += ' 偶数步可达 ' + cntEven + ' 个，奇数步可达 ' + cntOdd + ' 个。';
    if (queue.length === 0) desc += ' BFS 完成！';

    steps.push({
      current: u, visited: getVisitedList(visited),
      queue: queue.slice(), depths: depths.slice(),
      cntEven: cntEven, cntOdd: cntOdd, desc: desc
    });
  }

  steps.push({
    current: -1, visited: [0, 1, 2, 3, 4], queue: [],
    depths: depths.slice(), cntEven: cntEven, cntOdd: cntOdd,
    desc: 'BFS 完成！蓝色节点（偶数深度）' + cntEven + ' 个，橙色节点（奇数深度）' + cntOdd +
      ' 个。从蓝色节点出发，偶数步能到 ' + cntEven + ' 个；从橙色节点出发，偶数步能到 ' + cntOdd + ' 个。'
  });

  return steps;
})();

var esState = { stepIdx: 0, playing: false, timer: null, speed: 1000 };

function esRender() {
  var step = esSteps[esState.stepIdx];
  var svg = $('pathGraph');
  if (!svg) return;
  svg.innerHTML = '';

  var visitedSet = new Set(step.visited);
  var queueSet = new Set(step.queue);

  pathEdges.forEach(function (e) {
    var line = createSVG('line', {
      x1: pathNodes[e[0]].x, y1: pathNodes[e[0]].y,
      x2: pathNodes[e[1]].x, y2: pathNodes[e[1]].y,
      class: 'edge-line'
    });
    if (step.depths[e[0]] !== undefined && step.depths[e[1]] !== undefined) {
      line.classList.add('active');
    }
    svg.appendChild(line);
  });

  pathNodes.forEach(function (node, i) {
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 26, class: 'node-circle'
    });

    if (i === step.current) {
      circle.classList.add('current');
    } else if (queueSet.has(i)) {
      circle.classList.add('in-queue');
    } else if (visitedSet.has(i) && step.depths[i] !== undefined) {
      circle.classList.add(step.depths[i] % 2 === 0 ? 'even-depth' : 'odd-depth');
    }
    svg.appendChild(circle);

    var isColored = visitedSet.has(i) || i === step.current || queueSet.has(i);
    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: isColored ? '#fff' : '#475569', class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);

    if (step.depths[i] !== undefined && (visitedSet.has(i) || queueSet.has(i))) {
      var slabel = createSVG('text', {
        x: node.x, y: node.y - 38, 'text-anchor': 'middle',
        fill: step.depths[i] % 2 === 0 ? '#6366f1' : '#f59e0b',
        'font-family': 'JetBrains, monospace', 'font-weight': '700',
        'font-size': '12px', 'pointer-events': 'none', 'user-select': 'none'
      });
      slabel.textContent = step.depths[i] % 2 === 0 ? '偶' : '奇';
      svg.appendChild(slabel);
    }
  });

  $('evenStepInfo').textContent = step.desc;
}

function esPlay() {
  if (esState.playing) return;
  if (esState.stepIdx >= esSteps.length - 1) esState.stepIdx = 0;
  esState.playing = true;
  esTimerStep();
}
function esTimerStep() {
  if (!esState.playing) return;
  esRender();
  if (esState.stepIdx < esSteps.length - 1) {
    esState.stepIdx++;
    esState.timer = setTimeout(esTimerStep, esState.speed);
  } else { esState.playing = false; }
}
function esPause() { esState.playing = false; if (esState.timer) clearTimeout(esState.timer); }
function esStepForward() { esPause(); if (esState.stepIdx < esSteps.length - 1) { esState.stepIdx++; esRender(); } }
function esReset() { esPause(); esState.stepIdx = 0; esRender(); }

function initEvenSteps() {
  if (!$('pathGraph')) return;
  $('esPlay').addEventListener('click', esPlay);
  $('esPause').addEventListener('click', esPause);
  $('esStep').addEventListener('click', esStepForward);
  $('esReset').addEventListener('click', esReset);
  $('esSpeed').addEventListener('input', function () { esState.speed = parseInt(this.value); });
  esRender();
}

/* ============================================================
   3. 深度奇偶性 BFS 动画
   ============================================================ */
var dpTree = {
  nodes: [
    { label: '1', x: 300, y: 40 },
    { label: '2', x: 180, y: 130 },
    { label: '3', x: 420, y: 130 },
    { label: '4', x: 80, y: 230 },
    { label: '5', x: 280, y: 230 },
    { label: '6', x: 420, y: 230 },
    { label: '7', x: 280, y: 340 }
  ],
  edges: [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [4, 6]],
  children: [[1, 2], [3, 4], [5], [], [6], [], []]
};

var dpSteps = (function () {
  var steps = [];
  var visited = [];
  var queue = [];
  var depths = [];
  var cntEven = 0, cntOdd = 0;

  queue.push(0);
  depths[0] = 0;
  steps.push({
    current: -1, visited: [], queue: [0], depths: [0],
    cntEven: 0, cntOdd: 0,
    desc: '准备开始 BFS。根节点 1 入队，深度为 0（偶数）。'
  });

  while (queue.length > 0) {
    var u = queue.shift();
    visited[u] = true;
    if (depths[u] % 2 === 0) cntEven++; else cntOdd++;

    var newNodes = [];
    var kids = dpTree.children[u];
    for (var i = 0; i < kids.length; i++) {
      var v = kids[i];
      if (!visited[v] && depths[v] === undefined) {
        depths[v] = depths[u] + 1;
        queue.push(v);
        newNodes.push(v);
      }
    }

    var parity = depths[u] % 2 === 0 ? '偶数' : '奇数';
    var desc = '访问节点 ' + dpTree.nodes[u].label + '，深度 = ' + depths[u] + '（' + parity + '）。';
    if (newNodes.length > 0) {
      desc += '子节点 ' + newNodes.map(function (n) { return dpTree.nodes[n].label; }).join('、') +
        ' 入队，深度 = ' + (depths[u] + 1) + '。';
    }
    desc += ' 当前：偶数深度 ' + cntEven + ' 个，奇数深度 ' + cntOdd + ' 个。';
    if (queue.length === 0) desc += ' 队列为空，BFS 完成！';

    steps.push({
      current: u, visited: getVisitedList(visited),
      queue: queue.slice(), depths: depths.slice(),
      cntEven: cntEven, cntOdd: cntOdd, desc: desc
    });
  }

  return steps;
})();

var dpState = { stepIdx: 0, playing: false, timer: null, speed: 900 };

function dpRender() {
  var step = dpSteps[dpState.stepIdx];
  var svg = $('depthTree');
  if (!svg) return;
  svg.innerHTML = '';

  var visitedSet = new Set(step.visited);
  var queueSet = new Set(step.queue);

  dpTree.edges.forEach(function (e) {
    var n1 = dpTree.nodes[e[0]], n2 = dpTree.nodes[e[1]];
    var line = createSVG('line', {
      x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y, class: 'edge-line'
    });
    if (step.depths[e[0]] !== undefined && step.depths[e[1]] !== undefined) {
      line.classList.add('active');
    }
    svg.appendChild(line);
  });

  dpTree.nodes.forEach(function (node, i) {
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 26, class: 'node-circle'
    });

    if (i === step.current) {
      circle.classList.add('current');
    } else if (queueSet.has(i)) {
      circle.classList.add('in-queue');
    } else if (visitedSet.has(i) && step.depths[i] !== undefined) {
      circle.classList.add(step.depths[i] % 2 === 0 ? 'even-depth' : 'odd-depth');
    }
    svg.appendChild(circle);

    var isColored = visitedSet.has(i) || i === step.current || queueSet.has(i);
    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: isColored ? '#fff' : '#475569', class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);

    if (step.depths[i] !== undefined && (visitedSet.has(i) || queueSet.has(i))) {
      var dlabel = createSVG('text', {
        x: node.x, y: node.y - 35, 'text-anchor': 'middle', class: 'depth-label'
      });
      dlabel.textContent = 'd=' + step.depths[i];
      svg.appendChild(dlabel);
    }
  });

  var queueDiv = $('dpQueue');
  if (queueDiv) {
    queueDiv.innerHTML = '';
    step.queue.forEach(function (n) {
      var item = document.createElement('div');
      item.className = 'ds-item ' + (step.depths[n] % 2 === 0 ? 'even' : 'odd');
      item.textContent = dpTree.nodes[n].label;
      queueDiv.appendChild(item);
    });
    if (step.queue.length === 0) {
      queueDiv.innerHTML = '<span style="color:var(--muted);font-size:0.85rem;">队列为空</span>';
    }
  }

  var countDiv = $('dpCount');
  if (countDiv) {
    countDiv.innerHTML =
      '<span style="color: var(--accent); font-weight: 700;">偶数深度: ' + step.cntEven + '</span> · ' +
      '<span style="color: var(--accent2); font-weight: 700;">奇数深度: ' + step.cntOdd + '</span>';
  }

  $('depthStepInfo').textContent = step.desc;
}

function dpPlay() {
  if (dpState.playing) return;
  if (dpState.stepIdx >= dpSteps.length - 1) dpState.stepIdx = 0;
  dpState.playing = true;
  dpTimerStep();
}
function dpTimerStep() {
  if (!dpState.playing) return;
  dpRender();
  if (dpState.stepIdx < dpSteps.length - 1) {
    dpState.stepIdx++;
    dpState.timer = setTimeout(dpTimerStep, dpState.speed);
  } else { dpState.playing = false; }
}
function dpPause() { dpState.playing = false; if (dpState.timer) clearTimeout(dpState.timer); }
function dpStepForward() { dpPause(); if (dpState.stepIdx < dpSteps.length - 1) { dpState.stepIdx++; dpRender(); } }
function dpReset() { dpPause(); dpState.stepIdx = 0; dpRender(); }

function initDepthParity() {
  if (!$('depthTree')) return;
  $('dpPlay').addEventListener('click', dpPlay);
  $('dpPause').addEventListener('click', dpPause);
  $('dpStep').addEventListener('click', dpStepForward);
  $('dpReset').addEventListener('click', dpReset);
  $('dpSpeed').addEventListener('input', function () { dpState.speed = parseInt(this.value); });
  dpRender();
}

/* ============================================================
   4. 互动练习场
   ============================================================ */
var pgState = {
  nodes: [], edges: [], mode: 'add',
  connectFirst: -1, depths: null,
  calculated: false, selectedNode: -1, nextId: 0
};

function pgRender() {
  var svg = $('pgSvg');
  if (!svg) return;
  svg.innerHTML = '';
  var hasDepths = pgState.depths !== null;

  pgState.edges.forEach(function (e) {
    var n1 = pgState.nodes[e[0]], n2 = pgState.nodes[e[1]];
    if (!n1 || !n2) return;
    var line = createSVG('line', {
      x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y, class: 'edge-line'
    });
    if (hasDepths) line.classList.add('active');
    svg.appendChild(line);
  });

  pgState.nodes.forEach(function (node, i) {
    if (!node) return;
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 24, class: 'node-circle'
    });

    if (hasDepths && pgState.depths[i] !== undefined) {
      circle.classList.add(pgState.depths[i] % 2 === 0 ? 'even-depth' : 'odd-depth');
    }
    if (i === pgState.connectFirst) circle.classList.add('selected');
    if (pgState.selectedNode >= 0 && hasDepths && pgState.depths[i] !== undefined &&
        pgState.depths[pgState.selectedNode] !== undefined &&
        pgState.depths[i] % 2 === pgState.depths[pgState.selectedNode] % 2) {
      circle.classList.add('reachable');
    }

    circle.addEventListener('click', function (e) {
      e.stopPropagation();
      pgNodeClick(i);
    });
    svg.appendChild(circle);

    var isColored = (hasDepths && pgState.depths[i] !== undefined) || i === pgState.connectFirst;
    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: isColored ? '#fff' : '#475569', class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);

    if (hasDepths && pgState.depths[i] !== undefined) {
      var dlabel = createSVG('text', {
        x: node.x, y: node.y - 33, 'text-anchor': 'middle', class: 'depth-label'
      });
      dlabel.textContent = 'd=' + pgState.depths[i];
      svg.appendChild(dlabel);
    }
  });
}

function pgNodeClick(idx) {
  if (pgState.mode === 'connect') {
    if (pgState.connectFirst === -1) {
      pgState.connectFirst = idx;
      $('pgInfo').textContent = '已选择节点 ' + pgState.nodes[idx].label + '，再点击另一个节点连线。';
    } else if (pgState.connectFirst === idx) {
      pgState.connectFirst = -1;
      $('pgInfo').textContent = '模式：连线。点击两个节点连接它们。';
    } else {
      var exists = pgState.edges.some(function (e) {
        return (e[0] === pgState.connectFirst && e[1] === idx) ||
               (e[0] === idx && e[1] === pgState.connectFirst);
      });
      if (!exists) {
        pgState.edges.push([pgState.connectFirst, idx]);
        pgState.calculated = false; pgState.depths = null; pgState.selectedNode = -1;
        $('pgInfo').textContent = '已连接 ' + pgState.nodes[pgState.connectFirst].label + ' 和 ' + pgState.nodes[idx].label + '。';
      } else {
        $('pgInfo').textContent = '这条边已存在！';
      }
      pgState.connectFirst = -1;
    }
    pgRender();
  } else if (pgState.mode === 'delete') {
    pgState.nodes[idx] = null;
    pgState.edges = pgState.edges.filter(function (e) { return e[0] !== idx && e[1] !== idx; });
    pgState.calculated = false; pgState.depths = null; pgState.selectedNode = -1;
    $('pgInfo').textContent = '已删除节点。';
    pgRender();
  } else if (pgState.mode === 'add' && pgState.calculated) {
    pgState.selectedNode = (pgState.selectedNode === idx) ? -1 : idx;
    if (pgState.selectedNode >= 0) {
      var parity = pgState.depths[idx] % 2;
      var count = 0;
      pgState.depths.forEach(function (d) { if (d !== undefined && d % 2 === parity) count++; });
      $('pgInfo').textContent = '从节点 ' + pgState.nodes[idx].label + ' 出发（深度' + (parity === 0 ? '偶' : '奇') +
        '），偶数步能到达 ' + count + ' 个节点（绿色虚线圈出）。';
    } else {
      $('pgInfo').textContent = '点击节点查看它能偶数步到达哪些节点。';
    }
    pgRender();
  }
}

function pgCanvasClick(e) {
  if (pgState.mode !== 'add') return;
  var svg = $('pgSvg');
  var rect = svg.getBoundingClientRect();
  var x = (e.clientX - rect.left) * (600 / rect.width);
  var y = (e.clientY - rect.top) * (450 / rect.height);

  for (var i = 0; i < pgState.nodes.length; i++) {
    if (pgState.nodes[i]) {
      var dx = pgState.nodes[i].x - x, dy = pgState.nodes[i].y - y;
      if (Math.sqrt(dx * dx + dy * dy) < 60) return;
    }
  }

  pgState.nextId++;
  pgState.nodes.push({ label: String(pgState.nextId), x: x, y: y });
  pgState.calculated = false; pgState.depths = null; pgState.selectedNode = -1;
  $('pgInfo').textContent = '已添加节点 ' + pgState.nextId + '。继续点击空白处添加更多节点。';
  pgRender();
}

function pgCalculate() {
  var root = -1;
  for (var i = 0; i < pgState.nodes.length; i++) { if (pgState.nodes[i]) { root = i; break; } }
  if (root === -1) { $('pgInfo').textContent = '请先添加节点！'; return; }

  var depths = new Array(pgState.nodes.length).fill(undefined);
  var visited = new Array(pgState.nodes.length).fill(false);
  var queue = [root];
  visited[root] = true; depths[root] = 0;

  var adj = {};
  pgState.nodes.forEach(function (n, i) { if (n) adj[i] = []; });
  pgState.edges.forEach(function (e) {
    if (pgState.nodes[e[0]] && pgState.nodes[e[1]]) {
      adj[e[0]].push(e[1]); adj[e[1]].push(e[0]);
    }
  });

  while (queue.length > 0) {
    var u = queue.shift();
    for (var j = 0; j < adj[u].length; j++) {
      var v = adj[u][j];
      if (!visited[v]) { visited[v] = true; depths[v] = depths[u] + 1; queue.push(v); }
    }
  }

  pgState.depths = depths; pgState.calculated = true; pgState.selectedNode = -1;

  var cntEven = 0, cntOdd = 0;
  depths.forEach(function (d) { if (d !== undefined) { if (d % 2 === 0) cntEven++; else cntOdd++; } });

  var html = '<div class="data-struct"><div class="ds-title">统计结果</div>';
  html += '<div style="font-size:0.9rem;line-height:2;">';
  html += '<span style="color:var(--accent);font-weight:700;">偶数深度: ' + cntEven + '</span> · ';
  html += '<span style="color:var(--accent2);font-weight:700;">奇数深度: ' + cntOdd + '</span></div></div>';
  html += '<div class="answer-grid">';
  pgState.nodes.forEach(function (node, i) {
    if (!node || depths[i] === undefined) return;
    var parity = depths[i] % 2;
    html += '<div class="answer-card ' + (parity === 0 ? 'even' : 'odd') + '">';
    html += '<div class="node-num">节点 ' + node.label + '</div>';
    html += '<div class="ans-val">' + (parity === 0 ? cntEven : cntOdd) + '</div></div>';
  });
  html += '</div>';
  $('pgResults').innerHTML = html;
  $('pgInfo').textContent = '计算完成！节点已按深度奇偶性染色。点击任意节点查看它能偶数步到达的节点。';
  pgRender();
}

function pgLoadExample() {
  pgState.nodes = [
    { label: '1', x: 100, y: 80 },
    { label: '3', x: 300, y: 180 },
    { label: '2', x: 500, y: 80 },
    { label: '4', x: 300, y: 330 }
  ];
  pgState.edges = [[0, 1], [1, 2], [1, 3]];
  pgState.nextId = 4; pgState.calculated = false;
  pgState.depths = null; pgState.selectedNode = -1; pgState.connectFirst = -1;
  $('pgResults').innerHTML = '';
  $('pgInfo').textContent = '已加载示例（样例2：4个节点）。点击"计算答案"查看结果！';
  pgRender();
}

function pgClear() {
  pgState.nodes = []; pgState.edges = []; pgState.nextId = 0;
  pgState.calculated = false; pgState.depths = null;
  pgState.selectedNode = -1; pgState.connectFirst = -1;
  $('pgResults').innerHTML = '';
  $('pgInfo').textContent = '画布已清空。点击空白处添加节点。';
  pgRender();
}

function pgSetMode(mode) {
  pgState.mode = mode; pgState.connectFirst = -1;
  var names = { 'add': '添加节点', 'connect': '连线', 'delete': '删除' };
  var infos = {
    'add': pgState.calculated ? '点击节点查看它能偶数步到达哪些节点。' : '点击空白处创建节点。',
    'connect': '点击两个节点连接它们。',
    'delete': '点击节点删除它。'
  };
  $('pgInfo').textContent = '模式：' + names[mode] + '。' + infos[mode];
  $('pgModeAdd').classList.toggle('active', mode === 'add');
  $('pgModeConnect').classList.toggle('active', mode === 'connect');
  $('pgModeDelete').classList.toggle('active', mode === 'delete');
  pgRender();
}

function initPlayground() {
  if (!$('pgSvg')) return;
  $('pgSvg').addEventListener('click', pgCanvasClick);
  $('pgModeAdd').addEventListener('click', function () { pgSetMode('add'); });
  $('pgModeConnect').addEventListener('click', function () { pgSetMode('connect'); });
  $('pgModeDelete').addEventListener('click', function () { pgSetMode('delete'); });
  $('pgCalc').addEventListener('click', pgCalculate);
  $('pgLoadExample').addEventListener('click', pgLoadExample);
  $('pgClear').addEventListener('click', pgClear);
  pgRender();
}

/* ============================================================
   5. 测验
   ============================================================ */
var quizQuestions = [
  {
    q: '从节点 u 出发，经过偶数步能到达的节点 v，u 和 v 的深度（以任意节点为根）的奇偶性关系是？',
    options: ['必须相同', '必须不同', '没有关系', '取决于树的大小'],
    answer: 0,
    explanation: '偶数步到达 ⟺ 距离为偶数 ⟺ 深度差为偶数 ⟺ 深度奇偶性相同。'
  },
  {
    q: '一棵树中偶数深度节点有 a 个，奇数深度节点有 b 个。从一个奇数深度节点出发，偶数步能到达多少个节点？',
    options: ['a 个', 'b 个', 'a + b 个', '0 个'],
    answer: 1,
    explanation: '奇数深度节点只能偶数步到达其他奇数深度节点，所以答案是 b。'
  },
  {
    q: '本题（n ≤ 2×10⁵）的最优时间复杂度是？',
    options: ['O(n²)', 'O(n log n)', 'O(n)', 'O(1)'],
    answer: 2,
    explanation: '一次 BFS 求深度 + 一次遍历统计奇偶 = O(n)。'
  },
  {
    q: '如果题目改成"奇数步"结束漫步，从一个偶数深度节点出发，答案是什么？',
    options: ['偶数深度节点数 a', '奇数深度节点数 b', '总节点数 n', '0'],
    answer: 1,
    explanation: '奇数步到达 ⟺ 距离为奇数 ⟺ 深度奇偶性不同。偶数深度节点奇数步能到所有奇数深度节点，即 b 个。'
  },
  {
    q: '为什么步数和深度差具有相同的奇偶性？',
    options: [
      '因为树没有环',
      '因为步数 = up + down，深度差 = down - up，差值 = 2×up 一定是偶数',
      '因为 BFS 是层序遍历',
      '这只是巧合'
    ],
    answer: 1,
    explanation: '步数 - 深度差 = (up+down) - (down-up) = 2×up，恒为偶数，所以步数 ≡ 深度差 (mod 2)。'
  }
];

var quizAnswered = [];

function initQuiz() {
  var container = $('quizContainer');
  if (!container) return;

  quizQuestions.forEach(function (q, qi) {
    var div = document.createElement('div');
    div.className = 'quiz-question';

    var title = document.createElement('div');
    title.className = 'q-title';
    title.textContent = '第 ' + (qi + 1) + ' 题  ' + q.q;
    div.appendChild(title);

    var options = document.createElement('div');
    options.className = 'quiz-options';

    q.options.forEach(function (opt, oi) {
      var optDiv = document.createElement('div');
      optDiv.className = 'quiz-option';
      optDiv.textContent = String.fromCharCode(65 + oi) + '. ' + opt;
      optDiv.addEventListener('click', function () {
        if (quizAnswered[qi] !== undefined) return;
        quizAnswered[qi] = oi;

        if (oi === q.answer) {
          optDiv.classList.add('correct');
        } else {
          optDiv.classList.add('wrong');
          options.children[q.answer].classList.add('correct');
        }

        var feedback = div.querySelector('.quiz-feedback');
        feedback.classList.add('show');
        feedback.style.color = oi === q.answer ? 'var(--success)' : 'var(--danger)';
        feedback.innerHTML = (oi === q.answer ? '✓ 正确！' : '✗ 错误。') + q.explanation;

        var allAnswered = quizQuestions.every(function (_, i) { return quizAnswered[i] !== undefined; });
        if (allAnswered) {
          var score = quizQuestions.reduce(function (s, qq, i) {
            return s + (quizAnswered[i] === qq.answer ? 1 : 0);
          }, 0);
          var scoreDiv = $('quizScore');
          scoreDiv.classList.add('show');
          scoreDiv.style.background = score >= 4 ? 'var(--success-light)' : 'var(--accent2-light)';
          scoreDiv.style.color = score >= 4 ? 'var(--success)' : 'var(--accent2)';
          scoreDiv.textContent = '得分：' + score + ' / ' + quizQuestions.length + (score >= 4 ? '  🎉 太棒了！' : '  继续加油！');
        }
      });
      options.appendChild(optDiv);
    });

    div.appendChild(options);

    var feedback = document.createElement('div');
    feedback.className = 'quiz-feedback';
    div.appendChild(feedback);

    container.appendChild(div);
  });
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
    sections.forEach(function (s) { if (s.el.offsetTop <= scrollY) current = s; });
    links.forEach(function (l) { l.classList.remove('active'); });
    if (current) current.link.classList.add('active');
  });
}

/* ============================================================
   初始化
   ============================================================ */
document.addEventListener('DOMContentLoaded', function () {
  initExample1();
  initEvenSteps();
  initDepthParity();
  initPlayground();
  initQuiz();
  initNav();
});

})();
