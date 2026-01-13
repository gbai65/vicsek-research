import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from numba import jit, prange


@jit(nopython=True, parallel=True, fastmath=True)
def compute_forces(positions, velocities, box_size, cell_size, grid_size,
                   exclusion_factor, alignment_factor, cohesion_factor,
                   radius_exclusion, radius_align, dt, min_speed, max_speed):
    N = len(positions)
    new_velocities = velocities.copy()
    
    bird_cells = np.zeros((N, 2), dtype=np.int32)
    for i in range(N):
        cx = int(positions[i, 0] / cell_size) % grid_size
        cy = int(positions[i, 1] / cell_size) % grid_size
        bird_cells[i, 0] = cx
        bird_cells[i, 1] = cy
    
    for i in prange(N):
        my_cell_x = bird_cells[i, 0]
        my_cell_y = bird_cells[i, 1]
        my_pos = positions[i]
        my_vel = velocities[i]
        
        sep_force = np.zeros(2)
        align_force = np.zeros(2)
        coh_force = np.zeros(2)
        
        sep_count = 0
        align_count = 0
        
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                neighbor_cell_x = (my_cell_x + dx) % grid_size
                neighbor_cell_y = (my_cell_y + dy) % grid_size
                
                for j in range(N):
                    if i == j:
                        continue

                    if bird_cells[j, 0] != neighbor_cell_x or bird_cells[j, 1] != neighbor_cell_y:
                        continue
                    
                    disp = positions[j] - my_pos
                    disp[0] = disp[0] - box_size * np.round(disp[0] / box_size)
                    disp[1] = disp[1] - box_size * np.round(disp[1] / box_size)
                    
                    dist = np.sqrt(disp[0]**2 + disp[1]**2)
                    
                    if dist < 1e-8 or dist >= radius_align:
                        continue
                
                    if dist < radius_exclusion:
                        sep_force[0] -= disp[0] / dist
                        sep_force[1] -= disp[1] / dist
                        sep_count += 1
                    else:
                        vel_norm = np.sqrt(velocities[j, 0]**2 + velocities[j, 1]**2)
                        if vel_norm > 1e-8:
                            align_force[0] += velocities[j, 0] / vel_norm
                            align_force[1] += velocities[j, 1] / vel_norm
                        
                        coh_force[0] += disp[0] / dist
                        coh_force[1] += disp[1] / dist
                        
                        align_count += 1
        
        sep_norm = np.sqrt(sep_force[0]**2 + sep_force[1]**2)
        if sep_norm > 0:
            sep_force[0] /= sep_norm
            sep_force[1] /= sep_norm
        
        if align_count > 0:
            align_norm = np.sqrt(align_force[0]**2 + align_force[1]**2)
            if align_norm > 0:
                align_force[0] /= align_norm
                align_force[1] /= align_norm
            
            coh_norm = np.sqrt(coh_force[0]**2 + coh_force[1]**2)
            if coh_norm > 0:
                coh_force[0] /= coh_norm
                coh_force[1] /= coh_norm
        
        steer_x = (exclusion_factor * sep_force[0] + 
                   alignment_factor * align_force[0] + 
                   cohesion_factor * coh_force[0])
        steer_y = (exclusion_factor * sep_force[1] + 
                   alignment_factor * align_force[1] + 
                   cohesion_factor * coh_force[1])
        
        new_vel_x = my_vel[0] + steer_x * dt
        new_vel_y = my_vel[1] + steer_y * dt
        
        speed = np.sqrt(new_vel_x**2 + new_vel_y**2)
        if speed < min_speed:
            new_vel_x = new_vel_x / speed * min_speed
            new_vel_y = new_vel_y / speed * min_speed
        elif speed > max_speed:
            new_vel_x = new_vel_x / speed * max_speed
            new_vel_y = new_vel_y / speed * max_speed
        
        new_velocities[i, 0] = new_vel_x
        new_velocities[i, 1] = new_vel_y
    
    return new_velocities


class Sky:
    def __init__(
        self, 
        num_birds,
        exclusion_factor,
        alignment_factor,
        cohesion_factor,
        radius_exclusion=5,
        radius_align=15,
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
        
        self.cell_size = radius_align
        self.grid_size = int(np.ceil(sky_size / self.cell_size))

        self.positions = np.random.rand(num_birds, 2) * sky_size
        
        speeds = 1 + np.random.rand(num_birds)
        angles = np.random.rand(num_birds) * 2 * np.pi
        self.velocities = np.column_stack([
            speeds * np.cos(angles),
            speeds * np.sin(angles)
        ])

    def compute_new_velocities(self):
        return compute_forces(
            self.positions, self.velocities, self.box_size,
            self.cell_size, self.grid_size,
            self.exclusion_factor, self.alignment_factor, self.cohesion_factor,
            self.radius_exclusion, self.radius_align,
            self.dt, self.min_speed, self.max_speed
        )
    
    def calculate_order(self):
        speeds = np.linalg.norm(self.velocities, axis=1, keepdims=True)
        speeds[speeds < 1e-8] = 1
        directions = self.velocities / speeds
        
        if len(directions) > 5000: # sample for large flocks for efficiency
            sample = np.random.choice(len(directions), 5000, replace=False)
            directions = directions[sample]
        
        similarity = np.dot(directions, directions.T)
        return np.mean(similarity)

    def update(self):
        self.velocities = self.compute_new_velocities()
        self.positions += self.velocities * self.dt
        self.positions %= self.box_size

    def get_positions(self):
        return self.positions[:, 0], self.positions[:, 1]


if __name__ == "__main__":
    import time
    
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

    print(f"Simulating {len(sky.positions):,} birds...")
    print(f"Grid: {sky.grid_size}x{sky.grid_size} cells")
    print("Compiling Numba...")
    
    sky.update()
    
    print("Benchmarking...")
    start = time.time()
    for i in range(10):
        sky.update()
    elapsed = time.time() - start
    print(f"10 updates: {elapsed:.2f}s ({elapsed/10*1000:.1f}ms per frame)")
    print(f"FPS: {10/elapsed:.1f}")

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(0, sky.box_size)
    ax.set_ylim(0, sky.box_size)
    ax.set_aspect('equal')
    ax.axis('off')

    xs, ys = sky.get_positions()
    scatter = ax.scatter(xs, ys, s=10, alpha=0.6, c='black')

    frame_count = [0]
    times = []
    
    def update_frame(frame):
        start = time.time()
        sky.update()
        elapsed = time.time() - start
        times.append(elapsed)
        
        xs, ys = sky.get_positions()
        scatter.set_offsets(np.c_[xs, ys])
        
        frame_count[0] += 1
        if frame_count[0] % 20 == 0:
            avg_time = np.mean(times[-20:]) if times else 0
            fps = 1.0 / avg_time if avg_time > 0 else 0
            print(f"Frame {frame_count[0]}, Order: {sky.calculate_order():.4f}, "
                  f"Time: {avg_time*1000:.1f}ms, FPS: {fps:.1f}")
        
        return scatter,

    anim = FuncAnimation(fig, update_frame, interval=0, blit=True, cache_frame_data=False)
    plt.title(f"Flocking: {sky.positions.shape[0]:,} Birds", fontsize=14)
    plt.tight_layout()
    plt.show()
