import os

from atoms_core.entities.distribution import AtomDistribution


class Ubuntu(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="ubuntu",
            name="Ubuntu",
            logo="ubuntu-symbolic",
            releases=["jammy-20220818_07:42", "1kinetic-20220818_07:43"],
            remote_structure="https://uk.lxd.images.canonical.com/images/ubuntu/{0}/{1}/default/{2}/rootfs.tar.xz",
            remote_hash_structure="https://uk.lxd.images.canonical.com/images/ubuntu/{0}/{1}/default/{2}/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="ubuntu",
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
            f.write("APT::Sandbox::User \"root\";")
