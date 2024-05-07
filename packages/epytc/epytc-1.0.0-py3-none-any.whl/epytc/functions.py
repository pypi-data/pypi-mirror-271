import numpy as np
import math


class fn:
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
        for x in range(
            d.getLinkCount() - d.getLinkValveCount(), len(d.getLinkNameID())
        ):
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

    def incoming_links(num1, arr1):
        """Getting incoming links to a specific node

        :param num1: ID of a node
        :type num1: Integer
        :param arr1: Matrix of end node indices
        :type arr1: List
        :return: List of incoming links
        :rtype: List
        """
        links_connecting_to_node = []
        if arr1.count(num1 + 1) > 0:
            arr = np.array(arr1)
            bool_arr = arr == num1 + 1
            links_connecting_to_node = np.where(bool_arr)[0]
        return links_connecting_to_node

    def outgoing_links(num1, arr1):
        """Getting outgoing links from a specific node

        :param num1: ID of a node
        :type num1: Integer
        :param arr1: Matrix of start node indices
        :type arr1: List
        :return: List of outgoing links
        :rtype: List
        """
        links_connecting_from_node = []
        if arr1.count(num1 + 1) > 0:
            arr = np.array(arr1)
            bool_arr = arr == num1 + 1
            links_connecting_from_node = np.where(bool_arr)[0]
        return links_connecting_from_node

    def minimum_link_length(num1, num2, num3, arr1):
        """Estimating the minimum length to be specified for pumps and valves

        :param num1: Time steps in the filtered hydraulic report
        :type num1: Integer
        :param num2: Water quality time step
        :type num2: Integer
        :param num3: Tolerable flow velocity considered
        :type num3: Integer
        :param arr1: Matrix of link flow velocities
        :type arr1: List
        :return: Minimum link length
        :rtype: Float
        """
        min_vel = []
        for h in range(num1):
            min_val = np.min(arr1[h])
            min_vel.append(min_val)
        minimum_flow_velocity = np.min(min_vel)
        if minimum_flow_velocity < num3:
            minimum_flow_velocity = num3
        minimum_link_length = minimum_flow_velocity * num2
        return minimum_link_length

    def minimum_link_diameter(num1, num2, num3, arr1):
        """Estimating the minimum diameter to be specified for pumps and valves

        :param num1: Count of links
        :type num1: Integer
        :param num2: Count of pumps
        :type num2: Integer
        :param num3: Count of valves
        :type num3: Integer
        :param arr1: Matrix of link diameters
        :type arr1: List
        :return: Minimum diameter
        :rtype: Float
        """
        min_val = np.min(arr1)
        if min_val == 0:
            arr2 = arr1[0 : num1 - (num2 + num3)]
            min_val = np.min(arr2)
            minimum_link_diameter = min_val
        else:
            minimum_link_diameter = min_val
        return minimum_link_diameter

    def sync_time(d, H, num1, num2, num3, num4, num5, num6, num7, num8, str1, arr2):
        """Synchronizing water quality and hydraulic time steps

        :param d: EPANET model
        :type d: EPANET object
        :param H: Hydraulic simulation output from EPANET
        :type H: List
        :param num1: Current water quality time in the simulation in seconds
        :type num1: Integer
        :param num2: Total steps in the hydraulic report 'Time' that was expected
        :type num2: Integer
        :param num3: Base time period in seconds
        :type num3: Integer
        :param num4: Total hydraulic simuation time in seconds
        :type num4: Integer
        :param num5: Count of the day in water quality simulation
        :type num5: Integer
        :param num6: Base time period in day(s)
        :type num6: Float/ Integer
        :param num7: Water quality simulation time step in seconds
        :type num7: Integer
        :param num8: Expected time step in the hydraulic report
        :type num8: Integer
        :param str1: Option for synchronization
        :type str1: String
        :param arr1: Input pattern governing quality values(input) at the reservoir
        :type str1: Array
        :return: Synchronized steps
        :rtype: List
        """
        if str1 == "steady":
            if num1 == 0:
                h_step_expected = math.floor(num2 - (num3 / num4)) - 1
                h_step = h_step_expected
                reservoir_pattern_step = injection_pattern_step = 0
            else:
                h_step_expected = num8
                wq_time_cycle = num1 - (num5 - 1) * num6 * 24 * 3600
                wq_time_hydraulic_report = wq_time_cycle + (
                    int(d.getTimeSimulationDuration()) - num3
                )
                for x in range(num8, num2):
                    if wq_time_hydraulic_report <= H.Time[x]:
                        h_step = math.floor(x)
                        break
                reservoir_pattern_step = injection_pattern_step = (
                    len(arr2[0]) - (num2 - h_step) + 1
                )
        elif str1 == "dynamic":
            if num1 == 0:
                h_step_expected = 0
                h_step = h_step_expected
                reservoir_pattern_step = injection_pattern_step = 0
            else:
                h_step_expected = num8
                wq_time_cycle = num1
                wq_time_hydraulic_report = wq_time_cycle
                for x in range(num8, num2):
                    if wq_time_hydraulic_report <= H.Time[x]:
                        h_step = math.floor(x)
                        break
                reservoir_pattern_step = injection_pattern_step = h_step - int(
                    (num5 - 1) * (num6 * 24 * 3600 / num7)
                )
        out = [h_step, h_step_expected, reservoir_pattern_step, injection_pattern_step]
        return out

    def time_filter(H, num1, num2, num3):
        """Filtering out unwanted time steps from hydraulic analysis output

        :param H: Hydraulic simulation output from EPANET
        :type H: List
        :param num1: Ratio of time steps actually reported to time steps expected in the report
        :type num1: Float
        :param num2: Total steps in the hydraulic report 'Time' that was expected
        :type num2: Integer
        :param num3: Hydraulic simulation time step in seconds
        :type num3: Integer
        :return: Details of unwanted steps for water quality simulation
        :rtype: List
        """
        filtered_steps = []
        if num1 > 1:
            print("Filtering hydraulic analysis report.")
            for s in range(num2):
                if H.Time[s] % num3 != 0:
                    filtered_steps.append(s)
        return filtered_steps

    def time_data(arr1, arr2):
        """Cleaning time data

        :param arr1: Time ouput from EPANET hydraulic simulation
        :type arr1: List
        :param arr2: Details of unwanted steps for water quality simulation
        :return: Cleansed time output
        :rtype: List
        """
        arr2 = np.array(arr2)
        if len(arr2) > 0:
            out = np.delete(arr1, arr2, 0)
        else:
            out = arr1
        return out

    def velocity_data(arr1, arr2, str1):
        """Cleaning velocity data

        :param arr1: Link velocity ouput from EPANET hydraulic simulation
        :type arr1: List
        :param arr2: Details of unwanted steps for water quality simulation
        :return: Cleansed time output
        :param str1: Flow Unit
        :type str1: String
        :return: Cleansed velocity output
        :rtype: List
        """
        arr2 = np.array(arr2)
        if len(arr2) > 0:
            out = np.delete(arr1, arr2, 0)
        else:
            out = arr1
        if str1 == "GPM":
            out = np.multiply(out, 0.3048)
        return out

    def demand_data(arr1, arr2, str1):
        """Cleaning demand data

        :param arr1: Node demand ouput from EPANET hydraulic simulation
        :type arr1: List
        :param arr2: Details of unwanted steps for water quality simulation
        :return: Cleansed time output
        :param str1: Flow Unit
        :type str1: String
        :return: Cleansed demand output
        :rtype: List
        """
        arr2 = np.array(arr2)
        if len(arr2) > 0:
            out = np.delete(arr1, arr2, 0)
        else:
            out = arr1
        if str1 == "GPM":
            out = np.multiply(out, 6.3e-5)
        elif str1 == "LPS":
            out = np.multiply(out, 1e-3)
        elif str1 == "LPM":
            out = np.multiply(out, 1.67e-5)
        elif str1 == "CMH":
            out = np.multiply(out, (1 / 3600))
        return out

    def flow_data(arr1, arr2, str1):
        """Cleaning flow data

        :param arr1: Link flow ouput from EPANET hydraulic simulation
        :type arr1: List
        :param arr2: Details of unwanted steps for water quality simulation
        :return: Cleansed time output
        :param str1: Flow Unit
        :type str1: String
        :return: Cleansed flow output
        :rtype: List
        """
        arr2 = np.array(arr2)
        if len(arr2) > 0:
            out = np.delete(arr1, arr2, 0)
        else:
            out = arr1
        if str1 == "GPM":
            out = np.multiply(out, 6.3e-5)
        elif str1 == "LPS":
            out = np.multiply(out, 1e-3)
        elif str1 == "LPM":
            out = np.multiply(out, 1.67e-5)
        elif str1 == "CMH":
            out = np.multiply(out, (1 / 3600))
        return out

    def tank_volume_data(arr1, arr2, str1):
        """Cleaning tank volume data

        :param arr1: Tank volume ouput from EPANET hydraulic simulation
        :type arr1: List
        :param arr2: Details of unwanted steps for water quality simulation
        :return: Cleansed time output
        :param str1: Flow Unit
        :type str1: String
        :return: Cleansed tank volume output
        :rtype: List
        """
        arr2 = np.array(arr2)
        if len(arr2) > 0:
            out = np.delete(arr1, arr2, 0)
        else:
            out = arr1
        if str1 == "GPM":
            out = np.multiply(out, 0.0283)
        return out

    def maximum_segments(num1, num2, arr1, arr2):
        """Determining the maximum number of segments for pipe discretization

        :param num1: Tolerable flow velocity considered in metres per second
        :type num1: Float
        :param num2: Water quality simulation time step in seconds
        :type num2: Integer
        :param arr1: Matrix of link lengths
        :type arr1: List
        :param arr2: Matrix of link velocity values
        :type arr2: List
        :return: Maximum number of pipe segments
        :rtype: Integer
        """
        arr2[arr2 < num1] = 0
        arr2[arr2 == 0] = 100
        min_vel = np.min(arr2)
        index = np.where(arr2 == min_vel)
        len_min_vel_pipe = arr1[index[1][0]]
        max_segments = math.ceil(len_min_vel_pipe / (num1 * num2)) + 1
        return max_segments

    def reservoir_names(num1, arr1, arr2):
        """Displaying the names of reservoirs

        :param num1: Count of reservoirs
        :type num1: Integer
        :param arr1: Matrix of node names
        :type arr1: List
        :param arr2: Matrix of reservoir indices
        :type arr2: List
        :return: Names of reservoirs
        :rtype: String
        """
        for x in range(num1):
            print("Reservoir %d: %s" % (x + 1, arr1[arr2[x] - 1]))

    def tank_names(num1, arr1, arr2):
        """Displaying the names of tanks

        :param num1: Count of tanks
        :type num1: Integer
        :param arr1: Matrix of node names
        :type arr1: List
        :param arr2: Matrix of tank indices
        :type arr2: List
        :return: Names of tanks
        :rtype: String
        """
        for x in range(num1):
            print("Tank %d: %s" % (x + 1, arr1[arr2[x] - 1]))

    def pump_names(num1, num2, arr1):
        """Displaying the names of pumps

        :param num1: Count of pumps
        :type num1: Integer
        :param num2: Count of valves
        :type num2: Integer
        :param arr1: Matrix of link names
        :type arr1: List
        :return: Names of pumps
        :rtype: String
        """
        if num1 > 0:
            for x in range(num1):
                print("Pump %d: %s" % (x + 1, arr1[len(arr1) - num2 - (num1 - x)]))

    def valve_names(num1, arr1):
        """Displaying the names of valves

        :param num1: Count of valves
        :type num1: Integer
        :param arr1: Matrix of link names
        :type arr1: List
        :return: Names of valves
        :rtype: String
        """
        if num1 > 0:
            for x in range(num1):
                print("Valve %d: %s" % (x + 1, arr1[len(arr1) - (num1 - x)]))

    def simulation_info(num1, num2, num3, num4):
        """Displaying the basic information about the inputs selected for the simulation

        :param num1: Maximum number of iterations
        :type num1: Integer
        :param num2: Water quality simuation time in days
        :type num2: Float/ Integer
        :param num3: Water quality simuation time step in seconds
        :type num3: Integer
        :param num4: Total number of water quality simulation steps
        :type num4: Integer
        :return: Basic information about simulation
        :rtype: String
        """
        print("Number of iterations: %d" % (num1))
        print("Number of days for which water quality is simulated: %d" % (num2))
        print("Water quality simulation time step: %d seconds" % (num3))
        print("Number of water quality simulation steps: %d" % (num4))

    def msrt_info(num1, num2, num3):
        """Displaying the basic information about the MSRT model selected for the simulation

        :param num1: Count of water quality parameters
        :type num1: Integer
        :param num2: Count of bulk phase water quality parameters
        :type num2: Float/ Integer
        :param num3: Count of wall phase water quality parameters
        :type num3: Integer
        :return: Basic information about MSRT model
        :rtype: String
        """
        print("Number of water quality parameters in the MSRT model: %d" % (num1))
        print("Number of bulk phase water quality paraneters: %d" % (num2))
        print("Number of wall phase water quality paraneters: %d" % (num3))

    def omitted_nodes(num1, arr1, arr2):
        """Displaying the information about the nodes (if any) omitted from water quality analysis

        :param num1: Count of omitted nodes
        :type num1: Integer
        :param arr1: Matrix of node names
        :type arr1: List
        :param arr2: Matrix of indices of omitted nodes
        :type arr2: List
        :return: Details of omitted nodes
        :rtype: String
        """
        if num1 > 0:
            print("Number of nodes omitted for analysis: %d" % (num1))
            for x in range(num1):
                print("Omitted Node %d: %s" % (x + 1, arr1[arr2[x]]))

    def omitted_links(num1, arr1, arr2):
        """Displaying the information about the links (if any) omitted from water quality analysis

        :param num1: Count of omitted links
        :type num1: Integer
        :param arr1: Matrix of link names
        :type arr1: List
        :param arr2: Matrix of indices of omitted links
        :type arr2: List
        :return: Details of omitted links
        :rtype: String
        """
        if num1 > 0:
            print("Number of links omitted for analysis: %d" % (num1))
            for x in range(num1):
                print("Omitted Link %d: %s" % (x + 1, arr1[arr2[x]]))
