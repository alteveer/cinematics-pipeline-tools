import maya.cmds as cmds
import maya.mel as mel
import inspect

def debug(message):
	debug_message = "%(line)s : %(message)s" % {
		'line': inspect.currentframe().f_back.f_lineno,
		'message': message
	}
	print debug_message
	return debug_message
					
def hasActorX():
	debug("Looking for ActorX Export Plugin...")
	plugin = ""
	if mel.eval("getApplicationVersionAsFloat();") == 8.5:
		plugin = "ActorXTool85"
	elif mel.eval("getApplicationVersionAsFloat();") == 2008:
		plugin = "ActorXTool2008"
	elif mel.eval("getApplicationVersionAsFloat();") == 2009:
		plugin = "ActorXTool2009"
	if cmds.pluginInfo(q=1, ls=1) == None or cmds.pluginInfo(q=1, ls=1).count(plugin) == None:
		try:
			cmds.loadPlugin(plugin)
			return True
		except RuntimeError:
			return False
	else:
		return True