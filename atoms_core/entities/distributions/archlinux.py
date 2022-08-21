from atoms_core.entities.distribution import AtomDistribution


class ArchLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="archlinux", 
            name="Arch Linux",
            logo="arch-linux-symbolic",
            releases=["2022.08.05",],
            remote_structure="https://archive.archlinux.org/iso/{0}/archlinux-bootstrap-{0}-{1}.tar.gz",
            remote_hash_structure="https://archive.archlinux.org/iso/{0}/sha256sums.txt",
            remote_hash_type="sha256",
            architectures={"x86_64": "x86_64"},
            root="root.x86_64",
            container_image_name="archlinux",
            motd="""
============================================================
Welcome to the Arch Linux Atom Chroot!
============================================================
Some notes from the image maintainer(s):
Pacman is currently broken due to a bug in glibc. We are 
looking into a solution.

Report bugs in the Atoms repository.
Good luck!
""")
