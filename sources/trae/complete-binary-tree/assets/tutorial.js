/* ============================================================
   完全二叉子树计数 - JavaScript 互动教程
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
   树数据定义
   ============================================================ */

var trees = {
  ex1: {
    n: 4,
    lc: [0, 2, 4, 0, 0],
    rc: [0, 3, 0, 0, 0],
    pos: [
      null,
      { x: 300, y: 50 },
      { x: 180, y: 150 },
      { x: 420, y: 150 },
      { x: 100, y: 250 }
    ]
  },
  ex2: {
    n: 4,
    lc: [0, 2, 0, 4, 0],
    rc: [0, 3, 0, 0, 0],
    pos: [
      null,
      { x: 300, y: 50 },
      { x: 180, y: 150 },
      { x: 420, y: 150 },
      { x: 340, y: 250 }
    ]
  },
  ex3: {
    n: 9,
    lc: [0, 2, 4, 0, 7, 0, 0, 0, 0, 0],
    rc: [0, 3, 5, 6, 8, 0, 0, 0, 0, 0],
    pos: [
      null,
      { x: 300, y: 30 },
      { x: 180, y: 100 },
      { x: 420, y: 100 },
      { x: 100, y: 200 },
      { x: 260, y: 200 },
      { x: 480, y: 200 },
      { x: 50, y: 290 },
      { x: 150, y: 290 },
      { x: 430, y: 290 }
    ]
  }
};

/* ============================================================
   核心算法：后序 DFS 计算 height / isPerfect / isComplete
   ============================================================ */

function computeTree(tree) {
  var n = tree.n;
  var lc = tree.lc, rc = tree.rc;
  var h = new Array(n + 1);
  var perf = new Array(n + 1);
  var comp = new Array(n + 1);
  var order = [];

  function dfs(u) {
    var l = lc[u], r = rc[u];
    if (l === 0 && r === 0) {
      h[u] = 0; perf[u] = true; comp[u] = true;
    } else if (l !== 0 && r === 0) {
      dfs(l);
      h[u] = h[l] + 1;
      perf[u] = false;
      comp[u] = (h[l] === 0);
    } else if (l === 0 && r !== 0) {
      dfs(r);
      h[u] = h[r] + 1;
      perf[u] = false;
      comp[u] = false;
    } else {
      dfs(l);
      dfs(r);
      h[u] = Math.max(h[l], h[r]) + 1;
      perf[u] = perf[l] && perf[r] && (h[l] === h[r]);
      if (h[l] === h[r]) {
        comp[u] = comp[l] && perf[r];
      } else if (h[l] === h[r] + 1) {
        comp[u] = comp[l] && perf[r];
      } else {
        comp[u] = false;
      }
    }
    order.push(u);
  }

  dfs(1);
  return { h: h, perf: perf, comp: comp, order: order };
}

/* ============================================================
   1. 样例树静态渲染
   ============================================================ */

function renderStaticTree(svgId, tree, showResult) {
  var svg = $(svgId);
  if (!svg) return;
  svg.innerHTML = '';

  var data = computeTree(tree);

  tree.lc.forEach(function (lc_val, i) {
    if (i === 0) return;
    if (lc_val !== 0) {
      var p1 = tree.pos[i], p2 = tree.pos[lc_val];
      svg.appendChild(createSVG('line', {
        x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y, class: 'edge-line active'
      }));
    }
    if (tree.rc[i] !== 0) {
      var p3 = tree.pos[tree.rc[i]];
      svg.appendChild(createSVG('line', {
        x1: p1.x, y1: p1.y, x2: p3.x, y2: p3.y, class: 'edge-line active'
      }));
    }
  });

  for (var i = 1; i <= tree.n; i++) {
    var node = tree.pos[i];
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 24, class: 'node-circle'
    });
    if (showResult) {
      if (data.comp[i]) {
        circle.classList.add(data.perf[i] ? 'perfect' : 'complete');
      } else {
        circle.classList.add('incomplete');
      }
    }
    svg.appendChild(circle);

    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: '#fff', class: 'node-label'
    });
    text.textContent = i;
    svg.appendChild(text);

    if (showResult) {
      var badge = createSVG('text', {
        x: node.x, y: node.y + 42, 'text-anchor': 'middle',
        'font-family': 'Outfit, sans-serif', 'font-size': '16px', 'font-weight': '700',
        'pointer-events': 'none', 'user-select': 'none'
      });
      badge.textContent = data.comp[i] ? '\u2713' : '\u2717';
      badge.setAttribute('fill', data.comp[i] ? '#10b981' : '#ef4444');
      svg.appendChild(badge);
    }
  }
}

