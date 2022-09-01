import os


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

To help us debug this, please use the dnf command with the
"--rpmverbose debug" option.

Report bugs in the Atoms repository.
Good luck!
""" % distro

    @staticmethod
    def set_macros(chroot: str):
        macros_path = os.path.join(chroot, "usr/lib/rpm/macros.d")
        macros = [
            "/dev",
            "/media",
            "/mnt",
            "/proc",
            "/sys",
            "/tmp",
            "/var/lib",
            "/var/log",
        ]

        if not os.path.exists(macros_path):
            os.makedirs(macros_path)

        with open(os.path.join(macros_path, "macros.atoms"), "w") as f:
            f.write("%%_netsharedpath %s" % ":".join(macros))
