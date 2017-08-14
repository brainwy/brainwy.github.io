'''
Created on Sep 3, 2013

@author: Fabio

Also in:
    http://liclipse-sagi.rhcloud.com
    http://brainwy.github.io
'''
import os
import pyodict
import shutil
import warnings

# On a new release, update the links and version.

DOWNLOADS = '''
http://www.mediafire.com/file/un3yr12rklvq2va/liclipse_4.1.0_linux.gtk.x86.tar.gz
http://www.mediafire.com/file/r8sib7aj4rkvsgv/liclipse_4.1.0_linux.gtk.x86_64.tar.gz
http://www.mediafire.com/file/kvif2uqx0qji0c0/liclipse_4.1.0_macosx.cocoa.x86_64.dmg
http://www.mediafire.com/file/orw7z5a6xr664qf/liclipse_4.1.0_win32.x86.exe
http://www.mediafire.com/file/iw7le56zl8km7xn/liclipse_4.1.0_win32.x86_64.exe
http://www.mediafire.com/file/8r0190h6wepbatq/SHA256_AND_INSTALL_INSTRUCTIONS.txt
http://www.mediafire.com/file/ylk2hzpga0fkob9/UPDATE_SITE_4.1.0.zip
http://www.mediafire.com/file/b1yct3qu0qw8964/LICENSE.TXT
https://www.mediafire.com/folder/wjozcwrpr9a4o/LiClipse_4.1.0
'''

DOWNLOAD_REPLACEMENTS = {
    'all_versions_url': 'https://www.mediafire.com/folder/ka5iei6qnyaq4/LiClipse',
    'liclipse_version': '4.1.0',
}

help_location = r'X:\liclipse\plugins\com.brainwy.liclipse.help'
if not os.path.exists(help_location):
    scripts = os.path.dirname(__file__)
    liclipse_page = os.path.dirname(scripts)
    workspace = os.path.dirname(liclipse_page)
    help_location = os.path.join(workspace, 'liclipse', 'plugins', 'com.brainwy.liclipse.help')

# Uncomment to skip the generation of the help.
# help_location = ''

#===================================================================================================
# copytree
#===================================================================================================
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)


default_template_contents = open(os.path.join(os.path.dirname(__file__), 'template.html'), 'r').read()
this_file_dir = os.path.dirname(__file__)
page_dir = os.path.dirname(this_file_dir)


HEADER = '''
<h1 class="header_liclipse">LiClipse</h1>
<p>Lightweight editors, theming and usability improvements for Eclipse</p>
<!-- <p class="view"><a href="https://github.com/brainwy/liclipse.page">
    View the Project on GitHub <small>brainwy/liclipse.page</small></a></p> -->
<ul class="top1">
    <!-- <li><a href="http://???">Get It <strong>Download</strong></a></li> -->
    <li><a href="contact.html">Get in <strong>Contact</strong></a></li>
    <li><a href="http://liclipse.blogspot.com.br/">View <strong>Blog</strong></a></li>
    <li><a href="https://www.brainwy.com/tracker/LiClipse/">LiClipse<strong>Tracker</strong></a></li>
</ul>
<ul class="top2">
    <li class="lifull"><a href="download.html">Get it<strong>Download</strong></a></li>
</ul>
<ul class="top3">
    <li class="lifull"><a href="buy.html">Help to make it better<strong>Buy</strong></a></li>
</ul>



<p><small>Copyright 2013-2017 - Brainwy Software Ltda.<br/>Theme by <a href="https://github.com/orderedlist/minimal">orderedlist</a></small></p>
'''

#===================================================================================================
# apply_to
#===================================================================================================
def apply_to(filename, header=None, path=None, template_contents=None, kwargs=None, replace_body=None):
    with open(filename, 'r') as stream:
        contents = stream.read()
    body = extract(contents, 'body')
    if replace_body:
        body = replace_body(body)
    apply_to_contents(
        contents, os.path.basename(filename), body, header or HEADER, path=path, template_contents=template_contents, kwargs=kwargs)

def template_replace(contents, kwargs):

    to_replace = set(['title', 'image_area', 'quote_area', 'right_area', 'contents_area', 'body', 'header'])
    to_replace.update(kwargs.keys())

    for r in to_replace:
        c = kwargs.get(r, '')
        contents = contents.replace('%(' + r + ')s', c)
    return contents

