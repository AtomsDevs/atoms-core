import os

from atoms_core.entities.distribution import AtomDistribution


class Ubuntu(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="ubuntu",
            name="Ubuntu",
            logo="ubuntu-symbolic",
            releases=["22.04", "20.04"],
            remote_structure="http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/release/ubuntu-base-{0}-base-{1}.tar.gz",
            remote_hash_structure="http://cdimage.ubuntu.com/ubuntu-base/releases/{0}/release/SHA256SUMS",
            remote_hash_type="sha256",
            architectures={"x86_64": "amd64"},
            root="",
            container_image_name="ubuntu"
        )

    def get_remote_hash(self, _, release: str) -> str:
        return self.remote_hash_structure.format(release)

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
