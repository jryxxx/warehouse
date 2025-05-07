# !/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Date        : 2025/5/6 16:52
# @Author      : Ruiyang Jia
# @File        : envs.py
# @Software    : PyCharm
# @Description : 仓库环境配置模块

import matplotlib.pyplot as plt
from matplotlib.patches import Patch


class StackUnit:
    """
    StackUnit Class
    """

    color_map = {
        'H-beam': 'steelblue',
        'Rebar': 'orange',
        'Steel-Plate': 'seagreen',
    }

    def __init__(self, steel_type, x, y, z, dx, dy, dz):
        self.type = steel_type
        self.x, self.y, self.z = x, y, z
        self.dx, self.dy, self.dz = dx, dy, dz
        self.color = self.color_map.get(steel_type, 'gray')

    def required_area(self):
        """
        :return:
        """
        return (self.x + self.dx) * (self.y + self.dy) * (self.z + self.dz)


def draw(ax, origin, size, color='blue', alpha=0.5):
    """
    Draw a 3D box using bar3d.
    :param ax:
    :param origin:
    :param size:
    :param color:
    :param alpha:
    """
    x, y, z = origin
    dx, dy, dz = size
    ax.bar3d(x, y, z, dx, dy, dz, color=color, edgecolor='k', alpha=alpha)


class Envs:
    """
    Envs class
    """

    def __init__(self, x_max=300, y_max=300, z_max=300):
        self.x_max = x_max
        self.y_max = y_max
        self.z_max = z_max
        self.stack_units = []
        self.roads = []
        self.entries = []
        self.exits = []

    def add_entry(self, x, y, z, stack_x, stack_y, stack_z):
        """
        Add entry to the warehouse layout.
        :param x:
        :param y:
        :param z:
        :param stack_x:
        :param stack_y:
        :param stack_z:
        """
        self.entries.append((x, y, z, stack_x, stack_y, stack_z))

    def add_exit(self, x, y, z, stack_x, stack_y, stack_z):
        """
        Add exit to the warehouse layout.
        :param x:
        :param y:
        :param z:
        :param stack_x:
        :param stack_y:
        :param stack_z:
        """
        self.exits.append((x, y, z, stack_x, stack_y, stack_z))

    def add_road(self, x, y, z, stack_x, stack_y, stack_z):
        """
        Add road to the warehouse layout.
        :param x:
        :param y:
        :param z:
        :param stack_x:
        :param stack_y:
        :param stack_z:
        """
        self.roads.append((x, y, z, stack_x, stack_y, stack_z))

    def add_stack_region(self, steel_type, x_start, y_start, z_start, stack_x, stack_y, stack_z):
        """
        Add stack region to the warehouse layout.
        :param steel_type:
        :param x_start:
        :param y_start:
        :param z_start:
        :param stack_x:
        :param stack_y:
        :param stack_z:
        """
        unit = StackUnit(
            steel_type=steel_type,
            x=x_start, y=y_start, z=z_start,
            dx=stack_x, dy=stack_y, dz=stack_z
        )
        self.stack_units.append(unit)

    def update_stack_region(self, steel_type, layer):
        """
        Update stack region in the warehouse layout.
        :param steel_type:
        :param layer:
        """
        for stack in self.stack_units:
            if stack.type == steel_type:
                stack.dz += layer
                break

    def visualize(self, ax, show=False):
        """
        Visualize the warehouse layout in 3D.
        """
        # fig = plt.figure(figsize=(8, 8))
        # ax = fig.add_subplot(111, projection='3d')

        # Draw stack units
        for stack in self.stack_units:
            draw(ax, (stack.x, stack.y, stack.z), (stack.dx, stack.dy, stack.dz), color=stack.color)
        # Draw roads
        for x, y, z, stack_x, stack_y, stack_z in self.roads:
            draw(ax, (x, y, z), (stack_x, stack_y, stack_z), color='green', alpha=0.6)
        # Draw entries
        for x, y, z, stack_x, stack_y, stack_z in self.entries:
            draw(ax, (x, y, z), (stack_x, stack_y, stack_z), color='yellow', alpha=0.6)
        # Draw exits
        for x, y, z, stack_x, stack_y, stack_z in self.exits:
            draw(ax, (x, y, z), (stack_x, stack_y, stack_z), color='red', alpha=0.6)

        ax.set_xlim([0, self.x_max])
        ax.set_ylim([0, self.y_max])
        ax.set_zlim([0, self.z_max])
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        plt.title("Steel Warehouse Layout")
        # Add texts
        for stack in self.stack_units:
            draw(ax, (stack.x, stack.y, stack.z), (stack.dx, stack.dy, stack.dz), color=stack.color)
            cx = stack.x + stack.dx / 2
            cy = stack.y + stack.dy / 2
            cz = stack.z + stack.dz + 10
            ax.text(cx, cy, cz, str(int(stack.dz)), color='red', fontsize=16, weight='bold', ha='center')
        # Add legend
        legend_elements = [
            Patch(facecolor='steelblue', label='H-beam'),
            Patch(facecolor='orange', label='Rebar'),
            Patch(facecolor='seagreen', label='Steel-Plate'),
            Patch(facecolor='green', label='Road'),
            Patch(facecolor='yellow', label='Entry'),
            Patch(facecolor='red', label='Exit')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        plt.tight_layout()
        if show:
            plt.show()


if __name__ == '__main__':
    env = Envs()
    env.add_entry(146, 0, 0, 8, 0.2, 20)
    env.add_exit(0, 146, 0, 0.2, 8, 20)
    env.add_road(146, 0, 0, 8, 146, 0.2)
    env.add_road(0, 146, 0, 154, 8, 0.2)
    env.add_stack_region('H-beam', 0, 200, 0, 150, 100, 0.2)
    env.add_stack_region('Rebar', 150, 200, 0, 150, 100, 0.2)
    env.add_stack_region('Steel-Plate', 200, 0, 0, 100, 200, 0.2)
    env.visualize()
    env.update_stack_region('H-beam', 10)
    env.visualize()
