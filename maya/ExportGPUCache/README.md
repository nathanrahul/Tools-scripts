# Export GPU Cache

Created: November 2020

## Description
 - Creates a light weight scene with gpu caches.
 - Import list of alembics from a directory, assign a shader and export GPUCache of all the geos. 
 - Import the exported GPUCaches into a mayaScene and save it for the artist to use.
	
## Usecase
- This script is useful for heavy scenes that slowdown/crash maya, like heavy environments or photogrammetry assets. 
- It is a command line tool which enables artists to easily visualise heavy scenes without opening Maya.
- The gpu scene can be used for reviewing large scenes, either through playblasts or directly navigating through the scene in Maya.

