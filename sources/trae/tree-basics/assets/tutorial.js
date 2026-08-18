/* ============================================================
   树的基础教程 - JavaScript
   ============================================================ */

(function () {
'use strict';

var SVG_NS = 'http://www.w3.org/2000/svg';

function createSVG(tag, attrs) {
  var el = document.createElementNS(SVG_NS, tag);
  for (var k in attrs) el.setAttribute(k, attrs[k]);
  return el;
}
function $(id) { return document.getElementById(id); }

/* ============================================================
   共用树数据 (7 节点)
   ============================================================
   结构：
        1
       / \
      2   3
     / \  | \
    4   5 6  7
   ============================================================ */
var tree = {
  nodes: [
    { label: '1', x: 300, y: 50 },
    { label: '2', x: 180, y: 150 },
    { label: '3', x: 420, y: 150 },
    { label: '4', x: 90,  y: 250 },
    { label: '5', x: 270, y: 250 },
    { label: '6', x: 390, y: 250 },
    { label: '7', x: 510, y: 250 }
  ],
  edges: [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]],
  children: [[1,2],[3,4],[5,6],[],[],[],[]],
  parent: [-1,0,0,1,1,2,2],
  depth: [0,1,1,2,2,2,2]
};

/* ============================================================
   1. 基础概念：互动树
   ============================================================ */
function initBasicsTree() {
  var svg = $('basicsTree');
  if (!svg) return;

  var selectedNode = -1;

  function render() {
    svg.innerHTML = '';
    var isLeaf = [false,false,false,true,true,true,true];

    // 画边
    tree.edges.forEach(function (e) {
      var n1 = tree.nodes[e[0]], n2 = tree.nodes[e[1]];
      svg.appendChild(createSVG('line', {
        x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y, class: 'edge-line'
      }));
    });

    // 画节点
    tree.nodes.forEach(function (node, i) {
      var circle = createSVG('circle', {
        cx: node.x, cy: node.y, r: 26, class: 'node-circle'
      });

      if (i === selectedNode) {
        circle.classList.add('current');
      } else if (i === 0) {
        circle.classList.add('visited');
      } else if (isLeaf[i]) {
        circle.classList.add('visited-green');
      }

      circle.addEventListener('click', function () {
        selectedNode = i;
        render();
        showProps(i);
      });
      svg.appendChild(circle);

      var text = createSVG('text', {
        x: node.x, y: node.y + 5, 'text-anchor': 'middle',
        fill: '#fff', class: 'node-label'
      });
      text.textContent = node.label;
      svg.appendChild(text);

      // 深度标签
      var dl = createSVG('text', {
        x: node.x, y: node.y - 35, 'text-anchor': 'middle', class: 'depth-label'
      });
      dl.textContent = 'd=' + tree.depth[i];
      svg.appendChild(dl);
    });
  }

  function showProps(i) {
    var panel = $('propPanel');
    var childList = tree.children[i].map(function (c) {
      return tree.nodes[c].label;
    }).join(', ') || '无';
    var parentLabel = tree.parent[i] === -1 ? '无（根节点）' : tree.nodes[tree.parent[i]].label;
    var isLeaf = tree.children[i].length === 0;
    var degree = tree.children[i].length;

    panel.innerHTML =
      '<div class="card-title">节点 ' + tree.nodes[i].label + ' 的属性</div>' +
      '<div class="prop-row"><span class="prop-name">深度 (Depth)</span><span class="prop-val">' + tree.depth[i] + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">度 (Degree)</span><span class="prop-val">' + degree + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">父节点</span><span class="prop-val">' + parentLabel + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">子节点</span><span class="prop-val">' + childList + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">类型</span><span class="prop-val">' +
        (i === 0 ? '根节点' : (isLeaf ? '叶子节点' : '内部节点')) + '</span></div>';
  }

  render();
}

/* ============================================================
   2. 树的遍历动画
   ============================================================ */
var travState = {
  mode: 'preorder',
  stepIdx: 0,
  playing: false,
  timer: null,
  speed: 800,
  steps: [],
  visited: [],
  order: []
};

var travInfo = {
  preorder: {
    title: '前序遍历 (Preorder)',
    desc: '<p><strong>访问顺序：根 → 左子树 → 右子树</strong></p>' +
          '<p>先访问根节点，然后递归遍历左子树，最后递归遍历右子树。这是最"自然"的 DFS 顺序。</p>' +
          '<p>用途：复制一棵树、输出目录结构、表达式树的前缀表达式。</p>'
  },
  inorder: {
    title: '中序遍历 (Inorder)',
    desc: '<p><strong>访问顺序：左子树 → 根 → 右子树</strong></p>' +
          '<p>先递归遍历左子树，再访问根节点，最后递归遍历右子树。根在中间访问。</p>' +
          '<p>用途：二叉搜索树的中序遍历得到递增序列。注意：对于一般树（非二叉树），中序遍历需要定义"中间"的位置。</p>'
  },
  postorder: {
    title: '后序遍历 (Postorder)',
    desc: '<p><strong>访问顺序：左子树 → 右子树 → 根</strong></p>' +
          '<p>先递归遍历所有子树，最后访问根节点。根在最后访问。</p>' +
          '<p>用途：删除树（先删子树再删根）、子树大小计算、树形 DP。</p>'
  },
  level: {
    title: '层序遍历 (Level Order)',
    desc: '<p><strong>访问顺序：逐层从左到右</strong></p>' +
          '<p>使用 BFS（队列）实现。先访问第 0 层（根），再第 1 层，再第 2 层……</p>' +
          '<p>用途：求每个节点的深度、树的层序结构、BFS 搜索。</p>'
  }
};

function buildTravSteps(mode) {
  var steps = [];
  var visited = [];
  var order = [];

  steps.push({
    visited: [], current: -1, order: [],
    desc: '准备开始' + travInfo[mode].title + '。点击"播放"开始动画。'
  });

  if (mode === 'level') {
    // BFS 层序遍历
    var queue = [0];
    visited.push(0);
    while (queue.length > 0) {
      var u = queue.shift();
      order.push(u);
      var newKids = [];
      tree.children[u].forEach(function (v) {
        if (visited.indexOf(v) === -1) {
          visited.push(v);
          queue.push(v);
          newKids.push(v);
        }
      });
      steps.push({
        visited: visited.slice(), current: u, order: order.slice(),
        desc: '访问节点 ' + tree.nodes[u].label + '（第 ' + tree.depth[u] + ' 层）。' +
          (newKids.length > 0 ? '子节点 ' + newKids.map(function (n) { return tree.nodes[n].label; }).join('、') + ' 入队。' : '') +
          ' 队列：[' + queue.map(function (n) { return tree.nodes[n].label; }).join(', ') + ']'
      });
    }
  } else {
    // DFS 遍历
    function dfs(u) {
      if (mode === 'preorder') {
        visited.push(u);
        order.push(u);
        steps.push({
          visited: visited.slice(), current: u, order: order.slice(),
          desc: '访问节点 ' + tree.nodes[u].label + '（前序：根→左→右，根在第一个访问）。'
        });
      }

      tree.children[u].forEach(function (v) {
        dfs(v);
      });

      if (mode === 'postorder') {
        visited.push(u);
        order.push(u);
        steps.push({
          visited: visited.slice(), current: u, order: order.slice(),
          desc: '访问节点 ' + tree.nodes[u].label + '（后序：左→右→根，根在最后访问）。'
        });
      }

      if (mode === 'inorder' && u !== 0) {
        // 对一般树简化处理：先访问左子树，再访问自己，再访问右子树
      }
    }

    if (mode === 'inorder') {
      // 简化版中序：对每个节点，先访问第一个子节点，再访问自己，再访问剩余子节点
      function inorderDfs(u) {
        var kids = tree.children[u];
        if (kids.length > 0) inorderDfs(kids[0]);
        visited.push(u);
        order.push(u);
        steps.push({
          visited: visited.slice(), current: u, order: order.slice(),
          desc: '访问节点 ' + tree.nodes[u].label + '（中序：左→根→右，根在中间访问）。'
        });
        for (var i = 1; i < kids.length; i++) inorderDfs(kids[i]);
      }
      inorderDfs(0);
    } else {
      dfs(0);
    }
  }

  steps.push({
    visited: visited.slice(), current: -1, order: order.slice(),
    desc: traversInfo(mode) + ' 完成！访问顺序：' + order.map(function (n) { return tree.nodes[n].label; }).join(' → ')
  });

  return steps;
}

function traversInfo(mode) {
  return travInfo[mode].title;
}

function travRender() {
  var svg = $('traversalTree');
  if (!svg) return;
  svg.innerHTML = '';

  var step = travState.steps[travState.stepIdx];
  var visitedSet = new Set(step.visited);

  tree.edges.forEach(function (e) {
    var n1 = tree.nodes[e[0]], n2 = tree.nodes[e[1]];
    var line = createSVG('line', {
      x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y, class: 'edge-line'
    });
    if (visitedSet.has(e[0]) && visitedSet.has(e[1])) {
      line.classList.add('active');
    }
    svg.appendChild(line);
  });

  tree.nodes.forEach(function (node, i) {
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 26, class: 'node-circle'
    });
    if (i === step.current) {
      circle.classList.add('current');
    } else if (visitedSet.has(i)) {
      circle.classList.add('visited');
    }
    svg.appendChild(circle);

    var isColored = visitedSet.has(i) || i === step.current;
    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: isColored ? '#fff' : '#475569', class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);
  });

  $('travStepInfo').textContent = step.desc;
  renderOrder('travOrder', step.order);
}

