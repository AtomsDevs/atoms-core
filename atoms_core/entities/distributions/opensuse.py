from atoms_core.entities.distribution import AtomDistribution
from atoms_core.entities.distributions.helpers.rpm import RpmDistribution
from atoms_core.entities.distributions.helpers.common import CommonDistribution


class OpenSuse(AtomDistribution, RpmDistribution, CommonDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="opensuse",
            name="OpenSUSE",
            logo="opensuse-symbolic",
            releases=["Leap_15.1"],
            remote_structure="https://download.opensuse.org/repositories/Cloud:/Images:/{0}/images/openSUSE-{2}-OpenStack-rootfs.{1}.tar.xz",
            remote_hash_structure="https://download.opensuse.org/repositories/Cloud:/Images:/{0}/images/openSUSE-{2}-OpenStack-rootfs.{1}.tar.xz.sha256",
            remote_hash_type="sha256",
            architectures={"x86_64": "x86_64"},
            root="",
            container_image_name="opensuse",
            default_cmd=["bash", "--login"],
            motd=self._rpm_motd("OpenSUSE"),
        )

    def get_remote(self, architecture: str, release: str) -> str:
        return self.remote_structure.format(
            release,
            architecture,
            release.replace("_", "-")
        )

    def get_remote_hash(self, architecture: str, release: str) -> str:
        return self.remote_hash_structure.format(
            release,
            architecture,
            release.replace("_", "-")
        )

    def post_unpack(self, chroot: str):
        # workaround Code:RPM_UNPK_NO_PERM
        self.set_macros(chroot)

        # share/fake current user
        self.set_current_user(chroot)
