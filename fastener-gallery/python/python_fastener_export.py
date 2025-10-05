#!/usr/bin/env python3
"""Simple FreeCAD helper for generating parametric fastener previews.

Run this script with FreeCAD's Python interpreter. It creates light-weight
parametric solids for a few common fasteners and exports them as both STEP and
STL files so they can be reused by the web preview or downstream CAD tools.
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Callable, Dict

try:
  import FreeCAD as App
  import Part
  import Mesh
except ImportError as exc:  # pragma: no cover - executed only in FreeCAD env
  raise SystemExit(
      'This script must be executed with FreeCAD\'s Python interpreter.\n'
      'On Windows: "C:/Program Files/FreeCAD/bin/FreeCADCmd.exe" python_fastener_export.py ...\n'
      'On macOS/Linux: "freecadcmd" python_fastener_export.py ...'
  ) from exc


ShapeBuilder = Callable[[argparse.Namespace], Part.Shape]


def _hex_profile(width: float) -> Part.Face:
  radius = width / (2 * math.cos(math.pi / 6.0))
  points = []
  for index in range(6):
    angle = math.pi / 6.0 + index * math.pi / 3.0
    points.append(App.Vector(radius * math.cos(angle), radius * math.sin(angle), 0))
  points.append(points[0])
  wire = Part.makePolygon(points)
  return Part.Face(wire)


def build_hex_bolt(args: argparse.Namespace) -> Part.Shape:
  diameter = args.diameter
  length = args.length
  head_height = args.head_height or diameter * 0.7
  head_width = args.head_width or diameter * 1.5

  head = _hex_profile(head_width).extrude(App.Vector(0, 0, head_height))
  shank = Part.makeCylinder(diameter / 2.0, length)
  shank.translate(App.Vector(0, 0, -length))
  return head.fuse(shank)


def build_socket_cap(args: argparse.Namespace) -> Part.Shape:
  diameter = args.diameter
  length = args.length
  head_height = args.head_height or diameter * 0.8
  head_diameter = args.head_width or diameter * 1.6
  recess_diameter = diameter * 0.6

  head = Part.makeCylinder(head_diameter / 2.0, head_height)
  recess = Part.makeCylinder(recess_diameter / 2.0, head_height)
  head = head.cut(recess)
  shank = Part.makeCylinder(diameter / 2.0, length)
  shank.translate(App.Vector(0, 0, -length))
  return head.fuse(shank)


def build_hex_nut(args: argparse.Namespace) -> Part.Shape:
  diameter = args.diameter
  thickness = args.thickness or diameter * 0.8
  width = args.head_width or diameter * 1.8

  body = _hex_profile(width).extrude(App.Vector(0, 0, thickness))
  bore = Part.makeCylinder(diameter / 2.0, thickness * 1.2)
  bore.translate(App.Vector(0, 0, -thickness * 0.1))
  return body.cut(bore)


def build_flat_washer(args: argparse.Namespace) -> Part.Shape:
  inner = args.diameter / 2.0
  outer = args.outer / 2.0
  thickness = args.thickness
  outer_cyl = Part.makeCylinder(outer, thickness)
  inner_cyl = Part.makeCylinder(inner, thickness * 1.2)
  inner_cyl.translate(App.Vector(0, 0, -thickness * 0.1))
  return outer_cyl.cut(inner_cyl)


def build_blind_rivet(args: argparse.Namespace) -> Part.Shape:
  diameter = args.diameter
  grip = args.grip
  mandrel = Part.makeCylinder(diameter * 0.35, grip + diameter * 1.2)
  mandrel.translate(App.Vector(0, 0, -grip * 0.2))
  body = Part.makeCylinder(diameter / 2.0, grip)
  head = Part.makeCone(diameter, diameter * 1.6, diameter * 0.25)
  head.translate(App.Vector(0, 0, grip))
  return body.fuse(head).fuse(mandrel)


FASTENER_BUILDERS: Dict[str, ShapeBuilder] = {
  'hex_bolt': build_hex_bolt,
  'socket_cap': build_socket_cap,
  'hex_nut': build_hex_nut,
  'flat_washer': build_flat_washer,
  'blind_rivet': build_blind_rivet,
}


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument('--fastener', choices=FASTENER_BUILDERS.keys(), required=True)
  parser.add_argument('--output-dir', default='exports', help='Destination directory for generated files.')
  parser.add_argument('--diameter', type=float, default=12.0, help='Major diameter in millimetres.')
  parser.add_argument('--length', type=float, default=40.0, help='Shank length in millimetres (bolts & screws).')
  parser.add_argument('--head-height', type=float, default=None, help='Override head height for bolts and screws.')
  parser.add_argument('--head-width', type=float, default=None, help='Override across flats / head diameter.')
  parser.add_argument('--outer', type=float, default=24.0, help='Outer diameter for washers.')
  parser.add_argument('--thickness', type=float, default=4.0, help='Thickness for nuts and washers.')
  parser.add_argument('--grip', type=float, default=6.0, help='Grip range for blind rivets.')
  return parser


def export_shape(shape: Part.Shape, output_dir: Path, basename: str) -> None:
  doc = App.newDocument('FastenerExport')
  obj = doc.addObject('Part::Feature', 'Fastener')
  obj.Shape = shape
  doc.recompute()

  output_dir.mkdir(parents=True, exist_ok=True)

  step_path = output_dir / f'{basename}.step'
  stl_path = output_dir / f'{basename}.stl'

  Part.export([obj], str(step_path))
  Mesh.export([obj], str(stl_path))

  App.closeDocument(doc.Name)
  print(f'Exported {basename} -> {step_path} and {stl_path}')


def main() -> None:
  parser = build_parser()
  args = parser.parse_args()
  builder = FASTENER_BUILDERS[args.fastener]
  shape = builder(args)

  output_dir = Path(args.output_dir).expanduser().resolve()
  export_shape(shape, output_dir, args.fastener)


if __name__ == '__main__':
  main()
