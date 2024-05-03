"""SVG Spritesheet Maker

Makes an SVG spritesheet from SVG sprites.

An SVG spritesheet is a file that consists of various
SVG files, suitable for <use> in HTML rendered by browsers.
"""
from argparse import (ArgumentParser,
                      FileType,
                      RawDescriptionHelpFormatter)
from pathlib import Path
from lxml import etree
import lxml.html
from lxml.builder import E
import sys
import os
from typing import List


SVG_XMLNS = {"xmlns": "http://www.w3.org/2000/svg"}


class Sprite:
    """SVG sprite.
    """
    def __init__(self,
                 *,
                 id,
                 view_box="",
                 filename="",
                 symbol_node=None):
        self._id = (id
                    if id != ""
                    else str(Path(filename).stem))
        self._symbol_node = symbol_node
        self._view_box = view_box
        self._load_svg(filename)

    def _load_svg(self, filename) -> None:
        self._filename = filename
        self._child_nodes = None

        if filename != "":
            tree = etree.parse(self._filename)
            self._root = self._strip_namespace(tree.getroot())
            self._view_box = self._root.attrib.get("viewBox", "")
            self._child_nodes = self._root.getchildren()
        elif self._symbol_node is not None:
            self._symbol_node = self._strip_namespace(self._symbol_node)
            self._child_nodes = self._symbol_node.getchildren()

    def _strip_namespace(self, root: etree.Element) -> etree.Element:
        for e in root.getiterator():
            if not (isinstance(e,
                               etree._Comment
                               or isinstance(e,
                                             etree._ProcessingInstruction))):
                e.tag = etree.QName(e).localname
        etree.cleanup_namespaces(root)
        return root

    def export(self,
               *,
               show_use: bool = False,
               spritesheet_filename=""):
        """Exports sprite as SVG.

        Parameters
        ----------
        show_use : bool
            Export SVG using <use> if True.

        Returns
        -------
        str
            Exported data.
        """
        svg = None
        if show_use:
            svg = E("svg",
                    E("use", {"href": f"{Path(spritesheet_filename).name}#{self.id}"}))  # noqa
            return lxml.html.tostring(svg,
                                      pretty_print=True).decode()
        else:
            attrib = SVG_XMLNS
            attrib["viewBox"] = self._view_box
            svg = E("svg", attrib)
            for child in self._child_nodes:
                svg.append(child)
        return etree.tostring(svg,
                              pretty_print=True,
                              xml_declaration=True,
                              encoding="utf-8").decode()

    @property
    def id(self) -> str:
        """ID.
        """
        return self._id

    @property
    def view_box(self) -> str:
        """View box.
        """
        return self._view_box

    @property
    def filename(self) -> str:
        """File name.
        """
        return self._filename

    @property
    def child_nodes(self) -> List[etree.Element]:
        """Child nodes.
        """
        return self._child_nodes

    def __lt__(self, other):
        return self.id < other.id

    def __str__(self):
        return f"Sprite(id={self._id}, filename={self._filename})"


