from atoms_core.entities.distribution import AtomDistribution


class VoidLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="voidlinux",
            name="Void Linux",
            logo="void-linux-symbolic",
            releases=["20210930", ],
            remote_structure="https://repo-default.voidlinux.org/live/{0}/void-{1}-ROOTFS-{0}.tar.xz",
            remote_hash_structure=None,# TODO: support custom struct: https://repo-default.voidlinux.org/live/20210930/sha256sum.txt
            remote_hash_type=None,
            architectures={"x86_64": "x86_64"},
            root="",
            container_image_name="voidlinux",
        )
