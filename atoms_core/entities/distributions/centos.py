from atoms_core.entities.distribution import AtomDistribution


class Centos(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="centos",
            name="Centos",
            logo="centos-symbolic",
            releases=["9-20220818_07:09", ],
            remote_structure="https://uk.lxd.images.canonical.com/images/centos/{0}-Stream/{1}/default/{2}/rootfs.tar.xz",
            remote_hash_structure="https://uk.lxd.images.canonical.com/images/centos/{0}-Stream/{1}/default/{2}/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="centos",
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
