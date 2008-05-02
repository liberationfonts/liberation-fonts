VER = 1.04
FONTFORGE = /usr/bin/fontforge

SRCDIRS = $(shell find -type d | grep -v .git)
BINDIRS = $(shell find -type d | grep -v .git | grep -v src)
SRCFILES = $(shell find -type f | grep -v .git)
SFDFILES = $(shell ls ./src/*.sfd)
TTFFILES = $(shell ls ./build/*.ttf)
BINDOCS = AUTHORS ChangeLog COPYING License.txt README 

all: dist


build-ttf:
	$(foreach sfdfile, $(SFDFILES), $(FONTFORGE) -script ./scripts/sfd2ttf.pe $(sfdfile);)
	mkdir -p build && mv ./src/*.ttf ./build/


dist: clean build-ttf
	mkdir -p ../liberation-fonts_build/liberation-fonts
	cp $(TTFFILES) $(BINDOCS) ../liberation-fonts_build/liberation-fonts/
	mkdir -p ../liberation-fonts_tar
	cd ../liberation-fonts_build && tar czvf \
	  ../liberation-fonts_tar/liberation-fonts-$(VER).tar.gz \
	  liberation-fonts/

src: clean
	mkdir -p ../liberation-fonts_build/liberation-fonts
	$(foreach tardir, $(SRCDIRS), mkdir -p ../liberation-fonts_build/liberation-fonts/$(tardir);)
	$(foreach srcfile, $(SRCFILES), cp $(srcfile) ../liberation-fonts_build/liberation-fonts/$(shell dirname $(srcfile))/;)
	mkdir -p ../liberation-fonts_tar
	cd ../liberation-fonts_build && tar czvf \
	  ../liberation-fonts_tar/liberation-fonts-$(VER).src.tar.gz \
	  liberation-fonts/


clean:
	rm -rf build
	rm -rf ../liberation-fonts_build
	rm -rf ../liberation-fonts_tar