class Spritesheet:
    """SVG spritesheet.
    """
    def __init__(self, filename):
        self._filename = filename
        if self._is_new():
            self._create_svg()
        else:
            self._load_svg()

    def _is_new(self) -> bool:
        if os.path.exists(self._filename):
            with open(self._filename) as f:
                if '<svg' in f.read():
                    return False
        return True

    def _create_svg(self) -> None:
        self._root = E("svg", SVG_XMLNS,
                       E("defs"))

    def _load_svg(self) -> None:
        tree = etree.parse(self._filename)
        self._root = (tree.xpath("//xmlns:svg",
                                 namespaces=SVG_XMLNS)[0]
                      if len(tree.xpath("//xmlns:svg",
                                        namespaces=SVG_XMLNS)) > 0
                      else None)

    def add(self, sprite) -> None:
        """Adds sprite to spritesheet.

        Parameters
        ----------
        sprite : Sprite
            SVG sprite to add
        """
        defs = self._root.xpath("//xmlns:defs", namespaces=SVG_XMLNS)
        defs = defs[0] if len(defs) > 0 else self._root.xpath("//defs")
        defs = defs[0] if len(defs) > 0 else defs
        if defs is None or (isinstance(defs, list) and len(defs) == 0):
            raise RuntimeError("Could not find <defs>.")

        symbols = defs.xpath(f"//xmlns:symbol[@id='{sprite.id}']",
                             namespaces=SVG_XMLNS)
        if defs is not None and len(symbols) == 0:
            defs.append(E("symbol",
                          {"id": sprite.id,
                           "viewBox": sprite.view_box},
                          *sprite.child_nodes))
        elif len(symbols) > 0:
            raise RuntimeError(f"ID '{sprite.id}' "
                               "already exists in spritesheet.")

    def remove(self, sprite) -> None:
        """Removes sprite from spritesheet.

        Parameters
        ----------
        sprite : Sprite
            SVG sprite to remove
        """
        defs = self._root.xpath("//xmlns:defs", namespaces=SVG_XMLNS)
        defs = defs[0] if len(defs) > 0 else None
        symbols = defs.xpath(f"//xmlns:symbol[@id='{sprite.id}']",
                             namespaces=SVG_XMLNS)
        for s in symbols:
            s.getparent().remove(s)

    def update(self) -> None:
        """Saves changes to the spritesheet to a file.
        """
        self._tree = etree.ElementTree(self._root)
        self._tree.write(self._filename,
                         pretty_print=True,
                         encoding="utf-8",
                         xml_declaration=True)

    @property
    def filename(self) -> str:
        """File name.
        """
        return self._filename

    @property
    def sprites(self) -> List[Sprite]:
        """List of sprites in spritesheet.
        """
        sprites = []
        symbols = self._root.xpath("//xmlns:symbol",
                                   namespaces=SVG_XMLNS)
        for s in symbols:
            sprites.append(Sprite(id=s.attrib.get("id"),
                                  view_box=s.attrib.get("viewBox", ""),
                                  symbol_node=s))
        sprites.sort()
        return sprites

    def __str__(self):
        return f"Spritesheet(filename={self._filename})"


def _create_spritesheet(*sprites,
                        overwrite_allowed: bool,
                        spritesheet_filename: str) -> None:
    if not overwrite_allowed and os.path.exists(spritesheet_filename):
        raise RuntimeError(f"Spritesheet '{spritesheet_filename}' already "
                           "exists. You can overwrite it with the -F option.")
    elif os.path.exists(spritesheet_filename):
        os.remove(spritesheet_filename)

    sprites = list(sprites)
    spritesheet = Spritesheet(spritesheet_filename)

    for sprite in sprites:
        id_filename_pair = (sprite.split("=")
                            if "=" in sprite
                            else ["", sprite])
        sprite = Sprite(id=id_filename_pair[0],
                        filename=id_filename_pair[1])
        spritesheet.add(sprite)

    spritesheet.update()


def _add_sprite(*sprites,
                spritesheet_filename: str) -> None:
    if not os.path.exists(spritesheet_filename):
        raise RuntimeError(f"Spritesheet '{spritesheet_filename}' "
                           "does not exist.")

    sprites = list(sprites)
    spritesheet = Spritesheet(spritesheet_filename)

    for sprite in sprites:
        id_filename_pair = (sprite.split("=")
                            if "=" in sprite
                            else ["", sprite])
        sprite = Sprite(id=id_filename_pair[0],
                        filename=id_filename_pair[1])
        spritesheet.add(sprite)

    spritesheet.update()


def _remove_sprite(*sprites,
                   spritesheet_filename: str) -> None:
    if not os.path.exists(spritesheet_filename):
        raise RuntimeError(f"Spritesheet '{spritesheet_filename}' "
                           "does not exist.")

    sprites = list(sprites)
    spritesheet = Spritesheet(spritesheet_filename)

    for sprite in sprites:
        sprite = Sprite(id=sprite)
        spritesheet.remove(sprite)

    spritesheet.update()


def _list_sprites(*,
                  spritesheet_filename: str) -> None:
    spritesheet = Spritesheet(spritesheet_filename)

    for sprite in spritesheet.sprites:
        print(sprite.id)


def _export_sprites(*sprites,
                    show_use: bool,
                    spritesheet_filename: str) -> None:
    if not os.path.exists(spritesheet_filename):
        raise RuntimeError(f"Spritesheet '{spritesheet_filename}' "
                           "does not exist.")

    sprites = list(sprites)
    spritesheet = Spritesheet(spritesheet_filename)

    for sprite in spritesheet.sprites:
        if sprite.id in sprites:
            print(sprite.export(show_use=show_use,
                                spritesheet_filename=spritesheet_filename),
                  end="")


