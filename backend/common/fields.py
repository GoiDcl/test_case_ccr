from imagekit.models import ImageSpecField


class JpegImageSpecField(ImageSpecField):
    def __init__(
        self,
        processors=None,
        source=None,
        cachefile_storage=None,
        autoconvert=None,
        cachefile_backend=None,
        cachefile_strategy=None,
        spec=None,
        id=None,
    ):
        super().__init__(
            processors,
            'JPEG',
            {'progressive': True, 'quality': 90},
            source,
            cachefile_storage,
            autoconvert,
            cachefile_backend,
            cachefile_strategy,
            spec,
            id,
        )