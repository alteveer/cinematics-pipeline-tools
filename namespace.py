import maya.cmds as cmds
import maya.mel as mel
import util

def deleteOthers(ns):
	util.debug("Delete not in namespace: %s" % ns)
	cmds.select(ado=1)
	cmds.select(
		cmds.ls("%s:*" % ns), 
		d=1
	)
	cmds.delete(cmds.selectedNodes(dagObjects=1))

def add(namespace, objects):
	util.debug("Add selection to namespace")
	cmds.namespace(set=":")
	cmds.namespace(
		f=1,
		add=(str(namespace))
	)
	for i in objects:
		try:
			newName = str(namespace)+":"+i
			cmds.rename(i,newName)
		except RuntimeError:
			return 0
			exit("Error R80110: Unable to add",i,"to namespace.")
	return 1
	
def namespaces():	
	namespaces = []
	namespaceInfo = cmds.namespaceInfo(lon=1)
	for i in range(0,len(namespaceInfo)):
		if 	(namespaceInfo[i].count("UI")!=1) and (namespaceInfo[i].count("shared")!=1):
			namespaces.append(namespaceInfo[i])
	return namespaces

def remove(namespaces = 'all'):
	if namespaces == 'all':
		namespaces = cmds.namespaceInfo(lon = 1)
		
	for namespace in namespaces:
		cmds.namespace(f=1,mv=(namespace,":"))
		if namespace.count("UI") <1 and namespace.count("uv") <1 and namespace.count("shared") <1:
			cmds.namespace(f=1,rm=str(namespace))