function renderOrder(elId, order) {
  var div = $(elId);
  if (!div) return;
  var label = div.querySelector('.label');
  div.innerHTML = '';
  var l = document.createElement('span');
  l.className = 'label';
  l.textContent = '访问顺序：';
  div.appendChild(l);

  order.forEach(function (nodeIdx, i) {
    var item = document.createElement('span');
    item.className = 'order-item';
    item.style.background = 'var(--accent)';
    item.textContent = tree.nodes[nodeIdx].label;
    div.appendChild(item);
    if (i < order.length - 1) {
      var arrow = document.createElement('span');
      arrow.className = 'arrow';
      arrow.textContent = '→';
      div.appendChild(arrow);
    }
  });
}

function travPlay() {
  if (travState.playing) return;
  if (travState.stepIdx >= travState.steps.length - 1) travState.stepIdx = 0;
  travState.playing = true;
  travTimerStep();
}
function travTimerStep() {
  if (!travState.playing) return;
  travRender();
  if (travState.stepIdx < travState.steps.length - 1) {
    travState.stepIdx++;
    travState.timer = setTimeout(travTimerStep, travState.speed);
  } else { travState.playing = false; }
}
function travPause() { travState.playing = false; if (travState.timer) clearTimeout(travState.timer); }
function travStepForward() {
  travPause();
  if (travState.stepIdx < travState.steps.length - 1) { travState.stepIdx++; travRender(); }
}
function travReset() { travPause(); travState.stepIdx = 0; travRender(); }

