import os
from typing import List
from pathlib import Path

import gmsh
import numpy as np

from gcrack import GCrackBase
from gcrack.boundary_conditions import DisplacementBC


class GCrackData(GCrackBase):
    def generate_mesh(self, crack_points: List[np.ndarray]) -> gmsh.model:
        # Clear existing model
        gmsh.clear()
        # Parameters (geometry)
        L = self.pars["L"]
        W = self.pars["W"]
        # Parameters (discretization)
        h = L / 256
        h_min = self.R_int / 32
        # Points
        # Bot
        p1: int = gmsh.model.geo.addPoint(-W / 2, -L / 2, 0, h)
        p2: int = gmsh.model.geo.addPoint(W / 2, -L / 2, 0, h)
        # Mid
        p3: int = gmsh.model.geo.addPoint(-W / 2, 0, 0, h)  # Mid right node
        p4: int = gmsh.model.geo.addPoint(W / 2, 0, 0, h)  # Mid left node
        # Top
        p5: int = gmsh.model.geo.addPoint(-W / 2, L / 2, 0, h)
        p6: int = gmsh.model.geo.addPoint(W / 2, L / 2, 0, h)
        # Cracks
        pc_bot = []
        pc_top = []
        # Left crack
        for i, p in enumerate(reversed(crack_points)):
            # The crack tip is shared
            if i == 0:
                pc_new: int = gmsh.model.geo.addPoint(-p[0], -p[1], -p[2], h)
                pc_bot.append(pc_new)
                pc_top.append(pc_new)
            else:
                pc_new_bot: int = gmsh.model.geo.addPoint(-p[0], -p[1], -p[2], h)
                pc_bot.append(pc_new_bot)
                pc_new_top: int = gmsh.model.geo.addPoint(-p[0], -p[1], -p[2], h)
                pc_top.append(pc_new_top)

        # Right crack
        for i, p in enumerate(crack_points):
            # The crack tip is shared
            if i == len(crack_points) - 1:
                pc_new: int = gmsh.model.geo.addPoint(p[0], p[1], p[2], h)
                pc_bot.append(pc_new)
                pc_top.append(pc_new)
            else:
                pc_new_bot: int = gmsh.model.geo.addPoint(p[0], p[1], p[2], h)
                pc_bot.append(pc_new_bot)
                pc_new_top: int = gmsh.model.geo.addPoint(p[0], p[1], p[2], h)
                pc_top.append(pc_new_top)

        # Lines
        # Bot
        lb1: int = gmsh.model.geo.addLine(p1, p3)
        l2: int = gmsh.model.geo.addLine(p3, pc_bot[0])
        crack_lines_bot: List[int] = []
        for i in range(len(pc_bot) - 1):
            lb: int = gmsh.model.geo.addLine(pc_bot[i], pc_bot[i + 1])
            crack_lines_bot.append(lb)
        l3: int = gmsh.model.geo.addLine(pc_bot[-1], p4)
        lb4: int = gmsh.model.geo.addLine(p4, p2)
        lb5: int = gmsh.model.geo.addLine(p2, p1)
        # Top
        lt1: int = gmsh.model.geo.addLine(p5, p3)
        crack_lines_top: List[int] = []
        for i in range(len(pc_top) - 1):
            lt: int = gmsh.model.geo.addLine(pc_top[i], pc_top[i + 1])
            crack_lines_top.append(lt)
        lt4: int = gmsh.model.geo.addLine(p4, p6)
        lt5: int = gmsh.model.geo.addLine(p6, p5)

        # Surfaces
        # Bot
        cl1: int = gmsh.model.geo.addCurveLoop(
            [lb1, l2] + crack_lines_bot + [l3, lb4, lb5]
        )
        s1: int = gmsh.model.geo.addPlaneSurface([cl1])
        # Top
        cl2: int = gmsh.model.geo.addCurveLoop(
            [lt1, l2] + crack_lines_top + [l3, lt4, lt5]
        )
        s2: int = gmsh.model.geo.addPlaneSurface([cl2])

        # Boundaries
        self.boundaries = {
            "bot": lb5,
            "top": lt5,
        }
        # Physical groups
        # Domain
        domain: int = gmsh.model.addPhysicalGroup(2, [s1, s2], tag=21)
        gmsh.model.setPhysicalName(2, domain, "domain")
        # Boundaries
        for name, line in self.boundaries.items():
            pg: int = gmsh.model.addPhysicalGroup(1, [line], tag=self.boundaries[name])
            gmsh.model.setPhysicalName(1, pg, name)

        # Element size
        # Refine around the crack line
        field1: int = gmsh.model.mesh.field.add("Distance")
        gmsh.model.mesh.field.setNumbers(field1, "PointsList", [pc_bot[0], pc_bot[-1]])
        gmsh.model.mesh.field.setNumber(field1, "Sampling", 100)
        field2: int = gmsh.model.mesh.field.add("Threshold")
        gmsh.model.mesh.field.setNumber(field2, "InField", field1)
        gmsh.model.mesh.field.setNumber(field2, "DistMin", 1 * self.R_ext)
        gmsh.model.mesh.field.setNumber(field2, "DistMax", 8 * self.R_ext)
        gmsh.model.mesh.field.setNumber(field2, "SizeMin", h_min)
        gmsh.model.mesh.field.setNumber(field2, "SizeMax", h)
        gmsh.model.geo.synchronize()
        gmsh.model.mesh.field.setAsBackgroundMesh(field2)
        gmsh.model.mesh.generate(2)

        # # Display and exit for debug purposes
        # # Synchronize the model
        # gmsh.model.geo.synchronize()
        # # Display the GMSH window
        # gmsh.fltk.run()
        # exit()

        # Return the model
        return gmsh.model()

    def define_controlled_displacements(self) -> List[DisplacementBC]:
        """Define the displacement boundary conditions controlled by the load factor.

        Returns:
            List[DisplacementBC]: List of DisplacementBC(boundary_id, u_imp) where boundary_id is the boundary id (int number) in GMSH, and u_imp is the displacement vector (componements can be nan to let it free).
        """
        return [
            DisplacementBC(boundary_id=self.boundaries["bot"], u_imp=[0.0, -1.0]),
            DisplacementBC(boundary_id=self.boundaries["top"], u_imp=[0.0, 1.0]),
        ]

    def locate_measured_displacement(self) -> List[float]:
        """Define the point where the displacement is measured.

        Returns:
            List: Coordinate of the point where the displacement is measured
        """
        return [0, self.pars["L"] / 2]

    def locate_measured_forces(self) -> int:
        """Define the boundary where the reaction force are measured.

        Returns:
            int: Identifier (id) of the boundary in GMSH.
        """
        return self.boundaries["top"]

    def Gc(self, phi):
        return self.pars["Gc"]


