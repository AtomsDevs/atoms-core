class RpmDistribution:

    @staticmethod
    def _rpm_motd(distro: str):
        return """
============================================================
Welcome to the %s Atom Chroot!
============================================================
Some notes from the image maintainer(s):
We are aware of a problem installing some RPM packages that 
fail to extract. We are looking for a solution.

Report bugs in the Atoms repository.
Good luck!
""" % distro
