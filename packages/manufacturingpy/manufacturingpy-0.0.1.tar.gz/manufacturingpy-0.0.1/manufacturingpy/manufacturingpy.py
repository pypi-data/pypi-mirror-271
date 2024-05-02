#Functions

def efficiency(actual_output, max_possible_output):
    """
    Calculate the efficiency of a production line.

    Arguments:
    actual_output (float): The actual output from the production line.
    max_possible_output (float): The maximum possible output from the production line.

    Returns:
    float: The efficiency of the production line as a percentage.
    """
    if max_possible_output == 0:
        return 0
    else:
        efficiency = (actual_output / max_possible_output) * 100
        return efficiency

     

def takt_time(available_working_hours, unit_available_working_hours, customer_demand, tack_time_time_unit='s'):
    """
    Takt Time for a production line.

    Arguments:
     1 - production_time (float): The production time available in production_time unit.
     2 - production_time_unit (str): The time unit of production_time. It should be 'seconds', 'minutes' or 'hours'.
     3 - customer_demand (float): Customer demand.
     4 - result_time_unit (str, optional): The desired time unit for the result. It should be 'seconds', 'minutes' or 'hours'. Default is 'seconds'.

    Return:
    takt_time (float): The Takt Time calculated in the result_time_unit.
    """
    # Seconds is standard, Convert to desired time unit
    if unit_available_working_hours == 'm':
        available_working_hours = available_working_hours * 60
    elif unit_available_working_hours == 'h':
        available_working_hours = available_working_hours * 3600

    takt_time = available_working_hours / customer_demand

    # Convert Takt Time to desired time unit
    if tack_time_time_unit == 'm':
        takt_time = takt_time / 60
    elif tack_time_time_unit == 'h':
        takt_time = takt_time / 3600

    return takt_time
     

def muda_explain(muda_type):
    """
    Provide an explanation for a given type of MUDA.

    Parameters:
    muda_type (str): The type of MUDA to explain. This should be one of the following: 'Defects', 'Overproduction', 'Waiting', 'Transport', 'Motion', 'Overprocessing', 'Inventory'.

    Returns:
    str: The explanation of the given MUDA type.
    """
    muda_explanations = {
        'Defects': 'Products or services that do not meet quality standards and need to be corrected or redone.',
        'Overproduction': 'Producing more than is necessary to meet customer demand.',
        'Waiting': 'Idle time while waiting for materials, information, equipment, etc.',
        'Transport': 'Unnecessary movement of materials or products within the company.',
        'Motion': 'Unnecessary movements of people or equipment that do not add value to the product or service.',
        'Overprocessing': 'Use of more complex processes, procedures, or equipment than necessary.',
        'Inventory': 'Excessive storage of products, components, or materials.'
    }

    return muda_explanations.get(muda_type, 'Invalid MUDA type. Please enter one of the following: Defects, Overproduction, Waiting, Transport, Motion, Overprocessing, Inventory.')

     

def muda_list(muda_index=None):
    """
    List the types of MUDA.

    Parameters:
    muda_index (int, optional): The index of the MUDA type to return. If not provided, all MUDA types are returned.

    Returns:
    str or list: The name of the MUDA type if an index is provided, otherwise a list of all MUDA types.
    """
    muda_types = ['Defects', 'Overproduction', 'Waiting', 'Transport', 'Motion', 'Overprocessing', 'Inventory']

    if muda_index is None:
        return muda_types
    elif 0 <= muda_index < len(muda_types):
        return muda_types[muda_index]
    else:
        return 'Invalid MUDA index. Please enter a number between 0 and 6.'

     

def oee(operating_time=None, planned_production_time=None, total_pieces_produced=None, ideal_cycle_time=None, good_pieces=None, metric='oee'):
    """
    Calculate the Overall Equipment Effectiveness (OEE), Availability, Performance, or Quality.

    Arguments:
    operating_time (float, optional): The actual operating time.
    planned_production_time (float, optional): The planned production time.
    total_pieces_produced (int, optional): The total number of pieces produced.
    ideal_cycle_time (float, optional): The ideal cycle time for producing one piece.
    good_pieces (int, optional): The number of good pieces produced.
    metric (str, optional): The metric to return. Must be 'oee', 'availability', 'performance', or 'quality'. Default is 'oee'.

    Returns:
    result (float or str): The calculated OEE, Availability, Performance, or Quality, or the descriptions of the three components if no parameters are provided.
    """
    if operating_time is None or planned_production_time is None or total_pieces_produced is None or ideal_cycle_time is None or good_pieces is None:
        return "The OEE is composed of three components: Availability, Performance, and Quality. Availability measures the proportion of the planned production time that is actually productive. Performance reflects the speed at which your production line operates compared to its maximum speed. Quality shows the quality of the pieces you are producing."

    # Calculate Availability
    availability = operating_time / planned_production_time

    # Calculate Performance
    performance = (total_pieces_produced * ideal_cycle_time) / operating_time

    # Calculate Quality
    quality = good_pieces / total_pieces_produced

    # Calculate OEE
    oee = availability * performance * quality

    # Return the requested metric
    if metric == 'availability':
        return availability
    elif metric == 'performance':
        return performance
    elif metric == 'quality':
        return quality
    else:
        return oee

     

def six_sigma(defects, opportunities, units):
    """
    Calculate the Six Sigma level of a process given the number of defects, opportunities, and units.

    Args:
    defects (int): The total number of defects found in the process.
    opportunities (int): The total number of opportunities for a defect to occur per unit. Its possible more than one per produced unit
    units (int): The total number of units.

    Returns:
    tuple: A tuple containing the DPMO and the corresponding Sigma level.
    """

    # Calculate DPMO
    dpmo = (defects / (opportunities * units)) * 1_000_000

    # Convert DPMO to Sigma level using a standard conversion table
    if dpmo > 308537:
        sigma_level = 1
    elif dpmo > 69767:
        sigma_level = 2
    elif dpmo > 6210:
        sigma_level = 3
    elif dpmo > 233:
        sigma_level = 4
    elif dpmo > 3.4:
        sigma_level = 5
    else:
        sigma_level = 6

    return dpmo, sigma_level
     