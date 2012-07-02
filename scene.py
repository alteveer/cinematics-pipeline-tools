import maya.cmds as cmds
import maya.mel as mel
import os
import util
mel.eval("source \"O:/ArtistTools/Maya/Scripts/zoo/zooShotsUtils.mel\"")
mel.eval("source \"O:/ArtistTools/Maya/Scripts/zoo/zooShelveIt.mel\"")
mel.eval("source \"O:/ArtistTools/Maya/Scripts/zoo/zooFlags.mel\"")
mel.eval("source \"O:/ArtistTools/Maya/Scripts/zoo/zooUtils.mel\"")
mel.eval("source \"O:/ArtistTools/Maya/Scripts/zoo/zooArrays_int.mel\"")
mel.eval("source \"O:/ArtistTools/Maya/Scripts/zoo/zooArrays_str.mel\"")
mel.eval("source \"O:/ArtistTools/Maya/Scripts/zoo/zooShots.mel\"")

GAME_RATE = 30

def open(path):
	if os.path.isfile(path):
		util.debug("Opening file %s." % path)
		cmds.file(rn="deleteMe")
		cmds.file(s=1)
		cmds.file(path, o=1,iv=1)
		return True
	else:
		return False
		
def length():
	shots = getShots()
	scene_start = cmds.playbackOptions(q = 1, ast = 1)
	scene_end = cmds.playbackOptions(q = 1, aet = 1)
	if shots[0]['start'] == scene_start and shots[-1]['end'] == scene_end:
		return scene_start, scene_end
	else:
		return False

def getShots():
	mel.eval("zooReorderShots;")
	shots = []
	for shot in range(0,len(mel.eval("zooListShots;"))):
		if mel.eval("zooGetShotInfo disable %s" % shot) == "0":
			shots.append({
					"start"	: 	int(mel.eval("zooGetShotInfo start %s" % shot)), 
					"end"	: 	int(mel.eval("zooGetShotInfo end %s" % shot))
				}
			)
	return shots									

def hasMasterCam():
	return cmds.ls("masterCam") != None and cmds.objectType(cmds.listRelatives("masterCam", s = 1), isType = "camera") == 1

def deleteOthers(node):
	util.debug("Deleting objects everything but '%s'" % node)
	cmds.select(ado=1)
	cmds.select(node, d=1)
	cmds.delete(cmds.selectedNodes(dagObjects=1))
	
def clearReferences():
	util.debug("Remove all references.")
	references = cmds.file(q = 1, r=1)
	for reference in references:
		util.debug("Clearing reference: %s." % reference)
		cmds.file(reference, ur = 1)

def importReferences(names = "all"):
	util.debug("Importing reference(s): %s" % names)
	references = cmds.file(q=1,r=1)
	if len(cmds.file(q=1,r=1)) < 1:
		util.debug("No references to import.")
	else:
		if names != "all":
			try:
				for name in names:
					references.index(name)
			except ValueError:
				util.debug("Cannot find reference %s" % name)
				return False
			else:
				references = names

		for reference in references:
			cmds.file(reference, ir=1)	
			util.debug("Importing reference: %s." % reference)
	return True

def makeCutTangentsStep(times):
	util.debug("Make keys linear at frame(s): %s " % times)
	for keyframe in times:
		cmds.keyTangent(lock = 0, itt = "linear", ott="step",time =(keyframe, keyframe))	

def audit():
	errors = []
	if(hasMasterCam() == False):
		util.debug("ERROR: Cannot find master camera.")
	if length() == False:
		util.debug("ERROR: Scene has no shots.")