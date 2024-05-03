import re

def formatter(source, language, css_class, options, md, classes, id_value, attrs=None, **kwargs):
    opt=''
    for x,y in options.items():
        opt+= f' {x}="{y}"'
    pattern = r'^\s*:\w+:\s*\w+.*$'
    source = re.sub(pattern, '', source, flags=re.MULTILINE)
    template=f"""<logic-editor {opt}>
    <script type="application/json">
        {source}
    </script>
    </logic-editor>"""
    return template
  
def validator(language, inputs, options, attrs, md):
    """Custom validator."""
    okay = True
    for k, v in inputs.items():
        options[k] = v
    return okay