from atoms_core.entities.distribution import AtomDistribution


class ArchLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="archlinux",
            name="Arch Linux",
            logo="arch-linux-symbolic",
            releases=["20220818_04:20", ],
            remote_structure="https://uk.lxd.images.canonical.com/images/archlinux/current/{1}/default/{0}/rootfs.tar.xz",
            remote_hash_structure="https://uk.lxd.images.canonical.com/images/archlinux/current/{1}/default/{0}/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="archlinux",
        )
