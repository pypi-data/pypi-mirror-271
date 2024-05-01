import json
import numpy as np
from typing import Optional, Union
from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML


class ComputationalDomain(Enum):
    L = 'L'
    dx = 'dx'
    Nx = 'Nx'
    T = 'T'
    dt = 'dt'


class InitialCondition:
    def __init__(self):
        self.is_using_custom_init_eta: bool
        self.is_using_custom_init_u: bool
        self.is_using_custom_init_u: bool
        self.eta_initial_arr: list
        self.eta_initial: str
        self.u_initial_arr: list
        self.u_initial: str


class WaveConfig:
    def __init__(self):
        self.is_hydrostatic: bool
        self.p_approx_method: bool
        self.momentum: bool


class Renderer:
    def __init__(self):
        self.y_axis_limit: list


def animate_1d(x_lim, y_lim, L_arr, eta, Nt, bottom=np.array([]), moving_seabed=False):
    fig, ax = plt.subplots()
    ax.set_xlim(x_lim[0], x_lim[1])
    ax.set_ylim(y_lim[0], y_lim[1])

    line, = ax.plot([], [], lw=2)

    if (bottom.size > 0):
        ax.plot(L_arr, -bottom)

    def init():
        line.set_data([], [])
        return line,

    def update(frame):
        x_values = L_arr
        y_values = eta[:, frame]
        line.set_data(x_values, y_values)
        return line,

    animation = FuncAnimation(fig, update, frames=Nt,
                              init_func=init, blit=True)

    plt.close()
    return HTML(animation.to_jshtml())


