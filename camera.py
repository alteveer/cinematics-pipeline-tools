import maya.cmds as cmds
import maya.mel as mel
import scene
import util

MASTER_CAMERA_NAME = "masterCam"

def export(path_to_save, script_name):
	shots = scene.getShots()
	scene_start, scene_end = scene.length()

	util.debug("Un-parenting master camera.")
	try:
		cmds.parent(MASTER_CAMERA_NAME,w=1)
	except RuntimeError:
		pass
	
	cmds.select(MASTER_CAMERA_NAME)
	masterCam = cmds.ls(sl = 1)[0]
	masterCamShape = cmds.listRelatives(MASTER_CAMERA_NAME, s = 1)[0]

	util.debug("Baking master camera.")
	cmds.bakeResults(	masterCam, \
										simulation = 1, 
										t=(scene_start, scene_end), \
										sampleBy = 1, \
										pok=1, \
										disableImplicitControl = 1, \
										at= ["tx","ty","tz","rx","ry","rz"])
	cmds.bakeResults(	masterCamShape, \
										simulation = 1, \
										t=(scene_start, scene_end), \
										sampleBy = 1, \
										pok=1, \
										disableImplicitControl = 1, \
										at="focalLength")
	
# unreference all, isolate cams

	util.debug("Removing references.")
	scene.clearReferences()

	util.debug("Isolating master camera.")
	scene.deleteOthers("masterCam")
	
#	makeUnrealCameraTree()
	util.debug("Making new master camera hierarchy for Unreal.")
	root = "masterCamRoot"
	position = "masterCamPosition"	
	fov = "masterCamFOV"
	cmds.select(cl = 1)
	#if cmds.objExists("masterCamRoot") == 0:
	root = cmds.joint(p = (0, 0, 0,), n = "masterCamRoot")
	position = cmds.joint(p = (0, 0, 0,), n = "masterCamPosition")
	fov = cmds.joint(p = (0, 0, 0,), n = "masterCamFOV")
	cmds.pointConstraint(masterCam,position,offset = (0 ,0 ,0),weight = 1)
	cmds.orientConstraint(masterCam,position,offset = (0 ,0 ,0),weight = 1)
	cmds.connectAttr(masterCam+"Shape.focalLength",fov+".translateZ")

#	bakeUnrealCamBones()
	util.debug("Baking new master camera hierarchy.")
	cmds.bakeResults(["masterCamFOV","masterCamRoot", "masterCamPosition"], \
										simulation = 1, \
										t=(scene_start, scene_end), \
										sampleBy = 1, \
										disableImplicitControl = 1, \
										sparseAnimCurveBake = 0, \
										at= ["tx","ty","tz","rx","ry","rz"])

	util.debug("Delete old master camera hierarchy.")
	scene.deleteOthers("masterCamRoot")

#	makeCutTangentsLinear()
	util.debug("Setting tangent to stepped for keys that occur on cuts: %s" % shots)
	cut_frames = []
	for shot in shots:
		cut_frames.append(shot['end'])
	scene.makeCutTangentsStep(cut_frames)

	
	psa_name = "%s_cam" % script_name
	util.debug("Creating .PSA file: %s" % psa_name)
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