VER = 1.07.2
#VER = 1.06.0.$(shell date +%Y%m%d)
FONTFORGE = fontforge

TMPDIR := $(shell mktemp -d)
SFDFILES := src/LiberationMono-Bold.sfd src/LiberationMono-BoldItalic.sfd src/LiberationMono-Italic.sfd src/LiberationMono-Regular.sfd src/LiberationSans-Bold.sfd src/LiberationSans-BoldItalic.sfd src/LiberationSans-Italic.sfd src/LiberationSans-Regular.sfd src/LiberationSerif-Bold.sfd src/LiberationSerif-BoldItalic.sfd src/LiberationSerif-Italic.sfd src/LiberationSerif-Regular.sfd src/LiberationSansNarrow-Regular.sfd src/LiberationSansNarrow-Bold.sfd src/LiberationSansNarrow-Italic.sfd src/LiberationSansNarrow-BoldItalic.sfd
SCRIPTS := scripts/sfd2ttf.pe scripts/ttf2sfd.pe
MISCFILES := AUTHORS ChangeLog COPYING License.txt README TODO

all: build

build:
	$(foreach sfdfile, $(SFDFILES), $(FONTFORGE) -script ./scripts/sfd2ttf.pe $(sfdfile);)
	mkdir -p liberation-fonts-ttf-$(VER)/
	mv src/*.ttf liberation-fonts-ttf-$(VER)/

dist: dist-sfd dist-ttf

dist-src: dist-sfd

dist-sfd:
	mkdir -p $(TMPDIR)/liberation-fonts-$(VER)/{src,scripts}
	cp ../README ./
	cp Makefile $(MISCFILES) $(TMPDIR)/liberation-fonts-$(VER)/
	cp $(SFDFILES) $(TMPDIR)/liberation-fonts-$(VER)/src/
	cp $(SCRIPTS) $(TMPDIR)/liberation-fonts-$(VER)/scripts/
	tar Cczvf $(TMPDIR)/ liberation-fonts-$(VER).tar.gz \
	  liberation-fonts-$(VER)/

dist-ttf: clean-ttf build
	cp $(MISCFILES) liberation-fonts-ttf-$(VER)/
	tar czvf liberation-fonts-ttf-$(VER).tar.gz liberation-fonts-ttf-$(VER)/
#	zip -j liberation-fonts-ttf-$(VER).zip liberation-fonts-ttf-$(VER)/*
	rm -rf liberation-fonts-ttf-$(VER)
clean: clean-ttf clean-src

clean-ttf:
	rm -rf ttf liberation-fonts-*

clean-src:
	rm -f *.tar.gz
