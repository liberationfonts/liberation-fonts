# Top level Makefile for module liberation-fonts
all : CVS/Root common-update
	@cvs update

common-update : common
	@cd common && cvs update

common : CVS/Root
	@cvs checkout common

CVS/Root :
	@echo "ERROR: This does not look like a CVS checkout" && exit 1

clean :
	@find . -type f -name *~ -exec rm -fv {} \;