function initExampleTrees() {
  renderStaticTree('ex1Tree', trees.ex1, true);
  renderStaticTree('ex2Tree', trees.ex2, true);
}

/* ============================================================
   2. 概念树网格（点击判定）
   ============================================================ */

var conceptTrees = [
  {
    name: 'A',
    nodes: [{ x: 150, y: 80 }],
    edges: [],
    isComplete: true,
    explain: '单个节点是叶子，叶子一定是完全二叉树。'
  },
  {
    name: 'B',
    nodes: [
      { x: 150, y: 40 }, { x: 100, y: 120 }, { x: 200, y: 120 }
    ],
    edges: [[0, 1], [0, 2]],
    isComplete: true,
    explain: '两层都满了，这是满二叉树，当然也是完全二叉树。'
  },
  {
    name: 'C',
    nodes: [
      { x: 150, y: 40 }, { x: 120, y: 120 }
    ],
    edges: [[0, 1]],
    isComplete: true,
    explain: '根有左子无右子，且左子是叶子。最后一层只有 1 个节点在最左边，符合完全二叉树。'
  },
  {
    name: 'D',
    nodes: [
      { x: 150, y: 40 }, { x: 180, y: 120 }
    ],
    edges: [[0, 1]],
    isComplete: false,
    explain: '根只有右子没有左子。最后一层从左到右，左边的位置空着，不符合完全二叉树。'
  },
  {
    name: 'E',
    nodes: [
      { x: 150, y: 30 },
      { x: 100, y: 90 }, { x: 200, y: 90 },
      { x: 70, y: 150 }, { x: 130, y: 150 }, { x: 170, y: 150 }, { x: 230, y: 150 }
    ],
    edges: [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [2, 6]],
    isComplete: true,
    explain: '三层全满，是满二叉树，当然也是完全二叉树。'
  },
  {
    name: 'F',
    nodes: [
      { x: 150, y: 30 },
      { x: 100, y: 90 }, { x: 200, y: 90 },
      { x: 70, y: 150 }
    ],
    edges: [[0, 1], [0, 2], [1, 3]],
    isComplete: true,
    explain: '前两层满，第三层只有 1 个节点在最左边的位置。符合完全二叉树。'
  },
  {
    name: 'G',
    nodes: [
      { x: 150, y: 30 },
      { x: 100, y: 90 }, { x: 200, y: 90 },
      { x: 170, y: 150 }
    ],
    edges: [[0, 1], [0, 2], [2, 3]],
    isComplete: false,
    explain: '第三层的节点在右边（右子的左子），但左边空着。不符合"从左到右排满"。'
  },
  {
    name: 'H',
    nodes: [
      { x: 150, y: 30 },
      { x: 120, y: 90 },
      { x: 90, y: 150 }
    ],
    edges: [[0, 1], [1, 2]],
    isComplete: false,
    explain: '第二层只有 1 个节点（缺右子），但还有第三层。第二层不满却有第三层，不符合完全二叉树。'
  }
];

