__all__ = ["band_filters_params",
           "master_sub_sequences_params",
           "nested_sub_sequences_params",
           "scheduling_params",
           "sky_constraints_params",
           "sky_exclusion_params",
           "sky_nightly_bounds_params",
           "sky_region_params",
           "sky_user_regions_params",
           "sub_sequences_params"]

def band_filters_params(is_general=True):
    """Create band filters registered field names.

    Parameters
    ----------
    is_general : bool
        Flag to use specific parameter tag.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    if is_general:
        param_tag = "general"
    else:
        param_tag = "sequence"
    params = []
    for filter_name in "u,g,r,i,z,y".split(','):
        field_stem = "{}_filter".format(filter_name)
        params.append("{}_{}_use".format(param_tag, field_stem))
        params.append("{}_num_visits".format(field_stem))
        params.append("{}_num_grouped_visits".format(field_stem))
        params.append("{}_{}_bright_limit".format(param_tag, field_stem))
        params.append("{}_{}_dark_limit".format(param_tag, field_stem))
        params.append("{}_{}_max_seeing".format(param_tag, field_stem))
        params.append("{}_{}_exposures".format(param_tag, field_stem))
    return params

def master_sub_sequences_params():
    """Create master sub-sequence registered field names.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    return ["master_sub_sequences"]

def nested_sub_sequences_params():
    """Create nested sub-sequence registered field names.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    return ["nested_sub_sequences"]

def scheduling_params(is_general=True):
    """Create scheduling registered field names.

    Parameters
    ----------
    is_general : bool
        Flag to use specific parameter tag.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    if is_general:
        param_tag = "general"
    else:
        param_tag = "sequence"
    return ["{}_scheduling_max_num_targets".format(param_tag),
            "{}_scheduling_accept_serendipity".format(param_tag),
            "{}_scheduling_accept_consecutive_visits".format(param_tag),
            "{}_scheduling_airmass_bonus".format(param_tag),
            "scheduling_restrict_grouped_visits",
            "scheduling_time_interval",
            "scheduling_time_window_start",
            "scheduling_time_window_max",
            "scheduling_time_window_end",
            "scheduling_time_weight"]

def sky_constraints_params():
    """Create sky constraints registered field names.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    return ["sky_constraints_max_airmass",
            "sky_constraints_max_cloud"]

def sky_exclusion_params(is_general=True):
    """Create sky exclusions registered field names.

    Parameters
    ----------
    is_general : bool
        Flag to use specific parameter tag.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    if is_general:
        param_tag = "general"
    else:
        param_tag = "sequence"
    return ["{}_sky_exclusions_dec_window".format(param_tag),
            "sky_exclusion_selections"]

def sky_nightly_bounds_params():
    """Create sky nightly bounds registered field names.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    return ["sky_nightly_bounds_twilight_boundary",
            "sky_nightly_bounds_delta_lst"]

def sky_region_params():
    """Create sky regions registered field names.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    return ["sky_region_selections", "sky_region_combiners"]

def sky_user_regions_params():
    """Create sky user regions registered field names.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    return ["sky_user_regions"]

def sub_sequences_params():
    """Create sub-sequence registered field names.

    Returns
    -------
    list[str]
        Set of registered field names.
    """
    return ["sub_sequences"]