function setTravMode(mode) {
  travState.mode = mode;
  travState.steps = buildTravSteps(mode);
  travState.stepIdx = 0;
  travPause();
  travRender();

  // 更新 tab 样式
  ['Preorder','Inorder','Postorder','Level'].forEach(function (m) {
    $('tab' + m).classList.toggle('active', m.toLowerCase() === mode);
  });

  // 更新说明
  $('travTitle').textContent = travInfo[mode].title;
  $('travDesc').innerHTML = travInfo[mode].desc;
}

function initTraversal() {
  if (!$('traversalTree')) return;
  setTravMode('preorder');
  $('travPlay').addEventListener('click', travPlay);
  $('travPause').addEventListener('click', travPause);
  $('travStep').addEventListener('click', travStepForward);
  $('travReset').addEventListener('click', travReset);
  $('travSpeed').addEventListener('input', function () { travState.speed = parseInt(this.value); });
  $('tabPreorder').addEventListener('click', function () { setTravMode('preorder'); });
  $('tabInorder').addEventListener('click', function () { setTravMode('inorder'); });
  $('tabPostorder').addEventListener('click', function () { setTravMode('postorder'); });
  $('tabLevel').addEventListener('click', function () { setTravMode('level'); });
}

/* ============================================================
   3. 子树大小动画
   ============================================================ */
