class HTMLLayout:
    """
    A mixin class for Tree that adds a __str__ method that will render a node and its children as an svg.

    Assumes the existance of the following attributes:
      _children     a dict[str,list]
      label         a str
      properties    a dict
    """

    _include_properties = False

    def __init__(
        self,
        include_properties=None,
    ) -> None:
        self._iinclude_properties = include_properties


    def __str__(self) -> str:
        html = self._box()
        prolog = '''<html>
        <head><title>Tree</title></head>
        <style>
        .column, .group, .outercontainer, .parent, .leaf, .properties { display:flex; flex-direction:column;}
        .children, .groupitems, .property { display: flex; flex-direction:row; align-items:stretch;}
        .children {border-top: black solid 1pt;}
        .parent {border-left: black solid 1pt; font-weight:bold;}
        .outercontainer { width:fit-content;}
        .leaf, .parent {padding: 0.5em;}
        .leaf {font-weight: bold;}
        .leaf:last-of-type { padding-right: 1em;} 
        .groupname {padding: 0.2em; font-size:8pt;}
        .group { background: #b8b8b8; background: linear-gradient(90deg, rgb(230 230 230) 0%, rgb(237 237 237) 25%, rgba(255, 255, 255, 1) 100%);}
        .key { padding-right:1em; }
        </style>
        <body><div class="outercontainer"
        '''
        epilog = """</div></body>
        </html>"""
        return f"{prolog}{html}{epilog}"
    
    def _box(self):
        node_name = self.label

        include_properties = self._include_properties  # class var
        if (
            self._iinclude_properties is not None
        ):  # override if instance variable is not None
            include_properties = self._iinclude_properties
        if include_properties:  # neither None or False
            props = [f'<div class="property"><div class="key">{k}</div><div class="value">{v}</div></div>' for k, v in self.properties.items()]
            props = f'<div class="properties">{"".join(props)}</div>'
        else:
            props = ""

        if self.is_leaf():
            return f'<div class="leaf"><div class="nodename">{node_name}</div>{props}</div>\n'
        else:
            groups = {}
            for group, children in self._children.items():
                childitems = []
                for child in children:
                    if child is not None:
                        childitems.append(child._box())
                groups[group] = "".join(childitems)
            groupdivs = "".join(f'<div class="group">\n<div class="groupname">{group}</div>\n<div class="groupitems">{html}</div>\n</div>\n' for group,html in groups.items())
            return f'<div class="column">\n<div class="parent"><div class="nodename">{node_name}</div>{props}</div>\n<div class="children">{groupdivs}</div>\n</div>'
