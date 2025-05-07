# !/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Date        : 2025/5/6 16:38
# @Author      : Ruiyang Jia
# @File        : main.py
# @Software    : PyCharm
# @Description : 主函数

import io
import time
import os
import random
from PIL import Image
import matplotlib.pyplot as plt
from utils.envs import Envs
from utils.personnel import DispatchSystem, WorkGroup, Worker, Task


def init_envs():
    """
    Initialize the environment for the dispatch system.
    :return: An instance of Envs class.
    """
    env = Envs()
    env.add_entry(146, 0, 0, 8, 0.2, 20)
    env.add_exit(0, 146, 0, 0.2, 8, 20)
    env.add_road(146, 0, 0, 8, 146, 0.2)
    env.add_road(0, 146, 0, 154, 8, 0.2)
    env.add_stack_region('H-beam', 0, 200, 0, 150, 100, 0.2)
    env.add_stack_region('Rebar', 150, 200, 0, 150, 100, 0.2)
    env.add_stack_region('Steel-Plate', 200, 0, 0, 100, 200, 0.2)
    # env.visualize()
    return env


def init_dispatch_system(tasks_num=10):
    """
    Initialize the dispatch system with work groups and tasks.
    :return: An instance of DispatchSystem class.
    """
    dispatch_system = DispatchSystem()

    # Create work groups
    group1 = WorkGroup(1, "Group A")
    group2 = WorkGroup(2, "Group B")

    # Add workers to groups
    worker1 = Worker(1, "Alice", ["H-beam"])
    worker2 = Worker(2, "Bob", ["Steel-Plate"])
    worker3 = Worker(3, "Alice", ["Rebar"])
    group1.add_member(worker1)
    group2.add_member(worker2)
    group2.add_member(worker3)
    dispatch_system.add_group(group1)
    dispatch_system.add_group(group2)

    # Create tasks
    task_types = ["H-beam", "Steel-Plate", "Rebar"]
    for task_id in range(1, tasks_num + 1):
        skill = random.choice(task_types)
        priority = random.randint(1, 5)
        dispatch_system.add_task(Task(task_id, skill, priority))

    # Assign tasks to workers
    dispatch_system.assign_tasks()

    # Visualize the dispatch system
    dispatch_system.show_assignments()
    return dispatch_system


def run_dispatch_cycle(env, dispatch, delay=1.0, pause=0.5):
    """
    Run the dispatch cycle where each worker performs one task at a time in parallel,
    and update the 3D warehouse visualization in real-time.

    :param dispatch:
    :param env:
    :param delay:
    :param pause:
    """
    plt.ion()
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    all_done = False

    while not all_done:
        all_done = True
        updates_made = False

        # Each worker tries to do one task
        for group in dispatch.groups:
            for worker in group.members:
                task = worker.do_one_task()
                if task:
                    # Update the warehouse environment
                    env.update_stack_region(task.skill_required, 10)
                    updates_made = True
                    all_done = False

        # If any task was performed, update the visualization
        if updates_made:
            ax.clear()
            env.visualize(ax, show=True)
            plt.draw()
            plt.pause(pause)

        time.sleep(delay)

    # Turn off interactive mode and keep the final plot open
    plt.ioff()
    plt.show()


def run_dispatch_simulation(env, dispatch):
    """
    Save to GIF.
    :param env:
    :param dispatch:
    """
    os.makedirs("results", exist_ok=True)

    fig = plt.figure(figsize=(8, 8), dpi=100)
    ax = fig.add_subplot(111, projection='3d')
    frames = []

    all_done = False
    while not all_done:
        all_done = True
        for group in dispatch.groups:
            for worker in group.members:
                task = worker.do_one_task()
                if task:
                    env.update_stack_region(task.skill_required, 10)
                    all_done = False
                    ax.clear()
                    env.visualize(ax)
                    fig.canvas.draw()
                    buf = io.BytesIO()
                    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
                    buf.seek(0)
                    img = Image.open(buf)
                    frames.append(img.copy())
                    buf.close()
                    plt.pause(0.5)

    if frames:
        frames[0].save(
            "results/dispatch_simulation.gif",
            save_all=True,
            append_images=frames[:],
            duration=200,
            loop=0,
            optimize=True
        )

    plt.close()


def main():
    """
    Main function to run the dispatch system.
    """
    env = init_envs()
    dispatch = init_dispatch_system(tasks_num=5)

    # vis
    # run_dispatch_cycle(env, dispatch)
    run_dispatch_simulation(env, dispatch)


if __name__ == '__main__':
    main()