var subState = { stepIdx: 0, playing: false, timer: null, speed: 800, steps: [] };

function buildSubSteps() {
  var steps = [];
  var sizes = [0,0,0,0,0,0,0];
  var visited = [];
  var stack = [];

  steps.push({
    visited: [], current: -1, stack: [], sizes: [0,0,0,0,0,0,0],
    desc: '准备开始计算子树大小。DFS 从根节点 1 开始。'
  });

  function dfs(u) {
    stack.push(u);
    steps.push({
      visited: visited.slice(), current: u, stack: stack.slice(),
      sizes: sizes.slice(),
      desc: '进入节点 ' + tree.nodes[u].label + '，初始 size[' + tree.nodes[u].label + '] = 1。'
    });

    sizes[u] = 1;
    steps.push({
      visited: visited.slice(), current: u, stack: stack.slice(),
      sizes: sizes.slice(),
      desc: 'size[' + tree.nodes[u].label + '] = 1（先算上自己）。'
    });

    tree.children[u].forEach(function (v) {
      dfs(v);
      sizes[u] += sizes[v];
      steps.push({
        visited: visited.slice(), current: u, stack: stack.slice(),
        sizes: sizes.slice(),
        desc: '子节点 ' + tree.nodes[v].label + ' 的子树大小为 ' + sizes[v] +
          '，累加到 size[' + tree.nodes[u].label + '] = ' + sizes[u] + '。'
      });
    });

    visited.push(u);
    stack.pop();
    steps.push({
      visited: visited.slice(), current: u, stack: stack.slice(),
      sizes: sizes.slice(),
      desc: '节点 ' + tree.nodes[u].label + ' 计算完成，size = ' + sizes[u] + '。' +
        (stack.length > 0 ? ' 返回到节点 ' + tree.nodes[stack[stack.length-1]].label + '。' : ' 栈空，全部完成！')
    });
  }

  dfs(0);
  return steps;
}

function subRender() {
  var svg = $('subtreeTree');
  if (!svg) return;
  svg.innerHTML = '';

  var step = subState.steps[subState.stepIdx];
  var visitedSet = new Set(step.visited);
  var stackSet = new Set(step.stack);

  tree.edges.forEach(function (e) {
    var n1 = tree.nodes[e[0]], n2 = tree.nodes[e[1]];
    var line = createSVG('line', {
      x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y, class: 'edge-line'
    });
    if (visitedSet.has(e[0]) && visitedSet.has(e[1])) {
      line.classList.add('active');
    }
    svg.appendChild(line);
  });

  tree.nodes.forEach(function (node, i) {
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 26, class: 'node-circle'
    });
    if (i === step.current) {
      circle.classList.add('current');
    } else if (visitedSet.has(i)) {
      circle.classList.add('visited-amber');
    }
    svg.appendChild(circle);

    var isColored = visitedSet.has(i) || i === step.current;
    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: isColored ? '#fff' : '#475569', class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);

    // 显示 size 值
    if (step.sizes[i] > 0) {
      var sl = createSVG('text', {
        x: node.x, y: node.y - 35, 'text-anchor': 'middle',
        fill: '#f59e0b', 'font-family': 'JetBrains, monospace',
        'font-weight': '700', 'font-size': '13px',
        'pointer-events': 'none', 'user-select': 'none'
      });
      sl.textContent = 'size=' + step.sizes[i];
      svg.appendChild(sl);
    }
  });

  // 渲染调用栈
  var stackDiv = $('subtreeStack');
  if (stackDiv) {
    stackDiv.innerHTML = '';
    step.stack.forEach(function (n, i) {
      var frame = document.createElement('div');
      frame.className = 'stack-frame';
      var isActive = (i === step.stack.length - 1);
      frame.style.background = isActive ? '#ef4444' : '#f59e0b';
      frame.textContent = 'dfs(' + tree.nodes[n].label + ')';
      stackDiv.appendChild(frame);
    });
    if (step.stack.length === 0) {
      stackDiv.innerHTML = '<span style="color:var(--muted);font-size:0.85rem;">栈为空</span>';
    }
  }

  $('subtreeStepInfo').textContent = step.desc;
}

