# The mako template that will be used by default to generate the rml
# document
default_template = """
<?xml version="1.0" encoding="utf-8" standalone="no" ?>
<!DOCTYPE document SYSTEM "rml_1_0.dtd">
<document>
  <template title="The title"
            pageSize="(8.5in, 11in)" leftMargin="2.0in" rightMargin="2.0in"
            topMargin="1.0in" bottomMargin="1.5in" showBoundary="0">
    <pageTemplate id="main">
      <frame id="content" x1="2in" y1="1.5in" width="4.5in" height="8.5in"/>
    </pageTemplate>
  </template>
  <stylesheet>
    <paraStyle name="p"  textColor="#353535" fontSize="10" leading="12"
               spaceAfter="10"/>
  </stylesheet>
  <story>

% for p in document.paragraphs:
    <para style="p" leftIndent="${p.level}cm">
       ${p.text}
    </para>
% endfor

  </story>
</document>
""".strip()
