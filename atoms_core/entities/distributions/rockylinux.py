from atoms_core.entities.distribution import AtomDistribution
from atoms_core.entities.distributions.helpers.rpm import RpmDistribution


class RockyLinux(AtomDistribution, RpmDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="rockylinux",
            name="Rocky Linux",
            logo="rockylinux-symbolic",
            releases=["9.0.20220720"],
            remote_structure="https://raw.githubusercontent.com/rocky-linux/sig-cloud-instance-images/Rocky-{0}-Base-{1}/layer.tar.xz",
            remote_hash_structure=None,
            remote_hash_type=None,
            architectures={"x86_64": "x86_64"},
            root="",
            container_image_name="rockylinux",
            default_cmd=["bash", "--login"],
            motd=self._rpm_motd("Rocky Linux")
        )
