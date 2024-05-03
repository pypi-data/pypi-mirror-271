from bmipy import Bmi
from typing import Any, Tuple
from HBV import utils
import numpy as np
import warnings

DICT_VAR_UNITS = {"Imax": "mm",
                  "Ce": "-",
                  "Sumax": "mm",
                  "Beta": "-",
                  "Pmax": "mm",
                  "Tlag": "d",
                  "Kf": "-",
                  "Ks": "-",
                  "FM": "mm/deg/d",
                  "Si": "mm",
                  "Su": "mm",
                  "Sf": "mm",
                  "Ss": "mm",
                  "Sp": "mm",
                  "M_dt": "mm/d",
                  "Ei_dt": "mm/d",
                  "Ea_dt": "mm/d",
                  "Qs_dt": "mm/d",
                  "Qf_dt": "mm/d",
                  "Q_tot_dt": "mm/d",
                  "Q": "mm/d"}


class HBV(Bmi):
    """HBV model wrapped in a BMI interface."""

    def initialize(self, config_file: str) -> None:
        """"Based on LeakyBucketBMI simple implementation of HBV without snow component
            Requires atleast:
            ---------------------
            'precipitation_file': xarray with "pr" variable & time component
            'potential_evaporation_file': xarray with "pev" variable of same nature as pr
            'parameters': list of 8 parameters by a ','
            'initial_storage' list of 4 storage parameters split by a ','

        """
        # open json files containing data
        self.config: dict[str, Any] = utils.read_config(config_file)

        # store forcing & obs
        self.ds_P = utils.load_var(self.config["precipitation_file"], "pr")
        self.P = self.ds_P.to_numpy()

        self.ds_EP = utils.load_var(self.config["potential_evaporation_file"], "evspsblpot")
        self.EP = self.ds_EP.to_numpy()

        self.ds_Tmean = utils.load_var(self.config["mean_temperature_file"], "tas")
        self.Tmean = self.ds_Tmean.to_numpy()

        # set up times
        self.time = self.ds_P['time'].astype("datetime64[s]").to_numpy()
        self.end_timestep = len(self.time)
        self.current_timestep = 0

        # time step size in seconds (to be able to do unit conversions) - change here to days
        self.dt = (
                          self.time[1] - self.time[0]
                  ) / np.timedelta64(1, "s") / 24 / 3600

        # define parameters 
        self.set_pars(np.array(self.config['parameters'].split(','), dtype=np.float64))

        # add memory vector for tlag & run weights function
        self.memory_vector_lag = self.set_empty_memory_vector_lag()

        # define storage & flow terms, flows 0, storages initialised 
        s_in = np.array(self.config['initial_storage'].split(','), dtype=np.float64)
        self.set_storage(s_in)

        # set other flows for initial step
        self.M_dt = 0  # snow melt
        self.Ei_dt = 0  # interception evaporation
        self.Ea_dt = 0  # actual evaportation
        self.Qs_dt = 0  # slow flow
        self.Qf_dt = 0  # fast flow
        self.Q_tot_dt = 0  # total flow
        self.Q = 0  # Final model prediction

        # other constant for Snow:
        self.Tt = -0.5  # Threshold temperature set for now. Can be between -1 to 1

    def set_pars(self, par) -> None:
        self.I_max = par[0]  # maximum interception
        self.Ce = par[1]  # Ea = Su / (sumax * Ce) * Ep
        self.Su_max = par[2]  # ''
        self.beta = par[3]  # Cr = (su/sumax)**beta
        self.P_max = par[4]  # Qus = Pmax * (Su/Sumax)
        self.T_lag = self.set_tlag(par[5])  # used in triangular transfer function
        self.Kf = par[6]  # Qf=kf*sf
        self.Ks = par[7]  # Qs=Ks*
        self.FM = par[8]  # degree day factor: Melt FM * (Tmean-Tt)

    def set_storage(self, stor) -> None:
        self.Si = stor[0]  # Interception storage
        self.Su = stor[1]  # Unsaturated Rootzone Storage
        self.Sf = stor[2]  # Fastflow storage
        self.Ss = stor[3]  # Groundwater storage
        self.Sp = stor[4]  # SnowPack storage

    def update(self) -> None:
        """ Updates model one timestep

        Old documentation:
            Function to run the update part of one timestep of the HBV model
            par: array/list containing 9 parameters: Imax,  Ce,  Sumax, beta,  Pmax,  T_lag,   Kf,   Ks, Fm (floats)
            s_in: array/list containing 5 storage terms which are input to the timestep: Si,  Su, Sf, Ss,Sp (floats)
            storage_terms: list of arrays which store: Si, Su, Sf, Ss,Sp, Ei_dt, Ea_dt, Qs_dt_lst, Qf_dt_lst, Q_tot_dt
            step_n - nth step which formard model takes: used to determin which Precipitaion & evaporation to use
        """
        if self.current_timestep < self.end_timestep:
            self.P_dt = self.P[self.current_timestep] * self.dt
            self.Ep_dt = self.EP[self.current_timestep]  * self.dt
            self.Tmean_i = self.Tmean[self.current_timestep]  * self.dt

            # split P into rain and snow:
            if self.Tmean_i < self.Tt:
                self.Pr = 0  # if snowing, no rainfall
                self.Ps = self.P_dt  # all precip goes into snow
                self.M_dt = 0  # too cold to meld
                self.Sp += self.Ps
            else:
                self.Pr = self.P_dt  # if not snowing, all rainfall
                self.Ps = 0  # No snow
                self.M_dt = min(self.Sp / self.dt, self.FM * (self.Tmean_i - self.Tt))  # melt factor * diff in temp
                self.Sp -= self.M_dt  # remove melt from snowpack content
                self.Pr += self.M_dt  # add it to `rainfall`: snow melt can also be intercepted

            # Interception Reservoir
            if self.Pr > 0:
                # if there is rain, no evap
                self.Si = self.Si + self.Pr  # increase the storage
                self.Pe_dt = max((self.Si - self.I_max) / self.dt, 0)
                self.Si = self.Si - self.Pe_dt
                self.Ei_dt = 0  # if rainfall, evaporation = 0 as too moist
            else:
                # Evaporation only when there is no rainfall
                self.Pe_dt = 0  # nothing flows in so must be 0
                self.Ei_dt = min(self.Ep_dt, self.Si / self.dt)  # evaporation limited by storage
                self.Si = self.Si - self.Ei_dt

            # split flow into Unsaturated Reservoir and Fast flow
            if self.Pe_dt > 0:
                cr = (self.Su / self.Su_max) ** self.beta
                Qiu_dt = (1 - cr) * self.Pe_dt  # flux from Ir to Ur
                self.Su = self.Su + Qiu_dt
                Quf_dt = cr * self.Pe_dt  # flux from Su to Sf
            else:
                Quf_dt = 0

            # Transpiration
            self.Ep_dt = max(0, self.Ep_dt - self.Ei_dt)  # Transpiration
            self.Ea_dt = self.Ep_dt * (self.Su / (self.Su_max * self.Ce))
            self.Ea_dt = min(self.Su, self.Ea_dt)  # limited by water in soil
            self.Su = self.Su - self.Ea_dt

            # Percolation
            Qus_dt = self.P_max * (self.Su / self.Su_max) * self.dt  # Flux from Su to Ss
            self.Su = self.Su - Qus_dt

            # Fast Reservoir
            self.Sf = self.Sf + Quf_dt
            self.Qf_dt = max(self.dt * self.Kf * self.Sf, 0)
            self.Sf = self.Sf - self.Qf_dt

            # Slow Reservoir
            self.Ss = self.Ss + Qus_dt
            self.Qs_dt = max(self.Ss * self.Ks * self.dt, 0)
            self.Ss = self.Ss - self.Qs_dt

            # total = fast + slow
            self.Q_tot_dt = self.Qs_dt + self.Qf_dt
            # add time lag to the process - Qm is set here
            self.add_time_lag()
            # self.Q = self.Q_tot_dt

            # Advance the model time by one step
            self.current_timestep += 1

    def updating_dict_var_obj(self) -> None:
        """Function which makes getting the objects more readable-  but adds more boiler plate.."""
        self.dict_var_obj = {
                            "Imax": self.I_max,
                            "Ce": self.Ce,
                            "Sumax": self.Su_max,
                            "Beta": self.beta,
                            "Pmax": self.P_max,
                            "Tlag": self.T_lag,
                            "Kf": self.Kf,
                            "Ks": self.Ks,
                            "FM": self.FM,
                            "Si": self.Si,
                            "Su": self.Su,
                            "Sf": self.Sf,
                            "Ss": self.Ss,
                            "Sp": self.Sp,
                            "M_dt": self.M_dt,
                            "Ei_dt": self.Ei_dt,
                            "Ea_dt": self.Ea_dt,
                            "Qs_dt": self.Qs_dt,
                            "Qf_dt": self.Qf_dt,
                            "Q_tot_dt": self.Q_tot_dt,
                            "Q": self.Q,
                            }

    def updating_obj_from_dict_var(self) -> None:
        """Function which inverts the dictionary above & sets objects correctly"""
        param_names = ["Imax", "Ce", "Sumax", "Beta", "Pmax", "Tlag", "Kf", "Ks", "FM"]
        stor_names = ["Si", "Su", "Sf", "Ss", "Sp"]
        self.set_pars([self.dict_var_obj[par] for par in param_names])
        self.set_storage([self.dict_var_obj[stor] for stor in stor_names])

    def weight_function(self):
        """Generates weights for convolution using generates a weibull weight function"""

        n_max = int(np.ceil(self.T_lag))
        if n_max == 1:
            weights = float(1)
        else:
            weights = np.zeros(n_max)
            th = self.T_lag / 2
            nh = int(np.floor(th))
            for i in range(0, nh):
                weights[i] = (float(i + 1) - 0.5) / th
            i = nh

            weights[i] = (1 + (float(i + 1) - 1) / th) * (th - int(np.floor(th))) / 2 + (
                        1 + (self.T_lag - float(i + 1)) / th) * (int(np.floor(th)) + 1 - th) / 2
            for i in range(nh + 1, int(np.floor(self.T_lag))):
                weights[i] = (self.T_lag - float(i + 1) + 0.5) / th

            if self.T_lag > int(np.floor(self.T_lag)):
                weights[int(np.floor(self.T_lag))] = (self.T_lag - int(np.floor(self.T_lag))) ** 2 / (2 * th)

            weights = weights / sum(weights)

        return weights

    def add_time_lag(self) -> None:
        """Adds lag based on weights and discharge"""
        # with support for T_lag =0
        if len(self.memory_vector_lag) > 0:
            # Distribute current Q_tot_dt to memory vector
            self.memory_vector_lag += self.weights * self.Q_tot_dt

            # Extract the latest Qm
            self.Q = self.memory_vector_lag[0]

            # Make a forecast to the next time step
            # This cycles the array [1,2,3,4] becomes [2,3,4,1]
            self.memory_vector_lag = np.roll(self.memory_vector_lag, -1)
            # the next last entry becomes 0 (outside of convolution lag)
            self.memory_vector_lag[-1] = 0

    def set_empty_memory_vector_lag(self):
        self.weights = self.weight_function()
        return np.zeros(self.T_lag)

    def get_component_name(self) -> str:
        return "HBV"

    def get_value(self, var_name: str, dest: np.ndarray) -> np.ndarray:
        # first update the dictionary to match the current values of object
        self.updating_dict_var_obj()
        # handle the memory vector
        if var_name[:len("memory_vector")] == "memory_vector":
            if var_name == "memory_vector":
                dest[:] = np.array(None)
                message = "No action undertaken. Please use `set_value(f'memory_vector{n}',src)` where n is the index."
                warnings.warn(message, category=SyntaxWarning)
            else:
                mem_index = int(var_name[len("memory_vector"):])
                if mem_index < len(self.memory_vector_lag):
                    dest[:] = self.memory_vector_lag[mem_index]
                else:
                    raise IndexError(
                        f'{mem_index} is out of range for memory vector size {len(self.memory_vector_lag)}')

            return dest
        # otherwise return the variable from the dictionary
        elif var_name in self.dict_var_obj:
            dest[:] = np.array(self.dict_var_obj[var_name])
            return dest
        else:
            raise ValueError(f"Unknown variable {var_name}")

    def get_var_units(self, var_name: str) -> str:
        # look up table
        if var_name in DICT_VAR_UNITS:
            return DICT_VAR_UNITS[var_name]
        else:
            raise ValueError(f"Unknown variable {var_name}")

    def set_value(self, var_name: str, src: np.ndarray) -> None:
        # update the dict which maps variables to their current value
        self.updating_dict_var_obj()
        # handle two special case:
        # 1. tlag which must be int and rests memory vector
        if var_name == "Tlag":
            old_T_lag = self.T_lag
            old_memory_vector = self.memory_vector_lag
            self.T_lag = self.set_tlag(src[0])
            # when we change Tlag, we shift over the size of the memory vector
            # assume that if we reset the Tlag value, we also always reset the memory vector
            new_memory_vector = self.set_empty_memory_vector_lag()
            # if the new vector is longer, we simply add the new values at the end
            if old_T_lag < self.T_lag:
                new_memory_vector[:old_T_lag] = old_memory_vector
            # if the new vector is shorter, we sum the old extra values to the last value: as not to `lose` water
            elif old_T_lag > self.T_lag:
                new_memory_vector = old_memory_vector[:self.T_lag]
                new_memory_vector[-1] += sum(old_memory_vector[self.T_lag:])
            # set new vector
            self.memory_vector_lag = new_memory_vector

        # 2. values in the memory vector must be set manually to work with DA
        elif var_name[:len("memory_vector")] == "memory_vector":
            if var_name == "memory_vector":
                message = "No action undertaken. Please use `set_value(memory_vector{n},src)` where n is the index."
                warnings.warn(message=message, category=SyntaxWarning)
                pass
            else:
                mem_index = int(var_name[len("memory_vector"):])
                if mem_index < len(self.memory_vector_lag):
                    self.memory_vector_lag[mem_index] = src[0]
                else:
                    raise IndexError(
                        f'{mem_index} is out of range for memory vector size {len(self.memory_vector_lag)}')

        # all other values can be set here
        elif var_name in self.dict_var_obj:
            self.dict_var_obj[var_name] = src[0]
            self.updating_obj_from_dict_var()

        else:
            raise ValueError(f"Unknown variable {var_name}")

    # this is a bad way, but oh well
    # first we set the new value in the dictionary
    # this doesn't update the obj...
    def get_output_var_names(self) -> Tuple[str]:
        return tuple([str(key) for key in DICT_VAR_UNITS.keys()])

    # The BMI has to have some time-related functionality:
    def get_start_time(self) -> float:
        """Return end time in seconds since 1 january 1970."""
        return get_unixtime(self.time[0])  # type: ignore

    def get_end_time(self) -> float:
        """Return end time in seconds since 1 january 1970."""
        return get_unixtime(self.time[-1])  # type: ignore

    def get_current_time(self) -> float:
        """Return current time in seconds since 1 january 1970."""
        # we get the timestep from the data, but the stopping condition requires it to go one beyond. 
        return get_unixtime(self.time[self.current_timestep])  # type: ignore

    def set_tlag(self, T_lag_in) -> int:
        """Ensures T_lag is an integer of at minimum 1"""
        T_lag = max(1, int(round(T_lag_in, 0)))
        return T_lag

    def get_time_step(self) -> float:
        if len(self.time) > 1:
            return float((self.time[1] - self.time[0]) / np.timedelta64(1, "s"))
        else:
            message = "No time series defined"
            warnings.warn(message=message, category=ImportWarning)
            return 0.0

    def get_time_units(self) -> str:
        return "seconds since 1970-01-01 00:00:00.0 +0000"

    # TODO implement setting different timestep?
    def get_value_at_indices(
            self, name: str, dest: np.ndarray, inds: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    # TODO implement
    def set_value_at_indices(self, name: str, inds: np.ndarray, src: np.ndarray) -> None:
        raise NotImplementedError()

    def get_var_itemsize(self, name: str) -> int:
        return np.array(0.0).nbytes

    def get_var_nbytes(self, name: str) -> int:
        return np.array(0.0).nbytes

    def get_var_type(self, name: str) -> str:
        return "float64"

    # Grid information
    def get_var_grid(self, name: str) -> int:
        raise 0

    def get_grid_rank(self, grid: int) -> int:
        return 2

    def get_grid_size(self, grid: int) -> int:
        return 1

    def get_grid_type(self, grid: int) -> str:
        return "rectilinear"

    # Uniform rectilinear
    def get_grid_shape(self, grid: int, shape: np.ndarray) -> np.ndarray:
        shape[:] = np.array([1, 1], dtype="int64")
        return shape

    def get_grid_origin(self, grid: int, origin: np.ndarray) -> np.ndarray:
        origin[:] = np.array([0., 0.])
        return origin

    # Non-uniform rectilinear, curvilinear
    def get_grid_x(self, grid: int, x: np.ndarray) -> np.ndarray:
        x[:] = self.ds_P["lon"].to_numpy()
        return x

    def get_grid_y(self, grid: int, y: np.ndarray) -> np.ndarray:
        y[:] = self.ds_P["lat"].to_numpy()
        return y

    def finalize(self) -> None:
        """"Nothing to wrapup"""
        pass

    # not implemented & not planning to

    def get_input_var_names(self) -> Tuple[str]:
        raise NotImplementedError()

    def get_input_item_count(self) -> int:
        raise NotImplementedError()

    def get_output_item_count(self) -> int:
        raise NotImplementedError()

    def get_value_ptr(self, name: str) -> np.ndarray:
        raise NotImplementedError()

    def get_var_location(self, name: str) -> str:
        raise NotImplementedError()

    def update_until(self, time: float) -> None:
        raise NotImplementedError()

    def get_grid_spacing(self, grid: int, spacing: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def get_grid_z(self, grid: int, z: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def get_grid_node_count(self, grid: int) -> int:
        raise NotImplementedError()

    def get_grid_edge_count(self, grid: int) -> int:
        raise NotImplementedError()

    def get_grid_face_count(self, grid: int) -> int:
        raise NotImplementedError()

    def get_grid_edge_nodes(self, grid: int, edge_nodes: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def get_grid_face_edges(self, grid: int, face_edges: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def get_grid_face_nodes(self, grid: int, face_nodes: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def get_grid_nodes_per_face(
            self, grid: int, nodes_per_face: np.ndarray) -> np.ndarray:
        raise NotImplementedError()


def get_unixtime(Ts: np.datetime64) -> int:
    """Get unix timestamp (seconds since 1 january 1970) from a np.datetime64."""
    return np.datetime64(Ts).astype("datetime64[s]").astype("int")
