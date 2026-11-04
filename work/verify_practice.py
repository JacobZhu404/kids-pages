# coding: utf-8
from pathlib import Path
import sys,types,math,runpy,html,os,zipfile
root=Path('public/practice').resolve();original=sys.modules.get('turtle')
expected={'branch':254,'natural':254,'koch':256,'snowflake':192,'sierpinski':243,'htree':255,'carpet':2048,'hilbert':255}
for name,count in expected.items():
 state={'x':0.,'y':0.,'angle':0.,'pen':True,'color':'#316d65','width':1.};lines=[]
 m=types.ModuleType('turtle')
 def goto(*args):
  x,y=args[0] if len(args)==1 else args
  if state['pen']:lines.append((state['x'],state['y'],x,y,state['color'],state['width']))
  state['x'],state['y']=x,y
 def forward(n):goto(state['x']+n*math.cos(math.radians(state['angle'])),state['y']+n*math.sin(math.radians(state['angle'])))
 m.goto=goto;m.forward=forward;m.backward=lambda n:forward(-n)
 m.left=lambda a:state.update(angle=state['angle']+a)
 m.right=lambda a:state.update(angle=state['angle']-a)
 m.setheading=lambda a:state.update(angle=a)
 m.penup=lambda:state.update(pen=False)
 m.pendown=lambda:state.update(pen=True)
 m.pensize=lambda n:state.update(width=n)
 m.pencolor=lambda c:state.update(color=c)
 for k in ['setup','speed','tracer','ht','update','done']:setattr(m,k,lambda *a:None)
 sys.modules['turtle']=m;runpy.run_path(str(root/(name+'.py')))
 assert len(lines)==count,(name,len(lines),count)
 xs=[p for line in lines for p in [line[0],line[2]]];ys=[p for line in lines for p in [line[1],line[3]]]
 lx,hx,ly,hy=min(xs),max(xs),min(ys),max(ys);pad=15
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="{} {} {} {}"><title>{}</title>'.format(lx-pad,-hy-pad,hx-lx+2*pad,hy-ly+2*pad,name)
 for x,y,X,Y,color,width in lines:svg+='<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="{}"/>'.format(x,-y,X,-Y,color,width)
 (root/(name+'.svg')).write_text(svg+'</svg>');print('PASS drawing',name,count)
 if name=='snowflake':assert math.hypot(state['x']+200,state['y']-120)<1e-6
 if name in ['branch','natural']:assert abs(state['x'])<1e-6 and abs(state['y']+220)<1e-6
if original:sys.modules['turtle']=original
else:del sys.modules['turtle']
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.show=lambda:None
os.chdir(str(root))
for name in ['passenger_stats','air_stats','air_compare','country_stats','group_stats']:
 plt.close('all');result=runpy.run_path(str(root/(name+'.py')))
 if name=='passenger_stats':assert result['df']['年龄'].mean()==31
 if name=='air_stats':assert result['df']['A站'].mean()==25 and result['df']['B站'].mean()==22.7
 if name=='air_compare':assert result['df']['差值'].max()==8
 if name=='country_stats':assert result['selected']['人均指标'].mean()==1900
 if name=='group_stats':assert result['summary'].loc[1,'mean']==90 and result['summary'].loc[3,'mean']==26.25
 print('PASS data',name)
with zipfile.ZipFile(str(root/'practice-pack.zip'),'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(root.iterdir()):
  if p.suffix in ['.py','.csv']:z.write(str(p),p.name)
print('PASS: all 13 programs, counts, return positions, statistics, bundle')
