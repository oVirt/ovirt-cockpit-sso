.PHONY: installdeps srpm

installdeps:
	dnf -y install make

# explicity mark the copr generated git repo directory (which is done prior to the mock
# call to the make_srpm and will be the current pwd) as safe for git commands
git-safe:
	git config --global --add safe.directory "$(shell pwd)"

srpm: installdeps git-safe
	make srpm
	cp tmp.repos/SRPMS/*.src.rpm $(outdir)