class SWE:
    def __init__(self):
        self.type = ''
        self.output = {}
        self.computational_domain: ComputationalDomain
        self.initial_condition: InitialCondition
        self.wave_config: WaveConfig = {}
        self.renderer = {}

    def simulation(self, dir, chunked=False):
        if (chunked):
            file_path = f"{dir}/simulation_result-0.dat"
        else:
            file_path = dir

        with open(file_path, 'r') as file:
            data = file.read()
        try:
            parsed_data = json.loads(data)
            self.type = parsed_data.get('type')
            self.computational_domain = parsed_data.get('computational_domain')
            self.initial_condition = parsed_data.get('initial_condition')

            if (chunked):
                combined_data = []
                next_chunk = parsed_data.get('next_chunk')

                while next_chunk is not None:
                    # Load the data from the chunk file
                    print(f'Reading chunk {next_chunk}')

                    file_path = f"{dir}/simulation_result-{next_chunk}.dat"
                    with open(file_path, 'r') as file:
                        json_data = json.load(file)
                        data_chunk = json_data["output"]["eta"]
                        next_chunk = json_data["next_chunk"]

                    # Append the chunk data to the combined data list
                    combined_data.append(data_chunk)

                final_shape = (
                    len(combined_data),
                    len(combined_data[0]),
                    len(combined_data[0][0]),
                    len(combined_data[0][0][0])
                )

                Nx = self.get_computational_domain('Nx')
                Ny = self.get_computational_domain('Ny')
                Nt = self.get_computational_domain('Nt')

                original_data = np.zeros([Nx, Ny, Nt])

                for chunk, chunk_data in enumerate(combined_data):
                    for x_index, x_data in enumerate(chunk_data):
                        for y_index, y_data in enumerate(x_data):
                            for t_index, t_value in enumerate(y_data):
                                original_data[x_index,
                                              y_index, chunk * 250 + t_index] = t_value

                print('Simulation loaded successfully')
                self.output = {
                    "eta": original_data
                }
            else:
                print('Simulation loaded successfully')
                self.output = parsed_data.get('output')

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        except FileNotFoundError:
            print("File not found")
        except Exception as e:
            print("An error occurred:", e)

    def get_eta(self):
        return np.array(self.output.get('eta'))

    # 1D
    def plot_across_spatial(self, t):
        if (self.type == '2d'):
            print('Please use plot_across_spatial_2d instead')
            return
        if (t > self.get_computational_domain('T')):
            print('Inputted t is too big')
            return

        Nx = self.get_computational_domain('Nx')
        L = self.get_computational_domain('L')
        L_arr = np.linspace(0, L, Nx)

        plt.figure()
        plt.plot(L_arr[:Nx], self.get_eta()[:Nx, t])
        plt.xlabel('$x$')
        plt.title(f'$t={t}$')
        plt.grid()

    def plot_across_time(self, x):
        if (self.type == '2d'):
            print('Please use plot_across_time_2d instead')
            return

        if (x > self.get_computational_domain('L')):
            print('Inputted x is too big')
            return

        Nt = self.get_computational_domain('Nt')
        T = self.get_computational_domain('T')
        T_arr = np.linspace(0, T, Nt)

        plt.figure()
        plt.plot(T_arr[:Nt], self.get_eta()[x, :Nt])
        plt.xlabel('t')
        plt.title(f'$x={x}$')

    def generate_animation(self, y_lim, Nt):
        if (self.type == '2d'):
            print('Please use generate_animation_2d instead')
            return

        L = self.get_computational_domain('L')
        Nx = self.get_computational_domain('Nx')
        L_arr = np.linspace(0, L, Nx)

        return animate_1d([L_arr[0], L_arr[-1]], y_lim, L_arr, self.get_eta()[:Nx, :Nt],
                          Nt)

    # 2D
    def plot_across_spatial_2d(self, plane, at, t):
        if (self.type == '1d'):
            print('Please use plot_across_spatial instead')
            return

        if (t > self.get_computational_domain('T')):
            print('Inputted t is too big')
            return

        L = self.get_computational_domain('L')
        Nx = self.get_computational_domain('Nx')
        M = self.get_computational_domain('M')
        Ny = self.get_computational_domain('Ny')

        dx = self.get_computational_domain('dx')
        dy = self.get_computational_domain('dy')
        dt = self.get_computational_domain('dt')

        plt.figure()
        plt.grid()

        if (plane == 'xz'):
            horizontal_axis = np.linspace(0, L, Nx)
            plt.plot(horizontal_axis[:Nx], self.get_eta()[
                     :Nx, int(at // dy), int(t // dt)])
            plt.xlabel('$x$')
            plt.title(f'$x={at}$')
        elif (plane == 'yz'):
            horizontal_axis = np.linspace(0, M, Ny)
            plt.plot(horizontal_axis[:Ny], self.get_eta()[
                     int(at // dx), :Ny, int(t // dt)])
            plt.xlabel('$y$')
            plt.title(f'$y={at}$')

    def plot_across_time_2d(self, x, y):
        if (self.type == '1d'):
            print('Please use plot_across_time instead')
            return
        if (x > self.get_computational_domain('L') or y > self.get_computational_domain('M')):
            print('Inputted x or y is too big')
            return

        Nt = self.get_computational_domain('Nt')
        T = self.get_computational_domain('T')
        T_arr = np.linspace(0, T, Nt)

        dx = self.get_computational_domain('dx')
        dy = self.get_computational_domain('dy')

        plt.figure()
        plt.plot(T_arr[:Nt], self.get_eta()
                 [int(x // dx), int(y // dy), :Nt])
        plt.xlabel('t')
        plt.title(f'$x={x}, y={y}$')

    def generate_animation_2d(self, plane, at, z_lim, Nt):
        if (self.type == '1d'):
            print('Please use generate_animation instead')
            return

        L = self.get_computational_domain('L')
        Nx = self.get_computational_domain('Nx')
        M = self.get_computational_domain('M')
        Ny = self.get_computational_domain('Ny')

        if (plane == 'xz'):
            horizontal_axis = np.linspace(0, L, Nx)
            return animate_1d([horizontal_axis[0], horizontal_axis[-1]], z_lim, horizontal_axis, self.get_eta()[:Nx, at, :Nt],
                              Nt)

        elif (plane == 'yz'):
            horizontal_axis = np.linspace(0, M, Ny)

            return animate_1d([horizontal_axis[0], horizontal_axis[-1]], z_lim, horizontal_axis, self.get_eta()[at, :Ny, :Nt],
                              Nt)

    def get_computational_domain(self, val: ComputationalDomain = None):
        if (val):
            return self.computational_domain.get(val)
        return self.computational_domain

    def get_initial_condition(self, val=None):
        if (val):
            return self.initial_condition.get(val)
        return self.initial_condition

    def get_wave_config(self, val=None):
        if (val):
            return self.wave_config.get(val)
        return self.wave_config

    def get_renderer(self, val=None):
        if (val):
            return self.renderer.get(val)
        return self.renderer

    def export_bathymetry_from_array(self, array):
        bathymetry = {"bathymetry": [[j for j in i] for i in array]}
        file_path = 'bathymetry.dat'

        with open(file_path, 'w') as file:
            json.dump(bathymetry, file, indent=2)

        print(f'Bathymetry data has been written to {file_path}')

    def export_init_eta_from_array(self, array):
        init_eta = {"init_eta": [i for i in array]}
        file_path = 'init_eta.dat'

        with open(file_path, 'w') as file:
            json.dump(init_eta, file, indent=2)

        print(f'Initial Eta data has been written to {file_path} ')

    def export_init_u_from_array(self, array):
        init_u = {"init_u": [i for i in array]}
        file_path = 'init_u.dat'

        with open(file_path, 'w') as file:
            json.dump(init_u, file, indent=2)

        print(f'Initial u data has been written to {file_path} ')

    def export_init_v_from_array(self, array):
        init_u = {"init_v": [i for i in array]}
        file_path = 'init_v.dat'

        with open(file_path, 'w') as file:
            json.dump(init_u, file, indent=2)

        print(f'Initial v data has been written to {file_path} ')

    def export_init_u1_from_array(self, array):
        init_u1 = {"init_u1": [i for i in array]}
        file_path = 'init_u1.dat'

        with open(file_path, 'w') as file:
            json.dump(init_u1, file, indent=2)

        print(f'Initial u1 data has been written to {file_path} ')

    def export_init_u2_from_array(self, array):
        init_u2 = {"init_u2": [i for i in array]}
        file_path = 'init_u2.dat'

        with open(file_path, 'w') as file:
            json.dump(init_u2, file, indent=2)

        print(f'Initial u2 data has been written to {file_path} ')

    def export_boundary_u_l_from_array(self, array):
        boundary_2d = {"boundary_u_l": [
            i for i in [[j for j in i] for i in array]]}
        file_path = 'boundary_u_l.dat'

        with open(file_path, 'w') as file:
            json.dump(boundary_2d, file, indent=2)

        print(f'Boundary u left data has been written to {file_path} ')

    def export_boundary_u_r_from_array(self, array):
        boundary_2d = {"boundary_u_r": [i for i in array]}
        file_path = 'boundary_u_r.dat'

        with open(file_path, 'w') as file:
            json.dump(boundary_2d, file, indent=2)

        print(f'Boundary u right data has been written to {file_path} ')

    def export_boundary_u_f_from_array(self, array):
        boundary_2d = {"boundary_u_f": [i for i in array]}
        file_path = 'boundary_u_f.dat'

        with open(file_path, 'w') as file:
            json.dump(boundary_2d, file, indent=2)

        print(f'Boundary u front data has been written to {file_path} ')

    def export_boundary_u_b_from_array(self, array):
        boundary_2d = {"boundary_u_b": [i for i in array]}
        file_path = 'boundary_u_b.dat'

        with open(file_path, 'w') as file:
            json.dump(boundary_2d, file, indent=2)

        print(f'Boundary u back data has been written to {file_path} ')