#===================================================================================================
# apply_to_contents
#===================================================================================================
def apply_to_contents(contents, basename, body, header, path=None, template_contents=None, kwargs=None):
    if kwargs is None:
        kwargs = {}
    kwargs.update({'body': body, 'header': header})

    contents = template_replace((template_contents or default_template_contents), kwargs)

    if path:
        filename = os.path.join(page_dir, path, basename)
    else:
        filename = os.path.join(page_dir, basename)
    with open(filename, 'w') as out_stream:
        out_stream.write(contents)


#===================================================================================================
# extract
#===================================================================================================
def extract(contents, tag):
    i = contents.index('<%s>' % tag)
    j = contents.rindex('</%s>' % tag)
    return contents[i + len(tag) + 2:j]


class Info:
    def __init__(self, title, open_source):
        self.title = title
        self.open_source = open_source
        self.title = title
        self.filename = None


FILE_TO_INFO = pyodict.odict([
    ('change_color_theme.html', Info('Changing colors', False)),
    ('launch.html', Info('Running/Launching', False)),
    ('search.html', Info('Improved Search', False)),
    ('supported_languages.html', Info('Language Support', True)),
    ('scope_definition.html', Info('Language Scopes', True)),
    ('ctags.html', Info('Ctags', True)),
    ('indent.html', Info('Specifying indentation', True)),
    ('templates.html', Info('Templates', True)),
    ('spell_checking.html', Info('Spell Checking', True)),
    ('customize_javascript.html', Info('JavaScript editor customization', False)),
    ('customize_html.html', Info('HTML editor customization', False)),
    ('customize_yaml.html', Info('YAML editor customization', False)),
    ('textmate_bundles.html', Info('TextMate Bundles integration', True)),
    ('preview.html', Info('HTML Preview', False)),
])


if os.path.exists(help_location):
    for f in os.listdir(help_location):
        if not f.endswith('.html'):
            continue
        if f not in FILE_TO_INFO:
            raise ValueError('Not expecting: %s' % (f,))
        FILE_TO_INFO[f].filename = os.path.join(help_location, f)
else:
    print('Dir: %s does not exist (unable to generate related pages)' % help_location)

#===================================================================================================
# create_manual_header
#===================================================================================================
def create_manual_header():
    lis = []
    open_source = []
    for file_basename, file_info in FILE_TO_INFO.iteritems():
        if not file_info.open_source:
            lis.append('<p><a href="%s">%s</a></p>' % (
                os.path.basename(file_info.filename),
                file_info.title
            ))
        else:
            open_source.append('<p><a href="%s">%s</a></p>' % (
                os.path.basename(file_info.filename),
                file_info.title
            ))

    open_source = '''
<h1>Manual</h1>
<br/>
Choose the topic you're interested in...<br/>
<br/>
<ul>
%(li)s
</ul>
<br><br><br>
''' % {'li': '\n'.join(open_source)}

    open_source += '<br/>' * 25

    return '''
%(li)s<br><br><br>
<p><small>Copyright 2013-2017 - Brainwy Software Ltda.<br/>Theme by <a href="https://github.com/orderedlist/minimal">orderedlist</a></small></p>
''' % {'li': '\n'.join(lis)}, open_source
MANUAL_OPEN_SOURCE_HEADER = None

if os.path.exists(help_location):
    MANUAL_NOT_OPEN_SOURCE_HEADER, MANUAL_OPEN_SOURCE_HEADER = create_manual_header()
else:
    warnings.warn('Not creating help. %s does not exist.' % (help_location,))



#===================================================================================================
# create_manual_page
#===================================================================================================
def create_manual_page():


    manual_body = '''
<h3>Choose the topic you're interested in...</h3>
Note: for the manual on the Open Source <a href="text/index.html">LiClipseText</a> component (which provides syntax highlighting and languages customization), visit the
<a href="text/manual.html">LiClipseText Manual</a>
'''
    apply_to_contents(manual_body, 'manual.html', manual_body, MANUAL_NOT_OPEN_SOURCE_HEADER, None, None)



