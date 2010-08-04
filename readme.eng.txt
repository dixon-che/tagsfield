# TagsField for Django


## WHAT IS IT

TagsField -- is a small app for [Django](http://www.djangoproject.com/),
that implements tagging for arbitrary objects in your applications with
a form control for editing tags.

The application contains:

- Tag model representing tag's value (a word) without any additional fields.
  It can be extended as you like.
- New field class TagsField which is basically a standard ManyToManyField
  extended to support its own form widget.
- Form widget for editing tags with an autocomplete


## FEATURES

This things will likely influence your decision of using or not using TagsField:

- Tags creation is entirely 'user-managed' meaning that when a user adds a tag
that does not exist it is created automatically.

- Autocomplete doesn't use ajax and all tags are loaded along with a page. Thus
this thing may be not useful for systems with many tags.

- Autocomplete is case insensitive and also ignores insignificant differences
  in spelling (ignores punctuation, whitespace and the word "the")

- Tags are not categorized. If you use tags for different types of objects then
initial tags for them will be the same.


## INSTALLATION AND USAGE

1.  Put 'tagsfield' directory somewhere on Python path

2.  Include 'tagsfield' in INSTALLED_APPS

3.  Install necessary db tables using ./manage.py syncdb

4.  Copy (or link) 'media' directory under your MEDIA_ROOT, where it can be accessed
    over HTTP under MEDIA_URL.

Then you can use tags in your models:

    from tagsfield.models import Tag
    from tagsfield import fields

    class Article(models.Model):
        ...
        tags = fields.TagsField(Tag)

Now you can use the field "tags" the same as the default ManyToManyField. The
only difference is that in forms created for the model tags will be displayed as a
set of autocomplete widgets (see. included demo.html). In order for these widgets
to actually work you should include on the page necessary scripts and styles:

    <head>
    ...
    {{ form.media }}
    ...
    </head>

The field will also work in admin and for this you don't need to manually include
media on a page since admin already does it for you.

Tags are usually stored in the library's built-in Tag model. They are
used for auto-completion in forms. You can use your own models instead but make
sure that it meets the following requirements:

- contains the field 'value' — displayed tag text
- contains the field 'norm_value' — normalized text by which tags are searched
- all other fields should either be nullable or have default values in order to
  be able to create tag object knowing only a value


## SETTINGS

There's one optional setting:

`TAGS_URL`
: URL to the "tag's page" on your site (if you plan to have one). Usually
  it shows a list of objects that are linked to a certain tag. The setting
  should be in the form of 'http://domain/path/%s/' where %s is replaced with
  tag's value.
  If not set then tags are displayed without links at all.


## ABOUT

Version: 2.3
URL:    http://softwaremaniacs.org/soft/tagsfield/en/
Author:  Ivan Sagalaev (Maniac@SoftwareManiacs.Org)

For license terms see LICENSE files (in short, it's BSD).
