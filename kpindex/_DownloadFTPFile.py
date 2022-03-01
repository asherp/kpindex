from . import Globals
from ftplib import FTP

def _GetCallback(f,ftp,fname):
	'''
	callback function for downloading the file
	
	Inputs
	======
	f : file
		instance of an open file (binary)
	ftp : FTP()
		ftp instance
	fname : str
		Name of the file on the server
	
	'''
	#get the size of the file
	size = ftp.size(Globals.ftpdir+fname)
	
	#set progress to 0
	progress = 0
	
	def callback(chunk):
		f.write(chunk)
		progress += len(chunk)
		
		ndone = np.int32(50*progress/size)
		sdone = '\r[' + '='*ndone + '-'*(50-ndone) + ']'
		print(sdone,end='')
		
	return callback


def _DownloadFTPFile(fname):
	'''
	Downloads a file from an FTP site, returns the full path of the 
	local version of that file.
	
	Inputs:
		addr: full address of file to be downloaded e.g. 
			ftp://a.b.c/folder/file.txt
		fname: file name e.g. file.txt
		
	Returns:
		full path to downloaded file
	'''

	#login to the FTP server
	ftp = FTP(Globals.ftpbase)
	ftp.login()  
	ftp.cwd(Globals.ftpdir)
	
	#open the output file
	f = open(Globals.DataPath+'tmp/'+fname,"wb")	
	
	#get the callback function
	cb = _GetCallback(f,ftp,fname)
	
	#download binary file using ftplib
	ftp.retrbinary('RETR '+fname, cb)
	
	#close the file
	f.close()
	
	#close FTP connection
	ftp.close()
	
	#return the file name
	return Globals.DataPath+'tmp/'+fname
