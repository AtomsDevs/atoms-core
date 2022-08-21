import os

from atoms_core.entities.distribution import AtomDistribution


class Ubuntu(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="ubuntu",
            name="Ubuntu",
            logo="ubuntu-symbolic",
            releases=["jammy"],
            remote_structure=None,
            remote_hash_structure=None,
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="ubuntu"
        )

    def __get_base_path(self, architecture: str, release: str) -> str:
        base_url = "https://uk.lxd.images.canonical.com/images/ubuntu/{release}/{architecture}/default".format(
            release=release, architecture=architecture
        )
        build = self._get_latest_remote_dir(base_url)
        return "{0}/{1}".format(base_url, build)
        
    def get_remote(self, architecture: str, release: str) -> str:
        return "{0}/rootfs.tar.xz".format(self.__get_base_path(architecture, release))
            
    def get_remote_hash(self, architecture: str, release: str) -> str:
        return "{0}/SHA256SUMS".format(self.__get_base_path(architecture, release))

    def post_unpack(self, chroot):
        # workaround Code:APT_UNTRUSTED_KEYS
        with open(os.path.join(chroot, "etc/apt/sources.list"), "r") as f:
            sources = f.read()
            sources = sources.replace("deb ", "deb [trusted=yes] ")
            sources = sources.replace("deb-src ", "deb-src [trusted=yes] ")
            with open(os.path.join(chroot, "etc/apt/sources.list"), "w") as f:
                f.write(sources)

        # workaround Code:NO_APT_CHWN_PERM
        with open(os.path.join(chroot, "etc/apt/apt.conf.d/01atom"), "w") as f:
            f.write("APT::Sandbox \"0\";")
            f.write("APT::Sandbox::User \"root\";")
