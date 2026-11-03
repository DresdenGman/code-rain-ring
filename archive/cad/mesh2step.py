import sys
from OCP.StlAPI import StlAPI_Reader
from OCP.TopoDS import TopoDS_Shape, TopoDS
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing, BRepBuilderAPI_MakeSolid
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.TopAbs import TopAbs_SHELL
from OCP.TopExp import TopExp_Explorer
for n in sys.argv[1:]:
    s=TopoDS_Shape(); StlAPI_Reader().Read(s,f"cad/{n}_lowpoly.stl")
    sw=BRepBuilderAPI_Sewing(1e-4); sw.Add(s); sw.Perform(); sh=sw.SewedShape()
    out=sh
    ex=TopExp_Explorer(sh,TopAbs_SHELL)
    if ex.More():
        try:
            ms=BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(ex.Current())); out=ms.Solid()
        except Exception as e: print("solid fail",e)
    w=STEPControl_Writer(); w.Transfer(out,STEPControl_AsIs); w.Write(f"cad/{n}.step"); print(n,"ok")