function initConceptGrid() {
  var grid = $('conceptGrid');
  if (!grid) return;

  conceptTrees.forEach(function (ct, idx) {
    var card = document.createElement('div');
    card.className = 'concept-card';
    card.dataset.idx = idx;

    var svg = document.createElementNS(SVG_NS, 'svg');
    svg.setAttribute('viewBox', '0 0 300 200');

    ct.edges.forEach(function (e) {
      svg.appendChild(createSVG('line', {
        x1: ct.nodes[e[0]].x, y1: ct.nodes[e[0]].y,
        x2: ct.nodes[e[1]].x, y2: ct.nodes[e[1]].y,
        class: 'edge-line active'
      }));
    });

    ct.nodes.forEach(function (node, i) {
      svg.appendChild(createSVG('circle', {
        cx: node.x, cy: node.y, r: 18, class: 'node-circle',
        fill: '#cbd5e1', stroke: '#94a3b8', 'stroke-width': '1.5'
      }));
      var t = createSVG('text', {
        x: node.x, y: node.y + 4, 'text-anchor': 'middle',
        fill: '#475569', 'font-family': 'JetBrains, monospace',
        'font-weight': '700', 'font-size': '12px',
        'pointer-events': 'none', 'user-select': 'none'
      });
      t.textContent = i + 1;
      svg.appendChild(t);
    });

    card.appendChild(svg);

    var verdict = document.createElement('div');
    verdict.className = 'verdict';
    verdict.textContent = '? 点击查看';
    card.appendChild(verdict);

    var explain = document.createElement('div');
    explain.className = 'explain';
    explain.textContent = ct.explain;
    card.appendChild(explain);

    card.addEventListener('click', function () {
      if (card.classList.contains('revealed')) return;
      card.classList.add('revealed');
      card.classList.add(ct.isComplete ? 'correct' : 'wrong');
      verdict.textContent = ct.isComplete ? '\u2713 完全二叉树' : '\u2717 不是完全二叉树';

      svg.querySelectorAll('.node-circle').forEach(function (c, i) {
        c.setAttribute('fill', ct.isComplete ? '#10b981' : '#ef4444');
        c.setAttribute('stroke', 'none');
      });
      svg.querySelectorAll('text').forEach(function (t) {
        if (t.getAttribute('fill') !== 'none' && t.tagName === 'text') {
          t.setAttribute('fill', '#fff');
        }
      });
    });

    grid.appendChild(card);
  });
}

/* ============================================================
   3. 递归判定 - 互动属性面板
   ============================================================ */

function initApproachExplorer() {
  var svg = $('approachTree');
  if (!svg) return;

  var tree = trees.ex2;
  var data = computeTree(tree);

  svg.innerHTML = '';

  tree.lc.forEach(function (lc_val, i) {
    if (i === 0) return;
    if (lc_val !== 0) {
      var p1 = tree.pos[i], p2 = tree.pos[lc_val];
      svg.appendChild(createSVG('line', {
        x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y, class: 'edge-line active'
      }));
    }
    if (tree.rc[i] !== 0) {
      var p3 = tree.pos[tree.rc[i]];
      svg.appendChild(createSVG('line', {
        x1: p1.x, y1: p1.y, x2: p3.x, y2: p3.y, class: 'edge-line active'
      }));
    }
  });

  for (var i = 1; i <= tree.n; i++) {
    (function (nodeIdx) {
      var node = tree.pos[nodeIdx];
      var circle = createSVG('circle', {
        cx: node.x, cy: node.y, r: 24, class: 'node-circle'
      });
      circle.addEventListener('click', function () {
        showApproachProps(nodeIdx);
        svg.querySelectorAll('.node-circle').forEach(function (c) {
          c.classList.remove('selected');
        });
        circle.classList.add('selected');
      });
      svg.appendChild(circle);

      var text = createSVG('text', {
        x: node.x, y: node.y + 5, 'text-anchor': 'middle',
        fill: '#fff', class: 'node-label'
      });
      text.textContent = nodeIdx;
      svg.appendChild(text);
    })(i);
  }

  function showApproachProps(idx) {
    var panel = $('approachPanel');
    var isLeaf = tree.lc[idx] === 0 && tree.rc[idx] === 0;
    var caseName;
    if (isLeaf) caseName = '叶子节点';
    else if (tree.lc[idx] !== 0 && tree.rc[idx] === 0) caseName = '只有左子 ' + tree.lc[idx];
    else if (tree.lc[idx] === 0 && tree.rc[idx] !== 0) caseName = '只有右子 ' + tree.rc[idx];
    else caseName = '左子 ' + tree.lc[idx] + '，右子 ' + tree.rc[idx];

    var hVal = data.h[idx];
    var pVal = data.perf[idx];
    var cVal = data.comp[idx];

    panel.innerHTML =
      '<div class="card-title">节点 ' + idx + '</div>' +
      '<div class="prop-row"><span class="prop-name">情形</span><span class="prop-val">' + caseName + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">height</span><span class="prop-val">' + hVal + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">isPerfect</span><span class="prop-val ' + (pVal ? 'true' : 'false') + '">' + (pVal ? 'true' : 'false') + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">isComplete</span><span class="prop-val ' + (cVal ? 'true' : 'false') + '">' + (cVal ? 'true' : 'false') + '</span></div>';

    if (!isLeaf && tree.lc[idx] !== 0 && tree.rc[idx] !== 0) {
      var hL = data.h[tree.lc[idx]], hR = data.h[tree.rc[idx]];
      var detail;
      if (hL === hR) detail = 'h[l]==h[r](' + hL + '==' + hR + ') \u2192 comp[l] && perf[r]';
      else if (hL === hR + 1) detail = 'h[l]==h[r]+1(' + hL + '==' + hR + '+1) \u2192 comp[l] && perf[r]';
      else detail = 'h[l]=' + hL + ', h[r]=' + hR + ' \u2192 false';
      panel.innerHTML += '<div class="prop-row"><span class="prop-name">判定依据</span><span class="prop-val" style="font-size:0.8rem;">' + detail + '</span></div>';
    } else if (tree.lc[idx] !== 0 && tree.rc[idx] === 0) {
      panel.innerHTML += '<div class="prop-row"><span class="prop-name">判定依据</span><span class="prop-val" style="font-size:0.8rem;">h[l]==' + data.h[tree.lc[idx]] + (data.h[tree.lc[idx]] === 0 ? ' \u2192 true' : ' \u2192 false') + '</span></div>';
    } else if (tree.lc[idx] === 0 && tree.rc[idx] !== 0) {
      panel.innerHTML += '<div class="prop-row"><span class="prop-name">判定依据</span><span class="prop-val" style="font-size:0.8rem;">只有右子 \u2192 false</span></div>';
    }
  }
}

