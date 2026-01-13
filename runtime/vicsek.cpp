#include <bits/stdc++.h>
#include <chrono>
#include <random>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <filesystem>

#ifdef _OPENMP
#include <omp.h>
#endif

#include "cnpy.h"

using namespace std;
//imports lowk broken but i fix later; code works fine

int main() {
    const string LOGDIR = "temp_logs";
    filesystem::create_directories(LOGDIR);

    const string ORDER_FILE = LOGDIR + "/temp_order.txt";
    const string FINAL_STATE_FILE = LOGDIR + "/final_state.npz";
    const string CHECKPOINT_FMT = LOGDIR + "/checkpoint_%07d.npz";

    int L = 150;
    double rho = 0.5;
    size_t N = static_cast<size_t>(rho * L * L);

    double r0 = 1.0;
    double deltat = 1.0;
    double factor = 1.0;
    double v0 = r0 / deltat * factor;
    double eta = 0.5;

    const long long NSTEPS = 1'000'000;
    const int CHECKPOINT_EVERY = 1000;


    mt19937_64 seed_rng(
        chrono::high_resolution_clock::now().time_since_epoch().count());
    uniform_real_distribution<double> unif01(0.0, 1.0);
    uniform_real_distribution<double> angle_unif(-M_PI, M_PI);

    vector<double> pos(2 * N);
    vector<double> orient(N);

    for (size_t i = 0; i < N; ++i) {
        pos[2 * i + 0] = unif01(seed_rng) * L;
        pos[2 * i + 1] = unif01(seed_rng) * L;
        orient[i] = angle_unif(seed_rng);
    }

    long long steps = 0;
    auto starttime = chrono::steady_clock::now();

    {
        ofstream f(ORDER_FILE);
        f << time(nullptr) << "\n";
        f << "L=" << L << ", rho=" << rho << ", N=" << N
          << ", r0=" << r0 << ", deltat=" << deltat
          << ", factor=" << factor << ", v0=" << v0
          << ", eta=" << eta << "\n";
    }

    vector<double> cosv(N), sinv(N);

    int nc = std::max(1, int(floor((double)L / r0)));
    double cell_size = (double)L / nc;
    size_t ncells = (size_t)nc * (size_t)nc;

    vector<int> head(ncells, -1);
    vector<int> next(N, -1);

    auto build_cell_list = [&](const vector<double>& pos_vec) {
        std::fill(head.begin(), head.end(), -1);
        for (int i = 0; i < (int)N; ++i) {
            int cx = int(pos_vec[2*i] / cell_size);
            int cy = int(pos_vec[2*i+1] / cell_size);
            if (cx < 0) cx = 0; else if (cx >= nc) cx = nc-1;
            if (cy < 0) cy = 0; else if (cy >= nc) cy = nc-1;
            int cid = cx + cy * nc;
            next[i] = head[cid];
            head[cid] = i;
        }
    };

    auto save_state = [&](const string& filename) {
        vector<size_t> pos_shape = {N, 2};
        cnpy::npz_save(filename, "pos", pos.data(), pos_shape, "w");

        vector<size_t> oshape = {N};
        cnpy::npz_save(filename, "orient", orient.data(), oshape, "a");

        vector<size_t> sshape = {1};
        cnpy::npz_save(filename, "steps", &steps, sshape, "a");

        double params[7] = {
            (double)L, rho, (double)N, r0, deltat, v0, eta};
        vector<size_t> pshape = {7};
        cnpy::npz_save(filename, "params", params, pshape, "a");

        cout << "\nState saved to " << filename
             << " (step " << steps << ")\n";
    };

    int max_threads = 1;
#ifdef _OPENMP
    max_threads = omp_get_max_threads();
#endif
    vector<mt19937_64> thread_rngs(max_threads);
    uint64_t base_seed = chrono::high_resolution_clock::now().time_since_epoch().count();
    for (int t=0; t<max_threads; ++t)
        thread_rngs[t].seed(base_seed + 1315423911u * (t+1));

    uniform_real_distribution<double> uniform_noise(-M_PI, M_PI);

    try {
        for (; steps < NSTEPS; ++steps) {
            build_cell_list(pos);

            double r0sq = r0 * r0;
#pragma omp parallel for schedule(dynamic)
            for (int i = 0; i < (int)N; ++i) {
                int tid = 0;
#ifdef _OPENMP
                tid = omp_get_thread_num();
#endif
                auto &rng = thread_rngs[tid];
                std::uniform_real_distribution<double> noise_dist(0.0, 1.0);

                double xi = pos[2*i];
                double yi = pos[2*i+1];
                int cx = int(xi / cell_size);
                int cy = int(yi / cell_size);

                double sx = 0.0, sy = 0.0;

                for (int dx = -1; dx <= 1; ++dx) {
                    int ncx = cx + dx;
                    if (ncx < 0) ncx += nc;
                    else if (ncx >= nc) ncx -= nc;
                    for (int dy = -1; dy <= 1; ++dy) {
                        int ncy = cy + dy;
                        if (ncy < 0) ncy += nc;
                        else if (ncy >= nc) ncy -= nc;
                        int cid = ncx + ncy * nc;

                        for (int j = head[cid]; j != -1; j = next[j]) {
                            double dxij = pos[2*j] - xi;
                            double dyij = pos[2*j+1] - yi;
                            if (dxij >  L/2.0) dxij -= L;
                            else if (dxij < -L/2.0) dxij += L;
                            if (dyij >  L/2.0) dyij -= L;
                            else if (dyij < -L/2.0) dyij += L;

                            double dsq = dxij*dxij + dyij*dyij;
                            if (dsq <= r0sq) {
                                sx += cos(orient[j]);
                                sy += sin(orient[j]);
                            }
                        }
                    }
                }

                double noise = (uniform_noise(rng)) * eta;
                double theta = atan2(sy, sx) + noise;
                orient[i] = theta;
                cosv[i] = cos(theta);
                sinv[i] = sin(theta);
            }

#pragma omp parallel for schedule(static)
            for (int i = 0; i < (int)N; ++i) {
                double x = pos[2*i] + v0 * cosv[i];
                double y = pos[2*i+1] + v0 * sinv[i];

                if (x >= L) x -= L;
                else if (x < 0.0) x += L;
                if (y >= L) y -= L;
                else if (y < 0.0) y += L;

                pos[2*i] = x;
                pos[2*i+1] = y;
            }

            double sumx = 0.0, sumy = 0.0;
#pragma omp parallel for reduction(+:sumx,sumy)
            for (int i = 0; i < (int)N; ++i) {
                sumx += cosv[i];
                sumy += sinv[i];
            }
            double order = hypot(sumx, sumy) / N;

            {
                ofstream f(ORDER_FILE, ios::app);
                double elapsed =
                    chrono::duration<double>(chrono::steady_clock::now() - starttime)
                        .count();
                f << "#" << setw(7) << setfill('0') << steps
                  << ", " << fixed << setprecision(3)
                  << elapsed << "s, "
                  << setprecision(6) << order << "\n";
            }

            if (steps % CHECKPOINT_EVERY == 0) {
                char buf[256];
                sprintf(buf, CHECKPOINT_FMT.c_str(), (int)steps);
                save_state(buf);
            }
        } 
    } catch (...) {
        cout << "\nInterrupted.\n";
    }

    save_state(FINAL_STATE_FILE);
    cout << "Simulation finished.\n";
    return 0;
}
