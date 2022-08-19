from atoms_core.entities.distribution import AtomDistribution


class Gentoo(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="gentoo",
            name="Gentoo",
            logo="gentoo-symbolic",
            releases=["20220818_16:07", ],
            remote_structure="https://uk.lxd.images.canonical.com/images/gentoo/current/{1}/systemd/{0}/rootfs.tar.xz",
            remote_hash_structure="https://uk.lxd.images.canonical.com/images/gentoo/current/{1}/systemd/{0}/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="gentoo",
        )
