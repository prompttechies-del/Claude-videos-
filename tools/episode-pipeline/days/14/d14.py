# ----- Day 14: The Big Pitch Is Coming -----
clawd=Toon("clawd",(.05,-.3,0),ORA)
bit=Toon("bit",(.45,-.3,0),(.04,.22,.85),scale=.36,eyem=mat("cyan",(.2,.9,1),.3,em=8,emc=(.2,.9,1)),W=9,D=7,Hh=7,antenna=True)
maya=Human("maya",(1.5,.3,-.15))
bpy.ops.mesh.primitive_plane_add(size=1,location=(-.55,.55,.4),rotation=(math.pi/2,0,0)); wb=bpy.context.object; wb.scale=(.7,.434,1)
wm=bpy.data.materials.new("wbm"); wm.use_nodes=True; wn=wm.node_tree.nodes; wbsdf=wn["Principled BSDF"]; wim=wn.new("ShaderNodeTexImage")
WB=[bpy.data.images.load(bpy.path.abspath(f"//v{DAY}/wb_{i:02d}.png")) for i in range(18)]; wim.image=WB[0]
wm.node_tree.links.new(wim.outputs["Color"],wbsdf.inputs["Base Color"]); wm.node_tree.links.new(wim.outputs["Color"],wbsdf.inputs["Emission Color"]); wbsdf.inputs["Emission Strength"].default_value=.6; wbsdf.inputs["Roughness"].default_value=.25
wb.data.materials.append(wm)
FR_=mat("wbframe",(.75,.76,.78),.3,metal=.7)
boxo("wbF1",(-.55,.555,.62),(.73,.02,.02),FR_); boxo("wbF2",(-.55,.555,.18),(.73,.02,.02),FR_); boxo("wbF3",(-.915,.555,.4),(.02,.02,.46),FR_); boxo("wbF4",(-.185,.555,.4),(.02,.02,.46),FR_)
boxo("wbL1",(-.85,.58,.09),(.03,.03,.18),FR_); boxo("wbL2",(-.25,.58,.09),(.03,.03,.18),FR_)
SHOTS=[(0,4.35,(1.75,-1.9,.75),(1.62,-1.6,.72),(1.5,.3,.68),(1.5,.2,.7),50),
 (4.35,5.8,(.47,-1.0,.22),(.46,-.85,.2),(.45,-.3,.12),(.45,-.3,.12),55),
 (5.8,15.3,(-.15,-1.7,.45),(-.4,-1.3,.45),(-.5,.55,.38),(-.55,.55,.4),40),
 (15.3,40,(-.6,-.95,.36),(-.66,-.05,.33),(-.68,.55,.32),(-.68,.55,.32),50)]
def animate(t,FRi):
    camera(t,SHOTS)
    n=0 if t<8.9 else min(7,1+int((t-8.9)/.33)); e=int(seg(t,16.0,17.6)*10)
    wim.image=WB[7+e] if t>16.0 else WB[n]
    red_alert(.5*seg(t,16.0,16.4)*(.7+.3*(int(t*7)%2)))
    maya.armR.rotation_euler.x=-2.0*seg(t,2.8,3.1)*(1-seg(t,4.0,4.3)) - 1.5*seg(t,13.7,14)*(1-seg(t,15,15.3))
    maya.H.rotation_euler.z=.05*math.sin(t*2)+math.radians(-30)*seg(t,11.5,11.9); maya.R.location.z=-.15+.03*math.sin(t*1.3)
    maya.talk("maya",FRi); maya.eyes.scale.z=.12 if blink(t,.4) else (1.4 if t>16.2 else 1)
    bit.B.location.z=abs(math.sin(t*14))*.05*(4.4<t<5.6); bit.armL.rotation_euler.x=bit.armR.rotation_euler.x=-2.8*seg(t,4.4,4.55)*(1-seg(t,5.5,5.8))
    bit.armL.rotation_euler.x+=-2.3*seg(t,15.8,16.0); bit.R.rotation_euler.z=math.radians(-40)*seg(t,15.6,15.9)
    bit.talk("bit",FRi); bit.eyes_set(t,.7,wide=(4.4<t<5.8 or t>15.6))
    clawd.R.rotation_euler.z=math.radians(-35)*seg(t,6.0,6.4)*(1-seg(t,15.0,15.3))+math.radians(-35)*seg(t,16.0,16.4)
    clawd.armL.rotation_euler.x=-2.3*seg(t,6.2,6.4)*(1-seg(t,11,11.3)); clawd.talk("clawd",FRi); clawd.eyes_set(t,1.3,wide=(t>16.2))
render_loop(animate)
