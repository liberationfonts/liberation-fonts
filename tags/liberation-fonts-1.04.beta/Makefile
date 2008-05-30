VER = 1.04
FONTFORGE = /usr/bin/env fontforge

SRCDIRS = $(shell find -type d | grep -v .git)
BINDIRS = $(shell find -type d | grep -v .git | grep -v src)
SRCFILES = $(shell find -type f | grep -v .git)
SFDFILES = $(shell ls ./src/*.sfd)
TTFFILES = $(shell ls ./build-area/ttf/*.ttf)
BINDOCS = AUTHORS ChangeLog COPYING License.txt README 

all: dist


build:
	$(foreach sfdfile, $(SFDFILES), $(FONTFORGE) -script ./scripts/sfd2ttf.pe $(sfdfile);)
	mkdir -p build-area/ttf && mv ./src/*.ttf ./build-area/ttf/


sfd:
	$(foreach ttffile, $(TTFFILES), $(FONTFORGE) -script ./scripts/ttf2sfd.pe $(ttffile);)
	mkdir -p build-area/sfd && mv ./build-area/ttf/*.sfd ./build-area/sfd/


dist: clean-build build
	mkdir -p build-area/liberation-fonts-$(VER)
	cp $(TTFFILES) $(BINDOCS) build-area/liberation-fonts-$(VER)
	mkdir -p dist
	cd build-area && tar czvf  ../dist/liberation-fonts-$(VER).tar.gz  liberation-fonts-$(VER)/

src: clean-build
	mkdir -p build-area/liberation-fonts-$(VER)
	$(foreach tardir, $(SRCDIRS), mkdir -p build-area/liberation-fonts/liberation-fonts-$(VER)/$(tardir);)
	$(foreach srcfile, $(SRCFILES), cp $(srcfile) build-area/liberation-fonts/liberation-fonts-$(VER)/$(shell dirname $(srcfile))/;)
	mkdir -p dist
	cd build-area && tar czvf \
	  ../dist/liberation-fonts-$(VER).src.tar.gz \
	  liberation-fonts-$(VER)/


clean: clean-build
	rm -rf dist

clean-build:
	rm -rf build-area
