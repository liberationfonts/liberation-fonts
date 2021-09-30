# common targets:
# <no target>, build, ttf-dir: create dedicated dir with TTF files
# ttf:                         create export dir with TTF files, track changes
# 4web:                        dtto for TTF, WOFF, SVG, and EOT

FONTFORGE    = fontforge
PYTHON       = python3
FONTLINT     = fontlint

# TTF->EOT converters in fallback order
# the first one is canonical choice used in the release process
MKEOT        = mkeot
# URLs to be used for root string within EOT file;
# defaults to "libre roots" that allow usage on any common web page
MKEOT_URLS   = http:// https:// file://
TTF2EOT      = ttf2eot
ifneq ($(strip $(shell which $(MKEOT) 2>/dev/null)),)
    make_eot = $(MKEOT) $(1) $(MKEOT_URLS) > $(2)
else
    ifneq ($(strip $(shell which $(TTF2EOT) 2>/dev/null)),)
        make_eot = $(TTF2EOT) $(1) > $(2)
    else
        make_eot = $(error No tool for TTF->EOT conversion: $(MKEOT), $(TTF2EOT))
    endif
endif

EXPORTSCRIPT = scripts/fontexport.pe
FONTTOOLSCRIPT = scripts/setisFixedPitch-fonttools.py
FONTVERSION_UPDATE_SCRIPT = scripts/fontfile_version_update.py
SCRIPTS      = $(EXPORTSCRIPT) scripts/sfd2ttf.pe scripts/ttf2sfd.pe
MISCFILES    = AUTHORS ChangeLog LICENSE README.md TODO
SRCDIR       = src
EXPORTDIR    = export
CHECK_PREFIX = check

VER          = 2.1.5
NAME         = Liberation
VARIANTS     = \
    Mono-Regular       Mono-Bold        Mono-Italic       Mono-BoldItalic       \
    Sans-Regular       Sans-Bold        Sans-Italic       Sans-BoldItalic       \
    Serif-Regular      Serif-Bold       Serif-Italic      Serif-BoldItalic      

DISTPREFIX     := liberation-fonts-$(VER)
DISTPREFIX_TTF := liberation-fonts-ttf-$(VER)
SFDFILES       := $(addprefix $(SRCDIR)/$(NAME),    $(VARIANTS:=.sfd))
TTFFILES       := $(addprefix $(EXPORTDIR)/$(NAME), $(VARIANTS:=.ttf))

# keeping backward compatibility for "build"
all build: ttf-dir

versionupdate:
	$(PYTHON) $(FONTVERSION_UPDATE_SCRIPT) $(SRCDIR) $(VER)

$(EXPORTDIR):
	mkdir -p $@

# TrueType/OpenType Font, general usage
# - ttf cares about source file changes, using shared EXPORTDIR
# - ttf-dir should be a bit more efficient, creating dedicated dir for TTF
FORMATS = ttf
ttf-dir:: $(SFDFILES)
	$(FONTFORGE) -script $(EXPORTSCRIPT) -ttf $^
	$(PYTHON) $(FONTTOOLSCRIPT) src/LiberationMono-*.ttf
	mv  src/LiberationMono-Regular-fixed.ttf  src/LiberationMono-Regular.ttf
	mv  src/LiberationMono-Italic-fixed.ttf  src/LiberationMono-Italic.ttf
	mv  src/LiberationMono-Bold-fixed.ttf  src/LiberationMono-Bold.ttf
	mv  src/LiberationMono-BoldItalic-fixed.ttf  src/LiberationMono-BoldItalic.ttf
	mkdir -p $(DISTPREFIX_TTF)
	mv $(addsuffix .ttf,$(basename $^)) $(DISTPREFIX_TTF)

# web sites usage
# Web Open Font Format (WOFF); for all modern browsers (W3C recommendation)
FORMATS += woff
# SVG Font; only for WebKit and Presto based browsers (Firefox "avoids" it)
FORMATS += svg
# Embedded OpenType (EOT); MSIE only [extra recipe, FontForge can't create EOT]
FORMATS += eot
eot:: $(addprefix $(EXPORTDIR)/$(NAME), $(VARIANTS:=.eot))
	@echo
