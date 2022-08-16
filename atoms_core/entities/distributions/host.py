from atoms_core.entities.distribution import AtomDistribution


class Host(AtomDistribution):
    def __init__(self):
        super().__init__(
            distribution_id="host",
            name="Host distribution",
            logo="pm.mirko.Atoms-symbolic",
            releases=[],
            remote_structure="",
            remote_hash_structure="",
            remote_hash_type="",
            architectures={},
            root="",
            container_image_name=""
        )
