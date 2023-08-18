from atoms_core.entities.distribution import AtomDistribution
from atoms_core.entities.distributions.helpers.common import CommonDistribution


class VanillaOS(AtomDistribution, CommonDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="vanilla",
            name="Vanilla OS",
            logo="vanilla-symbolic",
            releases=["pico"],
            remote_structure=None,
            remote_hash_structure=None,
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="orchid",
            default_cmd=["bash", "--login"],
        )

    def __get_base_path(self, architecture: str, release: str) -> str:
        return "https://github.com/Vanilla-OS/pico-image/releases/download/continuous"

    def get_remote(self, architecture: str, release: str) -> str:
        return "{0}/vanilla-pico.tar.gz".format(
            self.__get_base_path(architecture, release)
        )

    def get_remote_hash(self, architecture: str, release: str) -> str:
        return "{0}/SHA256SUMS".format(self.__get_base_path(architecture, release))

    def post_unpack(self, chroot: str):
        # share/fake current user
        self.set_current_user(chroot)