function subPlay() {
  if (subState.playing) return;
  if (subState.stepIdx >= subState.steps.length - 1) subState.stepIdx = 0;
  subState.playing = true;
  subTimerStep();
}
function subTimerStep() {
  if (!subState.playing) return;
  subRender();
  if (subState.stepIdx < subState.steps.length - 1) {
    subState.stepIdx++;
    subState.timer = setTimeout(subTimerStep, subState.speed);
  } else { subState.playing = false; }
}
function subPause() { subState.playing = false; if (subState.timer) clearTimeout(subState.timer); }
function subStepForward() {
  subPause();
  if (subState.stepIdx < subState.steps.length - 1) { subState.stepIdx++; subRender(); }
}
function subReset() { subPause(); subState.stepIdx = 0; subRender(); }

function initSubtree() {
  if (!$('subtreeTree')) return;
  subState.steps = buildSubSteps();
  $('subPlay').addEventListener('click', subPlay);
  $('subPause').addEventListener('click', subPause);
  $('subStep').addEventListener('click', subStepForward);
  $('subReset').addEventListener('click', subReset);
  $('subSpeed').addEventListener('input', function () { subState.speed = parseInt(this.value); });
  subRender();
}

/* ============================================================
   4. LCA 交互
   ============================================================ */
var lcaState = { selected: [], lca: -1, path: [] };

function getPath(u, v) {
  // 求 u 到 v 的路径
  var pathU = [], pathV = [];
  var x = u, y = v;

  // 收集 u 到根的路径
  while (x !== -1) { pathU.push(x); x = tree.parent[x]; }
  // 收集 v 到根的路径
  while (y !== -1) { pathV.push(y); y = tree.parent[y]; }

  // 找 LCA
  var lca = -1;
  var i = pathU.length - 1, j = pathV.length - 1;
  while (i >= 0 && j >= 0 && pathU[i] === pathV[j]) {
    lca = pathU[i];
    i--; j--;
  }

  // 构建路径：u → LCA → v
  var path = [];
  for (var k = 0; k <= i; k++) path.push(pathU[k]);
  path.push(lca);
  for (var k = j; k >= 0; k--) path.push(pathV[k]);

  return { lca: lca, path: path };
}