$(EXPORTDIR)/%.eot: $(EXPORTDIR)/%.ttf | $(EXPORTDIR)
	$(call make_eot,$<,$@)
4web: ttf woff svg eot

# XXX: declare other formats here if needed (TeX, etc.)

# default for formats without extra recipes defined above (e.g., not "eot"):
# summary per-format target + single file export for these declared formats
define FORMAT_template =
$(1):: $$(addprefix $$(EXPORTDIR)/$$(NAME), $$(VARIANTS:=.$(1)))
	@echo
$$(EXPORTDIR)/%.$(1):: $$(SRCDIR)/%.sfd | $$(EXPORTDIR)
	$$(FONTFORGE) -script $$(EXPORTSCRIPT) -$$(lastword $$(subst ., ,$$@)) $$< 2>/dev/null
	mv $$(SRCDIR)/$$(notdir $$@) $$(EXPORTDIR)
endef
$(foreach format,$(FORMATS),$(eval $(call FORMAT_template,$(format))))

dist: clean-dist dist-sfd dist-ttf
dist-src: dist-sfd

dist-sfd:: $(SFDFILES)
	tempdir=$$(mktemp -d) \
	  && mkdir -p $${tempdir}/$(DISTPREFIX)/{src,scripts} \
	  && cp Makefile $(MISCFILES) $${tempdir}/$(DISTPREFIX) \
	  && cp $(SFDFILES) $${tempdir}/$(DISTPREFIX)/src \
	  && cp $(SCRIPTS) $(FONTTOOLSCRIPT) $(FONTVERSION_UPDATE_SCRIPT) $${tempdir}/$(DISTPREFIX)/scripts \
	  && tar Cczvhf $${tempdir} $(DISTPREFIX).tar.gz $(DISTPREFIX) \
	  || echo 'Problem encountered ($@)'; rm -rf -- $${tempdir}
dist-ttf: ttf
	$(PYTHON) $(FONTTOOLSCRIPT) export/LiberationMono-*.ttf
	mv  export/LiberationMono-Regular-fixed.ttf  export/LiberationMono-Regular.ttf
	mv  export/LiberationMono-Italic-fixed.ttf  export/LiberationMono-Italic.ttf
	mv  export/LiberationMono-Bold-fixed.ttf  export/LiberationMono-Bold.ttf
	mv  export/LiberationMono-BoldItalic-fixed.ttf  export/LiberationMono-BoldItalic.ttf
	tempdir=$$(mktemp -d) \
	  && mkdir -p $${tempdir}/$(DISTPREFIX_TTF) \
	  && cp $(MISCFILES) $(TTFFILES) $${tempdir}/$(DISTPREFIX_TTF) \
	  && tar Cczvhf $${tempdir} $(DISTPREFIX_TTF).tar.gz $(DISTPREFIX_TTF) \
	  || echo 'Problem encountered ($@)'; rm -rf -- $${tempdir}
# substitute tar line with this if needed:
#	  && zip -j $(DISTPREFIX_TTF).zip $(MISCFILES) $(TTFFILES) \

check:
	log="$(CHECK_PREFIX)_$$(git describe --dirty --always 2>/dev/null||date +%Y%m%d)" \
	  && for sfd in $(SFDFILES); do \
	         $(FONTLINT) $${sfd} 2>/dev/null | tee -a $${log}; echo; \
	     done

clean: clean-dist
	rm -rf -- $(DISTPREFIX)* $(DISTPREFIX_TTF)*
	rm -rf -- $(EXPORTDIR)
	rm -f -- $(CHECK_PREFIX)_*
	rm -f src/*.ttf 
clean-dist:
	rm -f -- *.tar.gz *.zip
	
install:
	mkdir -p $(DESTDIR)/usr/share/fonts/$(DISTPREFIX_TTF) || true
	install $(DISTPREFIX_TTF)/* $(DESTDIR)/usr/share/fonts/$(DISTPREFIX_TTF)

.PHONY: all build ttf-dir ttf dist dist-src dist-sfd dist-ttf 4web $(FORMATS) check clean clean-dist
