#include <bits/stdc++.h>
#include <chrono>
#include <random>
#include <iomanip>
#include <limits>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <cstdlib>
#ifdef _OPENMP
#include <omp.h>
#endif

#include "cnpy.h"

using namespace std;

struct Params {
    int L = 128;
    double eta;
    double rho;
    double v0;

    double r0 = 1.0;
    double deltat = 1.0;

    long long NSTEPS = 1'000'000;
    int CHECKPOINT_EVERY = 50000;
    size_t N;

    int CONVERGE_WINDOW = 20;
    double CONVERGE_TOL = 1e-6;

    Params(double eta, double rho, double v0)
        : eta(eta), rho(rho), v0(v0)
    {
        N = static_cast<size_t>(rho * L * L);
    }
};

void initialize_particles(
    const Params& P,
    vector<double>& pos,
    vector<double>& orient
) {
    mt19937_64 rng(chrono::high_resolution_clock::now().time_since_epoch().count());
    uniform_real_distribution<double> unif01(0.0, 1.0);
    uniform_real_distribution<double> angle_unif(-M_PI, M_PI);
    for (size_t i = 0; i < P.N; ++i) {
        pos[2*i]     = unif01(rng) * P.L;
        pos[2*i + 1] = unif01(rng) * P.L;
        orient[i]    = angle_unif(rng);
    }
}

void build_cell_list(
    const Params& P,
    const vector<double>& pos,
    vector<int>& head,
    vector<int>& next,
    int nc,
    double cell_size
) {
    fill(head.begin(), head.end(), -1);

    for (int i = 0; i < (int)P.N; ++i) {
        int cx = int(pos[2*i] / cell_size);
        int cy = int(pos[2*i+1] / cell_size);

        if (cx >= nc) cx = nc-1;
        if (cy >= nc) cy = nc-1;

        int cid = cx + cy * nc;

        next[i] = head[cid];
        head[cid] = i;
    }
}

void update_orientations(
    const Params& P,
    const vector<double>& pos,
    const vector<double>& old_cosv,    // <-- replaces orient
    const vector<double>& old_sinv,    // <-- add this
    vector<double>& new_orient,
    vector<double>& cosv,
    vector<double>& sinv,
    const vector<int>& head,
    const vector<int>& next,
    int nc,
    double cell_size,
    vector<mt19937_64>& thread_rngs
) {
    double r0sq = P.r0 * P.r0;

#pragma omp parallel for schedule(dynamic)
    for (int i = 0; i < (int)P.N; ++i) {
        int tid = 0;
#ifdef _OPENMP
        tid = omp_get_thread_num();
#endif
        auto& rng = thread_rngs[tid];
        uniform_real_distribution<double> noise_dist(-M_PI, M_PI);

        double xi = pos[2*i];
        double yi = pos[2*i+1];

        int cx = int(xi / cell_size);
        int cy = int(yi / cell_size);

        double sx = 0.0, sy = 0.0;

        // Neighbor contributions (using old orientations)
        for (int dx = -1; dx <= 1; ++dx) {
            int ncx = (cx + dx + nc) % nc;
            for (int dy = -1; dy <= 1; ++dy) {
                int ncy = (cy + dy + nc) % nc;
                int cid = ncx + ncy * nc;

                for (int j = head[cid]; j != -1; j = next[j]) {
                    double dxij = pos[2*j] - xi;
                    double dyij = pos[2*j+1] - yi;

                    if (dxij >  P.L/2.0) dxij -= P.L;
                    if (dxij < -P.L/2.0) dxij += P.L;
                    if (dyij >  P.L/2.0) dyij -= P.L;
                    if (dyij < -P.L/2.0) dyij += P.L;

                    if (dxij*dxij + dyij*dyij <= r0sq) {
                        sx += old_cosv[j];
                        sy += old_sinv[j];
                    }
                }
            }
        }
        double theta = atan2(sy, sx) + P.eta * noise_dist(rng);
        new_orient[i] = theta;          // store new orientation
        cosv[i] = cos(theta);
        sinv[i] = sin(theta);
    }
}

void update_positions(const Params& P, vector<double>& pos, const vector<double>& cosv, const vector<double>& sinv) {
#pragma omp parallel for schedule(static)
    for (int i = 0; i < (int)P.N; ++i) {
        double x = pos[2*i] + P.v0 * cosv[i];
        double y = pos[2*i+1] + P.v0 * sinv[i];
        x = fmod(x, P.L);
        if (x < 0) x += P.L;
        y = fmod(y, P.L);
        if (y < 0) y += P.L;
        pos[2*i] = x;
        pos[2*i+1] = y;
    }
}

double compute_order(const Params& P, const vector<double>& cosv, const vector<double>& sinv) {
    double sumx = 0.0, sumy = 0.0;
#pragma omp parallel for reduction(+:sumx,sumy)
    for (int i = 0; i < (int)P.N; ++i) {
        sumx += cosv[i];
        sumy += sinv[i];
    }
    double ts = hypot(sumx, sumy) / P.N;
    return ts;
}

