from atoms_core.entities.distribution import AtomDistribution


class VoidLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="voidlinux",
            name="Void Linux",
            logo="void-linux-symbolic",
            releases=["20220818_17:11", ],
            remote_structure="https://uk.lxd.images.canonical.com/images/voidlinux/current/{1}/default/{0}/rootfs.tar.xz",
            remote_hash_structure="https://uk.lxd.images.canonical.com/images/voidlinux/current/{1}/default/{0}/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="voidlinux",
        )
