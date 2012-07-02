import maya.cmds as cmds
import maya.mel as mel
import namespace as ns
import scene
import util

def export(path_to_save, script_name, namespace):
	util.debug("Importing all references, flattening scene.")
	scene.importReferences("all")
	
	shots = scene.getShots()
	scene_start, scene_end = scene.length()

	#util.debug("Selecting all joint hierarchies.")
	#cmds.select(all=1, hi=1)
	#cmds.select(cmds.ls(sl=1, typ='joint'), r=1)

	util.debug("Baking all animations.")
	scene_start, scene_end = scene.length()
	cmds.select("%s:root" % namespace, hi=1)
	cmds.select(cmds.ls(sl=1, typ='joint'), r=1)
	cmds.bakeResults(sm=1, t=(scene_start,scene_end), sb=1, sac=0, pok=0,at= ["tx","ty","tz","rx","ry","rz"])


	ns.deleteOthers(namespace)
	ns.remove()
	
	util.debug("Setting tangent to stepped for keys that occur on cuts: %s" % shots)
	cut_frames = []
	for shot in shots:
		cut_frames.append(shot['end'])
	scene.makeCutTangentsStep(cut_frames)

	psa_name = "%(script_name)s_%(namespace)s" % {
		'script_name': script_name,
		'namespace': namespace
	}
	util.debug("Creating .PSA file: %s" % psa_name)
	
	#for shot in shots:
	#	## Unreal xyz
	#	util.debug("{",shot,"[",\
	#	-cmds.getAttr("%s:root.translateZ" % namespace,t=shot['start']),\
	#	cmds.getAttr("%s:root.translateX" % namespace,t=shot['start']),\
	#	-cmds.getAttr("%s:root.translateY" % namespace,t=shot['start']),\
	#	"][",\
	#	-cmds.getAttr("%s:root.rotateZ" % namespace,t=shot['start']),\
	#	cmds.getAttr("%s:root.rotateX" % namespace,t=shot['start']),\
	#	-cmds.getAttr("%s:root.rotateY" % namespace,t=shot['start']),\
	#	"]}")

	for shot in shots:
		cmds.playbackOptions(min = shot['start'], max = shot['end'])
		sequence_name = "%(psa_name)s_%(#)02d" % {
			'psa_name'	:	psa_name, 
			'#'					:	shots.index(shot)
		}
		util.debug("Adding Sequence %s" % sequence_name)
		if shots.index(shot) == len(shots)-1 :
			if 'command AXExecute executed. ' == cmds.axexecute(path = path_to_save, animfile = psa_name, sequence = sequence_name, rate = scene.GAME_RATE, saveanim = 1):
				return True
			else:
				return False
		else:
			cmds.axexecute(path = path_to_save, animfile = psa_name, sequence = sequence_name, rate = scene.GAME_RATE)