void save_state(
    const string& filename,
    const Params& P,
    const vector<double>& pos,
    const vector<double>& orient,
    long long steps
) {
    vector<size_t> pos_shape = {P.N, 2};
    cnpy::npz_save(filename, "pos", pos.data(), pos_shape, "w");
    vector<size_t> oshape = {P.N};
    cnpy::npz_save(filename, "orient", orient.data(), oshape, "a");
    vector<size_t> sshape = {1};
    cnpy::npz_save(filename, "steps", &steps, sshape, "a");

    double params[7] = {(double)P.L, P.rho, (double)P.N, P.r0, P.deltat, P.v0, P.eta};

    vector<size_t> pshape = {7};
    cnpy::npz_save(filename, "params", params, pshape, "a");
    cout << "Saved: " << filename << " (step " << steps << ")\n";
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        std::cerr << "Usage: " << argv[0] << " <number> <eta> <rho> <v0>" << "\n";
        return 1;
    }
    int thisCount = (int) std::stod(argv[1]);
    double thisEta = (double) std::stod(argv[2]);
    double thisRho = (double) std::stod(argv[3]);
    double thisV0 = (double) std::stod(argv[4]);

    Params P = {thisEta, thisRho, thisV0};
    std::string directoryName = "slurm_temp_logs_" + std::to_string(thisCount);
    {
        int suffix = 1;
        std::string candidate = directoryName;
        while (std::filesystem::exists(candidate)) {
            candidate = directoryName + "_" + std::to_string(suffix++);
        }
        directoryName = candidate;
    }
    std::string outputFilePath = directoryName+"/outputs.txt";
    std::filesystem::create_directories(directoryName);
    std::ofstream outFile(outputFilePath);
    vector<double> pos(2 * P.N);
    vector<double> orient(P.N);
    vector<double> new_orient(P.N);   // FIXED: buffer for new orientations
    vector<double> cosv(P.N), sinv(P.N);
    vector<double> new_cosv(P.N), new_sinv(P.N);
    long long final_step = P.NSTEPS;



    outFile << "Simulation #" << std::to_string(thisCount) << ", Parameters: eta = " << std::to_string(thisEta) << " | rho = " << std::to_string(thisRho) << " | v0 = " << thisV0 << "s\n";
    initialize_particles(P, pos, orient);


    for (size_t i = 0; i < P.N; ++i) {
        cosv[i] = cos(orient[i]);
        sinv[i] = sin(orient[i]);
    }
    int nc = max(1, int(floor((double)P.L / P.r0)));
    double cell_size = (double)P.L / nc;

    vector<int> head(nc * nc, -1);
    vector<int> next(P.N, -1);

    int max_threads = 1;
#ifdef _OPENMP
    max_threads = omp_get_max_threads();
#endif

    vector<mt19937_64> thread_rngs(max_threads);
    uint64_t base_seed =
        chrono::high_resolution_clock::now()
        .time_since_epoch().count();
    for (int t = 0; t < max_threads; ++t)
        thread_rngs[t].seed(base_seed + 1234 * (t+1));

    auto start = chrono::steady_clock::now();

    vector<double> order_history;
    order_history.reserve(P.CONVERGE_WINDOW);

    for (long long step = 0; step < P.NSTEPS; ++step) {

        build_cell_list(P, pos, head, next, nc, cell_size);
        update_orientations(P, pos, cosv, sinv, new_orient, new_cosv, new_sinv, head, next, nc, cell_size, thread_rngs);
        orient.swap(new_orient);
        cosv.swap(new_cosv);
        sinv.swap(new_sinv);
        update_positions(P, pos, cosv, sinv);

        double order = compute_order(P, cosv, sinv);
        if (step % 1000 == 0) {
            double elapsed = (int) chrono::duration<double>(chrono::steady_clock::now() - start).count();
            outFile << "Step " << step << " | Order = " << std::setprecision(std::numeric_limits<double>::max_digits10) <<order;
            outFile << " | Time = " << elapsed << "s\n";
        }

        if (step % P.CHECKPOINT_EVERY == 0) {
            double elapsed = (int) chrono::duration<double>(chrono::steady_clock::now() - start).count();

            cout << "Step: " << step << ", Order: " << order;
            if (step % P.CHECKPOINT_EVERY == 0 && step!=0) {
                cout << ", Time: " << elapsed << "s\n";
            } else {
                cout << "\n";
            }

            order_history.push_back(order);

            if ((int)order_history.size() > P.CONVERGE_WINDOW)
                order_history.erase(order_history.begin());

            if ((int)order_history.size() == P.CONVERGE_WINDOW) {
                double mean = accumulate(order_history.begin(), order_history.end(), 0.0)
                            / P.CONVERGE_WINDOW;
                double variance = 0.0;
                for (double v : order_history)
                    variance += (v - mean) * (v - mean);
                variance /= P.CONVERGE_WINDOW;

                if (variance < P.CONVERGE_TOL) {
                    cout << "Converged at step " << step
                        << " | mean order = " << mean
                        << " | variance = " << variance << "\n";
                    final_step = step;
                    break;
                }
            }

            char fname[256];
        }
    }
    std::string newNewDirName = directoryName+"/final_state.npz";
    save_state(newNewDirName, P, pos, orient, final_step);

    cout << "\nSimulation finished. Total elapsed time: "<< (int) chrono::duration<double>(chrono::steady_clock::now() - start).count() << "s\n";
    outFile.close();
    return 0;
} 