/* ============================================================
   4. 算法动画
   ============================================================ */

var animState = {
  currentExample: 'ex1',
  stepIdx: 0,
  steps: [],
  playing: false,
  timer: null,
  speed: 1000
};

function buildAnimSteps(tree) {
  var data = computeTree(tree);
  var lc = tree.lc, rc = tree.rc;
  var steps = [];
  var h = {}, perf = {}, comp = {};
  var visited = [];
  var stack = [];

  steps.push({
    current: -1, stack: [], visited: [],
    h: {}, perf: {}, comp: {},
    desc: '准备开始后序 DFS。从根节点 1 出发。',
    nodeStatus: {}
  });

  function dfs(u) {
    stack.push(u);
    steps.push({
      current: u, stack: stack.slice(), visited: visited.slice(),
      h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
      desc: 'DFS(' + u + ') \u2192 进入节点 ' + u,
      nodeStatus: buildStatusMap(h, perf, comp, visited, u)
    });

    var l = lc[u], r = rc[u];

    if (l !== 0) {
      steps.push({
        current: u, stack: stack.slice(), visited: visited.slice(),
        h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
        desc: '节点 ' + u + ' 有左子 ' + l + '，先递归 DFS(' + l + ')',
        nodeStatus: buildStatusMap(h, perf, comp, visited, u)
      });
      dfs(l);
    }

    if (r !== 0) {
      steps.push({
        current: u, stack: stack.slice(), visited: visited.slice(),
        h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
        desc: '节点 ' + u + ' 有右子 ' + r + '，递归 DFS(' + r + ')',
        nodeStatus: buildStatusMap(h, perf, comp, visited, u)
      });
      dfs(r);
    }

    if (l === 0 && r === 0) {
      h[u] = 0; perf[u] = true; comp[u] = true;
      steps.push({
        current: u, stack: stack.slice(), visited: visited.slice(),
        h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
        desc: '节点 ' + u + ' 是叶子 \u2192 h=0, isPerfect=true, isComplete=true',
        nodeStatus: buildStatusMap(h, perf, comp, visited, u)
      });
    } else if (l !== 0 && r === 0) {
      h[u] = h[l] + 1;
      perf[u] = false;
      comp[u] = (h[l] === 0);
      steps.push({
        current: u, stack: stack.slice(), visited: visited.slice(),
        h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
        desc: '节点 ' + u + ' 只有左子 ' + l + ' \u2192 h=' + h[u] + ', isComplete=' + comp[u] + (comp[u] ? '（左子是叶子）' : '（左子不是叶子）'),
        nodeStatus: buildStatusMap(h, perf, comp, visited, u)
      });
    } else if (l === 0 && r !== 0) {
      h[u] = h[r] + 1;
      perf[u] = false;
      comp[u] = false;
      steps.push({
        current: u, stack: stack.slice(), visited: visited.slice(),
        h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
        desc: '节点 ' + u + ' 只有右子 ' + r + ' \u2192 isComplete=false',
        nodeStatus: buildStatusMap(h, perf, comp, visited, u)
      });
    } else {
      h[u] = Math.max(h[l], h[r]) + 1;
      perf[u] = perf[l] && perf[r] && (h[l] === h[r]);
      if (h[l] === h[r]) {
        comp[u] = comp[l] && perf[r];
      } else if (h[l] === h[r] + 1) {
        comp[u] = comp[l] && perf[r];
      } else {
        comp[u] = false;
      }
      var detail;
      if (h[l] === h[r]) detail = 'h[l]==h[r]=' + h[l] + ' \u2192 comp[l] && perf[r] = ' + comp[u];
      else if (h[l] === h[r] + 1) detail = 'h[l]=' + h[l] + ', h[r]=' + h[r] + ' (左高一层) \u2192 comp[l] && perf[r] = ' + comp[u];
      else detail = 'h[l]=' + h[l] + ', h[r]=' + h[r] + ' (高度差过大) \u2192 isComplete=false';
      steps.push({
        current: u, stack: stack.slice(), visited: visited.slice(),
        h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
        desc: '节点 ' + u + ' 有两子 \u2192 h=' + h[u] + ', isPerfect=' + perf[u] + ', isComplete=' + comp[u] + '（' + detail + '）',
        nodeStatus: buildStatusMap(h, perf, comp, visited, u)
      });
    }

    visited.push(u);
    stack.pop();
  }

  dfs(1);

  var cnt = 0;
  for (var i = 1; i <= tree.n; i++) if (comp[i]) cnt++;
  steps.push({
    current: -1, stack: [], visited: visited.slice(),
    h: cloneMap(h), perf: cloneMap(perf), comp: cloneMap(comp),
    desc: '遍历完成！isComplete=true 的节点有 ' + Object.keys(comp).filter(function (k) { return comp[k]; }).length + ' 个，答案 = ' + cnt,
    nodeStatus: buildStatusMap(h, perf, comp, visited, -1),
    finalResult: cnt
  });

  return steps;
}

