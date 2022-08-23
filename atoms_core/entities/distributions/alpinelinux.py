from atoms_core.entities.distribution import AtomDistribution


class AlpineLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="alpinelinux",
            name="Alpine Linux",
            logo="alpine-linux-symbolic",
            releases=["3.16.1", "3.16.0"],
            remote_structure="https://dl-cdn.alpinelinux.org/alpine/v{0}/releases/{1}/alpine-minirootfs-{2}-{1}.tar.gz",
            remote_hash_structure="https://dl-cdn.alpinelinux.org/alpine/v{0}/releases/{1}/alpine-minirootfs-{2}-{1}.tar.gz.sha256",
            remote_hash_type="sha256",
            architectures={"x86_64": "x86_64"},
            root="",
            container_image_name="alpine",
            default_cmd=["ash", "--login"],
            motd="""
============================================================
Welcome to the Alpine Linux Atom Chroot!
============================================================
Some notes from the image maintainer(s):
GUI apps are not supported due to musl not loading the required
librares. We are looking into a solution.

Report bugs in the Atoms repository.
Good luck!
""")

    def get_remote(self, architecture: str, release: str) -> str:
        return self.remote_structure.format(
            # only take major and minor version
            '.'.join(release.split('.')[:2]),
            architecture,
            release
        )

    def get_remote_hash(self, architecture: str, release: str) -> str:
        return self.remote_hash_structure.format(
            # only take major and minor version
            '.'.join(release.split('.')[:2]),
            architecture,
            release
        )
