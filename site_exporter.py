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

def batch_list(scene_location, cinematic_id, export_to, script_name, parts):
	mel.eval("source \"O:/ArtistTools/zoo/zooShotsUtils.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooShelveIt.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooFlags.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooUtils.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooArrays_int.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooArrays_str.mel\"")
	mel.eval("source \"O:/ArtistTools/zoo/zooShots.mel\"")
	
#	try:
	mcommand_callback = om.MCommandMessage.addCommandOutputCallback(callback, None)

	for part in parts:
		util.debug('Exporting %(script_name)s:%(part)s' % {
			'script_name':script_name,
			'part':part
		})
		try:
			fail = False
			messages = StringIO.StringIO()
			sys.stdout = messages
			
			post = {'_method':'PUT'}
	
			if util.hasActorX():
				if(scn.open(scene_location)):
					if part == 'camera':
						util.debug("Exporting camera")
						if cam.export(export_to, script_name):
							util.debug("Camera exported successfully.")
						else:
							util.debug('Export failed for: camera')
							fail = True
					else:
						util.debug("Exporting actor \"%s\"" % part)
						if act.export(export_to, script_name, part):
							util.debug("Actor \"%s\" exported successfully." % part)
						else:
							util.debug('Export failed for: %s' % part)
							fail = True
				else:
					util.debug("Couldn't open scene %s" % scene_location)	
					fail = True
			else:
				util.debug("Need ActorX plugin to perform exports.")
				fail = True

			if fail:
				endpoint = 'fail'
			else:
				endpoint = 'pass'
			connect_string = "http://%(server)s:%(port)s/cinematics/%(id)s/parts/%(part)s/%(endpoint)s" % {
				'endpoint':endpoint,
				'part':part,
				'id':cinematic_id,
				'server':ROBO_SERVER,
				'port':ROBO_PORT
			}
			sys.stdout = sys.__stdout__
			post.update({'messages': messages.getvalue()})
			util.debug(post)
	#		util.debug(urllib.urlencode(post))
			util.debug("Connect string: %s" % connect_string)
			urllib.urlopen(connect_string,urllib.urlencode(post))
		except Exception, e:
			util.debug('Exception: %s' % e)
			endpoint = 'fail'
			connect_string = "http://%(server)s:%(port)s/cinematics/%(id)s/parts/%(part)s/%(endpoint)s" % {
				'endpoint':endpoint,
				'part':part,
				'id':cinematic_id,
				'server':ROBO_SERVER,
				'port':ROBO_PORT
			}
			sys.stdout = sys.__stdout__
			post.update({'messages': messages.getvalue()})
			util.debug(post)
	#		util.debug(urllib.urlencode(post))
			util.debug("Connect string: %s" % connect_string)
			urllib.urlopen(connect_string,urllib.urlencode(post))

	om.MCommandMessage.removeCallback(mcommand_callback)
	messages.close()

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
#	except:
#		sys.stdout = sys.__stdout__
#		print "fail"
#		while(1):
#			1==1
#		


if __name__ == '__main__':
#	for a in sys.argv:
#		print a
	batch_list(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5:])