#===================================================================================================
# main
#===================================================================================================
def main():
    with open(os.path.join(this_file_dir, 'text', '_template.html')) as stream:
        text_template_contents = stream.read()
    with open(os.path.join(this_file_dir, 'text', '_template_manual.html')) as stream:
        text_template_manual_contents = stream.read()

    # Manual
    if os.path.exists(help_location):
        create_manual_page()
        values = FILE_TO_INFO.values()
        open_source_values = [x for x in values if x.open_source]

        for i, info in enumerate(values):
            if not info.open_source:
                apply_to(info.filename, header=MANUAL_NOT_OPEN_SOURCE_HEADER)

        for i, info in enumerate(open_source_values):
            if i == 0:
                prev = 'manual.html'
                title_prev = 'Manual'

                next = os.path.basename(open_source_values[i+1].filename)
                title_next = open_source_values[i+1].title

            elif i == len(open_source_values)-1:
                prev = os.path.basename(open_source_values[i-1].filename)
                title_prev = open_source_values[i-1].title

                next = 'manual.html'
                title_next='Manual'
            else:
                prev = os.path.basename(open_source_values[i-1].filename)
                title_prev = open_source_values[i-1].title

                next = os.path.basename(open_source_values[i+1].filename)
                title_next = open_source_values[i+1].title

            print 'applying to:', info.filename
            title_next = title_next.replace('&nbsp;', '')
            title_prev = title_prev.replace('&nbsp;', '')
            title_next = '(%s)' % title_next
            title_prev = '(%s)' % title_prev
            def replace_body(body):
                return body.replace('src="./images', 'src="../images')
            apply_to(info.filename, path='text', template_contents=text_template_manual_contents, kwargs={
                'title': info.title, 'root': 'manual.html', 'prev':prev, 'next':next, 'title_prev': title_prev, 'title_next':title_next},
                     replace_body=replace_body)
            basename = os.path.basename(info.filename)
            apply_to_contents('', basename,'This file was moved to: <a href="text/%s">text/%s</a>' % (basename,basename), HEADER, )

    # Others
    for line in DOWNLOADS.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.endswith('SHA256_AND_INSTALL_INSTRUCTIONS.txt'):
            DOWNLOAD_REPLACEMENTS['sha256_and_install_instructions_url'] = line

        elif line.endswith('LICENSE.TXT'):
            DOWNLOAD_REPLACEMENTS['license_url'] = line

        elif line.endswith('win32.x86_64.exe'):
            DOWNLOAD_REPLACEMENTS['win64_url'] = line

        elif line.endswith('win32.x86.exe'):
            DOWNLOAD_REPLACEMENTS['win32_url'] = line

        elif line.endswith('macosx.cocoa.x86_64.dmg'):
            DOWNLOAD_REPLACEMENTS['macos_url'] = line

        elif line.endswith('.zip') and 'UPDATE_SITE' in line:
            DOWNLOAD_REPLACEMENTS['update_site_url'] = line

        elif line.endswith('linux.gtk.x86_64.tar.gz'):
            DOWNLOAD_REPLACEMENTS['linux64_url'] = line

        elif line.endswith('linux.gtk.x86.tar.gz'):
            DOWNLOAD_REPLACEMENTS['linux32_url'] = line

        elif 'LiClipse_' in line:
            DOWNLOAD_REPLACEMENTS['folder_url'] = line

        else:
            raise AssertionError('Unexpected line: %s' % (line,))

    apply_to(os.path.join(this_file_dir, 'index.html'))
    apply_to(os.path.join(this_file_dir, 'languages.html'))
    apply_to(os.path.join(this_file_dir, 'history.html'))
    apply_to(os.path.join(this_file_dir, 'download.html'),kwargs=DOWNLOAD_REPLACEMENTS)
    apply_to(os.path.join(this_file_dir, 'license.html'))
    apply_to(os.path.join(this_file_dir, 'faq.html'))
    apply_to(os.path.join(this_file_dir, 'buy.html'))
    apply_to(os.path.join(this_file_dir, 'multi_edition_video.html'))
    apply_to(os.path.join(this_file_dir, 'contact.html'))


    apply_to(os.path.join(this_file_dir, 'text', 'index.html'), path='text', template_contents=text_template_contents, kwargs={'title': 'LiClipseText'})
    apply_to(os.path.join(this_file_dir, 'text', 'about.html'), path='text', template_contents=text_template_contents, kwargs={'title': 'About'})
    apply_to(os.path.join(this_file_dir, 'text', 'download.html'), path='text', template_contents=text_template_contents, kwargs={'title': 'Download'})
    if MANUAL_OPEN_SOURCE_HEADER is not None:
        apply_to_contents('', 'manual.html', MANUAL_OPEN_SOURCE_HEADER, '', path='text', template_contents=text_template_contents, kwargs={'title': 'Download'})
    apply_to(os.path.join(this_file_dir, 'text', 'screenshots.html'), path='text', template_contents=text_template_contents, kwargs={'title': 'Screenshots'})
    apply_to(os.path.join(this_file_dir, 'text', 'developers.html'), path='text', template_contents=text_template_contents, kwargs={'title': 'Developers'})

    if os.path.exists(help_location):
        copytree(os.path.join(help_location, 'images'), os.path.join(page_dir, 'images'))


if __name__ == '__main__':
    main()
    print 'Generation finished'
