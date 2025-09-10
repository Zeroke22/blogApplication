from django.contrib.sitemaps import Sitemap
from django.db.models import Exists, OuterRef, Max
from .models import Post
from django.urls import reverse
from taggit.models import Tag


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated

class TagSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        # Only include tags that have at least one *published* post
        published = Post.published.all()
        return (
            Tag.objects
            .annotate(has_posts=Exists(
                published.filter(tags__id=OuterRef('id'))
            ))
            .filter(has_posts=True)
        )

    def location(self, tag):
        # Uses your URL: path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag')
        return reverse('blog:post_list_by_tag', args=[tag.slug])

    def lastmod(self, tag):
        # Last modified = latest 'updated' among published posts with this tag
        return (
            Post.published
                .filter(tags__slug=tag.slug)
                .aggregate(last=Max('updated'))['last']
        )