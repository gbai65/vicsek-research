import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import cKDTree


class Sky:
    def __init__(
        self, 
        num_birds,
        exclusion_factor,
        alignment_factor,
        cohesion_factor,
        radius_exclusion=5,
        radius_align=20,
        sky_size=100,
        dt=0.1,
        max_speed=3.0,
        min_speed=0.2,
    ):
        self.box_size = sky_size
        self.dt = dt
        self.max_speed = max_speed
        self.min_speed = min_speed

        self.exclusion_factor = exclusion_factor
        self.alignment_factor = alignment_factor
        self.cohesion_factor = cohesion_factor

        self.radius_exclusion = radius_exclusion
        self.radius_align = radius_align

        self.positions = np.random.rand(num_birds, 2) * sky_size
        
        speeds = 1 + np.random.rand(num_birds)
        angles = np.random.rand(num_birds) * 2 * np.pi
        self.velocities = np.column_stack([
            speeds * np.cos(angles),
            speeds * np.sin(angles)
        ])

    def compute_new_velocities(self):
        N = len(self.positions)
        
        offsets = np.array([
            [0, 0], [1, 0], [-1, 0], [0, 1], [0, -1],
            [1, 1], [1, -1], [-1, 1], [-1, -1]
        ]) * self.box_size
        
        replicated_pos = np.vstack([self.positions + offset for offset in offsets])

        tree = cKDTree(replicated_pos)
        neighbor_lists = tree.query_ball_point(self.positions, self.radius_align)
        
        sep_forces = np.zeros((N, 2))
        align_forces = np.zeros((N, 2))
        coh_forces = np.zeros((N, 2))
        
        vel_speeds = np.linalg.norm(self.velocities, axis=1, keepdims=True)
        vel_speeds[vel_speeds < 1e-8] = 1
        vel_directions = self.velocities / vel_speeds
        
        for i in range(N):
            neighbors = np.array(neighbor_lists[i])
            if len(neighbors) <= 1:
                continue
            
            orig_idx = neighbors % N
            mask = orig_idx != i
            neighbors = neighbors[mask]
            orig_idx = orig_idx[mask]
            
            if len(orig_idx) == 0:
                continue
            
            n_pos = replicated_pos[neighbors]
            n_vel_dir = vel_directions[orig_idx]
            
            disp = n_pos - self.positions[i]
            dist = np.linalg.norm(disp, axis=1)
            
            valid = dist > 1e-8
            if not np.any(valid):
                continue
            
            disp = disp[valid]
            dist = dist[valid]
            n_vel_dir = n_vel_dir[valid]
            
            exc_mask = dist < self.radius_exclusion
            if np.any(exc_mask):
                sep = -np.sum(disp[exc_mask] / dist[exc_mask, np.newaxis], axis=0)
                sep_norm = np.linalg.norm(sep)
                if sep_norm > 1e-8:
                    sep_forces[i] = sep / sep_norm
            
            align_mask = dist >= self.radius_exclusion
            if np.any(align_mask):
                align = np.mean(n_vel_dir[align_mask], axis=0)
                align_norm = np.linalg.norm(align)
                if align_norm > 1e-8:
                    align_forces[i] = align / align_norm
                
                coh = np.sum(disp[align_mask] / dist[align_mask, np.newaxis], axis=0)
                coh_norm = np.linalg.norm(coh)
                if coh_norm > 1e-8:
                    coh_forces[i] = coh / coh_norm
        
        steer = (
            self.exclusion_factor * sep_forces +
            self.alignment_factor * align_forces +
            self.cohesion_factor * coh_forces
        )
        
        new_vels = self.velocities + steer * self.dt
        
        speeds = np.linalg.norm(new_vels, axis=1, keepdims=True)
        speeds = np.clip(speeds, self.min_speed, self.max_speed)
        new_vels = new_vels / np.linalg.norm(new_vels, axis=1, keepdims=True) * speeds
        
        return new_vels
    
    def calculate_order(self):
        speeds = np.linalg.norm(self.velocities, axis=1, keepdims=True)
        speeds[speeds < 1e-8] = 1
        directions = self.velocities / speeds
        avg_direction = np.mean(directions, axis=0)
        order = np.linalg.norm(avg_direction)
        return order

    def update(self):
        self.velocities = self.compute_new_velocities()
        self.positions += self.velocities * self.dt
        self.positions %= self.box_size

    def get_positions(self):
        return self.positions[:, 0], self.positions[:, 1]


if __name__ == "__main__":
    sky = Sky(
        num_birds=1000,
        exclusion_factor=0.3,
        alignment_factor=0.5,
        cohesion_factor=0.3,
        radius_exclusion=2,
        radius_align=10,
        sky_size=50,
        dt=0.1,
        max_speed=3.0,
        min_speed=0.1
    )

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, sky.box_size)
    ax.set_ylim(0, sky.box_size)
    ax.set_aspect('equal')

    xs, ys = sky.get_positions()
    scatter = ax.scatter(xs, ys, s=0.3, alpha=0.6)

    frame_count = [0]
    
    def update(frame):
        sky.update()
        xs, ys = sky.get_positions()
        scatter.set_offsets(np.c_[xs, ys])
        
        frame_count[0] += 1
        if frame_count[0] % 20 == 0:
            print(f"Frame {frame_count[0]}, Order: {sky.calculate_order():.4f}")
        
        return scatter,

    anim = FuncAnimation(fig, update, interval=1, blit=True, cache_frame_data=False)
    plt.title(f"Flocking Simulation: {sky.positions.shape[0]:,} Birds")
    plt.show()