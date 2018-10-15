
import tempfile
import shutil
import os
import subprocess
import time
import tarfile

class CupsManager:
	
	
	def __init__(self):
		
		self.backup_files=["/etc/cups/cupsd.conf","/etc/cups/printers.conf"]
		self.backup_dirs=["/etc/cups/ppd/"]
		
		
	#def init
	
	def get_time(self):
		
		return get_backup_name("CupsManager")
		
	#def get_time
	
	
	def backup(self,dir="/backup/"):
		
		try:
		
			file_path=dir+"/"+self.get_time()
			tar=tarfile.open(file_path,"w:gz")
			
			for f in self.backup_files:
				if os.path.exists(f):
					tar.add(f)
			
			for d in self.backup_dirs:
				if os.path.exists(d):
					tar.add(d)
			
			tar.close()
			
			return [True,file_path]
			
		except Exception as e:
			return [False,str(e)]
		
	#def test
	
	def restore(self,file_path=None):


		if file_path==None:
			for f in sorted(os.listdir("/backup"),reverse=True):
				if "CupsManager" in f:
					file_path="/backup/"+f
					break

		if file_path==None:
			return [False,"Backup file not found"]

		try:

			if os.path.exists(file_path):
				
				tmp_dir=tempfile.mkdtemp()
				tar=tarfile.open(file_path)
				tar.extractall(tmp_dir)
				tar.close()
				
				for f in self.backup_files:
					tmp_path=tmp_dir+f
					if os.path.exists(tmp_path):
						shutil.copy(tmp_path,f)
					
				for d in self.backup_dirs:
					tmp_path=tmp_dir+d
					if os.path.exists(tmp_path):
						cmd="cp -r " + tmp_path +"/* "  + d
						os.system(cmd)
				
				os.system("service cups restart")
						
				return [True,""]
				
		except Exception as e:
				
			return [False,str(e)]
		
	#def test


	
	
#class CupsManager


