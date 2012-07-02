"""
A Taskbar Icon with xp balloon tooltip support

Authors: Mike Gilardi and Colin Alteveer
"""
import json
import httplib
import socket
import wx
import win32api
import blocking_test
import TBIcon

class RoboTray(wx.App):
	ID_PING_TIMER = wx.NewId()
	PING_IN_MS = 60000
	
	ROBO_SERVER = 'rsmsnwolvcapture'
	ROBO_PORT = 3000
	RENDER_PROGRAM_PATH = "\"C:\\Program Files\\Autodesk\\Maya2008\\bin\\Render.exe\""
	RENDERER = "mr"
	
	r_dir = ""
	img_prefix = ""
	img_width = 1280
	img_height = 720
	startf = ""
	endf = ""
	file_to_render = ""
	
	c = httplib.HTTPConnection(ROBO_SERVER, ROBO_PORT, timeout=10)
	connected = False
	can_render = True
	rendering = False
	login = ""    
	computer = ""
	
	def __init__(self):
		wx.App.__init__(self, "")
		#self.test_connection()
		self.icon = wx.Icon('images\\robo.ico', wx.BITMAP_TYPE_ANY)
		self.tbicon = TBIcon.TBIcon(self)
		
		self.login = win32api.GetUserName()
		self.computer = win32api.GetComputerName() 
		self.timer_ping = wx.Timer(self, self.ID_PING_TIMER)
		self.Bind(wx.EVT_TIMER, self.Ping, id=self.ID_PING_TIMER)
		
		self.Ping("Manually triggered.")
		self.timer_ping.Start(self.PING_IN_MS)
		
	def Comm(self, target, method = 'GET'):
		try:
			self.c.request(method, target)
			self.connected = True

			return json.loads(self.c.getresponse().read())
			
		except socket.error, e:
			print "Cannot connect: %s" % e
			self.tbicon.ShowBalloonTip("", "I can't seem to connect to ROBO...")
			self.connected = False
			
			return False			

	def Ping(self, event):
		if not self.rendering:
			res = self.Comm("/comm/%(computer)s/ping" % { 'computer':	self.computer })
			if not res == False and 'available_frames' in res and res['available_frames']:
				#do something
				print 'getting a frame:'
				self.GetFrame()
			
			else:
				print 'nothing to render.'

#			if(not self.connected):
#				print "Connected: %(host)s:%(port)d" % {'host': self.c.host, 'port': self.c.port}
#   	  self.tbicon.ShowBalloonTip("", "Connected!")
	
	def GetFrame(self):
		res = self.Comm("/comm/%(computer)s/get_frame" % { 'computer': self.computer })
		#print res
		if 'job' in res:
			self.r_dir = "O:\cinematic\Renders\%s" % res['job']
			self.img_prefix = res['job']
			self.startf = res['frame']
			self.endf = res['frame']
			self.file_to_render = res['file']
			
#			if res['width']:
#				self.img_width = res['width']
#			if res['height']:
#				self.img_height = res['height']
			
			self.StartRender()
		else:
			print	"Cannot get a frame."
			
	def StartRender(self):
		if self.rendering:
			print "already rendering..."
		else:
			self.rendering = True
			#self.Bind(wx.EVT_IDLE, self.OnIdle)
			self.Bind(wx.EVT_END_PROCESS, self.OnProcessTerminate)
			# idle progress report
			
			proc = wx.Process(self)
			
			command_string = "%(rpp)s -renderer %(rend)s -rd %(render_directory)s -im %(image_prefix)s -x %(image_width)s -y %(image_height)s -s %(startf)s -e %(endf)s  %(file)s" % {
				'rpp':							self.RENDER_PROGRAM_PATH,
				'rend':							self.RENDERER,
				'render_directory':	self.r_dir,
				'image_prefix':			self.img_prefix,
				'image_width':			self.img_width,
				'image_height':			self.img_height,
				'startf': 					self.startf,
				'endf': 						self.endf,
				'file': 						self.file_to_render				
			}
			
			print command_string
			pid = wx.Execute(command_string,wx.EXEC_ASYNC, proc)
			
			if wx.Process.Exists(pid):
				
				res = self.Comm("/comm/%(computer)s/start" % { 'computer': self.computer })
				#self.OnProgressTick('Manual')
				print pid
			else:
				print "Couldn't start render"
				self.rendering = False
				self.Comm("/comm/%(computer)s/complete/fail" % { 'computer': self.computer })

	def OnProgressTick(self, event):
		res = self.Comm("/comm/%(computer)s/update" % { 'computer': self.computer })
		
	def OnProcessTerminate(self, event):
		print "Process %(pid)s exited with status %(status)s" % {'pid': event.GetPid(),'status': event.GetExitCode()}
		self.rendering = False
		self.Comm("/comm/%(computer)s/complete/%(status)s" % {
			'computer':	self.computer,
			'status':		event.GetExitCode()
		})

	def OnExit(self):
		self.tbicon.Destroy()
		self.c.close()
		exit(0)

if __name__ == "__main__":
	app = RoboTray()
	app.MainLoop()