function cloneMap(m) {
  var r = {};
  for (var k in m) r[k] = m[k];
  return r;
}

function buildStatusMap(h, perf, comp, visited, current) {
  var status = {};
  for (var k in h) {
    var idx = parseInt(k);
    status[idx] = {
      h: h[k], perf: perf[k], comp: comp[k],
      visited: visited.indexOf(idx) >= 0,
      current: idx === current
    };
  }
  return status;
}

function renderAnimStep() {
  var step = animState.steps[animState.stepIdx];
  if (!step) return;

  var tree = trees[animState.currentExample];
  var svg = $('animTree');
  svg.innerHTML = '';

  tree.lc.forEach(function (lc_val, i) {
    if (i === 0) return;
    if (lc_val !== 0) {
      var p1 = tree.pos[i], p2 = tree.pos[lc_val];
      svg.appendChild(createSVG('line', {
        x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y, class: 'edge-line active'
      }));
    }
    if (tree.rc[i] !== 0) {
      var p3 = tree.pos[tree.rc[i]];
      svg.appendChild(createSVG('line', {
        x1: p1.x, y1: p1.y, x2: p3.x, y2: p3.y, class: 'edge-line active'
      }));
    }
  });

  for (var i = 1; i <= tree.n; i++) {
    var node = tree.pos[i];
    var circle = createSVG('circle', {
      cx: node.x, cy: node.y, r: 24, class: 'node-circle'
    });

    if (step.nodeStatus[i]) {
      var s = step.nodeStatus[i];
      if (s.current) {
        circle.classList.add('current');
      } else if (s.visited) {
        if (s.perf) circle.classList.add('perfect');
        else if (s.comp) circle.classList.add('complete');
        else circle.classList.add('incomplete');
      }
    }

    svg.appendChild(circle);

    var text = createSVG('text', {
      x: node.x, y: node.y + 5, 'text-anchor': 'middle',
      fill: step.nodeStatus[i] ? '#fff' : '#475569',
      class: 'node-label'
    });
    text.textContent = i;
    svg.appendChild(text);
  }

  var stackEl = $('animStack');
  stackEl.innerHTML = '';
  step.stack.forEach(function (u) {
    var frame = document.createElement('div');
    frame.className = 'stack-frame';
    frame.style.background = '#6366f1';
    frame.textContent = 'DFS(' + u + ')';
    stackEl.appendChild(frame);
  });

  var propsEl = $('animProps');
  propsEl.innerHTML = '<div class="card-title">已计算节点</div>';
  var hasProps = false;
  for (var k in step.h) {
    hasProps = true;
    propsEl.innerHTML +=
      '<div class="prop-row"><span class="prop-name">节点 ' + k + '</span><span class="prop-val">h=' + step.h[k] + ', P=' + (step.perf[k] ? 'T' : 'F') + ', C=' + (step.comp[k] ? 'T' : 'F') + '</span></div>';
  }
  if (!hasProps) {
    propsEl.innerHTML += '<p style="color: var(--muted); font-size: 0.85rem;">等待动画开始...</p>';
  }

  $('animStepInfo').textContent = step.desc;

  if (step.finalResult !== undefined) {
    $('animResult').style.display = 'block';
    $('animCount').textContent = step.finalResult;
  } else {
    $('animResult').style.display = 'none';
  }
}