def main() -> None:
    """Runs script.
    """
    parser = ArgumentParser(prog="ssm.py",
                            description=__doc__,
                            formatter_class=RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers()

    parser_create = subparsers.add_parser("create",
                                          description="Create SVG spritesheet",
                                          help="Create SVG spritesheet")
    parser_create.set_defaults(_parser="create")
    parser_create.add_argument("-f",
                               required=True,
                               type=str,
                               metavar="SPRITESHEET_FILE",
                               help="SVG spritesheet file")
    parser_create.add_argument("-F",
                               action="store_true",
                               help="Overwrite existing spritesheet")
    parser_create.add_argument("sprites",
                               type=str,
                               metavar="SVG_SPRITES",
                               nargs="+",
                               help="SVG sprites")

    parser_list = subparsers.add_parser("list",
                                        description="List IDs of sprites in SVG spritesheet", # noqa
                                        help="List IDs of sprites in SVG spritesheet") # noqa
    parser_list.set_defaults(_parser="list")
    parser_list.add_argument("-f",
                             required=True,
                             type=FileType(encoding="UTF-8"),
                             metavar="SPRITESHEET_FILE",
                             help="SVG spritesheet file")

    parser_add = subparsers.add_parser("add",
                                       description="Add sprite(s) to SVG spritesheet", # noqa
                                       help="Add sprite(s) to SVG spritesheet")
    parser_add.set_defaults(_parser="add")
    parser_add.add_argument("-f",
                            required=True,
                            type=FileType(encoding="UTF-8"),
                            metavar="SPRITESHEET_FILE",
                            help="SVG spritesheet file")
    parser_add.add_argument("sprites",
                            type=str,
                            metavar="SVG_SPRITES",
                            nargs="+",
                            help="SVG sprites")

    parser_remove = subparsers.add_parser("remove",
                                          description="Remove sprite(s) from SVG spritesheet", # noqa
                                          help="Remove sprite(s) from SVG spritesheet") # noqa
    parser_remove.set_defaults(_parser="remove")
    parser_remove.add_argument("-f",
                               required=True,
                               type=FileType(encoding="UTF-8"),
                               metavar="SPRITESHEET_FILE",
                               help="SVG spritesheet file")
    parser_remove.add_argument("sprites",
                               type=str,
                               metavar="SVG_SPRITES",
                               nargs="+",
                               help="SVG sprites")

    parser_export = subparsers.add_parser("export",
                                          description="Export sprite(s) from SVG spritesheet", # noqa
                                          help="Export sprite(s) from SVG spritesheet") # noqa
    parser_export.set_defaults(_parser="export")
    parser_export.add_argument("-f",
                               required=True,
                               type=FileType(encoding="UTF-8"),
                               metavar="SPRITESHEET_FILE",
                               help="SVG spritesheet file")
    parser_export.add_argument("--use",
                               "-u",
                               action="store_true",
                               help="Print <use> for HTML")
    parser_export.add_argument("sprites",
                               type=str,
                               metavar="SVG_SPRITES",
                               nargs="+",
                               help="SVG sprites")

    try:
        if len(sys.argv[1:]) > 0:
            args = parser.parse_args(sys.argv[1:])
            if args._parser == "create":
                _create_spritesheet(*args.sprites,
                                    overwrite_allowed=args.F,
                                    spritesheet_filename=(args.f
                                                          if args.f is not None
                                                          else ""))
            elif args._parser == "add":
                _add_sprite(*args.sprites,
                            spritesheet_filename=(args.f.name
                                                  if args.f is not None
                                                  else ""))
            elif args._parser == "remove":
                _remove_sprite(*args.sprites,
                               spritesheet_filename=(args.f.name
                                                     if args.f is not None
                                                     else ""))
            elif args._parser == "list":
                _list_sprites(spritesheet_filename=(args.f.name
                                                    if args.f is not None
                                                    else ""))
            elif args._parser == "export":
                _export_sprites(*args.sprites,
                                show_use=args.use,
                                spritesheet_filename=(args.f.name
                                                      if args.f is not None
                                                      else ""))
        else:
            parser.print_help()
    except RuntimeError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
