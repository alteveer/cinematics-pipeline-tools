# Raven Cinematics Tools
# Authors: Mike Gilardi and Colin Alteveer

# This file is the best entry point for manual export (mayapy or command 
# listener window with bootstrap.py) of our Unreal Engine 3 cinematics scenes.
# site_auditor.py and site_exporter.py were used by our website to trigger many
# of the same functions, capture stdout, and report back to the site via web 
# service. We planned to implement a distributed queue for export and render
# jobs, the ground-work of which can be seen in tray_icon.py. We did use this 
# tray icon to do a distributed render of the claw-slash Raven bumper from 
# "X-Men Origins - Wolverine."
# 
# list() will chunk through all actors in the parameter "actors" (including the
# camera -- for every scene we exported a small sequence that encoded FOV and 
# DOF settings so that our director could do most of his work in Maya) and 
# place an animation binary in a directory for import to engine. "script_name"
# was the name of the scene in the script, usually of the format "XXX_9999" 
# which we used as a prefix for our anims.
#
# Our end-to-end workflow was as follows:
# 
# 1. Our director takes cleaned mo-cap and arranges the sequences into a maya 
#    scene, roughs-in some camera shots, and saves-off the block-in for one 
#    of our animators.
# 2. The animator does his animation work on the scene, saves it off again, and
#    uses our web application to audit the scene for proper setup and errors. 
#    If it passes, he selects which actors to export and sends off the batch. 
# 3. The web app fires off exports for the sequences that were selected and 
#    captures stdout/stderr from mayapy and routes it back to a web console for 
#    the animator.
# 4. Once the sequence is finished the animator is given "ok" or "error" status 
#    and he can choose to accept the generated export file and have it imported
#    into the engine for check-in. In the case of an error, the full log is 
#    available for debugging.
#
# The director and animators are free to iterate as they please, all import/
# export work is handled for them. When they are ready to make a final bink,
# they would tell the site to trigger the process and generate a pre-rendered, 
# super-sampled version of the in-game sequence.
#
# We never fully transitioned to using *only* our intranet site for dailies, 
# but whenever changes were pushed to a scene we were notified and we could 
# choose to trigger a render and then pass it off to be binked and converted 
# to .avi for our morning meetings.
# 
# camera, actor, scene, and util.py are all pretty self-explanatory, but we 
# used namespace.py to manipulate the referenced rigs in our scenes, and 
# bootstrap.py is a belt-and-suspenders import routine that let these 
# scripts work on 99% of our workstations. 
				
import scene
import actor
import camera
import util

def list(scene, path_to_save_psa, script_name, actors):	
	for actor in actors:
		scene.open(scene)
		if actor == 'cam':
			util.debug("Exporting camera")
			if camera.export(path_to_save_psa, script_name):
				util.debug("Camera exported successfully.")
			else:
				return False
		else:
			util.debug("Exporting actor \"%s\"" % actor)
			if actor.export(path_to_save_psa, script_name, actor):
				util.debug("Actor \"%s\" exported successfully." % actor)
			else:
				return False
	return True