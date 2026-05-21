import datetime
import os
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy import sparse
from scipy.spatial import cKDTree

ANIMATE = True
REANIMATE = False
LOGDIR = "py_temp_logs"
os.makedirs(LOGDIR, exist_ok=True)

# Define which steps you want to save as images
SAVE_IMAGE_AT_STEPS = [1, 500, 1000, 5000, 10000]
IMAGE_FMT = os.path.join(LOGDIR, "step_{:07d}.png")
FINAL_STATE_FILE = os.path.join(LOGDIR, "checkpoint_1280000.npz")
CHECKPOINT_FMT = os.path.join(LOGDIR, "checkpoint_{:07d}.npz")

L = 64
rho = 4
N = int(rho * L**2)
r0 = 1.0
deltat = 1.0
factor = 0.5
v0 = 0.1
eta = 0.3
NSTEPS = 10**6
CHECKPOINT_EVERY = 1000

pos = np.random.uniform(0, L, size=(N, 2))
orient = np.random.uniform(-np.pi, np.pi, size=N)
steps = 0
starttime = time.time()

if REANIMATE:
    data = np.load(FINAL_STATE_FILE, allow_pickle=True)
    pos = data["pos"]
    orient = data["orient"]
    steps = int(data["steps"].item())
    params = data["params"].item()
    L = int(params["L"])
    rho = float(params["rho"])
    N = int(params["N"])
    r0 = float(params["r0"])
    deltat = float(params["deltat"])
    v0 = float(params["v0"])
    eta = float(params["eta"])
    print(f"Resumed simulation from step {steps}")


def step():
    global pos, orient, steps
    steps += 1

    tree = cKDTree(pos, boxsize=[L, L])
    dist = tree.sparse_distance_matrix(
        tree, max_distance=r0, output_type="coo_matrix"
    )

    data = np.exp(1j * orient[dist.col])
    neigh = sparse.coo_matrix(
        (data, (dist.row, dist.col)), shape=dist.get_shape()
    )
    S = np.asarray(neigh.tocsr().sum(axis=1)).ravel()

    orient[:] = np.angle(S) + eta * np.random.uniform(-np.pi, np.pi, size=N)

    cos = np.cos(orient)
    sin = np.sin(orient)

    pos[:, 0] = (pos[:, 0] + v0 * cos) % L
    pos[:, 1] = (pos[:, 1] + v0 * sin) % L

    # Text logging logic has been removed from here

    return cos, sin


def save_state(filename):
    np.savez(
        filename,
        pos=pos,
        orient=orient,
        steps=steps,
        params=dict(
            L=L, rho=rho, N=N, r0=r0, deltat=deltat, v0=v0, eta=eta
        ),
    )
    print(f"\nState saved to {filename} (step {steps})")


def animate(i):
    cos, sin = step()
    qv.set_offsets(pos)
    qv.set_UVC(cos, sin, orient)

    # Save image if the current step matches our target list
    if steps in SAVE_IMAGE_AT_STEPS:
        fig.savefig(IMAGE_FMT.format(steps), dpi=150, bbox_inches="tight")
        print(f"Saved image snapshot at step {steps}")

    return (qv,)


if ANIMATE:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    qv = ax.quiver(
        pos[:, 0],
        pos[:, 1],
        np.cos(orient),
        np.sin(orient),
        orient,
        clim=[-np.pi, np.pi],
    )

    def on_close(event):
        save_state(FINAL_STATE_FILE)

    fig.canvas.mpl_connect("close_event", on_close)
    anim = FuncAnimation(
        fig, animate, frames=NSTEPS, interval=1, blit=True
    )
    plt.show()
else:
    # Set up a hidden plot figure for non-animated image generation
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(0, L)
    ax.set_ylim(0, L)
    qv = ax.quiver(
        pos[:, 0],
        pos[:, 1],
        np.cos(orient),
        np.sin(orient),
        orient,
        clim=[-np.pi, np.pi],
    )

    try:
        for _ in range(NSTEPS):
            cos, sin = step()

            # Save image if target step hit during non-animated run
            if steps in SAVE_IMAGE_AT_STEPS:
                qv.set_offsets(pos)
                qv.set_UVC(cos, sin, orient)
                fig.savefig(
                    IMAGE_FMT.format(steps), dpi=150, bbox_inches="tight"
                )
                print(f"Saved image snapshot at step {steps}")

            if steps % CHECKPOINT_EVERY == 0:
                save_state(CHECKPOINT_FMT.format(steps))
    except KeyboardInterrupt:
        print("\nInterrupted by user (Ctrl+C).")
    finally:
        save_state(FINAL_STATE_FILE)
        print("Simulation finished.")
