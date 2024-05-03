# -*- coding: utf-8 -*-
"""
  femagtools.dxfsl.geom
  ~~~~~~~~~~~~~~~~~~~~~

  a geometry is composed of connected shapes (lines, arcs, circles) which
  build areas

  Authors: Ronald Tanner, Beat Holm
"""
from __future__ import print_function

import numpy as np
import networkx as nx
import logging
import sys
from .corner import Corner
from .area import Area
from .shape import Element, Shape, Circle, Arc, Line, Point
from .shape import is_Circle, is_Arc, is_Line
from .machine import Machine
from femagtools.dxfsl.areabuilder import AreaBuilder
from .functions import less_equal, less, greater, greater_equal
from .functions import distance, alpha_line, alpha_points, alpha_angle
from .functions import point, points_are_close, is_point_inside_region
from .functions import line_m, line_n, lines_intersect_point
from .functions import middle_point_of_line, middle_point_of_arc
from .functions import middle_angle
from .functions import normalise_angle, is_same_angle
from .functions import part_of_circle, gcd
from .functions import point_on_arc, nodes_are_equal
from .functions import area_size
import io
import time

logger = logging.getLogger('femagtools.geom')


nxversion = int(nx.__version__.split('.')[0])
geom_mindist = 0.0


def plot_area(area):
    """plot area for debug purposes"""
    import matplotlib.pylab as pl
    import matplotlib.patches as pch
    fig = pl.figure()
    ax = fig.add_subplot(111)

    for e in area:
        if isinstance(e, Line):
            ax.add_line(pl.Line2D((e.p1[0], e.p2[0]),
                                  (e.p1[1], e.p2[1]),
                                  color='red'))
        elif isinstance(e, Arc):
            ax.add_patch(pch.Arc(e.center, 2*e.radius, 2*e.radius,
                                 angle=0,
                                 theta1=e.startangle*180/np.pi,
                                 theta2=e.endangle*180/np.pi,
                                 color='darkblue'))
        elif isinstance(e, Circle):
            ax.add_patch(pch.Circle(e.center,
                                    e.radius,
                                    fill=False, color='darkblue'))

    ax.axis('scaled', aspect='equal')
    pl.show()

#############################
#            geom           #
#############################


ndec = 6  # number of decimals to round to


def intersect_and_split(inp_elements, rtol, atol):
    logger.info("Load input elements ... ")
    out_elements = []
    for e in inp_elements:
        out_size = len(out_elements)
        intersect_and_split_element(e, out_elements, 0, out_size, rtol, atol)
    return out_elements


def intersect_and_split_element(el, out_elements, out_start,
                                out_size, rtol, atol):
    # appends splitted elements
    # Unchanged out_size prevents repeated processing in recursive calls
    for x in range(out_start, out_size):
        split_el = add_or_split(el, x, out_elements, rtol, atol)
        if len(split_el) > 0:
            for e in split_el:
                intersect_and_split_element(e, out_elements, x+1,
                                            out_size, rtol, atol)
            return
    out_elements.append(el)


def add_or_split(el, x, out_elements, rtol, atol):
    if out_elements[x] is None:
        return []
    split_el = el.overlapping_shape(out_elements[x], rtol, atol)
    if split_el:
        logger.debug("=== overlapping elements ===")
        out_elements[x] = None
        return split_el

    points = el.intersect_shape(out_elements[x], rtol, atol, True)
    if len(points) > 0:
        split_elements = out_elements[x].split(points, rtol, atol)
        if len(split_elements) > 0:
            out_elements += split_elements
            out_elements[x] = None
        split_el = el.split(points, rtol, atol)
        return split_el
    return []


def add_element(geom, e, rtol, atol):
    n = geom.find_nodes(e.start(), e.end())
    try:
        add_or_join(geom, n[0], n[1], e, rtol, atol)
    except Exception as ex:
        logger.warn("EXCEPTION in add_element: %s", ex)


def add_or_join(geom, n1, n2, entity, rtol, atol):
    """ adds a new entity to graph or joins entity with existing
    geom: Geometry
    n1, n2: nodes
    entity
    """
    if n1 == n2:
        logger.debug(
            "Tiny element with same node on both sides ignored: %s", n1)
        logger.debug(
            " -- element: %s", entity)
        return

    e = geom.get_edge_element(n1, n2)
    if not e:  # no duplicates
        geom.add_edge(n1, n2, entity)
        return

    logger.debug("Duplicate connection: %s <--> %s", n1, n2)
    if is_Line(e):
        if is_Line(entity):
            logger.debug("add_or_join(): Duplicate Lines ignored")
            return  # its ok

    if is_Arc(e):
        if is_Arc(entity):
            if points_are_close(e.center, entity.center, rtol=rtol, atol=atol):
                if points_are_close(e.p1, entity.p1):
                    logger.debug("add_or_join(): Duplicate Arcs ignored")
                    return  # its ok

    if is_Circle(entity):
        if is_Circle(e):
            logger.debug("add_or_join(): Duplicate Circle ignored")
            return  # its ok

    if is_Circle(entity) or is_Circle(e):
        e1, e2 = entity.cut_into_halves()
        logger.debug("===== add_or_join(): Element near circle is cut into halves =====")
        add_element(geom, e1, rtol, atol)
        add_element(geom, e2, rtol, atol)
        return  # halves installed

    m1 = e.center_of_connection()
    m2 = entity.center_of_connection()
    logger.debug("midpoints: %s -- %s", m1, m2)
    if points_are_close(m1, m2, rtol, 1e-2):
        logger.debug("Elements are close together")
        return  # ok

    e1, e2 = entity.cut_into_halves()
    logger.debug("===== add_or_join(): cut into halves =====")
    add_element(geom, e1, rtol, atol)
    add_element(geom, e2, rtol, atol)
    return  # halves installed


def get_nodes_of_paths(g, c):
    nodes = set()
    i = 1
    for s in c[:-1]:
        for e in c[i:]:
            logger.info("%s --%s:", s, e)
            for p in nx.all_simple_paths(g, s, e):
                logger.info("   %s", len(list(p)))
                nodes |= set([n for n in p if g.degree(n) < 3])
        i += 1
    return nodes


def convex_hull(nodes):
    """collect edges that build the convex hull."""

    # Get a local list copy of the nodes and sort them lexically.
    points = list(nodes)
    points.sort()
    if len(points) <= 1:
        return points

    # 2D cross product of OA and OB vectors, i.e. z-component of
    # their 3D cross product.
    # Returns a positive value, if OAB makes a counter-clockwise turn,
    # negative for clockwise turn, and zero if the points are collinear.
    def cross(o, a, b):
        dx = a[0] - o[0], a[1] - o[1]
        dy = b[0] - o[0], b[1] - o[1]
        return dx[0] * dy[1] - dx[1] * dy[0]

    # Build lower hull
    lower = []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)

    # Build upper hull
    upper = []
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)

    # Concatenation of the lower and upper hulls gives the convex hull.
    # Last point of each list is omitted because it is repeated at the
    # beginning of the other list.
    return lower[:-1] + upper[:-1]


def ccw(a, b, c):
    """
    checks if 3 points are placed counter clockwise or in line
    """
    cp = np.cross(np.asarray(b)-np.asarray(a),
                  np.asarray(c)-np.asarray(a))
    if np.allclose(cp, (0.0,)):
        return 0
    if cp > 0:
        return 1
    return -1


def intersect(a, b):
    """checks if 2 lines intersect"""
    return ccw(a.p1, a.p2, b.p1) != ccw(a.p1, a.p2, b.p2) and \
        ccw(b.p1, b.p2, a.p1) != ccw(b.p1, b.p2, a.p2)


def is_connected(a, b):
    if a == b:
        return False
    return a[0] == b[0] or a[1] == b[0] or a[0] == b[1] or a[1] == b[1]


def single_path(edges):
    """sort edges to create a sequence of connected edges"""
    if edges:
        p = [edges[0]]
        remaining = edges[1:]
        while remaining:
            edges = remaining[:]
            remaining = []
            for e in edges:
                if is_connected(p[-1], e):
                    p.append(e)
                elif is_connected(p[0], e):
                    p.insert(0, e)
                else:
                    remaining.append(e)
        return p
    return []


#############################
#         Geometrie         #
#############################

nodes_filecount = 0