function initAlgorithmAnimation() {
  animState.steps = buildAnimSteps(trees.ex1);
  renderAnimStep();

  $('tabEx1').addEventListener('click', function () {
    $('tabEx1').classList.add('active');
    $('tabEx2').classList.remove('active');
    animState.currentExample = 'ex1';
    animState.stepIdx = 0;
    animState.steps = buildAnimSteps(trees.ex1);
    animPause();
    renderAnimStep();
  });

  $('tabEx2').addEventListener('click', function () {
    $('tabEx2').classList.add('active');
    $('tabEx1').classList.remove('active');
    animState.currentExample = 'ex2';
    animState.stepIdx = 0;
    animState.steps = buildAnimSteps(trees.ex2);
    animPause();
    renderAnimStep();
  });

  $('animPlay').addEventListener('click', animPlay);
  $('animPause').addEventListener('click', animPause);
  $('animStep').addEventListener('click', animStepForward);
  $('animReset').addEventListener('click', animReset);
  $('animSpeed').addEventListener('input', function () {
    animState.speed = parseInt(this.value);
    if (animState.playing) {
      animPause();
      animPlay();
    }
  });
}

function animPlay() {
  if (animState.playing) return;
  if (animState.stepIdx >= animState.steps.length - 1) {
    animState.stepIdx = 0;
  }
  animState.playing = true;
  animState.timer = setInterval(function () {
    if (animState.stepIdx >= animState.steps.length - 1) {
      animPause();
      return;
    }
    animState.stepIdx++;
    renderAnimStep();
  }, animState.speed);
}

function animPause() {
  animState.playing = false;
  if (animState.timer) {
    clearInterval(animState.timer);
    animState.timer = null;
  }
}

function animStepForward() {
  animPause();
  if (animState.stepIdx < animState.steps.length - 1) {
    animState.stepIdx++;
    renderAnimStep();
  }
}

function animReset() {
  animPause();
  animState.stepIdx = 0;
  renderAnimStep();
}

/* ============================================================
   5. 互动练习
   ============================================================ */

