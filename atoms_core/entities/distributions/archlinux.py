import os

from atoms_core.entities.distribution import AtomDistribution


class ArchLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="archlinux", 
            name="Arch Linux",
            logo="arch-linux-symbolic",
            releases=["current",],
            remote_structure=None,
            remote_hash_structure=None,
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="archlinux",
            motd="""
============================================================
Welcome to the Arch Linux Atom Chroot!
============================================================
Some notes from the image maintainer(s):
glibc was downgraded to 2.35-2 to fix a compatibility issue
which broke Pacman.

Report bugs in the Atoms repository.
Good luck!
""" if "FLATPAK_ID" in os.environ else None)

    def __get_base_path(self, architecture: str, release: str) -> str:
        base_url = "https://uk.lxd.images.canonical.com/images/archlinux/{release}/{architecture}/default".format(
            release=release, architecture=architecture
        )
        build = self._get_latest_remote_dir(base_url)
        return "{0}/{1}".format(base_url, build)
        
    def get_remote(self, architecture: str, release: str) -> str:
        return "{0}/rootfs.tar.xz".format(self.__get_base_path(architecture, release))
            
    def get_remote_hash(self, architecture: str, release: str) -> str:
        return "{0}/SHA256SUMS".format(self.__get_base_path(architecture, release))

    def post_unpack(self, chroot: str):
        # workaround Code:FAIL_INIT_ALPM
        if "FLATPAK_ID" in os.environ:
            glibc = self._download_resource("https://repo.archlinuxcn.org/x86_64/glibc-linux4-2.35-2-x86_64.pkg.tar.zst")
            self._extract_resource(glibc, chroot)
            with open(os.path.join(chroot, "etc/pacman.conf"), "r") as f:
                lines = f.readlines()
            with open(os.path.join(chroot, "etc/pacman.conf"), "w") as f:
                for line in lines:
                    if "#IgnorePkg" in line:
                        f.write("IgnorePkg = glibc\n")
                        continue
                    f.write(line)
