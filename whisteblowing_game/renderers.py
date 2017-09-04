from django import forms
from django.forms.widgets import RadioFieldRenderer
# from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class MyCustomRenderer( RadioFieldRenderer ):
    def render( self ):
        """Outputs a series of <td></td> fields for this set of radio fields."""
        return( mark_safe( u''.join([ u"""<td>
        {1}</td><td>{0}</td>"""
            .format(w.choice_value, w.tag()) for w in self if w.choice_value] )))
