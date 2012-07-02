import maya.standalone
maya.standalone.initialize(name='python')
import maya.mel as mel
import maya.cmds as cmds
import maya.OpenMaya as om
import sys
sys.path.append(r'o:\ArtistTools\Python')
import raven
import raven.maya.cinematics.actor as act
import raven.maya.cinematics.camera as cam
import raven.maya.cinematics.scene as scn
import raven.maya.cinematics.util as util
#from raven.maya.cinematics import *
#import comm
#import json
import urllib
import StringIO
ROBO_SERVER = 'rsmsnwolvcaptur'
ROBO_PORT = 1492

def callback(nativeMsg, messageType, data):
	print nativeMsg#, messageType, data

def audit(path, cinematic_id):
	mel.eval("source \"O:/ArtistTools/zoo/zooShotsUtils.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooShelveIt.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooFlags.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooUtils.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooArrays_int.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooArrays_str.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooShots.mel\"")
	
	mcommand_callback = om.MCommandMessage.addCommandOutputCallback(callback, None)
	
	messages = StringIO.StringIO()
	sys.stdout = messages
	
	
	post = {'scene[error_messages]':[],'_method':'PUT'}
	#sys.stdout = messages
	
	#post['messages'].append(util.debug("File to open: %s" % path))
	try:
		if scn.open(path):
			print "File opened, begin audit"
			if len(scn.audit()) < 1:
				util.debug(scn.audit())
				shots = scn.getShots()
				util.debug(shots)
				scene_start, scene_end = scn.length()
				namespaces = []
				for ref in cmds.file(q=1, r=1):
					namespaces.append(cmds.referenceQuery(ref, rfn=True).replace('RN', ''))
	
				post.update({
					'namespaces':namespaces,
					'scene[start_time]':scene_start,
					'scene[end_time]':scene_end,
					'scene[shots]':shots
				})
	
				#post['messages'].append(util.debug("Scene passed."))
				print "Scene passed."
			else:
				print "Scene failed."
				post['scene[error_messages]'].append(scn.audit())
		else:
			print "File open failed"
			post['scene[error_messages]'].append(util.error(10012))
	except:
		util.debug("Runtime Error")
		post['scene[error_messages]'].append("Runtime Error")

	sys.stdout = sys.__stdout__
	
	post.update({'scene[debug_messages]': messages.getvalue()})
	om.MCommandMessage.removeCallback(mcommand_callback)
	messages.close()

	connect_string = "http://%(server)s:%(port)s/cinematics/%(id)s/scene" % {
		'id':cinematic_id,
		'server':ROBO_SERVER,
		'port':ROBO_PORT
	}
	util.debug("Connect string: %s" % connect_string)
	util.debug(post)
	util.debug(urllib.urlencode(post))
	urllib.urlopen(connect_string,urllib.urlencode(post))
#	maya.mel.file
	#print cmds.file(r=1, q=1)
	
	#print cmds.ls(type="joint")
#	for name, data in inspect.getmembers(maya.cmds.file):
#		print '%s :' % name, repr(data), '\n'
#	var = sceneInformation()
#	var = sceneInformation().hasMasterCamera()
#	var = sceneInformation().getCameraShots()
#	var = sceneInformation().removeDisabledShots()
#	var = sceneInformation().getCameraStartAndEndTimes()
#	var = sceneInformation().getActors()
#	var = sceneInformation().getApprovedActors()
#	var = sceneInformation().getSceneStartAndEndTimes()
#print sys.argv[0]
#	print "sleep"
#	while(1):
#		1==1
#		

if __name__ == '__main__':
	for a in sys.argv:
		print a
	audit(sys.argv[1], sys.argv[2])