class Geometry(object):
    """collection of connected shapes"""

    def __init__(self,
                 elements=[],
                 center=[],
                 rtol=1e-03,
                 atol=1e-03,
                 is_inner=False,
                 is_outer=False,
                 split=False,
                 debug=False):
        self._name = ''
        self.kind = ''
        self.mirror_corners = []
        self.start_corners = []
        self.end_corners = []
        self.sym_part = 0
        self.sym_counterpart = 0
        self.sym_slices = 0
        self.sym_slice_angle = 0.0
        self.alfa = 0.0
        self.center = []
        self.min_radius = 0.0
        self.max_radius = 0.0
        self.is_inner = is_inner
        self.is_outer = is_outer
        self.cut_lines = []
        self.sym_area = None
        self.airgaps = []
        self.area_list = []
        self.g = nx.Graph()
        self.rtol = rtol
        self.atol = atol
        self.debug = debug
        self.num_edges = 0
        self.wdg_is_mirrored = False
        i = 0

        def get_elements(elements, split):
            if split:
                return intersect_and_split(elements, self.rtol, self.atol)
            else:
                return elements

        for e in get_elements(elements, split):
            if e:
                e.id = i
                n = self.find_nodes(e.start(), e.end())
                try:
                    add_or_join(self, n[0], n[1], e, self.rtol, self.atol)
                except Exception as ex:
                    logger.warn("EXCEPTION %s", ex)
                    if e:  # must be a circle
                        self.g.add_node(e.center, object=e)
            i += 1

        self.num_edges = self.number_of_edges()

        if center:
            self.set_center(center)

    def shaft(self):
        """returns shaft diameter if any"""
        radius = []
        for a in self.arcs():
            if np.isclose(a.center, 0.0).all():
                logger.info("Shaft candidate (%f, %f) %r",
                            a.startangle/np.pi*180,
                            a.endangle/np.pi*180,
                            a.radius)
                if 0 < a.radius < self.diameters[-1]/2:
                    radius.append(a.radius)
        return 2*sorted(radius)[0] if radius else 0

    def set_diameters(self):
        try:
            min, max = self.min(), self.max()
            logger.info("Min %s max %s", min, max)
            self.diameters = (round(2*np.sqrt(min[0]**2 + min[1]**2), 3),
                              round(2*np.sqrt(max[0]**2 + max[1]**2), 3))
        except:
            self.diameters = []

    def move(self, offset):
        """moves all objects"""
        for e in self.g.edges(data=True):
            e[2]['object'].move(offset, ndec)
        for c in self.circles():
            c.move((-offset[0], -offset[1]))
        mapping = {n: (round(n[0] + offset[0], ndec),
                       round(n[1] + offset[1], ndec))
                   for n in self.g.nodes()}
        nx.relabel_nodes(self.g, mapping, copy=False)

    def rotate(self, alpha):
        """rotates all objects by angle alpha"""
        T = np.array(((np.cos(alpha), -np.sin(alpha)),
                      (np.sin(alpha), np.cos(alpha))))
        for e in self.g.edges(data=True):
            e[2]['object'].transform(T, alpha, ndec)
        for c in self.circles():
            c.transform(T, alpha, ndec)
        rotnodes = np.dot(T, np.asarray(self.g.nodes()).T).T.tolist()
        mapping = {n: (round(r[0], ndec),
                       round(r[1], ndec))
                   for n, r in zip(self.g.nodes(), rotnodes)}
        nx.relabel_nodes(self.g, mapping, copy=False)

    def check_geom(self, what):
        logger.debug("check geometry of %s", what)
        parts = int(round(np.pi * 2 / self.alfa, 1))
        logger.debug(" --parts......: %s", parts)
        logger.debug(" --ist alpha..: %s", self.alfa)
        real_alfa = np.pi * 2 / parts
        logger.debug(" --soll alpha.: %s", real_alfa)
        if not np.isclose(self.alfa, real_alfa):
            logger.debug(" --BAD angle ==> get corrected machine")
            return self.correct_geom(real_alfa)
        return None

    def correct_geom(self, correct_alpha):
        elements = []
        for e in self.g.edges(data=True):
            o = e[2]['object'].correct(self.alfa, correct_alpha, ndec)
            elements.append(o)
        geom = Geometry(elements,
                        center=self.center,
                        is_inner=self.is_inner,
                        is_outer=self.is_outer,
                        rtol=self.rtol,
                        atol=self.atol)
        geom.alfa = correct_alpha
        geom.kind = self.kind
        geom.sym_part = self.sym_part
        return geom

    def log_geom(self):
        logger.info("Kind............: %s", self.kind)
        logger.info("Center..........: %s", self.center)
        logger.info("Alpha...........: %s", self.alfa)
        logger.info("Is Inner........: %s", self.is_inner)
        logger.info("Is Outer........: %s", self.is_outer)
        logger.info("Min Radius......: %s", self.min_radius)
        logger.info("Max Radius......: %s", self.max_radius)
        logger.info("Mirror Corners..: %s", self.mirror_corners)
        logger.info("Start Corners...: %s", self.start_corners)
        logger.info("End Corners.....: %s", self.end_corners)
        logger.info("Edges...........: %s", self.num_edges)
        if self.sym_slices > 0:
            logger.info("Symmetry Slices.: %s", self.sym_slices)
            logger.info("Slice Angle.....: %s", self.sym_slice_angle)

    def scale(self, factor):
        """scales all objects"""
        for e in self.g.edges(data=True):
            e[2]['object'].scale(factor)
        for c in self.circles():
            c.scale(factor)
        mapping = {n: (round(factor * n[0], ndec),
                       round(factor * n[1], ndec))
                   for n in self.g.nodes()}
        nx.relabel_nodes(self.g, mapping, copy=False)
        self.diameters = tuple([factor*d for d in self.diameters])

    def find_nodes0(self, *points):
        """return closest nodes to points in arg within pickdist"""
        return [tuple([round(int(x/self.atol+0.5)*self.atol, ndec)
                       for x in p])
                for p in points]

    def find_nodes(self, *points, **kwargs):
        """return closest nodes to points in arg within pickdist"""
        n = []
        nodes = list(kwargs.get('g', self.g))
        if nodes:
            anodes = np.asarray(nodes)
            for p in points:
                # la.norm on numpy below 1.8 does not accept axis
                c = anodes - p
                dist = np.sqrt(np.einsum('ij, ij->i', c, c))
                # dist = la.norm(np.asarray(nodes) - p, axis=1)
                idx = dist.argmin()
                if dist[idx] < self.atol:
                    n.append(nodes[idx])
                else:
                    n.append((round(p[0], ndec), round(p[1], ndec)))
        else:
            return [(round(p[0], ndec), round(p[1], ndec)) for p in points]
        return n

    def find_node(self, p, **kwargs):
        """return closest nodes to points in arg within pickdist"""
        nodes = list(kwargs.get('g', self.g))
        if nodes:
            anodes = np.asarray(nodes)
            # la.norm on numpy below 1.8 does not accept axis
            c = anodes - p
            dist = np.sqrt(np.einsum('ij, ij->i', c, c))
            # dist = la.norm(np.asarray(nodes) - p, axis=1)
            idx = dist.argmin()
            if dist[idx] == 0.0:  # myself
                dist[idx] = 999.0
                idx = dist.argmin()
                if dist[idx] < 0.05:
                    return nodes[idx]
        return None

    def find_the_node(self, p, **kwargs):
        """return closest nodes to points in arg within pickdist"""
        nodes = list(kwargs.get('g', self.g))
        if nodes:
            anodes = np.asarray(nodes)
            # la.norm on numpy below 1.8 does not accept axis
            c = anodes - p
            dist = np.sqrt(np.einsum('ij, ij->i', c, c))
            # dist = la.norm(np.asarray(nodes) - p, axis=1)
            idx = dist.argmin()
            if dist[idx] < self.atol:
                return nodes[idx]
        return None

    def polyline_paths(self):
        """return lists of line paths"""
        paths = []
        g = self.g.copy()
        g.remove_edges_from(self.arcs())
        while g.number_of_edges() > 0:
            p = single_path(g.edges())
            g.remove_edges_from(p)
            # rearrange sequence to make it contiguous:
            px = [p[0]]
            for e in p[1:]:
                if px[-1][1] == e[1]:
                    px.append(tuple(reversed(e[:2])))
                elif px[0][0] == e[0]:
                    px.insert(0, tuple(reversed(e[:2])))
                elif px[0][0] == e[1]:
                    px.insert(0, e[:2])
                else:
                    px.append(e[:2])
            # only keep end point of each edge
            px[1:] = [x[-1] for x in px]
            px[0] = px[0][0]
            paths.append(px)
        return paths

    def number_of_nodes(self):
        """returns the number of nodes in graph"""
        return self.g.number_of_nodes()

    def number_of_edges(self):
        """return the number of edges in graph"""
        return self.g.number_of_edges()

    def get_node(self, p):
        for n in self.g.nodes():
            if points_are_close(p, n):
                return n
        return []

    def add_edge(self, n1, n2, entity):
        if points_are_close(n1, n2):
            logger.debug("WARNING in add_edge(): Points of %s are close together",
                         entity.classname())
            logger.debug("        n1 = %s, n2 = %s", n1, n2)
            logger.debug("        p1 = %s, p2 = %s", entity.p1, entity.p2)

        entity.set_nodes(n1, n2)
        logger.debug("add_edge %s - %s  (%s)", n1, n2, entity.classname())
        self.g.add_edge(n1, n2, object=entity)

    def get_edge(self, eg):
        return [[e[0], e[1], e[2]['object']] for e in self.g.edges(data=True)
                if e[2]['object'] is eg]

    def get_edge_element(self, n1, n2):
        e_dict = self.g.get_edge_data(n1, n2)
        if e_dict:
            return e_dict.get('object', None)
        return None

    def get_edge_nodes(self, edge):
        e = self.get_edge(edge)
        assert(len(e) == 1)
        return (e[0][0], e[0][1])

    def _remove_edge(self, n1, n2):
        logger.debug("remove_edge %s - %s", n1, n2)
        self.g.remove_edge(n1, n2)

    def remove_edge(self, edge):
        e = self.get_edge(edge)
        if len(e) != 1:
            logger.info("remove edge failed: %s", edge)
            raise ValueError("remove edge failed")
        assert(len(e) == 1)
        self._remove_edge(e[0][0], e[0][1])

    def remove_edges(self, edges):
        for e in edges:
            self.remove_edge(e)

    def add_line(self, n1, n2, color=None, linestyle=None):
        line = Line(Element(start=n1, end=n2),
                    color=color,
                    linestyle=linestyle)
        add_or_join(self,
                    n1,
                    n2,
                    line,
                    self.rtol,
                    self.atol)

    def add_arc(self, n1, n2, center, radius, color=None, linestyle=None):
        angle_n1 = alpha_line(center, n1)
        angle_n2 = alpha_line(center, n2)
        arc = Arc(Element(center=center,
                          radius=radius,
                          start_angle=angle_n1*180/np.pi,
                          end_angle=angle_n2*180/np.pi),
                  color=color,
                  linestyle=linestyle)
        add_or_join(self,
                    n1,
                    n2,
                    arc,
                    self.rtol,
                    self.atol)

    def elements(self, type):
        """return lists of objects"""
        return [e[2]['object'] for e in self.g.edges(data=True)
                if isinstance(e[2]['object'], type)]

    def arcs(self):
        """return lists of arcs"""
        return self.elements(Arc)

    def lines(self):
        """return lists of lines"""
        return self.elements(Line)

    def split_lines_longer_than(self, length):
        """split lines longer than length"""
        new_lines = []
        rem_lines = []
        for p1, p2, data in [e for e in self.g.edges(data=True)
                             if isinstance(e[2]['object'], Line)]:
            ln = data['object']
            if ln.length() > length:
                p = ln.center_of_connection()
                new_lines += ln.split([p])
                rem_lines.append((p1, p2))

        for p1, p2 in rem_lines:
            self._remove_edge(p1, p2)
        for new_ln in new_lines:
            add_or_join(self,
                        new_ln.node1(ndec),
                        new_ln.node2(ndec),
                        new_ln,
                        self.rtol,
                        self.atol)

    def circles(self):
        """return list of circle nodes"""
        return [n[1]['object'] for n in self.g.nodes(data=True)
                if n[1] and isinstance(n[1]['object'], Circle)]

    def nodes(self):
        for n in self.g.nodes():
            yield n

    def get_nodes(self):
        nodes = [n for n in self.g.nodes()]
        return nodes

    def virtual_nodes(self):
        nodes = []
        for e in self.elements(Shape):
            nodes += e.get_nodes()
        return nodes

    def angle_nodes(self, center, angle, rtol, atol):
        nodes = []
        for n in self.g.nodes():
            if points_are_close(center, n, rtol, atol):
                # Da gibt es keinen brauchbaren Winkel
                nodes.append(n)
            elif np.isclose(angle, alpha_line(center, n), rtol, atol):
                nodes.append(n)
        return nodes

    def radius_nodes(self, center, radius, rtol, atol):
        nodes = []
        for n in self.g.nodes():
            d = distance(center, n)
            if np.isclose(d, radius, rtol, atol):
                # Da gibt es keinen brauchbaren Winkel
                nodes.append(n)
        return nodes

    def get_corner_list(self, center, angle, rtol=1e-04, atol=1e-04):
        # Die Funktion liefert eine sortierte Liste aller Nodes auf einer
        # Linie als Corner-Objekte.
        corners = [Corner(center, c)
                   for c in self.angle_nodes(center, angle, rtol, atol)]
        center_added = len(corners) == 1
        if len(corners) == 1:
            logger.debug('get_corner_list: the center is a corner')
            corners.append(Corner(center, tuple(center)))
        if len(corners) > 1:
            corners.sort()
        return center_added, corners

    def start_min_corner(self, i):
        return self.start_corners[0][i]

    def start_max_corner(self, i):
        return self.start_corners[-1][i]

    def dist_start_max_corner(self):
        logger.debug("begin of dist_start_max_corner")
        logger.debug("start corners: %s", self.start_corners)
        d = distance(self.center, self.start_corners[-1])
        logger.debug("end of dist_start_max_corner: %s", d)
        return d

    def dist_end_max_corner(self):
        logger.debug("begin of dist_end_max_corner")
        logger.debug("end corners: %s", self.end_corners)

        if self.is_mirrored():
            return self.dist_start_max_corner()
        d = distance(self.center, self.end_corners[-1])
        logger.debug("end of dist_end_max_corner: %s", d)
        return d

    def dist_start_min_corner(self):
        logger.debug("begin of dist_start_min_corner")
        logger.debug("start corners: %s", self.start_corners)
        d = distance(self.center, self.start_corners[0])
        logger.debug("end of dist_start_min_corner: %s", d)
        return d

    def dist_end_min_corner(self):
        logger.debug("begin of dist_end_min_corner")
        logger.debug("end corners: %s", self.end_corners)

        if self.is_mirrored():
            return self.dist_start_min_corner()
        d = distance(self.center, self.end_corners[0])
        logger.debug("end of dist_end_min_corner: %s", d)
        return d

    def get_start_airgap_corner(self):
        if self.is_inner:
            p = (self.max_radius, 0.0)
            cp = self.start_corners[-1]
        else:
            p = (self.min_radius, 0.0)
            cp = self.start_corners[0]
        if points_are_close(p, cp, atol=0.5):
            return cp, True
        return p, False

    def get_end_airgap_corner(self):
        if self.is_inner:
            p = point(self.center, self.max_radius, self.alfa, ndec)
            cp = self.end_corners[-1]
        else:
            p = point(self.center, self.min_radius, self.alfa, ndec)
            cp = self.end_corners[0]
        if points_are_close(p, cp, atol=0.5):
            return cp, True
        return p, False

    def get_start_airgap_corner_point(self):
        p, b = self.get_start_airgap_corner()
        return Point(p)

    def get_end_airgap_corner_point(self):
        p, b = self.get_end_airgap_corner()
        return Point(p)

    def get_airgap_radius(self):
        if self.is_inner:
            return self.max_radius
        if self.is_outer:
            return self.min_radius
        return None

    def get_opposite_radius(self):
        if self.is_inner:
            return self.min_radius
        if self.is_outer:
            return self.max_radius
        return None

    def area_size(self):
        pts = [p for p in self.start_corners]
        end_pts = [p for p in reversed(self.end_corners)]
        return area_size(pts + end_pts)

    def repair_hull_line(self, center, angle, corners, with_center, rtol=None, atol=None):
        # We need to set our own tolerance range
        # to find the right points
        if not rtol:
            rtol = 1e-3
        if not atol:
            atol = 1e-3

        logger.debug("begin repair_hull_line(center=%s, angle=%s)", center, angle)

        if len(corners) < 2:
            # no hull without more than 1 corners
            logger.debug('end of repair_hull_line: only %s corners: EXIT',
                         len(corners))
            return

        [c.set_keep_node() for c in corners if c.is_equal(center, rtol, atol)]
        for p1, p2, data in [e for e in self.g.edges(data=True)]:
            clist_p1 = [c for c in corners if c.is_equal(p1, 0.0, 1e-7)]
            clist_p2 = [c for c in corners if c.is_equal(p2, 0.0, 1e-7)]
            if len(clist_p1) > 1:
                logger.warning("WARNING in repair_hull_line(): %s corners and p1 close together",
                               len(clist_p1))
                logger.warning("        p1 = %s, p2 = %s", p1, p2)
            if len(clist_p2) > 1:
                logger.warning("WARNING in repair_hull_line(): %s corners and p2 close together",
                               len(clist_p2))
                logger.warning("        p2 = %s, p1 = %s", p2, p1)

            if clist_p1 and clist_p2:
                # Both points are in the hull
                el = data['object']
                if isinstance(el, Line):
                    logger.debug("remove Line: %s <> %s", p1, p2)
                    self._remove_edge(p1, p2)
                else:
                    [corner.set_keep_node() for corner in clist_p1]
                    [corner.set_keep_node() for corner in clist_p2]
                    if isinstance(el, Arc):
                        alpha_start = el.startangle
                        alpha_end = el.endangle
                        alpha_mid = middle_angle(alpha_start, alpha_end)
                        self._remove_edge(p1, p2)
                        a1 = Arc(Element(center=el.center,
                                         radius=el.radius,
                                         start_angle=alpha_start*180/np.pi,
                                         end_angle=alpha_mid*180/np.pi))
                        a2 = Arc(Element(center=el.center,
                                         radius=el.radius,
                                         start_angle=alpha_mid*180/np.pi,
                                         end_angle=alpha_end*180/np.pi))
                        self.add_edge(p1, a1.node2(ndec), a1)
                        self.add_edge(a2.node1(ndec), p2, a2)
            else:
                clist = []
                if clist_p1:
                    clist = [c for c in clist_p1]
                elif clist_p2:
                    clist = [c for c in clist_p2]
                [corner.set_keep_node() for corner in clist]

        try:
            [self.g.remove_node(c.point())
             for c in corners if not c.keep_node()]
        except Exception as e:
            logger.warn("Warning: %s", e)

        # Rebuild Corner-list after correction
        center_added, corners = self.get_corner_list(center, angle, rtol, atol)
        for c in corners:
            logger.debug("Correct Corner: %s", c)

        if with_center:
            c_corner = Corner(center, tuple(center))
            if c_corner not in corners:
                corners.append(c_corner)

        if len(corners) > 1:
            corners.sort()
            p1 = corners[0].point()
            for c in corners[1:]:
                p2 = c.point()
                self.add_edge(p1, p2, Line(Element(start=p1, end=p2)))
                p1 = p2

        self.set_minmax_radius()
        logger.debug('end of repair_hull_line')

    def set_center(self, center):
        self.center = center
        self.set_minmax_radius()

    def set_minmax_radius(self):
        if not self.center:
            raise ValueError("FATAL ERROR: no center in Geometry")
        self.min_radius = 99999.0
        self.max_radius = 0.0
        for e in self.elements(Shape):
            min_dist, max_dist = e.minmax_from_center(self.center)
            self.min_radius = min(self.min_radius, min_dist)
            self.max_radius = max(self.max_radius, max_dist)

    def complete_hull_line(self, angle):
        logger.debug("begin complete_hull_line")
        if not self.center:
            raise ValueError("FATAL ERROR: no center in Geometry")

        center_added, corners = self.get_corner_list(self.center, angle)
        assert(corners)
        c_min = Corner(self.center, point(self.center, self.min_radius, angle, ndec))
        c_max = Corner(self.center, point(self.center, self.max_radius, angle, ndec))

        c_first = corners[0]
        if not c_min.is_same_corner(c_first):
            c_min.is_new_point = True
            p1 = c_min.point()
            p2 = c_first.point()
            self.add_edge(p1, p2, Line(Element(start=p1, end=p2)))

        c_last = corners[len(corners)-1]
        if not c_max.is_same_corner(c_last):
            c_max.is_new_point = True
            p2 = c_max.point()
            p1 = c_last.point()
            self.add_edge(p1, p2, Line(Element(start=p1, end=p2)))
        logger.debug("end complete_hull_line")
        return (c_min, c_max)

    def complete_hull_arc(self, startangle, startcorner,
                          endangle, endcorner, radius):
        nodes = self.radius_nodes(self.center, radius, 1e-04, 1e-04)

        if startcorner.is_new_point:
            start_p = startcorner.point()
            nodes_sorted = [(distance(start_p, n), n) for n in nodes
                            if not points_are_close(start_p, n)]
            nodes_sorted.sort()
            p = nodes_sorted[0][1]
            angle_p = alpha_line(self.center, p)
            self.add_edge(start_p, p, Arc(
                Element(center=self.center, radius=radius,
                        start_angle=startangle*180/np.pi,
                        end_angle=angle_p*180/np.pi)))

        if endcorner.is_new_point:
            end_p = endcorner.point()
            nodes_sorted = [(distance(end_p, n), n) for n in nodes
                            if not points_are_close(end_p, n)]
            inx = len(nodes_sorted)-1
            p = nodes_sorted[inx][1]
            angle_p = alpha_line(self.center, p)
            self.add_edge(p, end_p, Arc(
                Element(center=self.center, radius=radius,
                        start_angle=angle_p*180/np.pi,
                        end_angle=endangle*180/np.pi)))

    def get_corner_nodes(self, center, angle):
        rtol = 1e-4
        atol = 1e-4

        center_added, corners = self.get_corner_list(center, angle, rtol, atol)
        if len(corners) < 2:
            return ()  # not enough corners
        return (corners[0].point(), corners[len(corners)-1].point())

    def get_angle(self, alpha1, alpha2):
        if np.isclose(alpha1, alpha2, 0.001, 0.001):
            return 0.0
        return alpha_angle(alpha1, alpha2)

    def get_edge_neighbors_list(self, alpha, info):
        n1 = info['n1']
        n2 = info['n2']

        nbrs = [n for n in self.g.neighbors(n2)
                if not (points_are_close(n, n1) or points_are_close(n, n2))]
        if len(nbrs) == 0:
            logger.debug("      FATAL: no neighbors of %s available ???", n2)
            return []

        angles = []
        for c, n in enumerate(nbrs):
            info_next = self.get_edge_info(n2, n)
            angle = self.get_angle(alpha, info_next['alpha_start'])
            angles.append((angle, c, info_next))

        info_rev = self.get_reverse_edge_info(info)
        angle = self.get_angle(alpha, info_rev['alpha_start'])
        angles.append((angle, c+1, info_rev))
        angles.sort(reverse=True)
        return angles

    def is_lefthand_edge(self, alpha, info1, info2):
        logger.debug("   begin of is_lefthand_edge()")
        angle1 = self.get_angle(alpha, info1['alpha_start'])
        angle2 = self.get_angle(alpha, info2['alpha_start'])
        if not np.isclose(angle1, angle2, 0.005, 0.005):
            logger.debug("   UNEXPECTED DIFFERENT ANGLES")
            return angle1 > angle2

        alpha_start = info1['alpha_start']

        if self.is_edge_arc(info1):
            if self.is_edge_arc(info2):
                logger.debug("   ARC - ARC")

                i1_dist = distance(info1['n1'], info1['n2'])
                i2_dist = distance(info2['n1'], info2['n2'])
                min_dist = min(i1_dist, i2_dist) / 1.5

                circ = Circle(Element(center=info1['n1'],
                                      radius=min_dist))
                pt = info1['element'].intersect_circle(circ)
                if len(pt) != 1:
                    logger.debug("WARNING: intersect problem at %s",
                                 info1['n1'])
                    i1_alpha = info1['alpha_n2']
                else:
                    i1_alpha = alpha_line(info1['n1'], pt[0])
                i1_angle = self.get_angle(alpha_start, i1_alpha)

                circ = Circle(Element(center=info2['n1'],
                                      radius=min_dist))
                pt = info2['element'].intersect_circle(circ)
                if len(pt) != 1:
                    logger.debug("WARNING: intersect problem at %s",
                                 info2['n1'])
                    i2_alpha = info2['alpha_n2']
                else:
                    i2_alpha = alpha_line(info2['n1'], pt[0])
                i2_angle = self.get_angle(alpha_start, i2_alpha)

                rslt = normalise_angle(i1_angle) > normalise_angle(i2_angle)
                logger.debug("   end of is_lefthand_edge() = %s",
                             rslt)
                return rslt

            logger.debug("   ARC - LINE")

            e1 = info1['element']
            d2 = distance(e1.center, info2['n2'])
            if not np.isclose(e1.radius, d2, 0.005, 0.005):
                angle1 = self.get_angle(alpha, info1['alpha_n2'])
                angle = alpha_angle(angle1, angle2)
                logger.debug("   NOT close together")
                rslt = greater(angle, np.pi)
                logger.debug("   end of is_lefthand_edge() = %s", rslt)
                return rslt

            next_info2 = self.next_edge_lefthand_side(info2)
            if not next_info2:
                logger.debug("FATAL ERROR")
                raise ValueError("FATAL ERROR: no edge found")

            return self.is_lefthand_edge(alpha, info1, next_info2)

        if not self.is_edge_arc(info2):
            # two overlapping lines
            logger.debug("   end of is_lefthand_edge(): overlap")
            return True

        logger.debug("   LINE - ARC")

        rslt = not self.is_lefthand_edge(alpha, info2, info1)
        logger.debug("   end of is_lefthand_edge() = %s", rslt)
        return rslt

    def next_edge_lefthand_side(self, info_curr):  # current
        alpha = normalise_angle(info_curr['alpha_n2'] + np.pi)
        logger.debug("   next_edge_lefthand_side( alpha=%s )", alpha)

        nbrs = self.get_edge_neighbors_list(alpha, info_curr)
        if len(nbrs) == 0:
            logger.debug("      no neighbors available ???")
            return None  # unexpected end

        if len(nbrs) < 3:
            for a, c, info_next in nbrs:
                if not info_next['reverse']:
                    return info_next
            raise ValueError("FATAL ERROR in next_edge_lefthand_side() !!")

        logger.debug("   POINT WITH %s NEIGHBORS", len(nbrs)-1)

        f_angle, f_c, f_info_next = nbrs[0]
        f_info_next['angle'] = f_angle

        for n_angle, n_c, n_info_next in nbrs[1:]:
            n_info_next['angle'] = n_angle
            if np.isclose(f_angle, n_angle, 0.01, 0.01):
                logger.debug("   SAME DIRECTION")
                # ACHTUNG
                if self.is_lefthand_edge(alpha, f_info_next, n_info_next):
                    logger.debug("   == first is on the left side")
                    angle = self.get_angle(alpha,
                                           n_info_next['alpha_start'] - 0.01)
                    n_info_next['angle'] = angle
                else:
                    logger.debug("   == next is on the left side")
                    angle = self.get_angle(alpha,
                                           f_info_next['alpha_start'] - 0.01)
                    f_info_next['angle'] = angle

            f_angle = n_angle
            f_info_next = n_info_next

        nbrs2 = [(e['angle'], c, e) for a, c, e in nbrs
                 if not e['reverse']]
        nbrs2.sort(reverse=True)
        return nbrs2[0][2]

    def get_edge_info(self, n1, n2):
        e_dict = self.g.get_edge_data(n1, n2)
        if not e_dict:
            raise ValueError("Fatal: no edge-data found from {} to {}"
                             .format(n1, n2))

        e = e_dict.get('object', None)
        if not e:
            raise ValueError("Fatal: no object found from {} to {}"
                             .format(n1, n2))

        x = e.get_node_number(n1)
        alpha_n1 = e.get_alpha(n1)

        info = {'n1': n1,
                'n2': n2,
                'data': e_dict,
                'element': e,
                'x': x,
                'alpha_n1': alpha_n1,
                'alpha_n2': e.get_alpha(n2),
                'alpha_start': normalise_angle(alpha_n1 + np.pi),
                'tracked': e_dict.get(x, False),
                'reverse': False}
        return info

    def get_reverse_edge_info(self, info):
        alpha_n1 = info['alpha_n2']
        rev_info = {'n1': info['n2'],
                    'n2': info['n1'],
                    'data': info['data'],
                    'element': info['element'],
                    'x': 0,
                    'alpha_n1': alpha_n1,
                    'alpha_n2': info['alpha_n1'],
                    'alpha_start': normalise_angle(alpha_n1 + np.pi),
                    'tracked': False,
                    'reverse': True}
        return rev_info

    def is_edge_arc(self, info):
        return isinstance(info['element'], Arc)

    def log_edge_info(self, info):
        logger.debug('   node1 = %s', info['n1'])
        logger.debug('   node2 = %s', info['n2'])
        logger.debug('   x     = %s', info['x'])
        logger.debug('   lock  = (%s, %s, %s)',
                     info['data'].get(0, False),
                     info['data'].get(1, False),
                     info['data'].get(2, False))

    def set_edge_tracked(self, info):
        x = info['x']
        info['data'][x] = True  # footprint

    def get_new_area(self, start_n1, start_n2, solo):
        info_curr = self.get_edge_info(start_n1, start_n2)

        area = []
        result = {'area': area,
                  'elements': 1,
                  'msg': "<undefined>",
                  'reverse': False,
                  'ok': False}
        area.append(info_curr['element'])

        if info_curr['tracked']:
            result['msg'] = ("<== area already tracked (%s) ***",
                             info_curr['x'])
            result['area'] = None
            return result

        logger.debug('==> start of get_new_area()')
        self.log_edge_info(info_curr)
        self.set_edge_tracked(info_curr)

        e = info_curr['element']
        if (isinstance(e, Circle) and not isinstance(e, Arc)):
            result['msg'] = "area is a circle !!"
            logger.debug("<== %s", result['msg'])
            e_dict = info_curr['data']
            e_dict[1] = True  # footprint
            e_dict[2] = True  # footprint
            result['ok'] = True
            return result

        logger.debug("***** EDGE %s *****", 1)
        info_next = self.next_edge_lefthand_side(info_curr)
        if not info_next:
            result['msg'] = ("dead end ({}, {})"
                             .format(info_curr['n1'], info_curr['n2']))
            logger.debug("<== %s", result['msg'])
            return result
        self.log_edge_info(info_next)

        prev_n1 = info_curr['n1']
        next_n1 = info_next['n1']
        next_n2 = info_next['n2']

        alpha = normalise_angle(alpha_points(prev_n1,
                                             next_n1,
                                             next_n2))

        c = 1
        while not (nodes_are_equal(next_n1, start_n1) and
                   nodes_are_equal(next_n2, start_n2)):
            c += 1
            if c > self.num_edges * 2:
                logger.error("FATAL: *** over %s elements in area ? ***",
                             self.num_edges)
                plot_area(area)
                sys.exit(1)

            area.append(info_next['element'])

            if info_next['tracked']:
                result['msg'] = ("FATAL: area already tracked ({}) ***"
                                 .format(info_next['x']))
                logger.debug("<== %s", result['msg'])
                result['elements'] = c
                return result

            self.set_edge_tracked(info_next)

            info_curr = info_next
            logger.debug("***** EDGE %s *****", c)
            info_next = self.next_edge_lefthand_side(info_curr)
            if not info_next:
                result['msg'] = ("<== dead end ({},{})"
                                 .format(info_curr['n1'], info_curr['n2']))
                logger.debug("<== %s", result['msg'])
                result['elements'] = c
                return result
            self.log_edge_info(info_next)

            prev_n1 = info_curr['n1']
            next_n1 = info_next['n1']
            next_n2 = info_next['n2']

            a = normalise_angle(alpha_points(prev_n1,
                                             next_n1,
                                             next_n2))
            alpha += a

        logger.debug("  END OF get_new_area")

        if alpha < 0.0:
            result['msg'] = ("turn left expected, but it turned right ({})"
                             .format(alpha))
            logger.debug("<== %s", result['msg'])
            result['elements'] = c
            result['reverse'] = True
            return result

        result['msg'] = "area found !!"
        logger.debug("<== %s", result['msg'])
        result['elements'] = c
        result['ok'] = True
        return result

    def set_edge_attributes(self):
        if nxversion == 1:
            nx.set_edge_attributes(self.g, 0, True)
            nx.set_edge_attributes(self.g, 1, False)
            nx.set_edge_attributes(self.g, 2, False)
        else:
            nx.set_edge_attributes(self.g, True, 0)
            nx.set_edge_attributes(self.g, False, 1)
            nx.set_edge_attributes(self.g, False, 2)

    def create_list_of_areas(self, crunch=False):
        """ return list of areas for each node and their neighbors
        """
        if len(self.area_list) > 0:
            logger.debug("area list already available")
            # list already available
            return

        areabuilder = AreaBuilder(geom=self)
        areabuilder.create_list_of_areas(main=False)
        self.area_list = areabuilder.area_list
        return

        def append(area_list, a):
            for area in area_list:
                if area.is_identical(a):
                    return
            area_list.append(a)

        logger.debug("create new area list")
        self.set_edge_attributes()

        crunched = 0
        for n in self.g.nodes():
            if self.debug:
                print('.', end='', flush=True)

            finished = False
            while not finished:
                finished = True
                nbrs = [nbr for nbr in self.g.neighbors(n)]
                for next_n in nbrs:
                    result = self.get_new_area(n, next_n, len(nbrs) < 3)
                    if result['ok']:
                        area = result['area']
                        a = Area(area, self.center, 0.0)
                        logger.debug("Area %s found", a.identifier())
                        if crunch:
                            c = a.crunch_area(self)
                        else:
                            c = 0
                        append(self.area_list, a)
                        crunched += c
                        if c > 0:
                            # take care! may be there are new neighbors for n
                            finished = False
                            break

        logger.debug("%s areas found and %s elements concatenated",
                     len(self.area_list), crunched)

    def list_of_areas(self):
        self.create_list_of_areas()
        return self.area_list

    def remove_all_areas(self):
        self.create_list_of_areas()
        for area in self.area_list:
            area.remove_edges(self.g, ndec)

    def intersect_the_line(self, line, rtol=1e-04, atol=1e-04):
        for e in self.elements(Shape):
            pts = e.intersect_line(line, rtol, atol, False)
            if pts:
                return pts
        return []

    def the_point_is_inside(self, p, rtol=1e-04, atol=1e-04):
        for e in self.elements(Shape):
            if e.is_point_inside(p, rtol=rtol, atol=atol, include_end=True):
                # logger.info("point %s is inside %s", p, e)
                return True
        return False

    def copy_line(self, center, radius, start_angle, end_angle,
                  start_line, end_line, inner_circle, outer_circle, e,
                  rtol=1e-04,
                  atol=1e-04,
                  points_inner=None,
                  points_outer=None):
        """ Die Funktion kopiert die Teile einer Linie, welche sich in der
            durch die Parameter definierten Teilkreisfläche befinden.
        """
        assert(isinstance(e, Line))
        if is_same_angle(start_angle, end_angle):
            pts_inner = inner_circle.intersect_line(e,
                                                    rtol,
                                                    atol,
                                                    False)
            pts_outer = outer_circle.intersect_line(e,
                                                    rtol,
                                                    atol,
                                                    False)
            points = pts_inner + pts_outer + [e.p2]
        else:
            pts_start = e.intersect_line(start_line,
                                         rtol,
                                         atol,
                                         False)
            pts_end = e.intersect_line(end_line,
                                       rtol,
                                       atol,
                                       False)
            pts_inner = inner_circle.intersect_line(e,
                                                    rtol,
                                                    atol,
                                                    False)
            pts_outer = outer_circle.intersect_line(e,
                                                    rtol,
                                                    atol,
                                                    False)
            points = pts_start + pts_end + \
                pts_inner + pts_outer + [e.p2]

        if points_inner is not None and pts_inner:
            points_inner += pts_inner
        if points_outer is not None and pts_outer:
            points_outer += pts_outer

        new_elements = []
        sorted_points = []

        for p in points:
            dist = distance(e.p1, p)
            sorted_points.append((dist, p))
        sorted_points.sort()

        p1 = e.p1
        for x, p2 in sorted_points:
            pm = middle_point_of_line(p1, p2)
            if is_point_inside_region(pm, center,
                                      inner_circle.radius,
                                      outer_circle.radius,
                                      start_angle, end_angle):
                new_elements.append(Line(Element(start=p1, end=p2)))
            p1 = p2

        return new_elements

    def copy_arc(self, center, radius, start_angle, end_angle,
                 start_line, end_line, inner_circle, outer_circle, e,
                 rtol=1e-04,
                 atol=1e-04,
                 points_inner=None,
                 points_outer=None):
        """ Die Funktion kopiert die Teile eines Kreissegments, welche sich in der
            durch die Parameter definierten Teilkreisfläche befinden.
        """
        assert(isinstance(e, Arc))
        if is_same_angle(start_angle, end_angle):
            pts_inner = inner_circle.intersect_arc(e,
                                                   rtol,
                                                   atol,
                                                   False)
            pts_outer = outer_circle.intersect_arc(e,
                                                   rtol,
                                                   atol,
                                                   False)
            points = pts_inner + pts_outer + [e.p2]
        else:
            pts_start = e.intersect_line(start_line,
                                         rtol,
                                         atol,
                                         False)
            pts_end = e.intersect_line(end_line,
                                       rtol,
                                       atol,
                                       False)
            pts_inner = inner_circle.intersect_arc(e,
                                                   rtol,
                                                   atol,
                                                   False)
            pts_outer = outer_circle.intersect_arc(e,
                                                   rtol,
                                                   atol,
                                                   False)
            points = pts_start + pts_end + \
                pts_inner + pts_outer + [e.p2]

        if points_inner is not None and pts_inner:
            points_inner += pts_inner
        if points_outer is not None and pts_outer:
            points_outer += pts_outer

        new_elements = []
        sorted_points = []

        alpha_start = alpha_line(e.center, e.p1)

        for p in points:
            alpha_next = alpha_line(e.center, p)
            if less_equal(alpha_next, alpha_start):
                alpha_next += 2*np.pi
            sorted_points.append((alpha_next, p))
            alpha_start = alpha_next
        sorted_points.sort()

        p1 = e.p1
        alpha_start = alpha_line(e.center, e.p1)
        for x, p2 in sorted_points:
            alpha_end = alpha_line(e.center, p2)
            pm = middle_point_of_arc(e.center, e.radius, p1, p2, rtol=rtol, atol=atol)
            if is_point_inside_region(pm, center,
                                      inner_circle.radius,
                                      outer_circle.radius,
                                      start_angle, end_angle,
                                      rtol=rtol, atol=atol):
                if not (len(points) > 1 and
                        points_are_close(p1, p2, rtol=rtol, atol=atol)):
                    if len(points) == 1 and e.rtheta is not None:
                        a = Arc(Element(center=e.center,
                                        radius=e.radius,
                                        start_angle=alpha_start*180/np.pi,
                                        end_angle=alpha_end*180/np.pi,
                                        width=e.width,
                                        height=e.height,
                                        rtheta=e.rtheta,
                                        start_param=e.start_param,
                                        end_param=e.end_param))
                    else:
                        a = Arc(Element(center=e.center,
                                        radius=e.radius,
                                        start_angle=alpha_start*180/np.pi,
                                        end_angle=alpha_end*180/np.pi))
                    if points_are_close(a.p1, a.p2, rtol=1e-02, atol=1e-02):
                        logger.debug("ATTENTION: creation of a tiny arc")
                        a.set_attribute("tiny")
                    new_elements.append(a)
            alpha_start = alpha_end
            p1 = p2
        return new_elements

    def copy_circle(self, center, radius, start_angle, end_angle,
                    start_line, end_line, inner_circle, outer_circle, e,
                    rtol=1e-04,
                    atol=1e-04,
                    points_inner=None,
                    points_outer=None):
        """ Die Funktion kopiert die Teile eines Kreises, welche sich in der
            durch die Parameter definierten Teilkreisfläche befinden.
        """
        assert(isinstance(e, Circle))
        if is_same_angle(start_angle, end_angle):
            pts_inner = inner_circle.intersect_circle(e,
                                                      rtol,
                                                      atol,
                                                      False)
            pts_outer = outer_circle.intersect_circle(e,
                                                      rtol,
                                                      atol,
                                                      False)
            points = pts_inner + pts_outer
        else:
            pts_start = e.intersect_line(start_line,
                                         rtol,
                                         atol)
            pts_end = e.intersect_line(end_line,
                                       rtol,
                                       atol)
            pts_inner = inner_circle.intersect_circle(e,
                                                      rtol,
                                                      atol,
                                                      False)
            pts_outer = outer_circle.intersect_circle(e,
                                                      rtol,
                                                      atol,
                                                      False)
            points = pts_start + pts_end + pts_inner + pts_outer

        if points_inner is not None and pts_inner:
            points_inner += pts_inner
        if points_outer is not None and pts_outer:
            points_outer += pts_outer

        new_elements = []
        if len(points) < 2:
            if is_point_inside_region(e.p1, center,
                                      inner_circle.radius,
                                      outer_circle.radius,
                                      start_angle, end_angle):
                new_elements.append(
                    Circle(Element(center=e.center, radius=e.radius)))
            return new_elements

        sorted_points = []
        for p in points:
            alpha_p = alpha_line(e.center, p)
            sorted_points.append((alpha_p, p))
        sorted_points.sort()

        x, px = sorted_points[0]
        sorted_points.append((x, px))
        p1 = px
        alpha_start = alpha_line(e.center, p1)
        for x, p2 in sorted_points[1:]:
            alpha_end = alpha_line(e.center, p2)
            pm = middle_point_of_arc(e.center, e.radius, p1, p2, rtol=rtol, atol=atol)
            if is_point_inside_region(pm, center,
                                      inner_circle.radius,
                                      outer_circle.radius,
                                      start_angle, end_angle,
                                      rtol=rtol, atol=atol):
                a = Arc(Element(center=e.center,
                                radius=e.radius,
                                start_angle=alpha_start*180/np.pi,
                                end_angle=alpha_end*180/np.pi))
                new_elements.append(a)
            alpha_start = alpha_end
            p1 = p2
        return new_elements

    def copy_shape(self,
                   radius,
                   startangle,
                   endangle,
                   inner_radius,
                   outer_radius,
                   split=False,
                   rtol=0.0,
                   atol=0.0,
                   append_inner=False,
                   append_outer=False,
                   delete_appendices=False,
                   concatenate_tiny_el=False):
        """ Die Funktion kopiert die Teile von Shape-Objekten, welche sich in
            der durch die Parameter definierten Teilkreisfläche befinden.
        """
        logger.debug('begin copy_shape(%s, %s)', startangle, endangle)

        if not rtol:
            rtol = self.rtol
        if not atol:
            atol = self.atol
        rtol = 1e-5
        atol = 1e-4
        logger.debug(' -> rtol=%s,  atol=%s', rtol, atol)

        if is_same_angle(startangle, endangle):
            start_line = Line(
                Element(start=self.center,
                        end=point(self.center, radius+1, startangle)))
            end_line = Line(
                Element(start=self.center,
                        end=point(self.center, radius+1, startangle)))
        else:
            start_line = Line(
                Element(start=self.center,
                        end=point(self.center, radius+1, startangle)))
            end_line = Line(
                Element(start=self.center,
                        end=point(self.center, radius+1, endangle)))

        if np.isclose(normalise_angle(startangle),
                      normalise_angle(endangle), 0.0):
            inner_circle = Circle(Element(center=self.center, radius=inner_radius))
            outer_circle = Circle(Element(center=self.center, radius=outer_radius))
        else:
            inner_circle = Arc(Element(center=self.center, radius=inner_radius,
                                       start_angle=startangle*180/np.pi,
                                       end_angle=endangle*180/np.pi))
            outer_circle = Arc(Element(center=self.center, radius=outer_radius,
                                       start_angle=startangle*180/np.pi,
                                       end_angle=endangle*180/np.pi))

        new_elements = []
        pts_inner = [] if append_inner else None
        pts_outer = [] if append_outer else None

        for e in self.elements(Shape):
            if isinstance(e, Line):
                new_elements += self.copy_line(
                    self.center, radius, startangle, endangle,
                    start_line, end_line,
                    inner_circle, outer_circle, e,
                    rtol=rtol,
                    atol=atol,
                    points_inner=pts_inner,
                    points_outer=pts_outer)

            elif isinstance(e, Arc):
                new_elements += self.copy_arc(
                    self.center, radius, startangle, endangle,
                    start_line, end_line,
                    inner_circle, outer_circle, e,
                    rtol=rtol,
                    atol=atol,
                    points_inner=pts_inner,
                    points_outer=pts_outer)
            elif isinstance(e, Circle):
                new_elements += self.copy_circle(
                    self.center, radius, startangle, endangle,
                    start_line, end_line,
                    inner_circle, outer_circle, e,
                    rtol=rtol,
                    atol=atol,
                    points_inner=pts_inner,
                    points_outer=pts_outer)

        if pts_inner and len(pts_inner) > 1:
            pts_inner.sort(reverse=True)
            p1 = pts_inner[0]
            for p2 in pts_inner[1:]:
                start_angle = alpha_line(self.center, p1)
                end_angle = alpha_line(self.center, p2)
                arc = Arc(Element(center=self.center,
                                  radius=inner_radius,
                                  start_angle=start_angle*180/np.pi,
                                  end_angle=end_angle*180/np.pi))
                new_elements.append(arc)
                p1 = p2

        if pts_outer and len(pts_outer) > 1:
            pts_outer.sort(reverse=True)
            p1 = pts_outer[0]
            for p2 in pts_outer[1:]:
                start_angle = alpha_line(self.center, p1)
                end_angle = alpha_line(self.center, p2)
                arc = Arc(Element(center=self.center,
                                  radius=outer_radius,
                                  start_angle=start_angle*180/np.pi,
                                  end_angle=end_angle*180/np.pi))
                new_elements.append(arc)
                p1 = p2

        if concatenate_tiny_el:
            ok, new_elements = self.concatenate_tiny_elements(new_elements)
            if ok:
                split = True

        if delete_appendices:
            center = []
        else:
            center = self.center

        if split:
            logger.debug('new Geometry with split')
            geom = Geometry(new_elements,
                            center=center,
                            rtol=self.rtol,
                            atol=self.atol,
                            is_inner=self.is_inner,
                            is_outer=self.is_outer,
                            split=split)
        else:
            geom = Geometry(new_elements,
                            center=center,
                            rtol=self.rtol,
                            atol=self.atol,
                            is_inner=self.is_inner,
                            is_outer=self.is_outer)

        if delete_appendices:
            geom.delete_all_appendices()
            geom.set_center(self.center)
        logger.debug('end copy_shape')
        return geom

    def copy_all_elements(self, alpha):
        if alpha == 0.0:
            T = None
        else:
            T = np.array(((np.cos(alpha), -np.sin(alpha)),
                          (np.sin(alpha), np.cos(alpha))))

        all_el = []
        lines = 0
        arcs = 0
        circles = 0
        el = None
        for e in self.elements(Shape):
            if isinstance(e, Line):
                lines += 1
                el = Line(Element(start=e.p1,
                                  end=e.p2))
            elif isinstance(e, Arc):
                arcs += 1
                alpha_start = alpha_line(e.center, e.p1)
                alpha_end = alpha_line(e.center, e.p2)
                el = Arc(Element(center=e.center,
                                 radius=e.radius,
                                 start_angle=alpha_start*180/np.pi,
                                 end_angle=alpha_end*180/np.pi))
            elif isinstance(e, Circle):
                circles += 1
                el = Circle(Element(center=e.center,
                                    radius=e.radius))
            else:
                el = None
            if el is not None:
                if T is not None:
                    el.transform(T, alpha, ndec)
                all_el.append(el)

        logger.debug("copy_all_elements: %s lines, %s arcs, %s circles",
                     lines, arcs, circles)

        return all_el

    def new_clone(self, new_elements, split=False):
        return Geometry(new_elements,
                        center=self.center,
                        rtol=self.rtol,
                        atol=self.atol,
                        is_inner=self.is_inner,
                        is_outer=self.is_outer,
                        split=split)

    def is_new_angle(self, alpha_list, alpha):
        for a in alpha_list:
            if np.isclose(a, alpha):
                return False
        return True

    def concatenate_arc_elements(self, el, elements):
        if not is_Arc(el):
            return False

        def match(e1, e2):
            if e2.has_attribute("del"):
                return False
            if e2.has_attribute("tiny"):
                return False
            if not points_are_close(e1.center, e2.center):
                return False
            return np.isclose(e1.radius, e2.radius)

        elmts = [(e.p1, e) for e in elements if is_Arc(e) and match(el, e)]
        elmts.sort()

        ok = False
        for p, e in elmts:
            el_new = el.concatenate(None, None, e)
            if el_new:
                el.set_attribute("del")
                e.set_attribute("del")
                elements.append(el_new)
                el = el_new
                ok = True
        return ok

    def concatenate_line_elements(self, el, elements):
        if not is_Line(el):
            return False

        def match(e1, e2):
            if e2.has_attribute("del"):
                return False
            if e2.has_attribute("tiny"):
                return False
            return np.isclose(e1.m(999999.0), e2.m(999999.0))

        elmts = [(e.p1, e) for e in elements if is_Line(e) and match(el, e)]
        elmts.sort()

        ok = False
        for p, e in elmts:
            el_new = el.concatenate(None, None, e)
            if el_new:
                el.set_attribute("del")
                e.set_attribute("del")
                elements.append(el_new)
                el = el_new
                ok = True
        return ok

    def concatenate_tiny_elements(self, new_elements):
        logger.debug("begin concatenate_tiny_elements")
        tiny_elements = [e for e in new_elements if e.has_attribute("tiny")]
        if not tiny_elements:
            logger.debug("end concatenate_tiny_elements: (%s elements)", 0)
            return False, new_elements

        count = 0
        for e_tiny in tiny_elements:
            if is_Line(e_tiny):
                if self.concatenate_line_elements(e_tiny, new_elements):
                    count += 1
            elif is_Arc(e_tiny):
                if self.concatenate_arc_elements(e_tiny, new_elements):
                    count += 1

        new_list = [e for e in new_elements if not e.has_attribute("del")]
        logger.debug("end concatenate_tiny_elements: (%s elements)", count)
        return count>0, new_list

    def find_symmetry(self, radius,
                      startangle, endangle, sym_tolerance):
        arealist = self.list_of_areas()
        logger.debug("begin of find_symmetry: - %s areas available", len(arealist))
        if len(arealist) == 0:
            return False

        arealist.sort()

        def add(areas, a):
            if not a.is_circle():
                for area in areas:
                    if area.is_equal(a, sym_tolerance):
                        area.increment(a)
                        return
            areas.append(a)

        arealist_match = []
        for a in arealist:
            a.sym_tolerance = sym_tolerance
            add(arealist_match, a)

        for a in arealist_match:
            a.set_delta()
        arealist_match.sort()

        arealist_sym = [a for a in arealist_match if a.symmetry > 0]
        if not arealist_sym:
            logger.debug("end of find_symmetry: No symmetry-axis found (delta == 0.0)")
            return False

        ggt = arealist_sym[0].symmetry
        for a in arealist_sym[1:]:
            if ggt != a.symmetry:
                ggt = gcd(ggt, a.symmetry)
                if ggt == 1:
                    logger.warning("asymmetrical iteration of areas detected")
                    break

                if ggt != a.symmetry:
                    logger.warning("unhandled asymmetry")
                    break

        arealist_ok = [a for a in arealist_sym if a.symmetry == ggt]
        midlist = {}
        for a in arealist_ok:
            mid = round(a.start, 3)
            if midlist.get(mid, None) is None:
                midlist[mid] = [1, a]
            else:
                midlist[mid][0] = midlist[mid][0]+1

        arealist_srt = [[v[0], k, v[1]] for k, v in midlist.items()]
        arealist_srt.sort(reverse=True)

        if not arealist_srt:
            logger.debug("end of find_symmetry: no sorted arealist")
            return False

        area = arealist_srt[0][2]
        sym = area.symmetry
        area.delta = 2*np.pi/sym
        self.sym_slices = sym
        self.sym_slice_angle = area.delta

        for alpha in area.symmetry_lines(startangle, endangle):
            p = point(self.center, radius+5, alpha)
            line = Line(Element(start=self.center, end=p))
            self.add_cut_line(line)

        self.sym_area = area
        return True

    def has_symmetry_area(self):
        return self.sym_area is not None

    def symmetry_startangle(self):
        return self.sym_area.sym_startangle

    def symmetry_endangle(self):
        return self.sym_area.sym_endangle

    def get_symmetry_copies(self):
        if self.sym_counterpart == 0:
            return int(self.sym_part)

        x = gcd(self.sym_part, self.sym_counterpart)
        return int(self.sym_part / x - 1)

    def is_mirrored(self):
        return len(self.mirror_corners) > 0

    def winding_is_mirrored(self):
        return self.wdg_is_mirrored

    def get_alfa(self):
        if self.is_mirrored():
            return 2*self.alfa
        else:
            return self.alfa

    def __str__(self):
        real_alfa = 0
        if self.sym_part > 0:
            if self.is_mirrored():
                real_alfa = np.pi / self.sym_part
            else:
                real_alfa = 2*np.pi / self.sym_part
        return "name...........: {}\n".format(self._name) + \
               "kind...........: {}\n".format(self.kind) + \
               "sym_part.......: {}\n".format(self.sym_part) + \
               "sym_counterpart: {}\n".format(self.sym_counterpart) + \
               "alpha..........: {}\n".format(self.alfa) + \
               "alpha real.....: {}\n".format(real_alfa) + \
               "circle.........: {}\n".format(self.alfa * self.sym_part) + \
               "mirrored.......: {}\n".format(self.is_mirrored()) + \
               "radius.........: {} -- {}\n".format(self.min_radius,
                                                    self.max_radius)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
                self.__dict__ == other.__dict__)

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

    def __hash__(self):
        """Override the default hash behavior
        (that returns the id or the object)"""
        return hash(tuple(sorted(self.__dict__.items())))

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    def minmax(self):
        """ find min and max coordinates of all shapes
            ([<min-x>, <max-x>, <min-y>, <max-y>])
        """
        mm = [99999, -99999, 99999, -99999]

        for e in self.elements(Shape):
            n = e.minmax()
            mm[0] = min(mm[0], n[0])
            mm[1] = max(mm[1], n[1])
            mm[2] = min(mm[2], n[2])
            mm[3] = max(mm[3], n[3])

        return mm

    def add_cut_line(self, e):
        self.cut_lines.append(e)

    def clear_cut_lines(self):
        self.cut_lines = []

    def render_cut_lines(self, renderer):
        for e in self.cut_lines:
            e.render(renderer, 'darkred')

    def render_airgaps(self, renderer):
        for g in self.airgaps:
            if isinstance(g, Arc):
                renderer.arc(g.startangle, g.endangle,
                             g.center, g.radius,
                             color='red')
            elif isinstance(g, Circle):
                renderer.circle(g.center, g.radius,
                                color='red')
            elif isinstance(g, Line):
                renderer.line(g.p1, g.p2,
                              color='red')
            elif isinstance(g, Point):
                renderer.point(g.p1, 'o', color='red')

    def render_neighbors(self, renderer):
        for n in self.g.nodes():
            nbr_list = [nbr for nbr in self.g.neighbors(n)]
            if len(nbr_list) == 1:
                renderer.point(n, 'o', color='orange')
            elif len(nbr_list) == 2:
                renderer.point(n, 'o', color='green')
            elif len(nbr_list) == 3:
                renderer.point(n, 'o', color='red')
            elif len(nbr_list) == 4:
                renderer.point(n, 'o', color='blue')
            elif len(nbr_list) > 4:
                renderer.point(n, 'o', color='black')

    def render_area_fill(self, renderer):
        legend = {}
        for area in self.list_of_areas():
            if area.is_iron():
                area.render_fill(renderer)
                if area.name() and area.name() not in legend:
                    legend[area.name()] = area.render_legend(renderer)
            if area.is_shaft():
                area.render_fill(renderer)
                if area.name() and area.name() not in legend:
                    legend[area.name()] = area.render_legend(renderer)

        for area in self.list_of_areas():
            if area.is_air():
                area.render_fill(renderer)

        # magnet has no air inside
        for area in self.list_of_areas():
            if area.is_magnet():
                area.render_fill(renderer)
                if area.name() and area.name() not in legend:
                    legend[area.name()] = area.render_legend(renderer)

        # winding has no air inside
        for area in self.list_of_areas():
            if area.is_winding():
                area.render_fill(renderer)
                if area.name() and area.name() not in legend:
                    legend[area.name()] = area.render_legend(renderer)

        if legend:
            return [h for (k, h) in legend.items()]
        return []

    def get_points_in_iron(self):
        points = []
        for area in self.list_of_areas():
            p = area.get_point_inside(self)
            if p:
                points.append(p)
        return points

    def check_hull(self, radius, x, y, rtol, atol):
        node_count = 0
        miss_count = 0
        for h in convex_hull(self.virtual_nodes()):
            dist = distance(self.center, h)
            node_count += 1

            if not np.isclose(dist, radius, rtol, atol):
                if x is not None:
                    if np.isclose(x, h[0], rtol, atol):
                        continue
                if y is not None:
                    if np.isclose(y, h[1], rtol, atol):
                        continue
                miss_count += 1
        return miss_count == 0

    def get_machine(self):
        mm = self.minmax()
        height = mm[3]-mm[2]
        width = mm[1]-mm[0]
        atol = 3.0

        logger.debug("*** Begin of get_machine() ***")
        if np.isclose(height, width, self.rtol, self.atol):
            radius = width/2
            self.set_center([mm[1]-radius, mm[3]-radius])
            logger.info("check for full machine")
            if self.check_hull(radius, None, None, self.rtol, atol):
                logger.info(" - it is full")
                return Machine(self,
                               radius=radius,
                               startangle=0.0,
                               endangle=0.0)

            logger.info("check for quarter machine")
            radius = width
            self.set_center([mm[0], mm[2]])
            if self.check_hull(radius, mm[0], mm[2], self.rtol, atol):
                logger.info(" - it is a quarter")
                return Machine(self,
                               radius=radius,
                               startangle=0.0,
                               endangle=np.pi/2)

        elif np.isclose(width, height*2, self.rtol, self.atol):
            radius = width/2
            self.set_center([mm[1]-height, mm[2]])
            logger.info("check for half machine")
            if self.check_hull(radius, None, mm[2], self.rtol, atol):
                logger.info(" - it is a half")
                return Machine(self,
                               radius=radius,
                               startangle=0.0,
                               endangle=np.pi)

            self.set_center([mm[1]-height, mm[3]])
            if self.check_hull(radius, None, mm[3], self.rtol, atol):
                logger.info(" - it is a half")
                return Machine(self,
                               radius=radius,
                               startangle=np.pi,
                               endangle=0.0)

        elif np.isclose(width*2, height, self.rtol, self.atol):
            radius = width
            logger.info("check for half machine")
            self.set_center([mm[1], mm[3]-width])
            if self.check_hull(radius, mm[1], None, self.rtol, atol):
                logger.info(" - it is a half")
                return Machine(self, radius, np.pi/2.0, -np.pi/2.0)

            self.set_center([mm[0], mm[3]-width])
            if self.check_hull(radius, mm[0], None, self.rtol, atol):
                logger.info(" - it is a half")
                return Machine(self,
                               radius=radius,
                               startangle=-np.pi/2.0,
                               endangle=np.pi/2.0)

        machine = self.get_machine_part(mm)
        if machine:
            logger.info(" - it is 1/%s of a machine", machine.part)
            return machine

        logger.info("The shape of the Machine is unexpected")
        self.center = [0.0, 0.0]
        return Machine(self)

    def get_same_center(self, center_lst, center, rtol, atol):
        for c in center_lst:
            if points_are_close(c[1], center, rtol, atol):
                return c
        return None

    def get_machine_part(self, mm):
        logger.debug("*** Begin of get_machine_part() ***")

        h_points = [h for h in convex_hull(self.virtual_nodes())]
        center = self.get_center(h_points, mm)
        logger.debug(" - Center is %s", center)

        min_radius = 99999
        max_radius = 0
        startangle = 999.0
        endangle = -999.0

        for h in h_points:
            if not points_are_close(center, h, rtol=1e-02, atol=1e-03):
                angle = alpha_line(center, [round(h[0], 4), round(h[1], 4)])
                if angle < 0.0:
                    logger.debug(" - strange point %s", h)
                    logger.debug(" - hull-node %s ==> angle = %s", h, angle)
                startangle = min(startangle, angle)
                endangle = max(endangle, angle)

            dist = distance(center, h)
            min_radius = min(min_radius, dist)
            max_radius = max(max_radius, dist)

        center_left = round(center[0] - mm[0], 4)
        center_right = round(mm[1] - center[0], 4)
        center_down = round(center[1] - mm[2], 4)
        center_up = round(mm[3] - center[1], 4)

        min_r = min(center_left, center_right, center_up, center_down)
        max_r = max(center_left, center_right, center_up, center_down)

        logger.debug(" - startangle: %f12", startangle)
        logger.debug(" - endangle  : %f12", endangle)
        x = part_of_circle(startangle, endangle)
        logger.debug(" - slice     : 1/%d", x)

        logger.debug(" - center left : %f12", center_left)
        logger.debug(" - center right: %f12", center_right)
        logger.debug(" - center down : %f12", center_down)
        logger.debug(" - center up   : %f12", center_up)

        if x > 0:
            # it looks pretty good
            logger.debug(" - slice is 1/%d: EXIT", x)
            self.set_center([round(center[0], 8), round(center[1], 8)])
            M = Machine(self,
                        radius=max_radius,
                        startangle=startangle,
                        endangle=endangle)
            logger.debug("*** End of get_machine_part(): ok ***")
            return M

        if less_equal(center_left, 0.0) or less_equal(center_right, 0.0) or \
           less_equal(center_up, 0.0) or less_equal(center_down, 0.0):
            if not np.isclose(center_left, center_right):
                x = part_of_circle(startangle, endangle)

                if x > 2:
                    logger.debug(" - slice is 1/%d: EXIT", x)
                    self.set_center([round(center[0], 8), round(center[1], 8)])
                    return Machine(self,
                                   radius=max_radius,
                                   startangle=startangle,
                                   endangle=endangle)

        if min_radius >= max_radius*0.9 and min_r >= max_r*0.9:
            # Mit 10 % Abweichungen gehen wir noch von einem ganzen Motor aus.
            self.set_center([round(center[0], 8), round(center[1], 8)])
            return Machine(self,
                           radius=max(max_radius, max_r),
                           startangle=0.0,
                           endangle=0.0)

        if np.isclose(center_down, 0.0):
            min_r = min(center_left, center_right, center_up)
            if min_r >= max_r*0.9:
                # Vermutlich ein halber Motor
                self.set_center([round(center[0], 8), round(center[1], 8)])
                return Machine(self,
                               radius=max(max_radius, max_r),
                               startangle=0.0,
                               endangle=np.pi)

            if np.isclose(center_left, 0.0):
                min_r = min(center_right, center_up)
                if min_r >= max_r*0.9:
                    # Vermutlich ein viertel Motor
                    self.set_center([round(center[0], 8), round(center[1], 8)])
                    return Machine(self,
                                   radius=max(max_radius, max_r),
                                   startangle=0.0,
                                   endangle=np.pi/2)

        # TODO: handle half and quarter machines

        if np.isclose(center_left, center_right):
            # Der x-Wert des Center scheint zu stimmen.
            # Eine Symmetrie an der y-Achse ist möglich.
            # Dem y-Wert ist nicht zu trauen!
            if center_down > 0.0:
                # This center is too high.
                nodes = [n for n in convex_hull(
                    self.g.nodes()) if n[0] > center[0]]
                assert(nodes)
                p = nodes[0]
                for n in nodes[1:]:
                    if n[1] < p[1]:
                        p = n

                m_min = 99999.0
                for n in nodes:
                    m = line_m(p, n)
                    if m and m > 0.0:
                        m_min = min(m_min, m)

                y = line_n([p[0]-center[0], p[1]], m_min)
                center[1] = y
                angle = alpha_line(center, p)

        self.set_center([round(center[0], 8), round(center[1], 8)])
        return Machine(self,
                       radius=max_radius,
                       startangle=angle,
                       endangle=np.pi-angle)

    def get_center_xaxis(self, points):
        y_list = [(round(p[1], 3), p) for p in points]
        y_list.sort()
        center_y = y_list[0][0]
        eq_list = [y for y, p in y_list[1:] if np.isclose(center_y, y)]
        if len(eq_list) < 2:  # min 3 Points
            return (None, None)
        start_line = Line(Element(start=(-1e+8, center_y), end=(1e+8, center_y)))
        start_m = start_line.m()
        logger.debug("Startline(%s, %s)", start_line.p1, start_line.p2)
        neq_list = [(y, p) for y, p in y_list if not np.isclose(center_y, y)]
        if len(neq_list) < 2:
            return (None, center_y)
        center_x_list = []
        for inx in range(len(neq_list)-1):
            y0, p0 = neq_list[inx]
            for y, p in neq_list[inx+1:]:
                end_line = Line(Element(start=p0, end=p))
                end_m = end_line.m()
                logger.debug("Endline(%s, %s)", end_line.p1, end_line.p2)
                if end_m is None:
                    continue
                if np.isclose(start_m, end_m):
                    continue
                p = lines_intersect_point(start_line.p1, start_m, start_line.n(start_m),
                                          end_line.p1, end_m, end_line.n(end_m))
                if p:
                    center_x_list.append(round(p[0], 2))
        center_x_list.sort()
        logger.debug("Possible center x: %s", center_x_list)
        x0 = center_x_list[0]
        c = 0
        x_list = []
        for x in center_x_list[1:]:
            if np.isclose(x0, x):
                c += 1
            else:
                x_list.append((c, x0))
                x0 = x
                c = 0
        x_list.append((c, x0))
        x_list.sort(reverse=True)
        c, center_x = x_list[0]
        if c < 3:
            center_x = None
        else:
            if (c*100 / len(neq_list)) < 10:
                center_x = None
        logger.debug("Best Center(%s, %s)", center_x, center_y)
        return (center_x, center_y)

    def get_center_hull(self, points):
        p1 = points[0]
        points.append(p1)
        p2 = points[1]
        a1 = alpha_line(p1, p2)

        logger.debug(" - p1 = %s", p1)
        logger.debug(" - p2 = %s", p2)

        lines = []
        for p in points[2:]:
            logger.debug(" - pn = %s", p)
            a2 = alpha_line(p2, p)
            if not np.isclose(a1, a2):
                d = distance(p1, p2)
                logger.debug(" - d = %s: p1/p2 = %s/%s", d, p1, p2)
                lines.append([d, a1, p1, p2])
                p1 = p2
                a1 = a2
            p2 = p

        d = distance(p1, p2)
        logger.debug(" - d = %s: p1/p2 = %s/%s", d, p1, p2)
        lines.append([d, a1, p1, p2])

        if np.isclose(lines[0][1], lines[-1][1]):
            lines[0][0] += lines[-1][0]  # distance
            lines[0][2] = lines[-1][2]   # start point
            del lines[-1]

        lines.sort(reverse=True)
        for l in lines:
            logger.debug(" - Line %s", l)

        l1 = Line(Element(start=lines[0][2], end=lines[0][3]))
        l2 = Line(Element(start=lines[1][2], end=lines[1][3]))
        center = l1.intersect_line(l2, all=True)
        logger.debug("End of get_center: %s", center)
        if center:
            return center[0]
        return None

    def get_center_arcs(self):
        center_list = []
        for e in self.elements(Arc):
            center = (round(e.center[0], 3), round(e.center[1], 3))
            radius = round(e.radius, 1)
            c = self.get_same_center(center_list, center, self.rtol, self.atol)
            if c is None:
                center_list.append(([1], center, [radius]))
            else:
                c[0][0] += 1
                if radius not in c[2]:
                    c[2].append(radius)

        center = None
        arc_list = [[len(c[2]), c[0][0], c[1]] for c in center_list]
        arc_list.sort(reverse=True)

        if arc_list:
            c1 = arc_list[0]
            center = c1[2]
            if len(arc_list) > 1:
                c2 = arc_list[1]
                if not c1[0] > c2[0]:
                    center = None
        return center

    def get_center_dim(self, mm):
        return (round(mm[0], 4), round(mm[2], 4))

    def get_center(self, points, mm):
        logger.debug("Begin of get_center(%s points)", len(points))
        if len(points) < 3:
            return None

        center = None
        center_arcs = self.get_center_arcs()

        if center_arcs:
            center = center_arcs
        else:
            # Wir finden keine Arc-Objekte, welche uns einen Hinweis auf den
            # Center geben können. Wir versuchen in der Verzweiflung mit
            # center_hull oder x(min) und y(min)
            center_hull = self.get_center_hull(points)
            if center_hull:
                center = center_hull
            else:
                center = self.get_center_dim(mm)

        center_xaxis = self.get_center_xaxis(points)
        y = center_xaxis[1]
        if y is not None:
            if np.isclose(y, center[1], atol=0.3):
                center = (center[0], y)
        logger.debug("End of get_center ==> %s", center)
        return center

    def is_new_radius(self, radius_list, radius):
        for r, d in radius_list:
            if np.isclose(r, radius):
                return False
        return True

    def is_airgap(self, center, radius, startangle, endangle, circle, atol):
        """ Die Funktion untersucht, ob sich der Parameter circle in einem
            Luftspalt befindet.
        """
        ok = True
        borders = 0
        for e in self.elements(Shape):
            for p in e.intersect_circle(circle, 0.0, atol, True):
                if not self.is_border_line(center,
                                           startangle, endangle,
                                           e, atol):
                    logger.warning("BAD: Point %s", p)
                    self.airgaps.append(Point(p))
                    self.airgaps.append(e)
                    ok = False
                else:
                    borders += 1
        return (ok, borders)

    def is_border_line(self, center, startangle, endangle, e, atol):
        if isinstance(e, Line):
            if np.isclose(startangle, endangle):
                return False  # full

            if points_are_close(center, e.p1):
                angle_p2 = alpha_line(center, e.p2)
                if np.isclose(startangle, angle_p2, 1e-3, atol):
                    return True
                return np.isclose(endangle, angle_p2, 1e-3, atol)

            if points_are_close(center, e.p2):
                angle_p1 = alpha_line(center, e.p1)
                if np.isclose(startangle, angle_p1, 1e-3, atol):
                    return True
                return np.isclose(endangle, angle_p1, 1e-3, atol)

            angle_p1 = alpha_line(center, e.p1)
            if np.isclose(startangle, angle_p1, 1e-3, atol):
                angle_p2 = alpha_line(center, e.p2)
                return np.isclose(startangle, angle_p2, 1e-3, atol)

            if np.isclose(endangle, angle_p1, 1e-3, atol):
                angle_p2 = alpha_line(center, e.p2)
                return np.isclose(endangle, angle_p2, 1e-3, atol)
        return False

    def get_gaplist(self, center):
        gaplist = []
        for e in self.elements(Shape):
            gaplist += [e.minmax_from_center(center)]
        gaplist.sort()

        airgaps = []
        dist_max = 0.0
        for g in gaplist:
            if not less_equal(g[0], dist_max):
                airgaps.append((dist_max, g[0]))
            dist_max = max(dist_max, g[1])
        return airgaps

    def detect_airgaps(self, center, startangle, endangle, atol=0.1, with_end=False):
        """ Die Funktion sucht Luftspalt-Kandidaten und liefert eine Liste
            von Möglichkeiten mit jeweils einem minimalen und einem maximalen
            Radius als Begrenzung des Luftspalts.
        """
        gaplist = []
        for e in self.elements(Shape):
            if not self.is_border_line(center, startangle, endangle, e, atol):
                gaplist += [e.minmax_from_center(center)]
            else:
                min_r, max_r = e.minmax_from_center(center)
                if with_end and np.isclose(min_r, 0.0):
                    gaplist += [(0.0, 0.0)]

        gaplist.sort()

        min_radius = gaplist[0][0] + 1
        max_radius = gaplist[-1][1] - 1
        cur_radius = gaplist[0][1]
        airgaps = []

        if with_end:
            if self.is_inner:
                min_radius = gaplist[0][0] - 1
            else:
                max_radius = gaplist[-1][1] + 1

        for g in gaplist:
            if greater(g[0], cur_radius) and \
               greater(cur_radius, min_radius) and \
               less(g[0], max_radius):
                airgaps.append((cur_radius, g[0]))

            cur_radius = max(cur_radius, g[1])

        return airgaps

    def get_circles(self, center, radius):
        return [c for c in self.elements(Circle)
                if points_are_close(center, c.center) and
                np.isclose(radius, c.radius)]

    def delete_circle(self, center, radius):
        for c in self.elements(Circle):
            if points_are_close(center, c.center):
                if np.isclose(radius, c.radius):
                    logger.info("Center circle removed")
                    self.remove_edge(c)
                    return

    def alpha_of_circles(self, circles, center):
        angle = 0.0
        for c in circles:
            if isinstance(c, Arc):
                alpha_c_p1 = alpha_line(center, c.p1)
                alpha_c_p2 = alpha_line(center, c.p2)
                angle += alpha_angle(alpha_c_p1, alpha_c_p2)
            else:
                angle = 2*np.pi
        return angle

    def delete_airgap_circle(self, center,
                             lower_radius,
                             radius,
                             upper_radius,
                             angle_tot):
        lower_circles = self.get_circles(center, lower_radius)
        angle_sum = self.alpha_of_circles(lower_circles, center)
        if angle_sum / angle_tot < 0.5:
            return False

        upper_circles = self.get_circles(center, upper_radius)
        angle_sum = self.alpha_of_circles(upper_circles, center)
        if angle_sum / angle_tot < 0.5:
            return False

        self.remove_edges(self.get_circles(center, radius))
        return True

    def set_areas_inside_for_all_areas(self):
        logger.debug("begin set_areas_inside_for_all_areas")
        for area in self.list_of_areas():
            areas_inside = [a for a in self.area_list
                            if area.is_inside(a, self)]
            if not areas_inside:
                continue

            areas_notouch = {a.identifier(): a for a in areas_inside
                             if not area.has_connection(self, a, ndec)}
            area.areas_inside = areas_notouch

        for area in self.list_of_areas():
            logger.debug(" Inside %s is:", area.identifier())
            nested = [id for id in area.list_of_nested_areas_inside()]
            for id in nested:
                logger.debug(" -- remove %s inside %s", id, area.identifier())
                if area.areas_inside.get(id, None):
                    del area.areas_inside[id]
                else:
                    logger.warning("   %s already removed ?!", id)

        # for area in self.list_of_areas():
        #    logger.info("Inside %s is:", area.identifier())
        #    for id in area.areas_inside:
        #        logger.info(" ++ %s", id)
        logger.debug("end set_areas_inside_for_all_areas")

    def get_minmax_magnet(self):
        logger.debug("get_minmax_magnet")
        maglist = [a for a in self.list_of_areas() if a.is_magnet()]
        min_r = 9999
        max_r = -9999
        for m in maglist:
            min_r = min(min_r, m.min_dist)
            max_r = max(max_r, m.max_dist)
        return min_r, max_r

    def create_auxiliary_lines(self, rightangle, leftangle):
        logger.debug("begin of create_auxiliary_lines")
        self.set_areas_inside_for_all_areas()

        logger.debug("-> start create_auxiliary_lines")

        done = False
        for area in self.list_of_areas():
            if self.create_aux_lines(area, rightangle, leftangle):
                done = True

        logger.debug("end of create_auxiliary_lines")
        return done

    def create_aux_lines(self, area, rightangle, leftangle):
        logger.debug("begin of create_aux_lines(%s)", area.get_id())

        areas_inside = area.areas_inside.values()
        if not areas_inside:
            logger.debug("end create_aux_lines() for %s (no areas inside)",
                         area.get_id())
            return False

        logger.debug("areas found inside area(%s)", area.get_id())

        aux_color = 'red'
        aux_linestyle = 'dotted'

        areas_border = {a.get_id(): a for a in areas_inside
                        if area.has_connection(self, a, ndec)}
        areas_notouch = {a.get_id(): a for a in areas_inside
                         if not area.has_connection(self, a, ndec)}

        for id, a in areas_notouch.items():
            for id2, a2 in areas_border.items():
                if a.has_connection(self, a2, ndec):
                    areas_border[id2] = a2
                    break

        for id, a in areas_border.items():
            if id in areas_notouch:
                del areas_notouch[id]

        logger.debug("--- build notouch list ---")

        notouch_list = []
        notouch_area_list = [a for id, a in areas_notouch.items()]

        for id, a in areas_notouch.items():
            logger.debug(" --> areas_notouch: %s", id)
            if not notouch_list:
                logger.debug("   * append %s (%s)", id, a.get_id())
                notouch_list.append({id: a})
            else:
                touched = False
                for l in notouch_list:
                    for id2, a2 in l.items():
                        if a.has_connection(self, a2, ndec):
                            logger.debug("   . %s and %s are connected",
                                         a.get_id(),
                                         a2.get_id())
                            l[id] = a
                            touched = True
                            break
                    if touched:
                        break
                if not touched:
                    logger.debug("   + append %s (%s)", id, a.get_id())
                    notouch_list.append({id: a})

        logger.debug("--- search lowest gaps ---")
        created_lines = []

        # create a sorted list of lowest gaps over all areas
        # inside this area (parameter area).
        notouch_dist_list = []

        for lst in notouch_list:
            my_keys = list(lst.keys())
            my_areas = lst.values()

            low_gaps_to_parent = []
            low_gaps_to_childs = []

            for a in my_areas:
                logger.debug("==> get lowest gap from %s to %s",
                             area.get_id(),
                             a.get_id())

                low_gaps_to_parent += \
                    area.get_lowest_gap_list(a,
                                             self.center,
                                             self.max_radius,
                                             rightangle,
                                             leftangle)
                for a1 in notouch_area_list:
                    if not a1.get_id() in my_keys:
                        logger.debug("    get lowest gap from %s to %s",
                                     a.get_id(),
                                     a1.get_id())

                        low_gaps_to_childs += \
                            a1.get_lowest_gap_list(a,
                                                   self.center,
                                                   self.max_radius,
                                                   rightangle,
                                                   leftangle)

            assert(len(low_gaps_to_parent) > 0)
            low_gaps_to_parent.sort()
            low_gaps_to_childs.sort()

            aux_lines = {}
            gap_to_parent = low_gaps_to_parent[0]
            dist_to_parent = gap_to_parent[0]

            if low_gaps_to_childs:
                gap_to_child = low_gaps_to_childs[0]
                dist_to_child = gap_to_child[0]

                if dist_to_child < dist_to_parent:
                    logger.debug('gap child area is lower')
                    points = gap_to_child[1]
                    pattern = gap_to_child[2]
                    line = Line(Element(start=points[0],
                                        end=points[1]),
                                color=aux_color,
                                linestyle=aux_linestyle,
                                attr='auxline')
                    aux_lines['int'] = {'distance': dist_to_child,
                                        'p1': points[0],
                                        'p2': points[1],
                                        'line': line,
                                        'pattern': pattern,
                                        'connect': 'child',
                                        'id': gap_to_child[3]}

            my_notouch = [a for i, a in areas_notouch.items()
                          if i not in my_keys]

            points = gap_to_parent[1]
            pattern = gap_to_parent[2]
            id = gap_to_parent[3]
            connect = 'parent'
            logger.debug("   ==> try line from %s to %s",
                         points[0],
                         points[1])
            logger.debug("   Pattern is %s", pattern)
            line = Line(Element(start=points[0],
                                end=points[1]),
                        color=aux_color,
                        linestyle=aux_linestyle,
                        attr='auxline')

            intersection = False
            inner_gap_list = []
            for no_a in my_notouch:
                if no_a.intersect_line(line):
                    intersection = True
                    logger.debug("   --> intersection with %s",
                                 no_a.get_id())
                    inner_gap_list += \
                        no_a.get_lowest_gap_list(a,
                                                 self.center,
                                                 self.max_radius,
                                                 rightangle,
                                                 leftangle)

            dist = dist_to_parent
            if intersection:
                # intersection with other child area
                inner_gap_list.sort()
                dist = inner_gap_list[0][0]
                points = inner_gap_list[0][1]
                pattern = inner_gap_list[0][2]
                id = inner_gap_list[0][3]
                connect = 'child'
                logger.debug("  ==> intersection with other child area")
                line = Line(Element(start=points[0],
                                    end=points[1]),
                            color=aux_color,
                            linestyle=aux_linestyle,
                            attr='auxline')

            logger.debug("   +++ auxiliary line from %s to %s",
                         points[0], points[1])

            aux_lines['ext'] = {'distance': dist,
                                'p1': points[0],
                                'p2': points[1],
                                'line': line,
                                'pattern': pattern,
                                'connect': connect,
                                'id': id}

            if aux_lines:
                aux_lines['keys'] = my_keys
                x = len(notouch_dist_list)
                notouch_dist_list.append([dist_to_parent, x, aux_lines])

        # sort over distances to parent
        done = False
        area_to_parent_list = []
        notouch_dist_list.sort(reverse=True)

        for d, x, aux in notouch_dist_list:
            aux_line = aux.get('int', None)
            if aux_line:
                if aux_line['pattern'] in created_lines:
                    aux_line = None
            if not aux_line:
                aux_line = aux.get('ext', None)
            if aux_line:
                line = aux_line['line']
                n1 = self.find_the_node(aux_line['p1'])
                n2 = self.find_the_node(aux_line['p2'])
                if not (n1 and n2):
                    pts = self.split_and_get_intersect_points(line)
                    if len(pts) != 2:
                        logger.error("ERROR in create_aux_lines()")
                        logger.debug("Points: %s", pts)

                    n1 = self.find_the_node(line.node1(ndec))
                    n2 = self.find_the_node(line.node2(ndec))
                if n1 and n2:
                    add_or_join(self,
                                n1,
                                n2,
                                aux_line['line'],
                                self.rtol,
                                self.atol)
                    logger.debug("=== Create auxiliary line: %s", aux_line)
                    if aux_line['connect'] == 'child':
                        for a in areas_inside:
                            if a.get_id() == aux_line['id']:
                                area_to_parent_list.append(a)
                                break
                    done = True
                    created_lines.append(aux_line['pattern'])

        if not area.is_iron():
            logger.debug("end create_aux_lines() for %s (no iron)",
                         area.get_id())
            return done

        #   -----------------
        def id_of_inside_area(p):
            for a in areas_inside:
                if a.is_point_inside(p):
                    return a.id
            return 0

        #   -------------------------
        def connection_thru_main_area(pts):
            if len(pts) < 3:
                return True  # ok
            if len(areas_inside) < 2:
                return True  # ok

            id = id_of_inside_area(pts[0])
            if id == 0:  # strange
                return False  # bad

            next_id = id_of_inside_area(pts[1])
            if next_id == 0:
                return True  # ok

            id = next_id
            next_id = id_of_inside_area(pts[2])
            if id == next_id:  # thru inside-area
                return True  # ok

            return False

        #   ----------
        def takeSecond(elem):
            return elem[1]
        #   ----------

        # Arcs as additional auxiliary connections thru iron
        for a in area_to_parent_list:
            mid_dist = (a.min_dist + a.max_dist) / 2
            mid_angle = (a.min_angle + a.max_angle) / 2
            arc = Arc(Element(center=self.center,
                              radius=mid_dist,
                              start_angle=(rightangle)*180/np.pi,
                              end_angle=(mid_angle)*180/np.pi))
            pts = self.split_and_get_intersect_points(arc, aktion=False)
            pts.sort(key=takeSecond, reverse=True)
            if not connection_thru_main_area(pts):
                logger.debug("connection in nested areas")
                continue

            if len(pts) > 2:
                pts = pts[0:2]

            if len(pts) == 2:
                pts.sort(key=takeSecond)
                start_angle = alpha_line(self.center, pts[0])
                end_angle = alpha_line(self.center, pts[1])
                arc = Arc(Element(center=self.center,
                                  radius=mid_dist,
                                  start_angle=start_angle*180/np.pi,
                                  end_angle=end_angle*180/np.pi),
                          color=aux_color,
                          linestyle=aux_linestyle)
                arc.set_attribute('iron_sep')
                self.split_and_get_intersect_points(arc)
                n = self.find_nodes(pts[0], pts[1])
                self.add_edge(n[0], n[1], arc)

        logger.debug("end create_aux_lines() for %s",
                     area.get_id())
        return done

    def set_rotor(self):
        self.sym_counterpart = 1
        self.sym_part = 0

    def set_stator(self):
        self.sym_counterpart = 1
        self.sym_part = 2

    def is_rotor(self):
        if self.sym_counterpart:
            return self.sym_part < self.sym_counterpart
        return False

    def is_stator(self):
        if self.sym_counterpart:
            return self.sym_part > self.sym_counterpart
        return False

    def num_variable(self):
        if self.is_stator():
            return 'm.num_sl_gen'
        if self.is_rotor():
            return 'm.npols_gen'
        return 'm.{}_ncopies'.format(self.kind)

    def _delete_a_tiny_element(self, n0, n1, dict01, n2):
        dict12 = self.g.get_edge_data(n1, n2)
        if dict12.get('deleted', False):
            return False

        n12_el = dict12['object']
        if not isinstance(n12_el, Line):
            return False

        logger.debug("tiny line from %s to %s deleted", n0, n2)
        self._remove_edge(n0, n1)
        self._remove_edge(n1, n2)
        dict12['deleted'] = True
        dict01['deleted'] = True
        line = Line(Element(start=n0, end=n2))
        self.add_edge(n0, n2, line)
        return True

    def delete_tiny_elements(self, mindist):
        if mindist == 0.0:
            return

        edges = [edge for edge in self.g.edges(data=True)
                 if distance(edge[0], edge[1]) < mindist]
        if len(edges) > 0:
            logger.info("mindist=%s: %s tiny elements found",
                        mindist, len(edges))
        deleted = 0
        for edge in edges:
            if edge[2].get('deleted', False):
                continue

            nbrs_n1 = [nbr for nbr in self.g.neighbors(edge[0])
                       if nbr is not edge[1]]
            nbrs_n2 = [nbr for nbr in self.g.neighbors(edge[1])
                       if nbr is not edge[0]]

            if len(nbrs_n1) == 1:
                if self._delete_a_tiny_element(edge[1], edge[0],
                                               edge[2], nbrs_n1[0]):
                    deleted += 1
                    continue

            if len(nbrs_n2) == 1:
                if self._delete_a_tiny_element(edge[0], edge[1],
                                               edge[2], nbrs_n2[0]):
                    deleted += 1
                    continue

        if deleted:
            logger.info("%s tiny elements deleted", deleted)
        return

    def check_shaft_area(self, shaft):
        for a in self.list_of_areas():
            if not shaft.is_identical(a):
                if shaft.is_inside(a, self):
                    shaft.type = 6  # iron shaft (Zahn)
                    return
                if shaft.is_touching(a):
                    if not a.is_iron():
                        shaft.type = 6  # iron shaft (Zahn)
                        return

    def mark_connecting_edges(self, windings):
        logger.debug("begin of mark_connecting_edges")
        for a in windings:
            logger.debug("- id of winding: %s", a.identifier())
            for w in windings:
                if a.id != w.id:
                    elist = [e for e in a.list_of_equal_edges(w)]
                    logger.debug(" --> %s equal egdes", len(elist))
                    for e in elist:
                        e.init_attributes('lightblue', 'no_fsl')

    def search_subregions(self):
        if self.is_stator():
            self.search_stator_subregions()
        elif self.is_rotor():
            self.search_rotor_subregions()
        else:
            logger.warning("no stator or rotor assigned")
            self.search_unknown_subregions()
        self.looking_for_corners()

    def get_windings(self, type):
        windings = [a for a in self.list_of_areas() if a.type == type]
        for w in windings:
            inside = []
            for a in self.list_of_areas():
                if not w.is_identical(a):
                    if w.is_inside(a, self):
                        inside.append(a)
            if inside:
                w.set_type(0)  # air
        return [a for a in self.list_of_areas() if a.type == type]

    def collect_windings(self):
        logger.debug("begin of collect_windings")
        good_windings = self.get_windings(2)
        ugly_windings = self.get_windings(12)

        logger.debug("-- %s good and %s ugly windings",
                     len(good_windings),
                     len(ugly_windings))

        if not ugly_windings:
            logger.debug("#1 end of collect_windings: %s windings", len(good_windings))
            return good_windings

        if not good_windings:
            logger.debug("#2 end of collect_windings: %s windings", len(ugly_windings))
            [w.set_type(2) for w in ugly_windings]
            return [a for a in self.list_of_areas() if a.type == 2]

        # ggod and ugly windings available
        found = True
        while found:
            found = False
            for a in ugly_windings:
                if a.is_touching_areas(good_windings):
                    a.set_type(2)
                    found = True

            good_windings = [a for a in self.list_of_areas() if a.type == 2]
            ugly_windings = [a for a in self.list_of_areas() if a.type == 12]

        [w.set_type(0) for w in ugly_windings]
        good_windings = [a for a in self.list_of_areas() if a.type == 2]

        logger.debug("return %s bad windings as good windings", len(good_windings))
        logger.debug("end of collect_windings")
        return good_windings

    def search_stator_subregions(self, place=''):
        logger.debug("Begin of search_stator_subregions")

        if place == 'in':
            self.is_inner = True
        elif place == 'out':
            self.is_inner = False

        if self.alfa == 0.0:
            self.alfa = np.pi * 2.0

        stator_size = self.area_size()
        for area in self.list_of_areas():
            area.mark_stator_subregions(self.is_inner,
                                        stator_size,
                                        self.is_mirrored(),
                                        self.alfa,
                                        self.center,
                                        self.min_radius,
                                        self.max_radius)

        windings = self.collect_windings()
        [a.set_type(0) for a in self.list_of_areas() if a.type == 12]
        windings_found = len(windings)
        logger.debug("%d windings found", windings_found)

        if windings_found > 1:
            windings_surface = [[w.surface, w] for w in windings]
            windings_surface.sort(reverse=True)
            max_size = windings_surface[0][0]
            for sz, w in windings_surface:
                logger.debug("winding size = %s", sz)
                if sz / max_size < 0.95:
                    w.set_type(0)
                    if sz / max_size < 0.2:
                        windings_found -= 1
            windings = [a for a in self.list_of_areas()
                        if a.is_winding()]
            if windings_found > 2 and len(windings) == 1:
                logger.info("no windings remaining")
                # no windings
                [w.set_type(0) for w in windings]
                [a.set_type(1) for a in self.list_of_areas() if a.is_iron()]
                windings = []
            elif len(windings) < windings_found:
                logger.info("%d windings remaining", len(windings))
            if len(windings) > 2:
                self.mark_connecting_edges(windings)

        wdg_min_angle = 99999
        wdg_max_angle = 0
        wdg_min_dist = 99999
        wdg_max_dist = 0
        wdg_close_to_startangle = False
        wdg_close_to_endangle = False

        for w in windings:
            wdg_min_angle = min(wdg_min_angle, w.min_angle)
            wdg_max_angle = max(wdg_max_angle, w.max_angle)
            wdg_min_dist = min(wdg_min_dist, w.min_dist)
            wdg_max_dist = max(wdg_max_dist, w.max_dist)
            if w.close_to_startangle:
                wdg_close_to_startangle = True
            if w.close_to_endangle:
                wdg_close_to_endangle = True

        if windings_found:
            logger.debug("wdg_min_angle: %s", wdg_min_angle)
            logger.debug("wdg_max_angle: %s", wdg_max_angle)
            gap_startangle = wdg_min_angle
            gap_endangle = self.alfa - wdg_max_angle
            self.wdg_is_mirrored = self.is_mirrored()
            if np.isclose(gap_startangle,
                          gap_endangle,
                          atol=0.01):
                self.wdg_is_mirrored = False

        # air or iron near windings and near airgap ?
        air_areas = [a for a in self.list_of_areas() if a.type == 9]
        for a in air_areas:
            if a.around_windings(windings, self):
                logger.debug("Area %s", a.identifier())
                logger.debug(" - air-angle min/max = %s/%s",
                             a.min_air_angle,
                             a.max_air_angle)
                logger.debug(" - wdg-angle min/max = %s/%s",
                             wdg_min_angle,
                             wdg_max_angle)

                if a.close_to_startangle:
                    if not wdg_close_to_startangle:
                        logger.debug("#0.1 ===> close to startangle")
                        a.type = 6  # iron shaft (Zahn)
                        continue

                if a.close_to_endangle:
                    if not wdg_close_to_endangle:
                        logger.debug("#0.2 ===> close to endangle")
                        if(a.min_angle < wdg_min_angle and
                           a.close_to_ag):
                            a.type = 0  # air
                            continue

                        a.type = 6  # iron shaft (Zahn)
                        continue

                if greater_equal(a.min_air_angle, wdg_min_angle):
                    logger.debug("#0.3 ===> %s >= %s <===",
                                 a.min_air_angle,
                                 wdg_min_angle)

                    if a.close_to_endangle and self.is_mirrored():
                        logger.debug("#1 ===> endangle and mirrored <===")
                        a.type = 0  # air
                    elif less_equal(a.max_air_angle, wdg_max_angle):
                        logger.debug("#2 ===> %s <= %s <===",
                                     a.max_air_angle,
                                     wdg_max_angle)
                        a.type = 0  # air
                    else:
                        logger.debug("#3 ===> %s > %s <===",
                                     a.max_air_angle,
                                     wdg_max_angle)
                        a.type = 6  # iron shaft (Zahn)
                else:
                    logger.debug("#4 ===> %s < %s <===",
                                 a.min_air_angle,
                                 wdg_min_angle)
                    a.type = 6  # iron shaft (Zahn)
            else:
                logger.debug("#5 not around windings")
                a.type = 6  # iron shaft (Zahn)

        # yoke or shaft ?
        iron_areas = [a for a in self.list_of_areas() if a.type == 5]
        for a in iron_areas:
            if a.around_windings(windings, self):
                if less(a.min_dist, wdg_max_dist):
                    if less_equal(a.max_dist, wdg_max_dist):
                        a.type = 6  # iron shaft (Zahn)
                    else:
                        dist_low = wdg_max_dist - a.min_dist
                        dist_up = a.max_dist - wdg_max_dist
                        if dist_low > dist_up:
                            a.type = 6  # iron shaft (Zahn)

        shaft_areas = [a for a in self.list_of_areas() if a.type == 10]
        if shaft_areas:
            if len(shaft_areas) > 1:
                logger.warn("More than two shafts ?!?")
                return
            self.check_shaft_area(shaft_areas[0])

    def search_rotor_subregions(self, place=''):
        logger.info("Begin of search_rotor_subregions")

        if place == 'in':
            self.is_inner = True
        elif place == 'out':
            self.is_inner = False

        if self.alfa == 0.0:
            self.alfa = np.pi * 2.0

        types = {}
        for area in self.list_of_areas():
            t = area.mark_rotor_subregions(self.is_inner,
                                           self.is_mirrored(),
                                           self.alfa,
                                           self.center,
                                           self.min_radius,
                                           self.max_radius)
            if t in types:
                types[t] += 1
            else:
                types[t] = 1

        if 10 in types:
            logger.debug("Shaft is available")

        if 4 in types:  # magnet rectangle
            if types[4] > 1:
                logger.debug("%s embedded magnets in rotor", types[4])
                emb_mag_areas = [a for a in self.list_of_areas()
                                 if a.type == 4]
                [a.set_surface(self.is_mirrored()) for a in emb_mag_areas]
                max_surface = 0.0
                max_phi = 0.0
                for a in emb_mag_areas:
                    if a.surface > max_surface:
                        max_phi = a.phi
                        max_surface = a.surface

                for a in emb_mag_areas:
                    if a.surface < max_surface * 0.20:  # too small
                        logger.debug(
                            "embedded magnet too small: convert to air")
                        logger.debug("max surface : %s", max_surface)
                        logger.debug("area surface: %s", a.surface)
                        logger.debug("max phi     : %s", max_phi)
                        logger.debug("area phi    : %s", a.phi)
                        if not np.isclose(a.phi, max_phi):
                            a.set_type(0)  # air

            # set iron
            [a.set_type(1) for a in self.list_of_areas() if a.type == 3]

        iron_mag_areas = [a for a in self.list_of_areas() if a.type == 9]
        air_mag_areas = [a for a in self.list_of_areas() if a.type == 8]
        ag_areas = [a for a in self.list_of_areas() if a.close_to_ag]
        if len(ag_areas) == 1:
            if len(iron_mag_areas) == 1:
                [a.set_type(3) for a in iron_mag_areas]
                iron_mag_areas = []
            if len(air_mag_areas) == 1:
                [a.set_type(3) for a in air_mag_areas]
                air_mag_areas = []

        [a.set_type(1) for a in iron_mag_areas]
        [a.set_type(0) for a in air_mag_areas]

        if self.is_mirrored():
            mid_alfa = round(self.alfa, 3)
        else:
            mid_alfa = round(self.alfa / 2, 4)

        mag_areas = [[abs(round(a.phi, 3) - mid_alfa),
                      a.id,
                      a] for a in self.list_of_areas()
                     if a.type == 4]
        if len(mag_areas) > 2:
            mag_areas.sort()
            mag_phi = {}
            phi_prev = mag_areas[0][0]
            phi_curr = phi_prev

            for phi, id, a in mag_areas:
                # group around mid_alfa
                if phi > phi_prev + 0.33:
                    phi_curr = phi

                phi_prev = phi
                x = mag_phi.get(phi_curr, [0, []])
                x[0] += 1
                x[1].append(a)
                mag_phi[phi_curr] = x

            phi_list = [[l[0], p, l[1]] for p, l in mag_phi.items()]
            phi_list.sort(reverse=True)
            if len(phi_list) > 1:
                c0 = phi_list[0][0]
                c1 = phi_list[1][0]
                first = 1
                if c0 == c1:
                    first = 2

                for c, phi, a_lst in phi_list[first:]:
                    [a.set_type(0) for a in a_lst]

        shaft_areas = [a for a in self.list_of_areas() if a.type == 10]
        if shaft_areas:
            if len(shaft_areas) > 1:
                logger.warn("More than two shafts ?!?")
                return
            self.check_shaft_area(shaft_areas[0])

        logger.info("end of search_rotor_subregions")

    def search_unknown_subregions(self):
        logger.debug("begin of search_unknown_subregions")
        types = {}
        for area in self.list_of_areas():
            t = area.mark_unknown_subregions(self.is_mirrored(),
                                             self.alfa,
                                             self.center,
                                             self.min_radius,
                                             self.max_radius)
            if t in types:
                types[t] += 1
            else:
                types[t] = 1

        if 4 in types:  # magnet rectangle
            if types[4] > 1:
                logger.debug("%s embedded magnets in rotor", types[4])
                emb_mag_areas = [a for a in self.list_of_areas()
                                 if a.type == 4]
                [a.set_surface(self.is_mirrored()) for a in emb_mag_areas]
                max_surface = 0.0
                for a in emb_mag_areas:
                    max_surface = max(max_surface, a.surface)

                for a in emb_mag_areas:
                    if a.surface < max_surface * 0.20:  # too small
                        a.set_type(0)  # air

        logger.debug("end of search_unknown_subregions")

    def looking_for_corners(self):
        if self.is_inner:
            logger.debug("looking_for_corners: inner")
            start_cp = self.start_corners[-1]
            end_cp = self.end_corners[-1]
        else:
            logger.debug("looking_for_corners: outer")
            start_cp = self.start_corners[0]
            end_cp = self.end_corners[0]
        logger.debug("looking_for_corners: start=%s, end=%s",
                     start_cp, end_cp)
        for area in self.list_of_areas():
            area.mark_airgap_corners(start_cp, end_cp)
        return

    def num_areas_of_type(self, type):
        return len([area for area in self.list_of_areas()
                    if area.type == type])

    def num_of_windings(self):
        return self.num_areas_of_type(2)

    def area_close_to_endangle(self, type):
        return len([area for area in self.list_of_areas()
                    if area.type == type and area.close_to_endangle])

    def corners_dont_match(self):
        if self.is_mirrored():
            return False
        if len(self.start_corners) != len(self.end_corners):
            logger.warning("number of corners dont match: %s != %s",
                           len(self.start_corners),
                           len(self.end_corners))
            return True
        for i in range(len(self.start_corners)):
            d1 = distance(self.center, self.start_corners[i])
            d2 = distance(self.center, self.end_corners[i])
            if not np.isclose(d1, d2, atol=0.02):
                logger.warning("distance of corners dont match: %s != %s",
                               d1, d2)
                return True
        return False

    def search_appendices(self):
        c = 0
        end_nodes = []
        for n in self.g.nodes():
            nbrs = [nbr for nbr in self.g.neighbors(n)]
            if len(nbrs) == 1:
                el = self.get_edge_element(n, nbrs[0])
                if not el:
                    logger.error("Element not available ?!")
                    continue

                if not is_Circle(el):
                    end_nodes.append((n, nbrs[0], el))

        for n0, n1, el in end_nodes:
            logger.debug("Critical Node at %s", n0)
            if self.node_connected(n0):
                c += 1
            else:
                nn = self.find_node(n0)
                if nn:
                    logger.debug("Node %s is near %s", n0, nn)
                    try:
                        self._remove_edge(n0, n1)
                        self.add_edge(nn, n1, el)
                    except Exception:
                        logger.debug("delete of %s - %s failed", n0, n)
                        logger.debug("Element %s", el)
        return c

    def delete_appendices(self):
        c = 0
        end_nodes = []
        for n in self.g.nodes():
            nbrs = [nbr for nbr in self.g.neighbors(n)]
            if len(nbrs) == 1:
                end_nodes.append((n, nbrs[0]))

        for n0, n1 in end_nodes:
            logger.debug("Deadend Node at %s", n0)
            c += self.remove_appendix(n0, n1)
        return c

    def search_all_overlapping_elements(self):
        logger.debug("begin of search_all_overlapping_elements")
        c = 1
        corr = 0
        while c > 0:
            c = self.search_overlapping_elements()
            corr += c
        logger.debug("==> %s corrections performed", corr)
        logger.debug("end of search_all_overlapping_elements")

    def search_all_appendices(self):
        logger.debug("begin of search_all_appendices")
        corr = self.search_appendices()
        logger.debug("==> %s appendices connected", corr)
        logger.debug("end of search_all_appendices")

    def delete_all_appendices(self):
        logger.debug("begin of delete_all_appendices")
        corr = self.delete_appendices()
        logger.debug("==> %s appendices removed", corr)
        logger.debug("end of delete_all_appendices")

    def search_overlapping_elements(self):
        logger.debug("begin of search_overlapping_elements")
        count = 0

        for n in self.g.nodes():
            nbrs = [nbr for nbr in self.g.neighbors(n)]
            if len(nbrs) < 3:
                continue
            logger.debug("  Node %s has %s neighbors", n, len(nbrs))
            edges = []
            for nbr in nbrs:
                e_dict = self.g.get_edge_data(n, nbr)
                if not e_dict:
                    break
                e = e_dict.get('object', None)
                if not e:
                    break
                edges.append([nbr, e])

            if not edges:
                continue

            for i in range(len(edges)):
                e1 = edges[i][1]
                if e1 is None:
                    continue
                n1 = edges[i][0]
                over_edges = [[e1.length(), n1]]
                # list entry [<length of edge>, <end node of edge>]
                for j in range(i+1, len(edges)):
                    e2 = edges[j][1]
                    if e2 is None:
                        continue
                    n2 = edges[j][0]
                    if e1.overlapping_shapes(n, e2):
                        over_edges.append([e2.length(), n2])
                        edges[j][1] = None

                if len(over_edges) > 1:
                    if self.correct_overlapping(n, e1, over_edges):
                        count += 1
        logger.debug("end of search_overlapping_elements(correct=%s)", count)
        return count

    def correct_overlapping(self, n, e, edges):
        if len(edges) < 2:
            return False  # no correction
        edges.sort()
        if isinstance(e, Line):
            self.correct_overlapping_lines(n, edges)
            return True
        return False

    def correct_overlapping_lines(self, n, edges):
        logger.debug("begin of correct_overlapping_lines")
        logger.debug(" -- n=%s", n)
        assert(len(edges) > 1)

        n1 = edges[0][1]
        for edge in edges[1:]:
            n2 = edge[1]
            self._remove_edge(n, n2)
            line = Line(Element(start=n1, end=n2))
            self.add_edge(n1, n2, line)
            n1 = n2

        logger.debug(" -- corrected")
        logger.debug("end of correct_overlapping_lines")

    def connect_arc_or_line(self, n, el, n1, n2, tol=1e-05):
        elements = el.split([n], rtol=tol, atol=tol)
        if len(elements) != 2:
            logger.info("Not 2 Elements")
            logger.info("Node {} in Element {}".format(n, el))
            for e in elements:
                logger.info(e)
        assert(len(elements) == 2)

        logger.debug("HIT! Node %s is in %s", n, el)
        logger.debug(" => remove from %s to %s", n1, n2)
        self._remove_edge(n1, n2)

        for element in elements:
            logger.debug("Split: %s", element)

        rtol = tol
        atol = tol

        for element in elements:
            n1_inside = element.is_point_inside(n1,
                                                rtol=rtol,
                                                atol=atol,
                                                include_end=True)
            n2_inside = element.is_point_inside(n2,
                                                rtol=rtol,
                                                atol=atol,
                                                include_end=True)
            if n1_inside and n2_inside:
                logger.error("FATAL: both inside %s", element)
            elif not (n1_inside or n2_inside):
                logger.error("FATAL: neither is inside %s", element)
            else:
                if n1_inside:
                    logger.debug(" <= #1 add from %s to %s", n1, n)
                    self.add_edge(n1, n, element)
                else:
                    logger.debug(" <= #2 add from %s to %s", n2, n)
                    self.add_edge(n2, n, element)

    def connect_circle(self, n, el, n1, n2, tol=0.01):
        elements = el.split([n], rtol=tol, atol=tol)
        assert(len(elements) == 3)

        logger.debug("Node %s is in %s", n, el)
        logger.debug(" => remove from %s to %s", n1, n2)
        self._remove_edge(n1, n2)
        for element in elements:
            nodes = self.find_nodes(element.start(), element.end())
            self.add_edge(nodes[0], nodes[1], element)

    def node_connected(self, n):
        tol = 0.0001
        for e in self.g.edges(data=True):
            el = e[2].get('object', None)
            if el:
                if el.is_point_inside(n,
                                      rtol=tol,
                                      atol=tol,
                                      include_end=False):
                    if is_Circle(el):
                        self.connect_circle(n, el, e[0], e[1], tol=tol)
                    else:
                        self.connect_arc_or_line(n, el, e[0], e[1], tol=tol)
                    return True
        return False

    def remove_appendix(self, n1, n2, incr_text=''):
        e_dict = self.g.get_edge_data(n1, n2)
        if not e_dict:  # already removed
            return 0

        e = e_dict.get('object', None)
        if not e:  # unexpected
            return 0

        if isinstance(e, Circle):
            if not isinstance(e, Arc):
                return 0

        logger.debug("%s remove_appendix(%s, %s)", incr_text, n1, n2)
        self._remove_edge(n1, n2)
        c = 1
        nbrs = [nbr for nbr in self.g.neighbors(n2)]
        if len(nbrs) == 1:
            c += self.remove_appendix(n2, nbrs[0], incr_text + '.')
        return c

    def split_and_get_intersect_points(self, el, aktion=True):
        logger.debug("begin of split_and_get_intersect_points")
        rtol = 1e-03
        atol = 1e-03
        points = []
        for e in self.elements(Shape):
            pts = e.intersect_shape(el,
                                    rtol=rtol,
                                    atol=atol,
                                    include_end=True)
            if pts:
                pts_inside = []
                pts_real = []
                for p in pts:
                    if not e.is_point_inside(p, rtol, atol, False):
                        # get the real point
                        n = self.find_the_node(p)
                        if n:
                            for pt in points:
                                if points_are_close(pt, n):
                                    n = None
                                    break
                            if n:
                                pts_real.append(n)
                        elif e.get_point_number(p) == 1:  # strange
                            pts_real.append(e.p1)
                        else:
                            pts_real.append(e.p2)
                    else:
                        pts_real.append(p)
                        pts_inside.append(p)

                if pts_inside and aktion:
                    self.remove_edge(e)
                    elements = e.split(pts_inside, rtol, atol)
                    for e in elements:
                        n = self.find_nodes(e.start(), e.end())
                        if distance(n[0], n[1]) == 0.0:
                            logger.debug(
                                "=== OMIT ELEMENT WITH SAME NODES ===")
                        else:
                            self.add_edge(n[0], n[1], e)
                points += pts_real

        logger.debug("end of split_and_get_intersect_points")
        return points

    def _line_inside_windings(self, p1, p2):
        for area in self.list_of_areas():
            if area.is_winding():
                if area.is_point_inside(p1):
                    if area.is_point_inside(p2):
                        return True
        return False

    def inside_area_list(self, p):
        for area in self.list_of_areas():
            if area.is_point_inside(p):
                yield area

    def critical_touch_point(self, points):
        logger.debug("looking for critical touch-point")
        winding_touched = False
        for p in points[1:]:
            d = distance(self.center, p)
            logger.debug("-- p = %s, dist = %s", p, d)
            for a in self.inside_area_list(p):
                logger.debug("-- Area type = %s", a.type)
                logger.debug("        min=%s,  max= %s", a.min_dist, a.max_dist)
                logger.debug("        close to start = %s", a.close_to_startangle)
                logger.debug("        close to end   = %s", a.close_to_endangle)
                if a.is_winding():
                    winding_touched = True
                else:
                    if winding_touched and greater(a.max_dist, d, atol=0.001):
                        if not (a.close_to_startangle and a.close_to_endangle):
                            logger.debug("-- return %s", p)
                            return p
        return None

    def create_lines_outside_windings(self, points):
        if not points:
            return False
        created = False

        p1 = points[0]
        for p2 in points[1:]:
            if not points_are_close(p1, p2):
                if self._line_inside_windings(p1, p2):
                    logger.debug("in winding(%s, %s)", p1, p2)
                    p1 = p2
                    continue

                n = self.find_nodes(p1, p2)
                line = Line(Element(start=p1, end=p2),
                            color='darkred',
                            linestyle='dotted')
                self.add_edge(n[0], n[1], line)
                logger.debug("add line(%s, %s)", n[0], n[1])
                created = True
            p1 = p2

        return created

    def has_areas_touching_both_sides(self):
        for a in self.area_list:
            if a.is_touching_both_sides():
                return True
        return False

    def get_inner_airgap_line(self):
        logger.debug("begin of get_inner_airgap_line")

        if not self.is_inner:
            logger.debug("end of get_inner_airgap_line: not inner")
            return [], []
        for a in self.area_list:
            logger.debug("%s", a)
        area = [a for a in self.area_list if a.close_to_ag_endcorner]
        if len(area) != 1:
            logger.debug("end of get_inner_airgap_line: %s areas found", len(area))
            return [], []

        end_corner = self.end_corners[-1]
        logger.debug("END CORNER %s", end_corner)
        nodes = [n for n in area[0].list_of_nodes()]
        if not nodes:
            logger.debug("end of get_inner_airgap_line: no nodes found")
            return [], []
        n1 = nodes[0]
        if points_are_close(end_corner, n1):
            n2 = nodes[-1]
        else:
            n2 = n1
            for n1 in nodes[1:]:
                if points_are_close(end_corner, n1):
                    break
                n2 = n1

        if not points_are_close(end_corner, n1):
            logger.debug("end of get_inner_airgap_line: not close to endcorner")
            return [], []

        start_corner = self.start_corners[-1]

        logger.debug("EDGE FOUND: %s - %s", n1, n2)
        nodes = [n1, n2]
        info = self.get_edge_info(n1, n2)
        elements = [info.get('element', None)]
        while not points_are_close(start_corner, n2):
            info = self.next_edge_lefthand_side(info)
            if not info:
                return []
            n2 = info['n2']
            nodes.append(n2)
            elements.append(info.get('element', None))

        logger.debug("end of get_inner_airgap_line #%s", len(nodes))
        return nodes, elements

    def create_corner_areas(self):
        self.set_edge_attributes()
        self.create_inner_corner_auxiliary_areas()

    def create_and_append_area(self, n1, n2):
        rslt = self.get_new_area(n1, n2, False)
        logger.debug("create_and_append_area: %s", rslt)
        if rslt.get('ok', False):
            area = rslt['area']
            a = Area(area, self.center, 0.0)
            a.type = 0  # air
            self.area_list.append(a)
            return True
        logger.error("No area for air near airgap!!")
        return False

    def get_intersection_points(self, elements, line, n):
        points = []
        for e in elements:
            pts = e.intersect_line(line, include_end=True)
            if len(pts) == 1:
                if points_are_close(pts[0], n):
                    continue
            points += pts
        return points

    def create_inner_corner_auxiliary_areas(self):
        start_cp, start_exists = self.get_start_airgap_corner()
        end_cp, end_exists = self.get_end_airgap_corner()
        if start_exists and end_exists:
            return
        logger.debug("*** Corner Auxiliary Areas ***")
        airgap_line, airgap_el = self.get_inner_airgap_line()
        if not airgap_el:
            logger.debug("no airgapline found")
            return

        logger.debug("airgapline found !!")
        airgap_nodes = [n for n in airgap_line[1:]]
        del airgap_nodes[-1]

        if not start_exists:
            cp = self.start_corners[-1]
            logger.debug("Start Corner: %s -- %s", cp, start_cp)
            start_line = Line(Element(start=cp, end=start_cp),
                              color='red',
                              linestyle='dotted')

            start_cp = start_line.node2(ndec)
            for n in airgap_nodes:
                ag_line = Line(Element(start=start_cp, end=n))
                points = self.get_intersection_points(airgap_el, ag_line, n)
                if not points:  # no intersection
                    d = distance(self.center, n)
                    if np.isclose(d, self.max_radius):
                        self.add_arc(start_cp, n, self.center, self.max_radius,
                                     color='red',
                                     linestyle='dotted')
                    else:
                        self.add_line(start_cp, n,
                                      color='red',
                                      linestyle='dotted')
                    self.add_edge(cp, start_cp, start_line)
                    self.create_and_append_area(start_cp, n)
                    self.start_corners = self.get_corner_nodes(self.center,
                                                               0.0)
                    break

        if not end_exists:
            cp = self.end_corners[-1]
            logger.debug("End Corner: %s -- %s", cp, end_cp)
            end_line = Line(Element(start=cp, end=end_cp),
                            color='red',
                            linestyle='dotted')
            end_cp = end_line.node2(ndec)
            airgap_nodes.reverse()
            for n in airgap_nodes:
                ag_line = Line(Element(start=end_cp, end=n))
                points = self.get_intersection_points(airgap_el, ag_line, n)
                if not points:  # no intersection
                    d = distance(self.center, n)
                    if np.isclose(d, self.max_radius):
                        self.add_arc(n, end_cp, self.center, self.max_radius,
                                     color='red',
                                     linestyle='dotted')
                    else:
                        self.add_line(end_cp, n,
                                      color='red',
                                      linestyle='dotted')
                    self.add_edge(cp, end_cp, end_line)
                    self.create_and_append_area(n, end_cp)
                    self.end_corners = self.get_corner_nodes(self.center,
                                                             self.alfa)
                    break

    def print_nodes(self):
        print("=== List of Nodes ({}) ===".format(self.number_of_nodes()))
        for n in self.g.nodes():
            print(n)

    def write_nodes(self, filename):
        global nodes_filecount
        ts = time.localtime(time.time())
        nodes_filecount += 1
        name = "{}_{}_{:02}_{:02}_{:02}.{}".format(filename,
                                                   nodes_filecount,
                                                   ts.tm_hour,
                                                   ts.tm_min,
                                                   ts.tm_sec,
                                                   'txt')
        logger.info(">>> write nodes %s <<<", name)
        nodes = []
        for n in self.g.nodes():
            nodes.append(n)
        nodes.sort()

        content = []
        for n in nodes:
            content.append(u"{}".format(n))
            for nbr in self.g.neighbors(n):
                e_dict = self.g.get_edge_data(n, nbr)
                if not e_dict:
                    raise ValueError("Fatal: no edge-data found")
                e = e_dict['object']
                content.append(u" --> {}   e-nodes {} / {}"
                               .format(nbr, e.n1, e.n2))

        with io.open(name, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))
