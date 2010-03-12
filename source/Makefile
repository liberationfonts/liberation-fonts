VER = 1.05.2.$(shell date +%Y%m%d)
FONTFORGE = fontforge

TMPDIR := $(shell mktemp -d)
SFDFILES := src/LiberationMono-Bold.sfd src/LiberationMono-BoldItalic.sfd src/LiberationMono-Italic.sfd src/LiberationMono-Regular.sfd src/LiberationSans-Bold.sfd src/LiberationSans-BoldItalic.sfd src/LiberationSans-Italic.sfd src/LiberationSans-Regular.sfd src/LiberationSerif-Bold.sfd src/LiberationSerif-BoldItalic.sfd src/LiberationSerif-Italic.sfd src/LiberationSerif-Regular.sfd 
SCRIPTS := scripts/sfd2ttf.pe scripts/ttf2sfd.pe
MISCFILES := AUTHORS ChangeLog COPYING License.txt README

all: build

build:
	$(foreach sfdfile, $(SFDFILES), $(FONTFORGE) -script ./scripts/sfd2ttf.pe $(sfdfile);)
	mkdir -p ttf
	mv src/*.ttf ttf/	

dist: dist-sfd

dist-src: dist-sfd

dist-sfd:
	mkdir -p $(TMPDIR)/liberation-fonts-$(VER)/{src,scripts}
	cp Makefile $(MISCFILES) $(TMPDIR)/liberation-fonts-$(VER)/
	cp $(SFDFILES) $(TMPDIR)/liberation-fonts-$(VER)/src/
	cp $(SCRIPTS) $(TMPDIR)/liberation-fonts-$(VER)/scripts/
	tar Cczvf $(TMPDIR)/ liberation-fonts-$(VER).tar.gz \
	  liberation-fonts-$(VER)/

dist-ttf: clean-ttf build
	tar czvf liberation-fonts-ttf-$(VER).tar.gz ttf/*.ttf $(MISCFILES)
	zip -j liberation-fonts-ttf-$(VER).zip ttf/*.ttf $(MISCFILES)

clean: clean-ttf clean-src

clean-ttf:
	rm -rf ttf liberation-fonts-ttf-*

clean-src:
	rm -f *.tar.gz