if __name__ == "__main__":
    # Define the angles and associated initial crack length
    cases = {}
    cases["angle_0_test_1"] = {"a0": 2.82e-3, "alpha_deg": 0, "W": 0.02483, "L": 0.05}
    cases["angle_5_test_1"] = {"a0": 2.9e-3, "alpha_deg": 5, "W": 0.02499, "L": 0.05}
    cases["angle_10_test_1"] = {"a0": 2.9e-3, "alpha_deg": 10, "W": 0.02487, "L": 0.05}
    cases["angle_15_test_1"] = {"a0": 2.86e-3, "alpha_deg": 15, "W": 0.02489, "L": 0.05}
    cases["angle_20_test_1"] = {"a0": 2.89e-3, "alpha_deg": 20, "W": 0.0249, "L": 0.05}
    cases["angle_25_test_1"] = {"a0": 2.89e-3, "alpha_deg": 25, "W": 0.02484, "L": 0.05}
    cases["angle_30_test_1"] = {"a0": 2.85e-3, "alpha_deg": 30, "W": 0.02496, "L": 0.05}
    cases["angle_35_test_1"] = {"a0": 2.91e-3, "alpha_deg": 35, "W": 0.02484, "L": 0.05}
    cases["angle_40_test_1"] = {"a0": 2.91e-3, "alpha_deg": 40, "W": 0.02478, "L": 0.05}
    cases["angle_45_test_1"] = {"a0": 2.86e-3, "alpha_deg": 45, "W": 0.02495, "L": 0.05}
    cases["angle_50_test_1"] = {"a0": 2.91e-3, "alpha_deg": 50, "W": 0.0248, "L": 0.05}
    cases["angle_55_test_1"] = {"a0": 2.91e-3, "alpha_deg": 55, "W": 0.0248, "L": 0.05}
    cases["angle_60_test_1"] = {"a0": 2.84e-3, "alpha_deg": 60, "W": 0.02481, "L": 0.05}
    cases["angle_65_test_1"] = {"a0": 2.87e-3, "alpha_deg": 65, "W": 0.02495, "L": 0.05}
    cases["angle_70_test_1"] = {"a0": 2.87e-3, "alpha_deg": 70, "W": 0.02485, "L": 0.05}
    cases["angle_75_test_1"] = {"a0": 2.85e-3, "alpha_deg": 75, "W": 0.02481, "L": 0.05}
    cases["angle_80_test_1"] = {"a0": 2.87e-3, "alpha_deg": 80, "W": 0.02478, "L": 0.05}
    
    # Iterate through the cases
    for name, case in cases.items():
        # Convert alpha from degrees to radians
        alpha = np.deg2rad(case["alpha_deg"])
        # Define user parameters
        pars = {}
        pars["L"] = 50e-3
        pars["W"] = pars["L"] / 2  # TODO: Set the real width (per case) !!!
        pars["a0"] = 3e-3  # Initial crack length
        pars["Gc"] = 380

        # Set the crack increment size
        da = pars["W"] / 256

        # Initialize the simulation
        data = GCrackData(
            E=2.9e9,
            nu=0.39,
            da=da,
            # Nt=int(0.4 * pars["W"] / da),
            Nt=1,
            xc0=pars["a0"] * np.array([np.cos(alpha), np.sin(alpha), 0]),
            phi0=alpha,
            assumption_2D="plane_strain",
            pars=pars,
            sif_method="I-integral",
            s=2*da,  
        )
        # Run the simulation
        data.run()

        # Change the name of the directory
        current_dir = Path(".")
        subdirectories = [x for x in current_dir.iterdir() if x.is_dir()]
        last_modified_subdir = max(subdirectories, key=os.path.getmtime)
        res_dir = last_modified_subdir
        os.rename(res_dir, name)
