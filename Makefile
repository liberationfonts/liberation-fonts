VER = 1.04
FONTFORGE = /usr/bin/fontforge

SRCDIRS = $(shell find -type d | grep -v .git)
BINDIRS = $(shell find -type d | grep -v .git | grep -v src)
SRCFILES = $(shell find -type f | grep -v .git)
SFDFILES = $(shell ls ./src/*.sfd)
TTFFILES = $(shell ls ./build/ttf/*.ttf)
BINDOCS = AUTHORS ChangeLog COPYING License.txt README 

all: dist


ttf:
	$(foreach sfdfile, $(SFDFILES), $(FONTFORGE) -script ./scripts/sfd2ttf.pe $(sfdfile);)
	mkdir -p build/ttf && mv ./src/*.ttf ./build/ttf/


sfd:
	$(foreach ttffile, $(TTFFILES), $(FONTFORGE) -script ./scripts/ttf2sfd.pe $(ttffile);)
	mkdir -p build/sfd && mv ./build/ttf/*.sfd ./build/sfd/


dist: clean-build ttf
	mkdir -p ../liberation-fonts_build/liberation-fonts
	cp $(TTFFILES) $(BINDOCS) ../liberation-fonts_build/liberation-fonts/
	mkdir -p ../liberation-fonts_tar
	cd ../liberation-fonts_build && tar czvf \
	  ../liberation-fonts_tar/liberation-fonts-$(VER).tar.gz \
	  liberation-fonts/

src: clean-build
	mkdir -p ../liberation-fonts_build/liberation-fonts
	$(foreach tardir, $(SRCDIRS), mkdir -p ../liberation-fonts_build/liberation-fonts/$(tardir);)
	$(foreach srcfile, $(SRCFILES), cp $(srcfile) ../liberation-fonts_build/liberation-fonts/$(shell dirname $(srcfile))/;)
	mkdir -p ../liberation-fonts_tar
	cd ../liberation-fonts_build && tar czvf \
	  ../liberation-fonts_tar/liberation-fonts-$(VER).src.tar.gz \
	  liberation-fonts/


clean: clean-build
	rm -rf ../liberation-fonts_tar

clean-build:
	rm -rf build
	rm -rf ../liberation-fonts_build
