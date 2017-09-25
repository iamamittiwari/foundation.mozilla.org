from rest_framework import serializers
from urllib.parse import quote

from mezzanine.conf import settings
from networkapi.news.models import News


class NewsSerializer(serializers.ModelSerializer):

    glyph = serializers.SerializerMethodField()

    def get_glyph(self, instance):
        # Remote hosted? Return the remote URL
        if settings.USE_S3:
            return "{host}{glyph}".format(
                host=settings.MEDIA_URL,
                glyph=instance.glyph
            )

        # Stored on the local filesystem: return as an absolute URL
        request = self.context['request']

        return "{protocol}://{root}{url}{glyph}".format(
            protocol='https' if request.is_secure() else 'http',
            root=request.META['HTTP_HOST'],
            url=settings.MEDIA_URL,
            glyph=quote(str(instance.glyph))
        )

    """
    Serializes a News object
    """
    class Meta:
        model = News
        fields = (
            'headline',
            'outlet',
            'date',
            'link',
            'excerpt',
            'author',
            'glyph',
            'thumbnail',
            'is_video',
            'featured',
        )
