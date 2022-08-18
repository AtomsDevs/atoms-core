from atoms_core.entities.distribution import AtomDistribution


class AlmaLinux(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="almalinux",
            name="AlmaLinux",
            logo="almalinux-symbolic",
            releases=["9-20220817_23:08", ],
            remote_structure="https://uk.lxd.images.canonical.com/images/almalinux/{0}/{1}/default/{2}/rootfs.tar.xz",
            remote_hash_structure="https://uk.lxd.images.canonical.com/images/almalinux/{0}/{1}/default/{2}/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="almalinux",
        )

    def get_remote(self, architecture: str, release: str) -> str:
        # split release into version and build date
        release, build_date = release.split('-')
        return self.remote_structure.format(
            release,
            architecture,
            build_date
        )

    def get_remote_hash(self, architecture: str, release: str) -> str:
        # split release into version and build date
        release, build_date = release.split('-')
        return self.remote_hash_structure.format(
            release,
            architecture,
            build_date
        )
