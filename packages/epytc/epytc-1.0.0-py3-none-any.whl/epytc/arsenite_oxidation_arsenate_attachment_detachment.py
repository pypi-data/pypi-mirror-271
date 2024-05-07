"""Arsenite oxidation and arsenate attachment/detachment module
Reactive species (bulk) - Aqueous arsenite (mg/L), Aqueous arsenate (mg/L), Aqueous arsenic (mg/L), Residual chlorine (mg/L), and Total organic carbon (mg/L)
Reactive species (wall) - Adsorbed arsenate (mg/sq.m)
"""

import math
import random
import numpy as np


class module:
    def details():
        """Displaying the information about the MSRT model selected for water quality analysis

        :return: Details of module
        :rtype: String
        """
        print("Arsenite oxidation and arsenate attachemnt/detachment module loaded.")
        print("\nReactive species (bulk):")
        print(
            "Aqueous arsenite (mg/L)\nAqueous arsenate (mg/L)\nAqueous arsenic (mg/L)\
              \nResidual chlorine (mg/L)\nTotal organic carbon (mg/L)"
        )
        print("\nReactive species (wall):")
        print("Adsorbed arsenate (mg/sq.m)")

    def network(d):
        """Getting basic details of the network

        :param d: EPANET model
        :type d: EPANET object
        :return: Network details
        :rtype: List
        """
        network_info = [
            d.getNodeCount(),
            d.getLinkCount(),
            d.getNodeReservoirCount(),
            d.getNodeTankCount(),
            d.getLinkPumpCount(),
            d.getLinkValveCount(),
            d.getNodeNameID(),
            d.getLinkNameID(),
            d.getNodeReservoirIndex(),
            d.getNodeTankIndex(),
        ]
        index_pumps = []
        for x in range(
            d.getLinkCount() - (d.getLinkPumpCount() + d.getLinkValveCount()),
            len(d.getLinkNameID()) - d.getLinkValveCount(),
        ):
            index_pumps.append(x + 1)
        network_info.append(index_pumps)
        index_valves = []
        for x in range(d.getLinkCount() - d.getLinkValveCount(), len(d.getLinkNameID())):
            index_valves.append(x + 1)
        network_info.append(index_valves)
        network_info.extend(
            [
                d.getFlowUnits(),
                d.getNodesConnectingLinksIndex(),
                d.getConnectivityMatrix(),
            ]
        )
        # Conversion of GPM units to SI units
        if d.getFlowUnits() == "GPM":
            network_info.append(0.3048 * d.getLinkLength())
            network_info.append(25.4 * d.getLinkDiameter())
        else:
            network_info.extend([d.getLinkLength(), d.getLinkDiameter()])
        start_node_matrix = []
        end_node_matrix = []
        for x in range(d.getLinkCount()):
            var1 = d.getNodesConnectingLinksIndex()[x][0]
            var2 = d.getNodesConnectingLinksIndex()[x][1]
            start_node_matrix.append(var1)
            end_node_matrix.append(var2)
        network_info.extend([start_node_matrix, end_node_matrix])
        # Number of nodes omitted for analysis, if any
        number_omitted_nodes = 0
        # Index of omitted nodes
        index_omitted_nodes = []
        # Number of links omitted for analysis, if any
        number_omitted_links = 0
        # Index of omitted nodes
        index_omitted_links = []
        network_info.extend(
            [
                number_omitted_nodes,
                index_omitted_nodes,
                number_omitted_links,
                index_omitted_links,
            ]
        )
        return network_info
    
    def species():
        """Defining the species information of the MSRT module selected

        :return: Species information of the MSRT module
        :rtype: String
        """
        msrt_info = []
        number_water_quality_parameters = 6
        msrt_info.append(number_water_quality_parameters)
        number_bulk_water_quality_parameters = 5
        msrt_info.append(number_bulk_water_quality_parameters)
        number_wall_water_quality_parameters = 1
        msrt_info.append(number_wall_water_quality_parameters)
        number_model_variables = 14
        msrt_info.append(number_model_variables)
        msrt_info = [
            number_water_quality_parameters,
            number_bulk_water_quality_parameters,
            number_wall_water_quality_parameters,
            number_model_variables,
        ]
        return msrt_info

    def zero_order_reaction(num1):
        """Defining zero-order reaction

        :param num1: Water quality simulation time step in seconds
        :type num1: Integer
        :return: Solution of zero-order ordinary differential equation
        :rtype: Float
        """
        delta_zero_order = num1
        return delta_zero_order

    def first_order_reaction(num1, num2, num3):
        """Defining first-order reaction

        :param num1: Reaction rate constant
        :type num1: Float
        :param num2: Concentration value
        :type num2: Float
        :param num3: Water quality simulation time step in seconds
        :type num3: Integer
        :return: Solution of first-order ordinary differential equation
        :rtype: Float
        """
        m1 = num1 * num1
        m2 = num1 * (num2 + (num3 / 4) * m1)
        m3 = num1 * (num2 + (num3 / 4) * m2)
        m4 = num1 * (num2 + (num3 / 2) * m3)
        delta_first_order = (num3 / 6) * (m1 + 2 * m2 + 2 * m3 + m4)
        return delta_first_order

    def Reynolds_number(num1, num2, num3):
        """Defining Reynolds number

        :param num1: Pipe flow velocity in metres per second
        :type num1: Float
        :param num2: Pipe diameter in millimetres
        :type num2: Float
        :param num3: Kinematic viscosity of water in square metres per second
        :type num3: Float
        :return: Reynolds number 
        :rtype: Float
        """
        num4 = num2 * 1e-3
        reynolds_num = (num1 * num4) / num3
        return reynolds_num

    def Schmidt_number(num1, num2):
        """Defining Schmidt number

        :param num1: Kinematic viscosity of water in square metres per second
        :type num1: Float
        :param num2: Molecular diffusivity of a bulk phase species in square metres per second
        :type num2: Float
        :return: Schmidt number 
        :rtype: Float
        """
        schmidt_num = num1 / num2
        return schmidt_num

    def Sherwood_number(num1, num2, num3, num4):
        """Defining Sherwood number

        :param num1: Reynolds number
        :type num1: Float
        :param num2: Schmidt number
        :type num2: Float
        :return: Schmidt number
        :param num3: Pipe diameter in millimetres
        :type num3: Float
        :param num4: Pipe length in metres
        :type num4: Float
        :return: Sherwood number
        :rtype: Float
        """
        num5 = num3 * 1e-3
        if num1 < 2300:
            sherwood_num = 0.023 * (num1**0.83) * (num2**0.33)
        else:
            sherwood_num = 3.65 + (
                (0.0668 * (num5 / num4) * num1 * num2)
                / (1 + 0.04 * ((num5 / num4) * num1 * num2) ** (2 / 3))
            )
        return sherwood_num

    def mass_transfer_coefficient_cl(num1, num2, num3):
        """Defining mass-transfer coefficient for chlorine

        :param num1: Sherwood number
        :type num1: Float
        :param num2: Molecular diffusivity of chlorine in square metres per second
        :type num2: Float
        :return: Schmidt number
        :param num3: Pipe diameter in millimetres
        :type num3: Float
        :return: Mass-transfer coefficient for chlorine
        :rtype: Float
        """
        num4 = num3 * 1e-3
        kf_val_cl = num1 * (num2 / num4)
        return kf_val_cl

    def mass_transfer_coefficient_ars(num1, num2, num3, num4):
        """Defining mass-transfer coefficient for arsenic

        :param num1: Molecular diffusivity of arsenic in square metres per second
        :type num1: Float
        :param num2: Pipe diameter in millimetres
        :type num2: Float
        :return: Schmidt number
        :param num3: Pipe flow velocity is metres per second
        :type num3: Float
        :param num4: Kinematic viscosity of water in square metres per second
        :type num4: Float
        :return: Mass-transfer coefficient for arsenic
        :rtype: Float
        """
        num5 = num2 * 1e-3
        if num5 == 0:
            kf_val_ars = 1
        else:
            kf_val_ars = 0.026 * (num1 / num5) * ((num5 * num3 / num4) ** 0.8) * ((num4 / num1) ** 0.333)
        return kf_val_ars

    def hydraulic_mean_radius(num1):
        """Defining hydraulic mean radius

        :param num1: Pipe diameter in millimetres
        :type num1: Float
        :return: Hydraulic mean radius
        :rtype: Float
        """
        num2 = num1 * 1e-3
        rh_value = num2 / 4
        return rh_value

    def area_per_unit_vol(num1):
        """Defining area of croos-section

        :param num1: Pipe diameter in millimetres
        :type num1: Float
        :return: Area of cross-section
        :rtype: Float
        """
        num2 = num1 * 1e-3
        area_val = 4 / (1e3 * num2)
        return area_val
    
    def variables(num1, num2):
        """Defining variables of the MSRT module

        :param num1: Number of iterations
        :type num1: Integer
        :param num2: Number of variables corresponding to the MSRT module selected
        :type num2: Integer
        :return: Matrix of variable values
        :rtype: Array
        """
        variable_mat = np.zeros((num1, num2))
        # Temperature (degree Celsius)
        temperature_mean = 25
        temperature_var = 0.5
        # Rate constant (chlorine - TOC reaction) (L/mg-C/s)
        kbNC_lower = 2.19e4
        kbNC_upper = 3.81e4
        kbNC_mean = 3e4
        # Rate constant (chlorine wall reaction) (m/s)
        kwC_lower = 1.04e-7
        kwC_upper = 1.43e-5
        kwC_mean = 1.22e-6
        # Reaction yield constant (chlorine - TOC reaction) (mg-C/ mg-Cl)
        YN_upper = 0.15
        YN_lower = 2.50
        YN_mean = 0.61
        # Adsorbance rate constant (for arsenic) (L/mg/s)
        k_ads = 6.67e-5
        # Equilibrium constant (for arsenic) (mg/L)
        k_eq = 0.054
        # Maximum adsorbance density (for As(V)) (mg/sq.m)
        S_max = 500
        # Rate constant (chlorine - As(III) reaction) (L/mg/s)
        kbCAs = 3.64
        # Reaction yield constant (chlorine - As(III) reaction) (mg-Cl/ mg-As(III))
        YC = 0.96
        # Molecular diffusivity of chlorine (sq.m/s)
        Dm_chlorine = 12.5e-10
        # Molecular diffusivity of TOC (sq.m/s)
        Dm_toc_lower = 7.8e-10
        Dm_toc_upper = 11.5e-10
        Dm_toc_mean = 9.5e-10
        # Molecular diffusivity of arsenic (sq.m/s)
        Dm_arsenic = 7.5e-10
        # Molecular diffusivity of THMs (sq.m/s)
        dens_water = 997
        # Kinematic viscosity of water (sq.m/s)
        nu_water = 9.31e-7
        if num1 == 1:
            variable_mat[num1 - 1][0] = temperature_mean
            variable_mat[num1 - 1][1] = kbNC_mean * math.exp(-6050 / (temperature_mean + 273))
            variable_mat[num1 - 1][2] = kwC_mean
            variable_mat[num1 - 1][3] = YN_mean
            variable_mat[num1 - 1][4] = k_ads
            variable_mat[num1 - 1][5] = k_eq
            variable_mat[num1 - 1][6] = S_max
            variable_mat[num1 - 1][7] = kbCAs
            variable_mat[num1 - 1][8] = YC
            variable_mat[num1 - 1][9] = Dm_chlorine
            variable_mat[num1 - 1][10] = Dm_toc_mean
            variable_mat[num1 - 1][11] = Dm_arsenic
            variable_mat[num1 - 1][12] = dens_water
            variable_mat[num1 - 1][13] = nu_water
        else:
            for x in range(num1):
                variable_mat[x][0] = (1 - temperature_var) * temperature_mean + (
                    2 * temperature_var * temperature_mean
                ) * random.uniform(0, 1)
                variable_mat[x][1] = random.uniform(kbNC_lower, kbNC_upper) * math.exp(
                    -6050 / ((variable_mat[x][0]) + 273)
                )
                variable_mat[x][2] = random.uniform(kwC_lower, kwC_upper)
                variable_mat[x][3] = random.uniform(YN_lower, YN_upper)
                variable_mat[x][4] = k_ads
                variable_mat[x][5] = k_eq
                variable_mat[x][6] = S_max
                variable_mat[x][7] = kbCAs
                variable_mat[x][8] = YC
                variable_mat[x][9] = Dm_chlorine
                variable_mat[x][10] = random.uniform(Dm_toc_lower, Dm_toc_upper)
                variable_mat[x][11] = Dm_arsenic
                variable_mat[x][12] = dens_water
                variable_mat[x][13] = nu_water
        return variable_mat

    def pipe_reaction(num1, num2, num3, num4, num5, num6, num7, arr1, arr2):
        """Defining link reactions for the MSRT model selected

        :param num1: Water quality simulation time step in seconds
        :type num1: Integer
        :param num2: Link index
        :type num2: Integer
        :param num3: Grid index
        :type num3: Integer
        :param num4: Link flow velocity in metres per second
        :type num3: Float
        :param num5: Link diameter in millimetres
        :type num5: Float
        :param num6: Link length in metres
        :type num6: Float
        :param num7: Link segment length in metres
        :type num7: Float
        :param arr1: List of variable values
        :type arr1: List
        :param arr2: Matrix of link concentration values
        :type arr2: Array
        :return: Values corresponding to growth or decay of the concentration of water quality parameters
        :rtype: List
        """
        kbNC = arr1[1]
        kwC = arr1[2]
        YN = arr1[3]
        k_ads = arr1[4]
        k_eq = arr1[5]
        S_max = arr1[6]
        kbCAs = arr1[7]
        YC = arr1[8]
        Dm_chlorine = arr1[9]
        Dm_arsenic = arr1[11]
        nu_water = arr1[13]

        KbNC = kbNC * arr2[4][num3][num2]
        KbCAs = kbCAs * arr2[3][num3][num2]
        Re = module.Reynolds_number(num4, num5, nu_water)
        Sc_chlorine = module.Schmidt_number(nu_water, Dm_chlorine)
        Sh_chlorine = module.Sherwood_number(Re, Sc_chlorine, num5, num6)
        kfC = module.mass_transfer_coefficient_cl(Sh_chlorine, Dm_chlorine, num5)
        rh = module.hydraulic_mean_radius(num5)
        KwC = (kwC * kfC) / ((kwC + kfC) * rh)
        KfAs = module.mass_transfer_coefficient_ars(Dm_arsenic, num2, num4, nu_water)
        Sorb = (arr2[1][num3][num2] * (S_max - arr2[5][num3][num2]) - k_eq * arr2[5][num3][num2]) / (
            (1 / k_ads) + ((1 / KfAs) * (S_max - arr2[5][num3][num2]))
        )
        Av = module.area_per_unit_vol(num5)

        # Reactions within pipe
        delta_chlorine_toc_reac_pipe = module.first_order_reaction(KbNC, arr2[3][num3][num2], num1)
        delta_chlorine_wall_reac_pipe = module.first_order_reaction(KwC, arr2[3][num3][num2], num1)
        delta_toc_chlorine_reac_pipe = YN * delta_chlorine_toc_reac_pipe
        if module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1) > arr2[0][num3][num2]:
            delta_As3_chlorine_reac_pipe = arr2[0][num3][num2]
        else:
            delta_As3_chlorine_reac_pipe = module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1)
        delta_chlorine_As3_reac_pipe = YC * delta_chlorine_toc_reac_pipe
        if module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1) > arr2[0][num3][num2]:
            delta_As5_As3_reac_pipe = arr2[0][num3][num2]
        else:
            delta_As5_As3_reac_pipe = module.first_order_reaction(KbCAs, arr2[0][num3][num2], num1)
        # delta_As5_As3_reac_pipe = 0
        delta_As5_bulk_reac_pipe = Av * Sorb
        delta_As5_wall_reac_pipe = Sorb

        net_delta_chlorine_reac = (
            -delta_chlorine_toc_reac_pipe - delta_chlorine_wall_reac_pipe - delta_chlorine_As3_reac_pipe
        )
        net_delta_toc_reac = -delta_toc_chlorine_reac_pipe
        net_delta_As3_reac = -delta_As3_chlorine_reac_pipe
        net_delta_As5_reac_bulk = delta_As5_As3_reac_pipe - delta_As5_bulk_reac_pipe
        net_delta_As5_reac_wall = delta_As5_wall_reac_pipe
        net_delta_As_reac = net_delta_As3_reac + net_delta_As5_reac_bulk

        delta_mat = [
            net_delta_As3_reac,
            net_delta_As5_reac_bulk,
            net_delta_As_reac,
            net_delta_chlorine_reac,
            net_delta_toc_reac,
            net_delta_As5_reac_wall,
        ]
        return delta_mat

    def tank_reaction(num1, num2, num3, num4, num5, arr1, arr2, arr3):
        """Defining tank reactions for the MSRT model selected

        :param num1: Water quality simulation time step in seconds
        :type num1: Integer
        :param num2: Present water quality step
        :type num2: Integer
        :param num3: Tank index
        :type num3: Integer
        :param num4: Tank volume in previous water quality step
        :type num4: Integer
        :param num5: Tank volume in the present water quality step
        :type num5: Integer
        :param arr1: List of variable values
        :type arr1: List
        :param arr2: Matrix of initial tank concentration values
        :type arr2: Array
        :param arr2: Matrix of tank concentration values
        :type arr2: Array
        :return: Values corresponding to growth or decay of the concentration of water quality parameters
        :rtype: List
        """
        kbNC = arr1[1]
        YN = arr1[3]
        kbCAs = arr1[7]
        YC = arr1[8]

        if num2 == 1:
            tank_As3_conc = arr2[num3][0]
            tank_chlorine_conc = arr2[num3][3]
            tank_toc_conc = arr2[num3][4]
        else:
            tank_As3_conc = arr3[0][num2 - 1][num3]
            tank_chlorine_conc = arr3[3][num2 - 1][num3]
            tank_toc_conc = arr3[4][num2 - 1][num3]

        KbNC = kbNC * tank_toc_conc
        KbCAs = kbCAs * tank_chlorine_conc
        # Reactions within tank
        delta_chlorine_toc_reac_tank = (num4 / num5) * module.first_order_reaction(
            KbNC, tank_chlorine_conc, num1
        )
        delta_toc_chlorine_reac_tank = YN * delta_chlorine_toc_reac_tank
        if (num4 / num5) * module.first_order_reaction(KbCAs, tank_As3_conc, num1) > tank_As3_conc:
            delta_As3_chlorine_reac_tank = tank_As3_conc
        else:
            delta_As3_chlorine_reac_tank = (num4 / num5) * module.first_order_reaction(
                KbCAs, tank_As3_conc, num1
            )
        delta_chlorine_As3_reac_tank = YC * delta_As3_chlorine_reac_tank

        net_delta_chlorine_reac = -delta_chlorine_toc_reac_tank - delta_chlorine_As3_reac_tank
        net_delta_toc_reac = -delta_toc_chlorine_reac_tank
        net_delta_As3_reac = -delta_As3_chlorine_reac_tank
        net_delta_As5_reac = delta_As3_chlorine_reac_tank
        net_delta_As_reac = 0

        delta_mat = [
            net_delta_As3_reac,
            net_delta_As5_reac,
            net_delta_As_reac,
            net_delta_chlorine_reac,
            net_delta_toc_reac,
        ]
        return delta_mat

    def reservoir_quality(d, num1, num2, arr1, str1):
        """Defining source quality values for the reservoir(s)

        :param num1: Number of iterations
        :type num1: Integer
        :param num2: Variability in the random pattern for source quality
        :type num2: Float
        :param arr1: Quality values for the reservoir(s)
        :type arr1: Array
        :param str1: Input command for the random pattern
        :type str1: String
        :return: Values corresponding to source quality at the reservoir(s)
        :rtype: Array
        """
        num_reservoirs = module.network(d)[2]
        num_bulk_parameters = module.species()[1]
        if len(arr1) == num_reservoirs:
            if len(arr1[0]) == num_bulk_parameters:
                print("Reservoir quality updated.")
            else:
                print("Reservoir quality input error.")
                exit()
        reservoir_quality = np.zeros((num_reservoirs, num1, num_bulk_parameters))
        input = str1
        rand_vary = num2
        if input == "none":
            for x in range(num_reservoirs):
                reservoir_quality[x] = arr1[x]
        elif input == "rand":
            if num1 == 1:
                mat_min = arr1
                mat_max = arr1
            else:
                mat_min = np.multiply(arr1, (1 - rand_vary))
                mat_max = np.multiply(arr1, (1 + rand_vary))
            for x in range(num_reservoirs):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < num1:
                        reservoir_quality[x][z][y] = random.uniform(mat_min[x][y], mat_max[x][y])
                        z += 1
        return reservoir_quality

    def reservoir_pattern(d, num1, num2, arr1, arr2, arr3, str1):
        """Defining source quality pattern for the reservoir(s)

        :param num1: Base time period in day(s)
        :type num1: Float/Integer
        :param num2: Variability in the pattern
        :type num2: Float
        :param arr1: Start time step for the injection in the reservoir(s)
        :type arr1: Array
        :param arr2: End time step for the injection in the reservoir(s)
        :type arr2: Array
        :param arr3: Input value for the injection in the reservoir(s)
        :type arr3: Array
        :param str1: Input command for the pattern
        :type str1: String
        :return: Values corresponding to source quality pattern at the reservoir(s)
        :rtype: Array
        """
        num_reservoirs = module.network(d)[2]
        num_bulk_parameters = module.species()[1]
        h_time = d.getTimeHydraulicStep()
        pattern_steps = int(num1 * 24 * 3600 / h_time)
        pattern_mat = np.zeros((num_reservoirs, pattern_steps, num_bulk_parameters))
        # Input
        input = str1
        rand_vary = num2
        if input == "none":
            pattern_mat = np.add(pattern_mat, 1)
        elif input == "rand":
            for x in range(num_reservoirs):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < pattern_steps:
                        pattern_mat[x][z][y] = random.uniform(1 - rand_vary, 1 + rand_vary)
                        z += 1
        elif input == "specific":
            start_step_mat = arr1
            end_step_mat = arr2
            val_input = arr3
            if len(start_step_mat) == num_reservoirs and len(end_step_mat) == num_reservoirs:
                if len(start_step_mat[0]) <= pattern_steps and len(end_step_mat[0]) <= pattern_steps:
                    for x in range(num_reservoirs):
                        for y in range(len(start_step_mat[x])):
                            pattern_mat[x][start_step_mat[x][y] : end_step_mat[x][y]] = val_input[x][y]
            else:
                exit()
        return pattern_mat

    def injection_quality(num1, num2, arr1, arr2, str1):
        """Defining source quality values for the injection node(s)

        :param num1: Number of iterations
        :type num1: Integer
        :param num2: Variability in the random pattern for injection node quality
        :type num2: Float
        :param arr1: Index value(s) of injection node(s)
        :type arr1: List
        :param arr2: Quality values for the injection node(s)
        :type arr2: Array
        :param str1: Input command for the random pattern
        :type str1: String
        :return: Values corresponding to source quality at the injection node(s)
        :rtype: Array
        """
        # num1 - number of iterations; arr1 - matrix of injection nodes indices; arr2 - matrix of injection nodes quality
        # str1 - input value for pattern; num2 - percentage variation in the random pattern
        num_injection_nodes = len(arr1)
        num_bulk_parameters = module.species()[1]
        if len(arr2) == num_injection_nodes:
            if len(arr2[0]) == num_bulk_parameters:
                print("Reservoir quality updated.")
            else:
                print("Injection node quality input error.")
                exit()
        injection_quality = np.zeros((num_injection_nodes, num1, num_bulk_parameters))
        print("Injection nodes quality updated.")
        # Input
        input = str1
        rand_vary = num2 
        if input == "none":
            for x in range(num_injection_nodes):
                injection_quality[x] = arr2[x]
        elif input == "rand":
            if num1 == 1:
                mat_min = arr2
                mat_max = arr2
            else:
                mat_min = np.multiply(arr2, (1 - rand_vary))
                mat_max = np.multiply(arr2, (1 + rand_vary))
            for x in range(num_injection_nodes):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < num1:
                        injection_quality[x][z][y] = random.uniform(mat_min[x][y], mat_max[x][y])
                        z += 1
        return injection_quality

    def injection_pattern(d, num1, num2, arr1, arr2, arr3, arr4, str1):
        """Defining source quality pattern for the injection node(s)

        :param num1: Base time period in day(s)
        :type num1: Float/Integer
        :param num2: Variability in the pattern
        :type num2: Float
        :param arr1: Index value(s) of injection node(s)
        :type arr1: List
        :param arr2: Start time step for the injection in the injection node(s)
        :type arr2: Array
        :param arr3: End time step for the injection in the injection node(s)
        :type arr3: Array
        :param arr4: Input value for the injection in the injection node(s)
        :type arr4: Array
        :param str1: Input command for the pattern
        :type str1: String
        :return: Values corresponding to source quality pattern at the injection node(s)
        :rtype: Array
        """
        num_injection_nodes = len(arr1)
        num_bulk_parameters = module.species()[1]
        h_time = d.getTimeHydraulicStep()
        pattern_steps = int(num1 * 24 * 3600 / h_time)
        inj_pattern_mat = np.zeros((num_injection_nodes, pattern_steps, num_bulk_parameters))
        # Input
        input = str1
        rand_vary = num2
        if input == "none":
            inj_pattern_mat = np.add(inj_pattern_mat, 1)
        elif input == "rand":
            for x in range(num_injection_nodes):
                for y in range(num_bulk_parameters):
                    z = 0
                    while z < pattern_steps:
                        inj_pattern_mat[x][z][y] = random.uniform(1 - rand_vary, 1 + rand_vary)
                        z += 1
        elif input == "specific":
            start_step_mat = arr2
            end_step_mat = arr3
            val_input = arr4
            if len(start_step_mat) == num_injection_nodes and len(end_step_mat) == num_injection_nodes:
                if len(start_step_mat[0]) <= pattern_steps and len(end_step_mat[0]) <= pattern_steps:
                    for x in range(num_injection_nodes):
                        for y in range(len(start_step_mat[x])):
                            inj_pattern_mat[x][start_step_mat[x][y] : end_step_mat[x][y]] = val_input[x][y]
            else:
                exit()
        return inj_pattern_mat
