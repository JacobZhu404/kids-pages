(function(){
  if(window.__KG_EGGY_INIT__) return;
  window.__KG_EGGY_INIT__=true;
  var eggy=document.getElementById('kg-eggy');
  if(!eggy) return;
  var svg=eggy.querySelector('svg');
  var pl=document.getElementById('kg-pupil-l');
  var pr=document.getElementById('kg-pupil-r');
  var mouth=document.getElementById('kg-eggy-mouth');
  var body=eggy.querySelector('.kg-egg-body');
  var eyeL=document.getElementById('kg-eye-l'), eyeR=document.getElementById('kg-eye-r');
  var faces=[["#fde047","M42 84 Q50 90 58 84"],["#fca5a5","M42 86 Q50 80 58 86"],["#86efac","M42 82 Q50 92 58 82"],["#93c5fd","M42 88 Q50 84 58 88"]];
  var fi=0;
  var desktopW=70,desktopH=84;
  function viewportMetrics(){var v=window.visualViewport;return v?{left:v.offsetLeft||0,top:v.offsetTop||0,width:v.width,height:v.height}:{left:0,top:0,width:window.innerWidth,height:window.innerHeight};}
  var initialViewport=viewportMetrics();
  var W=Math.min(desktopW,Math.max(48,initialViewport.width<=860?56:70));
  var H=Math.round(desktopH*W/desktopW);
  function mp(p,cx,cy,mx,my){var r=eggy.getBoundingClientRect();var dx=mx-(r.left+cx*0.7+35),dy=my-(r.top+cy*0.7+42);var d=Math.sqrt(dx*dx+dy*dy)||1,max=4;p.setAttribute('cx',cx+Math.min(max,dx/d*max));p.setAttribute('cy',cy+Math.min(max,dy/d*max));}
  document.addEventListener('mousemove',function(e){if(flying)return;mp(pl,36,68,e.clientX,e.clientY);mp(pr,64,68,e.clientX,e.clientY);});
  document.addEventListener('touchmove',function(e){if(flying)return;if(e.touches[0]){mp(pl,36,68,e.touches[0].clientX,e.touches[0].clientY);mp(pr,64,68,e.touches[0].clientX,e.touches[0].clientY);}},{passive:true});
  var clickCount=0;
  function fireConfetti(){var box=document.getElementById('kg-confetti');if(!box){box=document.createElement('div');box.id='kg-confetti';document.body.appendChild(box);}var colors=['#0ea5e9','#fde047','#fb7185','#86efac','#fbbf24','#a78bfa','#f97316','#38bdf8'];var v=viewportMetrics(),cx=v.left+v.width-55,cy=v.top+v.height-50;for(var i=0;i<60;i++){var p=document.createElement('div');p.className='kg-cf';p.style.background=colors[i%colors.length];p.style.left=cx+'px';p.style.top=cy+'px';var ang=Math.random()*Math.PI*2,sp=60+Math.random()*120;var dx=Math.cos(ang)*sp,dy=Math.sin(ang)*sp-80;p.style.transition='transform 1.2s cubic-bezier(.2,.6,.4,1),opacity 1.2s ease';box.appendChild(p);requestAnimationFrame(function(el,xx,yy){return function(){el.style.opacity='1';el.style.transform='translate('+xx+'px,'+yy+'px) scale('+(0.5+Math.random())+') rotate('+(Math.random()*720)+'deg)';};}(p,dx,dy));setTimeout(function(el){return function(){el.style.opacity='0';};}(p),900);}setTimeout(function(){if(box.parentNode)box.parentNode.removeChild(box);},1500);}
  function fireExplosion(){
    var flash=document.getElementById('kg-flash');
    if(!flash){flash=document.createElement('div');flash.id='kg-flash';document.body.appendChild(flash);}
    flash.classList.remove('kg-on');void flash.offsetWidth;flash.classList.add('kg-on');
    setTimeout(function(){flash.classList.remove('kg-on');},750);
    var box=document.getElementById('kg-confetti');
    if(!box){box=document.createElement('div');box.id='kg-confetti';document.body.appendChild(box);}
    var v=viewportMetrics(),cx=v.left+v.width-55,cy=v.top+v.height-50;
    function blob(){
      var p=document.createElement('div');p.className='kg-cf';
      var roll=Math.random();
      if(roll<0.62){p.style.background=['#fb923c','#f97316','#ef4444','#fde047','#ffedd5','#fbbf24'][Math.floor(Math.random()*6)];p.style.width='10px';p.style.height='10px';p.style.boxShadow='0 0 12px rgba(249,115,22,.9),0 0 24px rgba(255,176,0,.6)';}
      else if(roll<0.85){p.style.background=['#fca5a5','#fed7aa','#fde68a'][Math.floor(Math.random()*3)];p.style.width=Math.random()<0.5?'6px':'9px';p.style.height='3px';p.style.borderRadius='2px';}
      else {p.style.background='#57534e';p.style.width='16px';p.style.height='16px';p.style.boxShadow='0 0 10px rgba(87,83,78,.5)';}
      p.style.left=cx+'px';p.style.top=cy+'px';
      var ang=Math.random()*Math.PI*2, sp=90+Math.random()*240;
      var dx=Math.cos(ang)*sp, dy=Math.sin(ang)*sp-70;
      p.style.transition='transform 1.4s cubic-bezier(.15,.55,.3,1),opacity 1.4s ease';
      box.appendChild(p);
      requestAnimationFrame(function(el,xx,yy){return function(){
        el.style.opacity='1';el.style.transform='translate('+xx+'px,'+yy+'px) scale('+(0.6+Math.random()*1.1)+') rotate('+(Math.random()*540)+'deg)';
      };}(p,dx,dy));
      setTimeout(function(el){return function(){el.style.opacity='0';};}(p),500+Math.random()*700);
    }
    for(var i=0;i<110;i++) blob();
    setTimeout(function(){if(box.parentNode)box.parentNode.removeChild(box);},1700);
    eggy.classList.add('kg-blasted');
    pl.setAttribute('r','2.8');pr.setAttribute('r','2.8');
    pl.setAttribute('cy','67');pr.setAttribute('cy','67');
    eyeL.setAttribute('r','12.5');eyeR.setAttribute('r','12.5');
    eyeL.setAttribute('cx','35');eyeR.setAttribute('cx','65');
    mouth.setAttribute('d','M44 84 Q50 91 56 84');
    eggy.style.filter='brightness(.85) saturate(.6)';
    setTimeout(function(){
      eggy.classList.remove('kg-blasted');
      pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');
      pl.setAttribute('cy','68');pr.setAttribute('cy','68');
      eyeL.setAttribute('r','11');eyeR.setAttribute('r','11');
      eyeL.setAttribute('cx','36');eyeR.setAttribute('cx','64');
      mouth.setAttribute('d',faces[fi][1]);
      eggy.style.filter='';
    },3500);
  }
  /* ==== 拖动 + 右下角隐形栅栏（墙在网页右下角 1/5 处）==== */
  var homeL=0, homeT=0;
  function bounds(){var v=viewportMetrics(),vw=v.width,vh=v.height;var rw=Math.max(vw/5,150),rh=Math.max(vh/5,120);return {L:v.left+vw-rw,T:v.top+vh-rh,R:v.left+vw,B:v.top+vh};}
  function setHome(){
    var v=viewportMetrics();W=Math.min(desktopW,Math.max(48,v.width<=860?56:70));H=Math.round(desktopH*W/desktopW);
    eggy.style.width=W+'px';eggy.style.height=H+'px';if(svg){svg.setAttribute('width',W);svg.setAttribute('height',H);}
    homeL=Math.max(v.left+8,v.left+v.width-W-20);homeT=Math.max(v.top+8,v.top+v.height-H-20);
    eggy.style.left=homeL+'px';eggy.style.top=homeT+'px';eggy.style.right='auto';eggy.style.bottom='auto';
  }
  function resetAppearance(){
    eggy.classList.remove('kg-blasted','kg-flying','kg-fallen','kg-crying','kg-dragging');svg.classList.remove('kg-wall-shake');svg.style.transform='';
    eggy.style.transform='';eggy.style.filter='';eggy.style.transition='';eggy.style.opacity='1';body.setAttribute('fill',faces[fi][0]);
    pl.setAttribute('cx','36');pr.setAttribute('cx','64');pl.setAttribute('cy','68');pr.setAttribute('cy','68');pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');
    eyeL.setAttribute('cx','36');eyeR.setAttribute('cx','64');eyeL.setAttribute('r','11');eyeR.setAttribute('r','11');mouth.setAttribute('d',faces[fi][1]);mouth.setAttribute('fill','none');
    var dirt=eggy.querySelector('.kg-dirt');if(dirt)dirt.style.opacity='0';var smoke=eggy.querySelector('.kg-smoke');if(smoke)smoke.style.opacity='0';var dustbox=document.getElementById('kg-dustbox');if(dustbox)dustbox.remove();
  }
  resetAppearance();setHome();
  function updateViewportHome(){if(down||flying)return;var v=viewportMetrics(),r=eggy.getBoundingClientRect();if(r.right>v.left+v.width||r.left<v.left||r.bottom>v.top+v.height||r.top<v.top)setHome();}
  window.addEventListener('resize',function(){abortFlight();resetCharge();if(down)release({type:'pointercancel'});setHome();});
  if(window.visualViewport){window.visualViewport.addEventListener('resize',updateViewportHome);window.visualViewport.addEventListener('scroll',updateViewportHome);}
  window.addEventListener('load',updateViewportHome,{once:true});[0,100,350,900].forEach(function(ms){setTimeout(updateViewportHome,ms);});
  var down=null, dragging=false, wallOn=false, lastDust=0, suppress=0, retTimer=null;
  // Continuous corner pressure arms the spring even when the pointer stops moving.
  var chargeTimer=null, chargeRAF=0, chargeSince=0, ready=false, spring=null, tension=0, chargeProgress=0, launchAngle=Math.PI/4;
  var flying=false, flightRAF=0, flightTimer=null, activePointer=null;
  function resetCharge(){
    if(chargeTimer) clearTimeout(chargeTimer);
    cancelAnimationFrame(chargeRAF);chargeRAF=0;
    chargeTimer=null;chargeSince=0;ready=false;chargeProgress=0;
    if(!flying)eggy.style.filter="";
    if(spring){spring.remove();spring=null;}
  }
  function drawSpring(recoil){
    if(!spring){
      spring=document.createElementNS('http://www.w3.org/2000/svg','svg');spring.id='kg-spring';
      spring.innerHTML='<path stroke="#a78bfa" stroke-width="9" opacity=".4"/><path stroke="#67e8f9" stroke-width="4"/><path stroke="white" stroke-width="1.3"/><polyline class="kg-aim" fill="none" stroke="#0ea5e9" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/><text text-anchor="end"/><rect class="kg-charge-track" rx="4" fill="#cbd5e1" opacity=".6"/><rect class="kg-charge-fill" rx="4" fill="#22d3ee"/>';
      document.body.appendChild(spring);
    }
    var w=window.innerWidth,h=window.innerHeight;
    spring.setAttribute('viewBox','0 0 '+w+' '+h);
    var span=Math.min(145,w*.28,h*.28), pull=recoil===undefined?10+chargeProgress*(14+tension*38):recoil;
    // Two anchors form a diagonal trampoline facing the upper-left launch direction.
    var x=w-12,y=h-12;
    var d='M '+(x-span)+' '+y+' Q '+(x-span/2+pull)+' '+(y-span/2+pull)+' '+x+' '+(y-span);
    spring.querySelectorAll('path').forEach(function(path){path.setAttribute('d',d);});
    var originX=parseFloat(eggy.style.left)+W/2,originY=parseFloat(eggy.style.top)+H/2;
    var ux=-Math.cos(launchAngle),uy=-Math.sin(launchAngle),length=75+25*chargeProgress;
    var tipX=originX+ux*length,tipY=originY+uy*length;
    var aim=spring.querySelector('.kg-aim');
    aim.setAttribute('points',(tipX-ux*12-uy*7)+','+(tipY-uy*12+ux*7)+' '+tipX+','+tipY+' '+(tipX-ux*12+uy*7)+','+(tipY-uy*12-ux*7)+' '+tipX+','+tipY+' '+originX+','+originY);
    aim.style.opacity=recoil===undefined?'0.85':'0';
    var label=spring.querySelector('text');label.setAttribute('x',w-20);label.setAttribute('y',h-span-24);
    var pulse=.5+.5*Math.sin(Date.now()/140);
    spring.querySelectorAll('path').forEach(function(path,i){
      path.style.opacity=String((i===0?.2+.25*pulse:.4+.6*chargeProgress));
    });
    label.textContent=recoil!==undefined?'':ready?'瞄准 '+Math.round(launchAngle*180/Math.PI)+'° · 松手起飞！':'蓄力 '+Math.floor(chargeProgress*100)+'% · 继续按住';
    var track=spring.querySelector('.kg-charge-track'),fill=spring.querySelector('.kg-charge-fill');
    [track,fill].forEach(function(bar){bar.setAttribute('x',w-140);bar.setAttribute('y',h-span-14);bar.setAttribute('height',6);});
    track.setAttribute('width',120);fill.setAttribute('width',120*chargeProgress);
    eggy.style.filter='drop-shadow(0 0 '+(3+chargeProgress*10+pulse*3)+'px rgba(34,211,238,'+(.2+chargeProgress*.7)+'))';
  }
  function cornerPressure(ox,oy){
    if(!chargeSince&&(ox<8||oy<8))return;
    // Once engaged, aiming remains latched until release or cancellation.
    if(ox>0||oy>0)launchAngle=Math.max(Math.PI/12,Math.min(Math.PI*5/12,Math.atan2(Math.max(0,oy),Math.max(0,ox))));
    tension=Math.min(1,Math.hypot(ox,oy)/150);
    if(ready){drawSpring();return;}
    if(chargeTimer) return;
    chargeSince=Date.now();
    function charging(){
      if(!down||!dragging)return;
      chargeProgress=Math.min(1,(Date.now()-chargeSince)/1500);
      drawSpring();chargeRAF=requestAnimationFrame(charging);
    }
    charging();
    chargeTimer=setTimeout(function(){
      chargeTimer=null;
      if(!down||!dragging) return;
      ready=true;drawSpring();
    },1500);
  }
  function abortFlight(){
    cancelAnimationFrame(flightRAF);flightRAF=0;
    if(flightTimer)clearTimeout(flightTimer);flightTimer=null;
    flying=false;eggy.classList.remove('kg-flying','kg-fallen','kg-crying');
    svg.style.transform='';eggy.style.transition='';eggy.style.transform='';eggy.style.filter='';
    setScaredFace(false);
  }
  function launch(){
    var x=parseFloat(eggy.style.left),y=parseFloat(eggy.style.top);
    var started=performance.now(),last=started;
    var speed=Math.hypot((window.innerWidth-W)*2.1,(window.innerHeight-H)*2.55);
    var vx=-Math.cos(launchAngle)*speed,vy=-Math.sin(launchAngle)*speed;
    cancelAnimationFrame(chargeRAF);chargeRAF=0;
    flying=true;suppress=Date.now()+3100;
    eggy.classList.remove('kg-bounce');eggy.classList.add('kg-flying');
    eggy.style.transform='';eggy.style.transition='none';wallOn=false;setScaredFace(true);
    if(spring){drawSpring(-35);spring.style.transition='opacity .3s';spring.style.opacity='0';}
    function finish(){
      abortFlight();resetCharge();setHome();squashFace(false);
    }
    // Gravity and inelastic collisions dissipate energy; land before walking home.
    var phase='air',phaseAt=0,fallAngle=0,walkStart=0,rollStart=0,rollEnd=0,rollDirection=1,scared=true;
    var gravity=Math.max(450,window.innerHeight*.95),impulse=0;
    // A safety cleanup only; normal completion is driven by landing, not a deadline.
    flightTimer=setTimeout(finish,20000);
    function ease(t){return t*t*(3-2*t);}
    function frame(now){
      if(!flying)return;
      var elapsed=now-started,dt=Math.min((now-last)/1000,.04);last=now;
      if(scared&&(elapsed>720||phase!=='air')){setScaredFace(false);scared=false;}
      var maxX=Math.max(0,window.innerWidth-W),floor=Math.max(0,window.innerHeight-H);
      var energy=Math.max(0,Math.min(1,Math.hypot(vx,vy)/Math.hypot((window.innerWidth-W)*2.1,(window.innerHeight-H)*2.55)));
      var angle=0,sx=1,sy=1;
      if(phase==='air'){
        vx*=Math.exp(-.10*dt);vy+=gravity*dt;
        x+=vx*dt;y+=vy*dt;
        if(x<0||x>maxX){x=Math.max(0,Math.min(x,maxX));vx=-vx*.72;impulse=1;dust(vx>0?-1:1,0);}
        if(y<0){y=0;vy=Math.abs(vy)*.68;impulse=1;dust(0,-1);}
        if(y>=floor){
          y=floor;
          if(Math.abs(vy)<200&&elapsed>1200){
            phase='roll';phaseAt=now;rollStart=x;
            rollDirection=vx<0?-1:1;
            var distance=Math.min(220,Math.max(130,Math.abs(vx)*.85));
            if((rollDirection<0?x:maxX-x)<distance*.65)rollDirection=-rollDirection;
            rollEnd=Math.max(0,Math.min(maxX,x+rollDirection*distance));
            fallAngle=rollDirection*24;vx=0;vy=0;
            eggy.classList.add('kg-fallen','kg-crying');mouth.setAttribute('d','M42 88 Q50 81 58 88');dust(0,1);
          }else{vy=-Math.abs(vy)*.66;vx*=.94;impulse=1;dust(0,1);}
        }
        impulse=Math.max(0,impulse-dt*5);
        sx=1+impulse*.18;sy=1-impulse*.16;
        angle=Math.sin(elapsed/150)*16*energy;
      }
      if(phase==='roll'){
        var rt=Math.min(1,(now-phaseAt)/950),rp=1-Math.pow(1-rt,2);
        x=rollStart+(rollEnd-rollStart)*rp;
        // Keep the rotating 70x84 box above the floor throughout the tumble.
        angle=rollDirection*360*rp;
        var radians=angle*Math.PI/180;
        var extent=(Math.abs(Math.sin(radians))*W+Math.abs(Math.cos(radians))*H)/2;
        y=floor-Math.max(0,extent-H/2)-Math.sin(rt*Math.PI)*7;
        if(rt>=1){phase='fallen';phaseAt=now;}
      }
      if(phase==='fallen'){
        var t=Math.min(1,(now-phaseAt)/800);
        y=floor;
        // Stay upright, cry briefly, then gently get up.
        sx=1;sy=1;
        angle=fallAngle*Math.sin(Math.min(1,t*4)*Math.PI/2)*(1-ease(Math.max(0,(t-.45)/.55)));
        angle+=Math.sin(t*28)*5*(1-t);
        if(t>=1){phase='walk';phaseAt=now;walkStart=x;squashFace(false);eggy.classList.remove('kg-fallen','kg-crying');}
      }
      if(phase==='walk'){
        var duration=Math.max(900,Math.abs(homeL-walkStart)/280*1000);
        var t=Math.min(1,(now-phaseAt)/duration),travel=ease(t);
        x=walkStart+(homeL-walkStart)*travel;
        var step=Math.sin((now-phaseAt)/65);
        var gait=Math.min(1,t*6,(1-t)*6);
        y=floor-Math.abs(step)*5*gait;angle=step*5*gait;
        if(t>=1){phase='settle';phaseAt=now;}
      }
      if(phase==='settle'){
        var t=Math.min(1,(now-phaseAt)/450);
        x=homeL;y=floor+(homeT-floor)*ease(t);angle=0;
        if(t>=1){finish();return;}
      }
      eggy.style.left=x+'px';eggy.style.top=y+'px';
      eggy.style.transform='scale('+sx+','+sy+')';
      var glow=phase==='air'?energy:0;
      eggy.style.filter='drop-shadow(0 0 '+(12*glow)+'px rgba(56,189,248,'+glow+'))';
      svg.style.transform='rotate('+angle+'deg)';
      flightRAF=requestAnimationFrame(frame);
    }
    flightRAF=requestAnimationFrame(frame);
  }
  document.addEventListener('visibilitychange',function(){if(document.hidden){if(down)release({type:'pointercancel'});abortFlight();resetCharge();setHome();}});
  window.addEventListener('blur',function(){if(down)release({type:'pointercancel'});});
  eggy.addEventListener('lostpointercapture',function(){if(down)release({type:'pointercancel'});});
  function squashFace(on){
    if(on){mouth.setAttribute('d','M42 87 Q50 81 58 87');pl.setAttribute('r','6.8');pr.setAttribute('r','6.8');}
    else{mouth.setAttribute('d',faces[fi][1]);pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');}
  }
  function setScaredFace(on){
    if(on){
      eyeL.setAttribute('r','12');eyeR.setAttribute('r','12');
      pl.setAttribute('r','4.7');pr.setAttribute('r','4.7');
      pl.setAttribute('cx','37');pr.setAttribute('cx','63');
      pl.setAttribute('cy','65');pr.setAttribute('cy','65');
      mouth.setAttribute('d','M47 86 Q50 82 53 86 Q50 90 47 86');
      mouth.setAttribute('fill','#1e293b');
    }else{
      eyeL.setAttribute('r','11');eyeR.setAttribute('r','11');
      pl.setAttribute('r','5.5');pr.setAttribute('r','5.5');
      pl.setAttribute('cx','36');pr.setAttribute('cx','64');
      pl.setAttribute('cy','68');pr.setAttribute('cy','68');
      mouth.setAttribute('d',faces[fi][1]);mouth.setAttribute('fill','none');
    }
  }
  function dust(ox,oy){
    var box=document.getElementById('kg-dustbox');
    if(!box){box=document.createElement('div');box.id='kg-dustbox';document.body.appendChild(box);}
    var r=eggy.getBoundingClientRect();
    var px=Math.abs(ox)>Math.abs(oy)?(ox>0?r.right-3:r.left+3):r.left+W/2+(Math.random()*12-6);
    var py=Math.abs(oy)>=Math.abs(ox)?(oy>0?r.bottom-3:r.top+3):r.top+H/2+(Math.random()*12-6);
    var dxdir=ox>0?1:-1, dydir=oy>0?1:-1;
    for(var i=0;i<7;i++){
      var d=document.createElement('span'); d.className='kg-dust';
      d.style.left=px+'px'; d.style.top=py+'px';
      var tx=(ox?dxdir*(12+Math.random()*28):(Math.random()*34-17));
      var ty=(oy?dydir*(10+Math.random()*22):(Math.random()*34-17))+16;
      var s=4+Math.random()*4;
      d.style.width=s+'px'; d.style.height=s+'px';
      box.appendChild(d);
      requestAnimationFrame(function(el,xx,dy){return function(){el.style.opacity='.85';el.style.transform='translate('+xx+'px,'+dy+'px) scale(.25)';};}(d,tx,ty));
      setTimeout(function(el){return function(){el.style.opacity='0';};}(d),300);
      setTimeout(function(el){return function(){if(el.parentNode)el.parentNode.removeChild(el);};}(d),620);
    }
  }
  eggy.addEventListener('pointerdown',function(e){
    if(flying||down||eggy.classList.contains('kg-blasted')) return;
    if(e.pointerType==='mouse'&&e.button!==0) return;
    if(retTimer){clearTimeout(retTimer);retTimer=null;}
    resetCharge();activePointer=e.pointerId;
    eggy.classList.remove('kg-bounce');eggy.style.transition='';
    var r=eggy.getBoundingClientRect();
    down={x:e.clientX,y:e.clientY,ox:r.left-e.clientX,oy:r.top-e.clientY};
    dragging=false;
    try{eggy.setPointerCapture(e.pointerId);}catch(err){}
  });
  window.addEventListener('pointermove',function(e){
    if(!down||e.pointerId!==activePointer) return;
    var dx=e.clientX-down.x, dy=e.clientY-down.y;
    if(!dragging && dx*dx+dy*dy<36) return;
    if(!dragging){dragging=true;eggy.classList.add('kg-dragging');}
    var b=bounds();
    var lx=down.ox+e.clientX, ly=down.oy+e.clientY;
    var cl=Math.max(b.L,Math.min(lx,b.R-W)), ct=Math.max(b.T,Math.min(ly,b.B-H));
    var ox=lx-cl, oy=ly-ct;
    cornerPressure(ox,oy);
    if(chargeSince){
      eggy.style.left=(b.R-W)+'px';eggy.style.top=(b.B-H)+'px';
      eggy.style.transform='scale(1,1)';wallOn=false;squashFace(false);
      svg.classList.remove('kg-wall-shake');
      return;
    }
    eggy.style.left=cl+'px'; eggy.style.top=ct+'px';
    var hit=(ox!==0||oy!==0), now=Date.now();
    if(hit){
      var ax=Math.min(24,Math.abs(ox)), ay=Math.min(24,Math.abs(oy));
      var scx=Math.max(0.62,Math.min(1.35,1-ax*0.014+ay*0.011));
      var scy=Math.max(0.62,Math.min(1.35,1-ay*0.014+ax*0.011));
      eggy.style.transform='scale('+scx.toFixed(3)+','+scy.toFixed(3)+')';
      if(!wallOn){wallOn=true;squashFace(true);svg.classList.remove('kg-wall-shake');void svg.offsetWidth;svg.classList.add('kg-wall-shake');dust(ox,oy);lastDust=now;}
      else if(now-lastDust>320){dust(ox,oy);lastDust=now;}
    }else if(wallOn){
      wallOn=false;squashFace(false);eggy.style.transform='';
    }
  },{passive:true});
  function release(e){
    if(!down||(e&&e.pointerId!==undefined&&e.pointerId!==activePointer)) return;
    var wasDrag=dragging, shouldLaunch=ready&&e&&e.type==='pointerup';
    down=null;activePointer=null;
    if(shouldLaunch){dragging=false;eggy.classList.remove('kg-dragging');launch();return;}
    resetCharge();
    if(wasDrag){
      dragging=false;eggy.classList.remove('kg-dragging');
      suppress=Date.now()+400;
      eggy.style.transition='left .4s cubic-bezier(.34,1.56,.64,1), top .4s cubic-bezier(.34,1.56,.64,1), transform .32s ease';
      eggy.style.left=homeL+'px'; eggy.style.top=homeT+'px'; eggy.style.transform='';
      retTimer=setTimeout(function(){eggy.style.transition='';retTimer=null;if(wallOn){wallOn=false;squashFace(false);}},460);
    }
  }
  window.addEventListener('pointerup',release);
  window.addEventListener('pointercancel',release);
  eggy.addEventListener('click',function(e){
    if(flying||Date.now()<suppress) return;
    fi=(fi+1)%faces.length;body.setAttribute('fill',faces[fi][0]);mouth.setAttribute('d',faces[fi][1]);eggy.classList.remove('kg-bounce');void eggy.offsetWidth;eggy.classList.add('kg-bounce');clickCount++;if(clickCount>=30){clickCount=0;fireExplosion();}else if(clickCount%10===0){fireConfetti();}
  });
})();
