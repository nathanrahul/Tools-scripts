""" Export GPU Cache
    Description: 
                 - Command line tool, enabling the artist to easily visualise heavy scenes.
                 - Creates a light weight scene with gpu caches. Useful for quick visualization of large sets, create dailies etc
                 - Import list of alembics from a directory, assign a shader and export GPUCache of all the geos. 
				 - Import the exported GPUCaches into a mayaScene and save it for the artist to use
	
	Usecase: This script is useful for heavy scenes that slowdown/crash maya. Useful for heavy environments or photogrammetry assets. 

	Author: Rahul Nathan
"""

# Import Statements
import maya.cmds as cmds
import os
import sys
import getpass

# Initialize Maya in batch mode
import maya.standalone
maya.standalone.initialize()

# Load Plugin
cmds.loadPlugin("gpuCache.so", quiet=True)
cmds.loadPlugin("AbcImport.so", quiet=True)
cmds.loadPlugin("AbcExport.so", quiet=True)

# Get Inputs
directoryPath = sys.argv[1]

#=================================================================#
# Main Function
#=================================================================#
def exportImportGPUCache(directoryPath):
    """ This is the main function of the script.
        Finds & imports alembic files and assigns a shader. 
        Exports GPU Cache and clears the scene
        Imports the exported GPU cache and saves a mayaScene
        
        Args:
            directoryPath (string): Directory path with the list of alembic files.
    """
	# Find Alembic files
	abcFileList = findAlembicFiles(directoryPath)
	# Create Phong Shader
	phongShader, phongShaderSG = creatPhongShader()

	importedAbc = None
	gpuCacheDir = None
	if len(abcFileList) == 0:
		cmds.error("Empty List")
	else:
		for abcFilePath in abcFileList:
			try:
				# Import Alembic
				abcFile = importAlembic(abcFilePath)
				# Assign PhongShader
				allGeos = cmds.listRelatives(cmds.ls(geometry=True), p=True, path=True)
				cmds.select(allGeos, r=True)
				for i in allGeos:
					cmds.sets(i, e=True, forceElement=phongShaderSG)

				#Export GPU Cache
				gpuCacheDir = exportGPUCache(directoryPath, abcFile, allGeos)

			except:
				pass

	if gpuCacheDir:
		# Import GPU Cache
		importGPUCache(gpuCacheDir)
		
		# Save Scene
		saveScene(directoryPath)

#=================================================================#
# Utils
#=================================================================#
def findAlembicFiles(directoryPath):
    """ Finds all alembic files from the provided directory
        Args:
            directoryPath (string): Directory path with the list of alembic files.
        Returns:
            abcFileList (list): List of alembic file paths from the provided directory.
    """
	# Find Alembic files
	abcFileList = []
	# Check path and find alembic files
	files = [f for f in os.listdir(directoryPath) if os.path.isfile(os.path.join(directoryPath, f))]
	for abcFile in files:
		if abcFile.lower().endswith('.abc'):
			abcFileList.append(os.path.join(directoryPath, abcFile))

	return abcFileList

def creatPhongShader():
    """ Creates a phongShader
        Returns:
            phongShader (string): shadingNode
            phongShaderSG (string): shadingGroup
    """
	# Create Phong Shader for preview
	phongShader = cmds.shadingNode('phong', asShader=True, name='phongShader')
	phongShaderSG = cmds.sets(name='phongShaderSG', empty=True, renderable=True, noSurfaceShader=True)
	cmds.connectAttr('%s.outColor'%phongShader, '%s.surfaceShader'%phongShaderSG)
	cmds.setAttr('%s.cosinePower'%phongShader, 50)
	cmds.setAttr('%s.specularColor'%phongShader, 0.182, 0.182, 0.182, type="double3")

	return phongShader, phongShaderSG

def importAlembic(abcFilePath):
    """ Imports the alembic into the scene.
        Renames the alembic as the file name.
        Args:
            abcFilePath (string): File path of the alembic file.
        Returns:
            abcFile (string): Name of the alembic file.
    """
	# Import Alembic
	abcFile = os.path.basename(abcFilePath)
	print("\nImporting %s"%abcFile)
	importedAbc = cmds.file(abcFilePath, type="Alembic", i=True, rnn=True)
	cmds.rename(cmds.ls(importedAbc, type="transform"), os.path.splitext(abcFile)[0])

	return abcFile

def exportGPUCache(dirPath, abcFile, allGeos):
    """ Exports GPU cache for the alembic file.
        Deletes all geos in the scene.
        Args:
            dirPath (string): Directory path with the list of alembic files.
            abcFile (string): Name of the alembic file.
            allGeos (list): List of geometry objects in the scene.
        Returns:
            gpuCacheDir (string): Path of the GPU Cache directory.
    """
	# Export GPU Cache + Clear scene
	print("\nExporting GPU cache for %s"%abcFile)
	gpuCacheDir = os.path.join(dirPath, "gpuCache")
	if os.path.isdir(gpuCacheDir) == False:
		os.mkdir(gpuCacheDir, 0775)

	cmds.gpuCache(allGeos, st=1, et=1, wm=True, fileName=os.path.splitext(abcFile)[0], directory=gpuCacheDir, smf=False)

	cmds.select(allGeos)
	cmds.delete()

	return gpuCacheDir

def importGPUCache(gpuCacheDir):
    """ Imports GPU Caches from the provided directory.
        Args:
            gpuCacheDir (string): Path of the GPU Cache directory.
    """
	# Find all GPU Cache files
	gpuCacheList = []
	if os.path.isdir(gpuCacheDir):
		try:
			for root, dirs, files in os.walk(gpuCacheDir):
				for abcFile in files:
					if abcFile.lower().endswith('.abc'):
						gpuCacheList.append(os.path.join(root, abcFile))
					else:
						print("No alembics found")

		except:
			print("Invalid Path")

	print gpuCacheList
	print "-"*30
    
    # Import GPU Cache
	for cacheFilePath in gpuCacheList:
		cacheFile = os.path.basename(cacheFilePath)
		print("Importing %s"%cacheFile)
		cmds.createNode("gpuCache", n=os.path.splitext(cacheFile)[0])
		cmds.setAttr("%s.cacheFileName"%os.path.splitext(cacheFile)[0], cacheFilePath, type="string")

def saveScene(dirPath):
    """ Saves the maya scene.
        Args:
            dirPath (string): Directory path with the list of alembic files.
    """
	# Save MayaScene
	mayaFileName = "gpuCacheFile_" + getpass.getuser() + ".ma"
	cmds.file(rename=os.path.join(dirPath, mayaFileName))
	cmds.file(save=True, type="mayaAscii")

	print "\nMaya Scene saved to below path"
	print os.path.join(dirPath, mayaFileName)
	print "="*30

#=================================================================#
# Execution
#=================================================================#
exportImportGPUCache(directoryPath)
