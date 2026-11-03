"""High-quality offscreen renders of the v10 assemblies with VTK (PBR metal, dark studio).
Usage: python render_hq_vtk.py  (writes renders/hq/*.png)"""
import vtk, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'renders','hq'); os.makedirs(OUT,exist_ok=True)
MAT={'shell':((0.80,0.80,0.82),1.0,0.28,1.0),'strip':((0.85,0.72,0.45),1.0,0.3,1.0),
 'glass':((0.6,0.8,0.7),0.0,0.05,0.25),'oled':((0.05,0.9,0.3),0.0,0.4,1.0),
 'pcb':((0.1,0.4,0.15),0.0,0.6,1.0),'bat_L':((0.75,0.1,0.1),0.3,0.5,1.0),
 'bat_R':((0.75,0.1,0.1),0.3,0.5,1.0),'socket':((0.9,0.75,0.2),1.0,0.25,1.0)}
def actor(path,key,off=(0,0,0),hide_inner=False):
    r=vtk.vtkSTLReader(); r.SetFileName(path)
    n=vtk.vtkPolyDataNormals(); n.SetInputConnection(r.GetOutputPort()); n.SetFeatureAngle(40)
    m=vtk.vtkPolyDataMapper(); m.SetInputConnection(n.GetOutputPort())
    a=vtk.vtkActor(); a.SetMapper(m); p=a.GetProperty(); c,met,rough,op=MAT[key]
    p.SetInterpolationToPhong(); p.SetColor(*c); p.SetAmbient(0.15); p.SetDiffuse(0.55 if met else 0.8); p.SetSpecular(0.9 if met else 0.3); p.SetSpecularPower(60 if met else 20); p.SetOpacity(op)
    if key=='oled': p.SetAmbient(1.0); p.SetAmbientColor(0.1,1.0,0.35)
    a.SetPosition(*off); return a
def scene(parts,cam,name,size=(2100,1400),bg=((0.02,0.02,0.025),(0.12,0.12,0.14)),title=None):
    ren=vtk.vtkRenderer(); ren.SetBackground(0.03,0.03,0.035)
    for a in parts: ren.AddActor(a)
    for pos,i in [((40,-40,60),1.0),((-50,30,30),0.5),((0,60,-20),0.4)]:
        l=vtk.vtkLight(); l.SetLightTypeToSceneLight(); l.SetPositional(False); l.SetPosition(*pos); l.SetFocalPoint(0,0,0); l.SetIntensity(i); ren.AddLight(l)
    ren.SetUseFXAA(True)
    c=ren.GetActiveCamera(); c.SetPosition(*cam[0]); c.SetFocalPoint(*cam[1]); c.SetViewUp(0,0,1); ren.ResetCamera(); c.Zoom(cam[2])
    if title:
        t=vtk.vtkTextActor(); t.SetInput(title); tp=t.GetTextProperty(); tp.SetFontSize(42); tp.SetColor(0.8,0.9,0.8); t.SetPosition(40,40); ren.AddActor2D(t)
    w=vtk.vtkRenderWindow(); w.SetOffScreenRendering(1); w.AddRenderer(ren); w.SetSize(*size); w.SetMultiSamples(0); w.Render()
    f=vtk.vtkWindowToImageFilter(); f.SetInput(w); f.ReadFrontBufferOff(); f.Update(); wr=vtk.vtkPNGWriter(); wr.SetFileName(os.path.join(OUT,name)); wr.SetInputConnection(f.GetOutputPort()); wr.Write(); print('wrote',name)
def parts(sz,explode=0,off=(0,0,0),keys=MAT):
    d=os.path.join(ROOT,'hardware',sz); e={'glass':4,'oled':3,'pcb':2,'bat_L':6,'bat_R':6,'strip':-3,'socket':-6,'shell':0}
    out=[]
    for k in keys:
        p=os.path.join(d,f'v10_{sz}_{k}.stl')
        if os.path.exists(p):
            dz=e[k]*explode; dy=(-4*explode if k=='strip' else 0)
            out.append(actor(p,k,(off[0],off[1]+dy,off[2]+dz)))
    return out
for sz in ['M','L']:
    scene(parts(sz),((45,-35,35),(0,0,0),1.05),f'{sz}_iso_hq.png',title=f'CodeRain Ring v10 - size {sz}')
    scene(parts(sz,explode=2.2),((50,-45,25),(0,0,0),0.9),f'{sz}_exploded_hq.png',size=(1400,1500),title=f'{sz}: exploded (glass / OLED / PCB / batteries / strip / socket)')
    scene(parts(sz),((0,0,60),(0,0,0),1.0),f'{sz}_top_hq.png',size=(1400,1400),title=f'{sz}: top view')
    scene(parts(sz),((60,0,0),(0,0,0),0.95),f'{sz}_side_hq.png',size=(1400,1400),title=f'{sz}: side view along finger')
scene(parts('M',off=(0,-15,0))+parts('L',off=(0,15,0)),((50,-20,40),(0,0,0),1.15),'ML_compare_hq.png',size=(2200,1300),title='M (left) vs L (right)')