function lcaRender() {
  var svg = $('lcaTree');
  if (!svg) return;
  svg.innerHTML = '';

  var pathSet = new Set(lcaState.path);
  var lcaSet = new Set([lcaState.lca]);
  lcaState.lca !== -1 && (lcaSet = new Set([lcaState.lca]));

  // 画边
  tree.edges.forEach(function (e) {
    var n1 = tree.nodes[e[0]], n2 = tree.nodes[e[1]];
    var line = createSVG('line', {
      x1: n1.x, y1: n1.y, x2: n2.x, y2: n2.y, class: 'edge-line'
    });
    if (pathSet.has(e[0]) && pathSet.has(e[1])) {
      line.classList.add('path');
    }
    svg.appendChild(line);
  });

  // 画节点
  tree.nodes.forEach(function (node, i) {
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 26, class: 'node-circle'
    });

    if (lcaState.lca === i) {
      circle.classList.add('lca');
    } else if (pathSet.has(i)) {
      circle.classList.add('path-node');
    } else if (lcaState.selected.indexOf(i) >= 0) {
      circle.classList.add('selected');
    }

    circle.addEventListener('click', function () { lcaClick(i); });
    svg.appendChild(circle);

    var isColored = pathSet.has(i) || lcaState.lca === i;
    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: isColored ? '#fff' : '#475569', class: 'node-label'
    });
    text.textContent = node.label;
    svg.appendChild(text);

    // 深度标签
    var dl = createSVG('text', {
      x: node.x, y: node.y - 35, 'text-anchor': 'middle', class: 'depth-label'
    });
    dl.textContent = 'd=' + tree.depth[i];
    svg.appendChild(dl);
  });

  // 更新面板
  var panel = $('lcaPanel');
  if (lcaState.selected.length === 0) {
    panel.innerHTML = '<div class="card-title">LCA 查询</div>' +
      '<p style="color: var(--muted); font-size: 0.85rem;">点击树上的两个节点</p>';
  } else if (lcaState.selected.length === 1) {
    panel.innerHTML = '<div class="card-title">LCA 查询</div>' +
      '<div class="prop-row"><span class="prop-name">已选节点 1</span><span class="prop-val">节点 ' + tree.nodes[lcaState.selected[0]].label + '</span></div>' +
      '<p style="color: var(--muted); font-size: 0.85rem; margin-top: 0.5rem;">再点击一个节点</p>';
  } else {
    var u = lcaState.selected[0], v = lcaState.selected[1];
    var lca = lcaState.lca;
    var dist = tree.depth[u] + tree.depth[v] - 2 * tree.depth[lca];
    var pathStr = lcaState.path.map(function (n) { return tree.nodes[n].label; }).join(' → ');

    panel.innerHTML = '<div class="card-title">LCA 查询结果</div>' +
      '<div class="prop-row"><span class="prop-name">节点 u</span><span class="prop-val">节点 ' + tree.nodes[u].label + ' (d=' + tree.depth[u] + ')</span></div>' +
      '<div class="prop-row"><span class="prop-name">节点 v</span><span class="prop-val">节点 ' + tree.nodes[v].label + ' (d=' + tree.depth[v] + ')</span></div>' +
      '<div class="prop-row"><span class="prop-name">LCA</span><span class="prop-val" style="color:var(--accent4)">节点 ' + tree.nodes[lca].label + ' (d=' + tree.depth[lca] + ')</span></div>' +
      '<div class="prop-row"><span class="prop-name">树上距离</span><span class="prop-val" style="color:var(--accent2)">' + dist + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">公式</span><span class="prop-val" style="font-size:0.8rem">' + tree.depth[u] + '+' + tree.depth[v] + '-2*'+tree.depth[lca]+'=' + dist + '</span></div>' +
      '<div style="margin-top:0.5rem;font-size:0.85rem;color:var(--muted);">路径：' + pathStr + '</div>';
  }
}

function lcaClick(i) {
  if (lcaState.selected.length >= 2) {
    lcaState.selected = [i];
    lcaState.lca = -1;
    lcaState.path = [];
  } else if (lcaState.selected.length === 1 && lcaState.selected[0] === i) {
    lcaState.selected = [];
    lcaState.lca = -1;
    lcaState.path = [];
  } else {
    lcaState.selected.push(i);
    if (lcaState.selected.length === 2) {
      var result = getPath(lcaState.selected[0], lcaState.selected[1]);
      lcaState.lca = result.lca;
      lcaState.path = result.path;
    }
  }
  lcaRender();
}

function initLCA() {
  if (!$('lcaTree')) return;
  $('lcaResetBtn').addEventListener('click', function () {
    lcaState.selected = [];
    lcaState.lca = -1;
    lcaState.path = [];
    lcaRender();
  });
  lcaRender();
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
  initBasicsTree();
  initTraversal();
  initSubtree();
  initLCA();
  initNav();
});

})();