function initInteractivePractice() {
  var svg = $('practiceTree');
  if (!svg) return;

  var tree = trees.ex3;
  var data = computeTree(tree);
  var showAll = false;

  function render() {
    svg.innerHTML = '';

    tree.lc.forEach(function (lc_val, i) {
      if (i === 0) return;
      if (lc_val !== 0) {
        var p1 = tree.pos[i], p2 = tree.pos[lc_val];
        svg.appendChild(createSVG('line', {
          x1: p1.x, y1: p1.y, x2: p2.x, y2: p2.y, class: 'edge-line active'
        }));
      }
      if (tree.rc[i] !== 0) {
        var p3 = tree.pos[tree.rc[i]];
        svg.appendChild(createSVG('line', {
          x1: p1.x, y1: p1.y, x2: p3.x, y2: p3.y, class: 'edge-line active'
        }));
      }
    });

    for (var i = 1; i <= tree.n; i++) {
      (function (nodeIdx) {
        var node = tree.pos[nodeIdx];
        var circle = createSVG('circle', {
          cx: node.x, cy: node.y, r: 22, class: 'node-circle'
        });

        if (showAll) {
          if (data.perf[nodeIdx]) circle.classList.add('perfect');
          else if (data.comp[nodeIdx]) circle.classList.add('complete');
          else circle.classList.add('incomplete');
        }

        circle.addEventListener('click', function () {
          svg.querySelectorAll('.node-circle').forEach(function (c) {
            c.classList.remove('selected');
          });
          circle.classList.add('selected');
          showPracticeProps(nodeIdx);
        });

        svg.appendChild(circle);

        var isColored = showAll;
        var text = createSVG('text', {
          x: node.x, y: node.y + 5, 'text-anchor': 'middle',
          fill: isColored ? '#fff' : '#475569',
          class: 'node-label'
        });
        text.textContent = nodeIdx;
        svg.appendChild(text);

        if (showAll) {
          var badge = createSVG('text', {
            x: node.x, y: node.y + 40, 'text-anchor': 'middle',
            'font-family': 'Outfit, sans-serif', 'font-size': '15px', 'font-weight': '700',
            'pointer-events': 'none', 'user-select': 'none'
          });
          badge.textContent = data.comp[nodeIdx] ? '\u2713' : '\u2717';
          badge.setAttribute('fill', data.comp[nodeIdx] ? '#10b981' : '#ef4444');
          svg.appendChild(badge);
        }
      })(i);
    }
  }

  function showPracticeProps(idx) {
    var panel = $('practicePanel');
    var isLeaf = tree.lc[idx] === 0 && tree.rc[idx] === 0;
    var caseName;
    if (isLeaf) caseName = '叶子节点';
    else if (tree.lc[idx] !== 0 && tree.rc[idx] === 0) caseName = '只有左子 ' + tree.lc[idx];
    else if (tree.lc[idx] === 0 && tree.rc[idx] !== 0) caseName = '只有右子 ' + tree.rc[idx];
    else caseName = '左子 ' + tree.lc[idx] + '，右子 ' + tree.rc[idx];

    panel.innerHTML =
      '<div class="card-title">节点 ' + idx + '</div>' +
      '<div class="prop-row"><span class="prop-name">情形</span><span class="prop-val">' + caseName + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">height</span><span class="prop-val">' + data.h[idx] + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">isPerfect</span><span class="prop-val ' + (data.perf[idx] ? 'true' : 'false') + '">' + (data.perf[idx] ? 'true' : 'false') + '</span></div>' +
      '<div class="prop-row"><span class="prop-name">isComplete</span><span class="prop-val ' + (data.comp[idx] ? 'true' : 'false') + '">' + (data.comp[idx] ? 'true' : 'false') + '</span></div>';
  }

  render();

  $('practiceShowAll').addEventListener('click', function () {
    showAll = true;
    render();
    var cnt = 0;
    for (var i = 1; i <= tree.n; i++) if (data.comp[i]) cnt++;
    $('practiceResult').style.display = 'block';
    $('practiceCount').textContent = cnt;
  });

  $('practiceReset').addEventListener('click', function () {
    showAll = false;
    render();
    $('practiceResult').style.display = 'none';
    $('practicePanel').innerHTML = '<div class="card-title">节点属性</div><p style="color: var(--muted); font-size: 0.85rem;">点击树上的节点</p>';
  });
}

/* ============================================================
   6. 知识测验
   ============================================================ */

