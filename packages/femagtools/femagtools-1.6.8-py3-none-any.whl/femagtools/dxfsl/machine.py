# -*- coding: utf-8 -*-
"""a machine consists of 2 parts and has a geometry

"""
from __future__ import print_function
import numpy as np
import logging
from .shape import Element, Circle, Arc, Line
from .corner import Corner
from femagtools.dxfsl.symmetry import Symmetry
from .functions import point, points_are_close, distance
from .functions import alpha_angle, normalise_angle, middle_angle, third_angle
from .functions import alpha_line, line_m, line_n, mirror_point
from .functions import within_interval, part_of_circle
from .functions import less, less_equal, greater, greater_equal
logger = logging.getLogger('femagtools.geom')


#############################
#          Machine          #
#############################

class Machine(object):
    def __init__(self, geom, radius=0.0, startangle=0.0, endangle=0.0):
        self.geom = geom
        self.center = self.geom.center
        self.radius = radius
        self.startangle = startangle
        self.endangle = endangle
        self.mirror_orig_geom = None
        self.mirror_geom = None
        self.mirror_startangle = 0.0
        self.mirror_endangle = 0.0
        self.part = self.part_of_circle()
        self.airgaps = []
        self.airgap_radius = 0.0
        self.airgap2_radius = 0.0
        self.previous_machine = None
        if not self.center:
            raise ValueError("FATAL ERROR: no center in Geometry")

    def __str__(self):
        return "Machine\n" + \
               "Center: ({})\n".format(self.center) + \
               "Radius: {}\n".format(self.radius) + \
               "Angles: Start={}, End={}\n".format(self.startangle,
                                                   self.endangle) + \
               "Mirror: {}\n".format(self.mirror_geom is not None)

    def log_machine(self, what):
        logger.info("Machine %s", what)
        self.geom.log_geom()

    def is_a_machine(self):
        return self.radius > 0.0

    def is_in_middle(self):
        return self.radius > 0.0 and \
            points_are_close(self.center, [0.0, 0.0], 1e-8)

    def is_full(self):
        return self.radius > 0.0 and \
            self.startangle == 0.0 and self.endangle == 0.0

    def is_half_up(self):
        return self.radius > 0.0 and \
               np.isclose(self.startangle, 0.0, 1e-8) and \
               (np.isclose(self.endangle, np.pi, 1e-8) or
                np.isclose(self.endangle, -np.pi, 1e-8))

    def is_half_down(self):
        return self.radius > 0.0 and \
               (np.isclose(self.endangle, np.pi, 1e-8) or
                np.isclose(self.endangle, -np.pi, 1e-8)) and \
               np.isclose(self.startangle, 0.0, 1e-8)

    def is_half_left(self):
        return self.radius > 0.0 and \
               np.isclose(self.startangle, np.pi/2, 1e-8) and \
               np.isclose(self.endangle, -np.pi/2, 1e-8)

    def is_half_right(self):
        return self.radius > 0.0 and \
               np.isclose(self.startangle, -np.pi/2, 1e-8) and \
               np.isclose(self.endangle, np.pi/2, 1e-8)

    def is_half(self):
        return self.is_half_up() or self.is_half_down() or \
               self.is_half_left() or self.is_half_right()

    def is_quarter(self):
        return self.radius > 0.0 and \
               np.isclose(alpha_angle(self.startangle, self.endangle), np.pi/2)

    def is_startangle_zero(self):
        return np.isclose(self.startangle, 0.0)

    def move_to_middle(self):
        if not self.is_in_middle():
            if self.radius > 0.0:
                offset = [-(self.center[0]), -(self.center[1])]
                self.geom.move(offset)
                self.set_center(0.0, 0.0)
                self.geom.clear_cut_lines()
                return True
        return False

    def set_center(self, x, y):
        self.center[0] = x
        self.center[1] = y
        self.geom.set_center(self.center)

    def set_radius(self, radius):
        self.radius = radius

    def set_kind(self, kind):
        self.geom.kind = kind

    def set_inner(self):
        self.geom.is_inner = True

    def set_outer(self):
        self.geom.is_outer = True

    def clear_cut_lines(self):
        self.geom.clear_cut_lines()
        if self.mirror_geom is not None:
            self.mirror_geom.clear_cut_lines()

    def cut_is_possible(self, r_in, r_out):
        if r_in > 0.0:
            if less(self.geom.min_radius, r_in, rtol=0.0001):
                if less_equal(self.geom.max_radius, r_in, rtol=0.0001):
                    return False
                return True
        if r_out > 0.0:
            if greater(self.geom.max_radius, r_out, rtol=0.0001):
                if greater_equal(self.geom.min_radius, r_out, rtol=0.0001):
                    return False
                return True
        return False

    def cut(self, r_in, r_out):
        radius_in = r_in
        radius_out = r_out
        if r_out == 0.0:
            radius_out = self.radius + 10

        clone = self.geom.copy_shape(self.radius,
                                     0.0,
                                     2*np.pi,
                                     radius_in,
                                     radius_out,
                                     False,
                                     append_inner=(r_in > 0.0),
                                     append_outer=(r_out > 0.0))

        if r_out == 0.0:
            r_out = self.radius

        m = Machine(clone,
                    radius=r_out,
                    startangle=self.startangle,
                    endangle=self.endangle)

        m.mirror_geom = self.mirror_geom
        m.part = self.part

        m.set_alfa_and_corners()
        m.set_kind(self.geom.kind)
        return m

    def copy(self, startangle, endangle,
             airgap=False, inside=True, split=False,
             delete_appendices=False,
             concatenate_tiny_el=False):
        if airgap and self.airgap_radius > 0.0:
            if inside:
                if self.airgap2_radius > 0.0:
                    new_radius = min(self.airgap_radius, self.airgap2_radius)
                else:
                    new_radius = self.airgap_radius
                clone = self.geom.copy_shape(self.radius,
                                             startangle, endangle,
                                             0.0, new_radius,
                                             split=split,
                                             delete_appendices=delete_appendices,
                                             concatenate_tiny_el=concatenate_tiny_el)
            else:
                new_radius = self.radius
                gap_radius = max(self.airgap_radius, self.airgap2_radius)
                clone = self.geom.copy_shape(self.radius,
                                             startangle, endangle,
                                             gap_radius, self.radius+9999,
                                             split=split,
                                             delete_appendices=delete_appendices,
                                            concatenate_tiny_el=concatenate_tiny_el)

            circ = Circle(Element(center=self.center,
                                  radius=self.airgap_radius))
            clone.add_cut_line(circ)
        else:
            new_radius = self.radius
            clone = self.geom.copy_shape(self.radius,
                                         startangle, endangle, 0.0,
                                         self.radius+9999,
                                         split=split,
                                         delete_appendices=delete_appendices,
                                         concatenate_tiny_el=concatenate_tiny_el)

        if not np.isclose(normalise_angle(startangle),
                          normalise_angle(endangle), 0.0):
            start_p = point(self.center, self.radius+5, startangle)
            start_line = Line(Element(start=self.center, end=start_p))
            clone.add_cut_line(start_line)

            end_p = point(self.center, self.radius+5, endangle)
            end_line = Line(Element(start=self.center, end=end_p))
            clone.add_cut_line(end_line)

        if not np.isclose(alpha_angle(startangle, endangle), 2*np.pi):
            return Machine(clone,
                           radius=new_radius,
                           startangle=startangle,
                           endangle=endangle)
        else:
            # Der Originalwinkel bleibt bestehen
            return Machine(clone,
                           radius=new_radius,
                           startangle=self.startangle,
                           endangle=self.endangle)

    def full_copy(self):
        clone = self.geom.copy_shape(self.radius,
                                     0.0, 2*np.pi,
                                     0.0, self.radius+9999)
        return clone.get_machine()

    def copy_mirror(self, startangle, midangle, endangle):
        logger.debug("begin of copy_mirror")
        geom1 = self.geom.copy_shape(self.radius,
                                     startangle,
                                     midangle,
                                     0.0,
                                     self.radius+9999,
                                     rtol=1e-08,
                                     atol=1e-08)
        geom2 = self.geom.copy_shape(self.radius,
                                     midangle,
                                     endangle,
                                     0.0,
                                     self.radius+9999,
                                     rtol=1e-08,
                                     atol=1e-08)

        machine = Machine(geom1,
                          radius=self.radius,
                          startangle=startangle,
                          endangle=midangle)
        machine.mirror_orig_geom = self.geom
        machine.mirror_geom = geom2
        machine.mirror_startangle = midangle
        machine.mirror_endangle = endangle
        logger.debug("end of copy_mirror")
        return machine

    def has_mirrored_windings(self):
        if not self.is_mirrored():
            return False
        return self.geom.area_close_to_endangle(2) > 0

    def undo_mirror(self):
        assert(self.is_mirrored())
        assert(self.previous_machine)
        self.previous_machine.clear_mirror()
        self.previous_machine.set_alfa_and_corners()
        self.previous_machine.set_kind(self.geom.kind)
        return self.previous_machine

    def clear_mirror(self):
        self.mirror_orig_geom = None
        self.mirror_geom = None
        self.mirror_startangle = 0.0
        self.mirror_endangle = 0.0
        self.geom.mirror_corners = []

    def rotate_to(self, new_startangle):
        if np.isclose(new_startangle, self.startangle):
            return

        if points_are_close(self.center, [0.0, 0.0]):
            angle = new_startangle - self.startangle
            self.geom.rotate(angle)
            self.startangle = new_startangle
            self.endangle += angle

    def airgap(self, correct_airgap=0.0, correct_airgap2=0.0, atol=0.1):
        logger.debug('begin airgap (locking for airgap)')
        self.airgap_radius = 0.0
        self.airgap2_radius = 0.0

        if np.isclose(self.radius, 0.0):
            logger.debug('end airgap: no radius')
            return False

        if correct_airgap < 0:
            logger.debug('end airgap: no airgap (%s)', correct_airgap)
            return False  # no airgap

        self.airgaps = []
        airgaps = self.geom.detect_airgaps(self.center,
                                           self.startangle,
                                           self.endangle, atol)

        alpha = alpha_angle(self.startangle, self.endangle)

        if len(airgaps) == 1:
            self.airgaps = airgaps
        elif len(airgaps) > 0:
            lower_radius = -1.0
            upper_radius = -1.0

            for g in airgaps:
                if np.isclose(g[0], upper_radius):
                    if not self.geom.delete_airgap_circle(self.center,
                                                          lower_radius,
                                                          upper_radius,
                                                          g[1],
                                                          alpha):
                        lower_radius = g[0]
                else:
                    if lower_radius > 0.0:
                        self.airgaps.append((lower_radius, upper_radius))
                    lower_radius = g[0]
                upper_radius = g[1]
            self.airgaps.append((lower_radius, upper_radius))

        if len(self.airgaps) > 0:
            airgap_candidates = []
            prv_radius = 0
            for g in self.airgaps:
                gap_radius = round((g[0]+g[1])/2.0, 6)
                gap_dist = g[1] - g[0]
                prv_dist = g[0] - prv_radius
                prv_radius = g[1]
                circle = Circle(Element(center=self.center,
                                        radius=gap_radius))
                ok, borders = self.geom.is_airgap(self.center,
                                                  self.radius,
                                                  self.startangle,
                                                  self.endangle,
                                                  circle, atol)
                if not ok:
                    logger.error("FATAL: No Airgap with radius {}".
                                 format(gap_radius))
                    self.geom.airgaps.append(circle)
                    return True  # bad exit

                airgap_candidates.append((borders, circle, gap_dist, prv_dist))
                self.geom.airgaps.append(circle)

                if correct_airgap > 0.0:
                    if within_interval(correct_airgap, g[0], g[1], 0.0, 0.0):
                        self.airgap_radius = gap_radius  # ok

                if correct_airgap2 > 0.0:
                    if within_interval(correct_airgap2, g[0], g[1], 0.0, 0.0):
                        self.airgap2_radius = gap_radius  # ok

        if correct_airgap > 0.0 and self.airgap_radius == 0.0:
            logger.error("No airgap with radius {} found"
                         .format(correct_airgap))
            self.show_airgap_candidates(airgap_candidates, False)
            logger.debug("end airgap: bad")
            return True  # bad exit

        if correct_airgap2 > 0.0 and self.airgap2_radius == 0.0:
            logger.error("No airgap2 with radius {} found"
                         .format(correct_airgap2))
            self.show_airgap_candidates(airgap_candidates, False)
            logger.debug("end airgap: bad")
            return True  # bad exit

        if len(self.airgaps) == 0:
            logger.debug('end airgap: No airgap found')
            return False  # no airgaps found

        if self.airgap_radius > 0.0:
            logger.debug("end airgap: radius=%s", self.airgap_radius)
            return False  # correct airgap set

        gaps = [c for b, c, d, prv_d in airgap_candidates if b == 0]

        if len(gaps) == 1:  # one candidate without border intersection
            self.airgap_radius = gaps[0].radius
            logger.debug("end airgap: radius=%s", self.airgap_radius)
            return False  # ok

        if len(airgap_candidates) == 1:  # one candidate found
            self.airgap_radius = airgap_candidates[0][1].radius
            logger.debug("end airgap: radius=%s", self.airgap_radius)
            return False  # ok

        self.airgap_radius = self.show_airgap_candidates(airgap_candidates,
                                                         True)
        logger.debug("end airgap: radius=%s", self.airgap_radius)
        return False  # ok

    def show_airgap_candidates(self, airgap_candidates, get_one):
        if get_one:
            logger.info("{} airgap candidate(s) found:"
                        .format(len(airgap_candidates)))
        else:
            print("{} airgap candidate(s) found:"
                  .format(len(airgap_candidates)))

        dist = 999
        circle = None
        pos_list = []
        for b, c, d, prv_d in airgap_candidates:
            if get_one:
                logger.info(" --- {}   (width={})".format(c.radius, d))
            else:
                print(" --- {}   (width={})".format(c.radius, d))
            if d < dist:
                dist = d
                circle = c

            inner_pc = (c.radius - self.geom.min_radius) / \
                       (self.geom.max_radius - self.geom.min_radius)
            pos = np.abs(inner_pc * 100 - 50)
            logger.debug("Abstand Mitte in % = {}".format(pos))
            prv_dist_percent = int(round(prv_d / self.geom.max_radius, 2) * 100)
            logger.debug("Abstand Vorheriger abs=%s in prz=%s (%s)",
                         prv_d, prv_dist_percent, self.geom.max_radius)
            if pos < 20:
                pos_list.append([pos, d, c])
            elif prv_dist_percent <= 1:
                pos_list.append([prv_dist_percent, d, c])
        if get_one:
            if pos_list:
                dist_list = [[d, c] for pos, d, c in pos_list]
                dist_list.sort()
                circle = dist_list[0][1]

            logger.info("airgap {} prefered".format(circle.radius))
            return circle.radius

        print("Use options --airgap/--airgap2 <float> to specify")
        return None

    def has_airgap(self):
        return self.airgap_radius > 0.0

    def airgap_x(self):
        return self.airgap_radius

    def airgap_y(self):
        return 0.1

    def part_of_circle(self, pos=2):
        return part_of_circle(self.startangle, self.endangle, pos)

    def delete_center_circle(self):
        gaps = self.geom.get_gaplist(self.center)
        if len(gaps) < 2:
            return

        first_gap = gaps[0][1]
        second_gap = gaps[1][0]
        if first_gap != second_gap:
            return

        first_dist = gaps[0][1]
        second_dist = gaps[1][1] - gaps[1][0]
        if first_dist < 1.0:
            if second_dist / first_dist > 10.0:
                self.geom.delete_circle((0.0, 0.0), first_dist)

    def repair_hull(self):
        logger.debug('begin repair_hull(%s, %s)', self.startangle, self.endangle)
        if self.is_full() and not self.has_airgap():
            self.delete_center_circle()

        if self.startangle == self.endangle:
            logger.debug('end of repair_hull: circle')
            return

        self.repair_hull_geom(self.geom, self.startangle, self.endangle)

        if self.mirror_geom:
            self.repair_hull_geom(self.mirror_geom,
                                  self.mirror_startangle,
                                  self.mirror_endangle)
        logger.debug('end of repair_hull')

    def repair_hull_geom(self, geom, startangle, endangle):
        logger.debug('begin repair_hull_geom (%s, %s)', startangle, endangle)

        rtol = 1e-4
        atol = 1e-4
        c_corner = Corner(self.center, self.center)
        start_c_added, start_corners = geom.get_corner_list(self.center, startangle,
                                                            rtol=rtol, atol=atol)
        end_c_added, end_corners = geom.get_corner_list(self.center, endangle,
                                                        rtol=rtol, atol=atol)
        if start_c_added or end_c_added:
            rtol = 1e-3
            atol = 1e-3
            start_c_added, start_corners = geom.get_corner_list(self.center, startangle,
                                                                rtol=rtol, atol=atol)
            end_c_added, end_corners = geom.get_corner_list(self.center, endangle,
                                                            rtol=rtol, atol=atol)

        geom.repair_hull_line(self.center,
                              startangle, start_corners,
                              c_corner in end_corners,
                              rtol=rtol, atol=atol)
        geom.repair_hull_line(self.center,
                              endangle, end_corners,
                              c_corner in start_corners,
                              rtol=rtol, atol=atol)
        logger.debug('end of repair_hull_geom')

    def create_stator_auxiliary_lines(self):
        logger.debug("create_stator_auxiliary_lines")
        return self.geom.create_auxiliary_lines(self.startangle, self.endangle)

    def create_rotor_auxiliary_lines(self):
        logger.debug("create_rotor_auxiliary_lines")
        done = False
        ag_list = self.geom.detect_airgaps(self.center,
                                           self.startangle, self.endangle,
                                           atol=0.001,
                                           with_end=True)
        if ag_list:
            radius_list = [(ag[0], (ag[0] + ag[1]) / 2, ag[1]) for ag in ag_list]

            min_mag, max_mag = self.geom.get_minmax_magnet()
            if self.geom.is_inner:
                radius_list.sort()
                rmin, rmid, rmax = radius_list[0]
                start = 0
                for r in radius_list[1:]:
                    if np.isclose(rmax, r[0]):
                        # SHAFT
                        rmin, rmid, rmax = r
                        start = 1
                    break

                for r in radius_list[start:]:
                    if (r[2] - r[0]) > 4:
                        radius = (r[1] + r[2]) / 2
                    elif (r[2] - r[1]) > 1:
                        radius = r[1]
                    else:
                        radius = min_mag + 1
                    if radius < min_mag:
                        if self.create_arc(radius, attr='iron_sep'):
                            done = True

        if self.geom.create_auxiliary_lines(self.startangle, self.endangle):
            done = True
        return done

    def set_alfa_and_corners(self):
        self.geom.start_corners = self.geom.get_corner_nodes(self.center,
                                                             self.startangle)
        self.geom.end_corners = self.geom.get_corner_nodes(self.center,
                                                           self.endangle)
        self.geom.alfa = alpha_angle(self.startangle, self.endangle)

        if self.mirror_geom is not None:
            self.geom.mirror_corners = self.geom.end_corners
            self.mirror_geom.start_corners = \
                self.mirror_geom.get_corner_nodes(self.center,
                                                  self.mirror_startangle)
            self.mirror_geom.end_corners = \
                self.mirror_geom.get_corner_nodes(self.center,
                                                  self.mirror_endangle)

    def is_mirrored(self):
        return self.mirror_geom is not None

    def num_of_layers(self):
        w = self.geom.num_of_windings()
        if w > 0 and self.geom.winding_is_mirrored():
            return w*2
        return w

    def find_symmetry(self, sym_tolerance, is_inner, is_outer):
        logger.debug("begin of find_symmetry")
        if self.radius <= 0.0:
            return False

        symmetry = Symmetry(geom=self.geom,
                            startangle=self.startangle,
                            endangle=self.endangle)
        parts = symmetry.find_symmetry()  # temp solution
        logger.debug(">>> Symmetry parts = %s <<<", parts)

        if parts > 1:
            found = True
        else:
            found = self.geom.find_symmetry(self.radius,
                                            self.startangle, self.endangle,
                                            sym_tolerance)
        if not found and len(self.geom.area_list) < 5:
            if is_inner:
                found = self.find_stator_symmetry(sym_tolerance, True)
            elif is_outer:
                found = self.find_stator_symmetry(sym_tolerance, False)

        if self.part != 1:  # not full
            logger.debug("end of find_symmetry: not full")
            return found

        if found:
            angle = self.geom.sym_slice_angle
            logger.debug(" - #1:  %s slices with angle %s",
                         self.geom.sym_slices,
                         angle)
        else:
            logger.debug(" - #1:  no symmetry found")
            angle = np.pi/2
        elist = self.geom.copy_all_elements(-angle)
        logger.debug(" - %s elements copied", len(elist))
        clone = self.geom.new_clone(elist)

        f = clone.find_symmetry(self.radius,
                                self.startangle,
                                self.endangle,
                                sym_tolerance)
        if f:
            logger.debug(" - #2:  %s slices with angle %s",
                         clone.sym_slices,
                         clone.sym_slice_angle)
        else:
            logger.debug(" - #2:  no symmetry found")

        if not found:
            if f:
                self.geom = clone
            logger.debug("end of find_symmetry: %s slices",
                         self.geom.sym_slices)
            return f

        if f and clone.sym_slices > self.geom.sym_slices:
            self.geom = clone
            logger.debug("end of find_symmetry: %s slices",
                         self.geom.sym_slices)
            return True

        elist = clone.copy_all_elements(-angle)
        logger.debug(" - %s elements copied", len(elist))
        clone = clone.new_clone(elist)

        f = clone.find_symmetry(self.radius,
                                self.startangle,
                                self.endangle,
                                sym_tolerance)
        if f:
            logger.debug(" - #3:  %s slices with angle %s",
                         clone.sym_slices,
                         clone.sym_slice_angle)
        else:
            logger.debug(" - #3:  no symmetry found")

        if f and clone.sym_slices > self.geom.sym_slices:
            self.geom = clone
            logger.debug("end of find_symmetry: %s slices",
                         self.geom.sym_slices)
            return True

        logger.debug("end of find_symmetry: full")
        return found

    def find_stator_symmetry(self, sym_tolerance, is_inner):
        logger.debug("*** Begin of find_stator_symmetry ***")
        if is_inner:
            radius = self.geom.max_radius - 1
        else:
            radius = self.geom.min_radius + 1

        elist = [Circle(Element(center=self.center,
                                radius=radius))]
        elist += self.geom.copy_all_elements(0.0)
        clone = self.geom.new_clone(elist, split=True)
        found = clone.find_symmetry(self.radius,
                                    self.startangle,
                                    self.endangle,
                                    sym_tolerance)
        if found:
            logger.debug(" --> symmetry found <--")
            self.geom.sym_slices = clone.sym_slices
            self.geom.sym_slice_angle = clone.sym_slice_angle
            self.geom.sym_area = clone.sym_area
            self.geom.cut_lines = clone.cut_lines
        logger.debug("*** End of find_stator_symmetry ***")
        return found

    def get_symmetry_slice(self):
        logger.debug("begin get_symmetry_slice")
        if not self.geom.has_symmetry_area():
            logger.debug("end get_symmetry_slice: no symmetry area")
            return None

        machine_slice = self.copy(self.geom.symmetry_startangle(),
                                  self.geom.symmetry_endangle(),
                                  concatenate_tiny_el=True)
        machine_slice.clear_cut_lines()
        machine_slice.repair_hull()
        machine_slice.rotate_to(0.0)
        machine_slice.set_alfa_and_corners()
        logger.debug("end get_symmetry_slice: angle start: {}, end: {}"
                     .format(self.geom.symmetry_startangle(),
                             self.geom.symmetry_endangle()))
        return machine_slice

    def get_forced_symmetry(self, part):
        logger.debug("begin get_forced_symmetry")
        if not self.is_full():
            logger.error("it's not a full machine")
            return None

        startangle = 0.0
        endangle = np.pi*2 / part
        machine = self.copy(startangle, endangle)
        machine.clear_cut_lines()
        machine.repair_hull()
        machine.set_alfa_and_corners()
        logger.debug("end get_forced_symmetry")
        return machine

    def get_third_symmetry_mirror(self):
        logger.debug("begin get_third_symmetry_mirror")
        first_thirdangle = third_angle(self.startangle, self.endangle)
        second_thirdangle = middle_angle(first_thirdangle, self.endangle)

        machine_mirror_1 = self.copy_mirror(self.startangle,
                                            first_thirdangle,
                                            second_thirdangle)
        machine_mirror_1.clear_cut_lines()
        machine_mirror_1.repair_hull()
        machine_mirror_1.set_alfa_and_corners()
        if not machine_mirror_1.check_symmetry_graph(0.001, 0.05):
            logger.debug("end get_third_symmetry_mirror: no mirror first third")
            return None

        machine_mirror_2 = self.copy_mirror(first_thirdangle,
                                            second_thirdangle,
                                            self.endangle)
        machine_mirror_2.clear_cut_lines()
        machine_mirror_2.repair_hull()
        machine_mirror_2.set_alfa_and_corners()
        if not machine_mirror_2.check_symmetry_graph(0.001, 0.05):
            logger.debug("end get_third_symmetry_mirror: no mirror second third")
            return None

        machine_mirror_1.previous_machine = self
        logger.debug("end get_third_symmetry_mirror: ok")
        return machine_mirror_1

    def get_symmetry_mirror(self):
        logger.debug("begin get_symmetry_mirror")
        if self.part == 1:
            # a complete machine
            startangle = 0.0
            endangle = 0.0
            midangle = np.pi
        else:
            startangle = self.startangle
            endangle = self.endangle
            midangle = middle_angle(self.startangle, self.endangle)
            machine_mirror = self.get_third_symmetry_mirror()
            if machine_mirror:
                logger.debug("end get_symmetry_mirror: third found")
                return machine_mirror

        logger.debug(" - angles: start: {}, mid: {}, end: {}"
                     .format(startangle, midangle, endangle))
        machine_mirror = self.copy_mirror(startangle, midangle, endangle)
        machine_mirror.clear_cut_lines()
        machine_mirror.repair_hull()
        machine_mirror.set_alfa_and_corners()
        if machine_mirror.check_symmetry_graph(0.001, 0.05):
            machine_mirror.previous_machine = self
            machine_mirror.rotate_to(0.0)
            machine_mirror.set_alfa_and_corners()
            logger.debug("end get_symmetry_mirror: found")
            return machine_mirror

        logger.debug("end get_symmetry_mirror: no mirror")
        return None

    def get_symmetry_part(self):
        if self.is_mirrored():
            return self.part/2
        else:
            return self.part

    def get_num_slots(self):
        if self.geom.winding_is_mirrored():
            return self.part/2
        elif self.is_mirrored():
            return self.part/2
        else:
            return self.part

    def get_num_poles(self):
        return self.get_symmetry_part()

    def get_num_parts(self):
        if self.geom.is_rotor():
            return self.get_num_poles()
        if self.geom.is_stator():
            return self.get_num_slots()
        return self.get_symmetry_part()  # strange

    def check_symmetry_graph(self, rtol, atol):
        logger.debug("begin check_symmetry_graph")
        axis_p = point(self.center, self.radius, self.mirror_startangle)
        axis_m = line_m(self.center, axis_p)
        axis_n = line_n(self.center, axis_m)

        def is_node_available(mirror_n, nodes, rtol, atol):
            hits = 0
            for n in nodes:
                if points_are_close(n, mirror_n, rtol, atol):
                    hits += 1
            return hits

        def get_hit_factor(geom1, geom2):
            hit_nodes = 0
            hit_inside = 0
            hit_ag = 0
            hit_no = 0
            if not geom1.g.nodes():
                return 0.0

            def near_opposite_airgap(n, third_radius):
                if not third_radius:
                    return False
                d = distance(self.center, n)
                if geom1.is_inner:
                    return d < third_radius
                else:
                    return d > third_radius

            logger.debug("begin get_hit_factor")

            nodes_near_ag = []
            logger.debug(" -- nodes1: %s,  nodes2: %s",
                         len(geom1.g.nodes()), len(geom2.g.nodes()))
            airgap_radius = geom1.get_airgap_radius()
            opposite_radius = geom1.get_opposite_radius()
            if not (airgap_radius and opposite_radius):
                airgap_radius = self.radius
                opposite_radius = self.radius
                third_radius = None
            else:
                if opposite_radius > airgap_radius:
                    third_radius = airgap_radius + (opposite_radius - airgap_radius) * 0.90
                else:
                    third_radius = airgap_radius - (airgap_radius - opposite_radius) * 0.90
            logger.debug(" -- radius ag: %s,  opposite: %s", airgap_radius, opposite_radius)

            for n in geom1.g.nodes():
                mirror_n = mirror_point(n, self.center, axis_m, axis_n)
                logger.debug("  Node %s <==> %s", n, mirror_n)
                hits = is_node_available(mirror_n, geom2.g.nodes(), rtol=rtol*2, atol=atol*2)
                if hits:
                    logger.debug(" ==> MATCH %s NODE", hits)
                    hit_nodes += 1
                elif near_opposite_airgap(n, third_radius):
                    hits = is_node_available(mirror_n, geom2.g.nodes(), rtol=rtol*10, atol=atol*5)
                    if hits:
                        logger.debug(" ==> MATCH %s NODE (more tolerant)", hits)
                        hit_nodes += 1
                    elif geom2.the_point_is_inside(mirror_n, rtol=rtol*5, atol=atol*2):
                        hit_nodes += 1
                        hits = 1
                if not hits:
                    d = distance(self.center, n)
                    logger.debug(" -- r={}, d={}".format(self.radius, d))
                    if np.isclose(d, airgap_radius, rtol=rtol, atol=atol):
                        hit_ag += 1
                    elif np.isclose(d, airgap_radius, rtol=0.075, atol=atol):
                        # very tolerant
                        nodes_near_ag.append(n)
                    elif geom2.the_point_is_inside(mirror_n, rtol=rtol*10, atol=atol):
                        hit_inside += 1
                    else:
                        hit_no += 1

            if nodes_near_ag:
                logger.debug(" -- %s candidates near airgap --", len(nodes_near_ag))
                for n in nodes_near_ag:
                    alfa = alpha_line(self.center, n)
                    if geom1.is_inner:
                        p = point(self.center, airgap_radius + 10.0, alfa)
                    else:
                        p = point(self.center, airgap_radius - 10.0, alfa)
                    line = Line(Element(start=n, end=p))
                    pts = geom1.intersect_the_line(line)
                    if pts:
                        hit_no += 1
                    else:
                        logger.debug(" -- Node %s is in touch with airgap", n)
                        hit_ag += 1

            logger.debug(" -- temporary nodes hits: %s: factor is %s",
                         hit_nodes, float(hit_nodes) / len(geom1.g.nodes()))
            logger.debug(" -- temporary inside hits: %s: factor is %s",
                         hit_inside, float(hit_inside) / len(geom1.g.nodes()))
            logger.debug(" -- temporary airgap hits: %s: factor is %s",
                         hit_ag, float(hit_ag) / len(geom1.g.nodes()))
            logger.debug(" -- temporary no hits: %s: factor is %s",
                         hit_no, float(hit_no) / len(geom1.g.nodes()))
            # hit_inside and hit_no are unused
            factor = float(hit_nodes + hit_ag) / len(geom1.g.nodes())
            logger.debug("end get_hit_factor => %s", factor)
            return factor

        hit_factor1 = get_hit_factor(self.geom,
                                     self.mirror_geom)
        logger.debug("=> hit_factor1 = {}".format(hit_factor1))
        if hit_factor1 < 0.9:
            logger.debug("end get_hit_factor: hit_factor1 < 0.9")
            return False  # not ok

        hit_factor2 = get_hit_factor(self.mirror_geom,
                                     self.geom)
        logger.debug("=> hit_factor2 = {}".format(hit_factor2))
        if hit_factor2 < 0.9:
            logger.debug("end get_hit_factor: hit_factor2 < 0.9")
            return False  # not ok

        if hit_factor1 < 0.93 and hit_factor2 < 0.93:
            logger.debug("end get_hit_factor: hit_factors < 0.93")
            return False  # not ok

        logger.debug("end check_symmetry_graph: ok")
        return True

    def sync_with_counterpart(self, cp_machine):
        self.geom.sym_counterpart = cp_machine.get_symmetry_part()
        self.geom.sym_part = self.get_symmetry_part()
        cp_machine.geom.sym_counterpart = self.get_symmetry_part()
        cp_machine.geom.sym_part = cp_machine.get_symmetry_part()

    def search_subregions(self):
        logger.debug("Search subregions")
        self.geom.search_subregions()

    def rebuild_subregions(self):
        logger.debug("Rebuild subregions")
        self.geom.set_edge_attributes()
        self.geom.area_list = []
        self.geom.search_subregions()

    def delete_tiny_elements(self, mindist):
        self.geom.delete_tiny_elements(mindist)

    def create_arc(self, radius,
                   color='red', linestyle='dotted',
                   attr=None):
        arc = Arc(Element(center=self.center,
                          radius=radius,
                          start_angle=(self.startangle-0.1)*180/np.pi,
                          end_angle=(self.endangle+0.1)*180/np.pi))
        pts = self.geom.split_and_get_intersect_points(arc)
        if len(pts) != 2:
            logger.warning("create_arc(): Bad Points: %s", pts)
            # self.geom.add_edge(arc.node1(4), arc.node2(4), arc)
            return False

        arc = Arc(Element(center=self.center,
                          radius=radius,
                          start_angle=self.startangle*180/np.pi,
                          end_angle=self.endangle*180/np.pi),
                  color=color,
                  linestyle=linestyle)
        arc.set_attribute(attr)
        n = self.geom.find_nodes(pts[0], pts[1])
        self.geom.add_edge(n[0], n[1], arc)
        return True

    def get_iron_separator(self, radius_list):
        if len(radius_list) < 2:
            return 0.0

        r_min = radius_list[0][0]
        for r in radius_list[1:]:
            if np.isclose(r[2], r_min, atol=0.001):
                return r[2]
            r_min = r[0]

        return 0.0

    def create_mirror_lines_outside_windings(self):
        logger.debug("create_mirror_lines_outside_windings")

        if not self.geom.has_areas_touching_both_sides():
            logger.debug("end create_mirror_lines_outside_windings: not done")
            return

        radius = self.radius+10
        ag_list = self.geom.detect_airgaps(self.center,
                                           self.startangle, self.endangle,
                                           atol=0.001,
                                           with_end=True)
        radius_list = [(ag[0], (ag[0] + ag[1]) / 2, ag[1]) for ag in ag_list]
        radius_list.sort(reverse=True)

        midangle = middle_angle(self.startangle, self.endangle)
        line = Line(
            Element(start=self.center,
                    end=point(self.center, radius, midangle)))

        pts = self.geom.split_and_get_intersect_points(line, aktion=False)
        pts.sort()

        p_critical = self.geom.critical_touch_point(pts)
        if p_critical:
            d_critical = distance(self.center, p_critical)
            logger.info("Critical Point: %s, len=%s", p_critical, d_critical)
            sep_radius = self.get_iron_separator(radius_list)
            logger.debug("Iron Separator found: %s", sep_radius)
            if sep_radius > 0.0 and sep_radius < d_critical:
                radius = sep_radius
            else:
                for r in radius_list:
                    logger.debug("Gap Radius = %s", r[1])
                    if r[1] < d_critical:
                        if self.create_arc(r[1]):
                            radius = r[1]
                        break
#        else:
#            sep_radius = self.get_iron_separator(radius_list)
#            if sep_radius > 0.0:
#                logger.debug("Iron Separator found: %s", sep_radius)
#                radius = sep_radius

        # install line
        line = Line(
            Element(start=self.center,
                    end=point(self.center, radius, midangle)))

        pts = self.geom.split_and_get_intersect_points(line)
        pts.sort()

        if self.geom.create_lines_outside_windings(pts):
            self.geom.area_list = []
            logger.debug("create subregions again")
            self.geom.create_list_of_areas()
            self.geom.search_subregions()

        logger.debug("end create_mirror_lines_outside_windings")

    def check_and_correct_geom(self, what):
        geom = self.geom.check_geom(what)
        if geom:
            logger.warning("=== Angle correction (%s) ===", what)
            self.geom = geom
            self.startangle = 0.0
            self.endangle = self.geom.alfa
            self.clear_cut_lines()
            self.repair_hull()
            self.set_alfa_and_corners()
