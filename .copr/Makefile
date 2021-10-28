.PHONY: installdeps srpm

installdeps:
	dnf -y install make

srpm: installdeps
	make srpm
	cp tmp.repos/SRPMS/*.src.rpm $(outdir)
