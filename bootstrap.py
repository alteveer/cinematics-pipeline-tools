import maya.standalone
maya.standalone.initialize(name='python')
import maya.mel as mel
import sys
sys.path.append(r'o:\ArtistTools\Python')
#sys.path.append(r'c:\ravenlocal\ArtistTools\Python')
import raven
import raven.maya.cinematics.actor as act
import raven.maya.cinematics.camera as cam
import raven.maya.cinematics.scene as scn
import raven.maya.cinematics.util as util
import raven.maya.cinematics.batch as bat
from raven.maya.cinematics import *
reload(raven)
reload(raven.maya)
reload(raven.maya.cinematics)
reload(raven.maya.cinematics.actor)
reload(raven.maya.cinematics.camera)
reload(raven.maya.cinematics.namespace)
reload(raven.maya.cinematics.scene)
reload(raven.maya.cinematics.util)
mel.eval("source \"O:/ArtistTools/zoo/zooShotsUtils.mel\"")
mel.eval("source \"O:/ArtistTools/zoo/zooShelveIt.mel\"")
mel.eval("source \"O:/ArtistTools/zoo/zooFlags.mel\"")
mel.eval("source \"O:/ArtistTools/zoo/zooUtils.mel\"")
mel.eval("source \"O:/ArtistTools/zoo/zooArrays_int.mel\"")
mel.eval("source \"O:/ArtistTools/zoo/zooArrays_str.mel\"")
mel.eval("source \"O:/ArtistTools/zoo/zooShots.mel\"")
