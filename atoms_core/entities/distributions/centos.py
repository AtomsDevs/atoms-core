from atoms_core.entities.distribution import AtomDistribution
from atoms_core.entities.distributions.helpers.rpm import RpmDistribution


class Centos(AtomDistribution, RpmDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="centos",
            name="Centos",
            logo="centos-symbolic",
            releases=["9-Stream", ],
            remote_structure=None,
            remote_hash_structure=None,
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="centos",
            default_cmd=["bash", "--login"],
            motd=self._rpm_motd("AlmaLinux")
        )

    def __get_base_path(self, architecture: str, release: str) -> str:
        base_url = "https://uk.lxd.images.canonical.com/images/centos/{release}/{architecture}/default".format(
            release=release, architecture=architecture
        )
        build = self._get_latest_remote_dir(base_url)
        return "{0}/{1}".format(base_url, build)
        
    def get_remote(self, architecture: str, release: str) -> str:
        return "{0}/rootfs.tar.xz".format(self.__get_base_path(architecture, release))
            
    def get_remote_hash(self, architecture: str, release: str) -> str:
        return "{0}/SHA256SUMS".format(self.__get_base_path(architecture, release))