var quizData = [
  {
    question: '一棵完全二叉树有 n 个节点，它的第 k 层（从 0 开始）最多有多少个节点？',
    options: ['k', '2^k', '2^(k-1)', 'k^2'],
    answer: 1,
    explain: '完全二叉树的第 k 层最多有 2^k 个节点（满二叉树时达到最大）。'
  },
  {
    question: '一个节点只有左子（叶子），它的子树是完全二叉树吗？',
    options: ['是', '不是', '取决于左子的高度', '取决于节点编号'],
    answer: 0,
    explain: '只有左子且左子是叶子时，子树高度为 1，最后一层只有 1 个节点在最左边，符合完全二叉树定义。'
  },
  {
    question: '一个节点只有右子，它的子树是完全二叉树吗？',
    options: ['是', '不是', '取决于右子的高度', '取决于节点编号'],
    answer: 1,
    explain: '只有右子没有左子，最后一层的节点不在最左边，违反了"从左到右排满"的规则。'
  },
  {
    question: '节点有左右子，h[l]=2, h[r]=2，此时 isComplete 的判定条件是什么？',
    options: [
      'comp[l] && comp[r]',
      'comp[l] && perf[r]',
      'perf[l] && perf[r]',
      'comp[l] && comp[r] && perf[r]'
    ],
    answer: 1,
    explain: 'h[l]==h[r] 时，左可以"缺"最后一层（只需 isComplete），右必须满（需要 isPerfect）。所以条件是 comp[l] && perf[r]。'
  },
  {
    question: '本题（完全二叉子树计数）的时间复杂度是？',
    options: ['O(n)', 'O(n log n)', 'O(n^2)', 'O(n^3)'],
    answer: 0,
    explain: '每个节点只访问一次，后序 DFS 的时间复杂度是 O(n)。'
  },
  {
    question: '节点有左右子，h[l]=3, h[r]=1，isComplete 等于？',
    options: ['true', 'false', '取决于 comp[l]', '取决于 perf[r]'],
    answer: 1,
    explain: 'h[l]=3, h[r]=1，高度差为 2（超过 1），中间有空层，isComplete = false。'
  }
];

function initKnowledgeTest() {
  var container = $('quizContainer');
  if (!container) return;

  quizData.forEach(function (q, idx) {
    var item = document.createElement('div');
    item.className = 'quiz-item';

    var question = document.createElement('div');
    question.className = 'quiz-question';
    question.textContent = (idx + 1) + '. ' + q.question;
    item.appendChild(question);

    var options = document.createElement('div');
    options.className = 'quiz-options';

    q.options.forEach(function (opt, optIdx) {
      var btn = document.createElement('button');
      btn.className = 'quiz-option';
      btn.textContent = String.fromCharCode(65 + optIdx) + '. ' + opt;
      btn.addEventListener('click', function () {
        if (options.classList.contains('locked')) return;
        options.classList.add('locked');
        options.querySelectorAll('.quiz-option').forEach(function (b) {
          b.classList.add('disabled');
        });

        if (optIdx === q.answer) {
          btn.classList.add('correct');
        } else {
          btn.classList.add('wrong');
          options.querySelectorAll('.quiz-option')[q.answer].classList.add('correct');
        }

        var feedback = item.querySelector('.quiz-feedback');
        feedback.classList.add('show');
        feedback.classList.add(optIdx === q.answer ? 'correct' : 'wrong');
        feedback.textContent = (optIdx === q.answer ? '\u2713 正确！' : '\u2717 不对。') + ' ' + q.explain;
      });
      options.appendChild(btn);
    });

    item.appendChild(options);

    var feedback = document.createElement('div');
    feedback.className = 'quiz-feedback';
    item.appendChild(feedback);

    container.appendChild(item);
  });
}

/* ============================================================
   7. 导航高亮
   ============================================================ */

function initNavHighlight() {
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
}

/* ============================================================
   初始化
   ============================================================ */

document.addEventListener('DOMContentLoaded', function () {
  initExampleTrees();
  initConceptGrid();
  initApproachExplorer();
  initAlgorithmAnimation();
  initInteractivePractice();
  initKnowledgeTest();
  initNavHighlight();
});

})();
