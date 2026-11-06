from aeon.dj_pipeline import ephys, spike_sorting

experiment_name = "abcEphys02-aeon3"
SUBJECT = "IAA-1150342"
paramset_id_str = "cjh_405"
sorting_method = "kilosort4"

# Probe insertion to set up sorting for, or None for every insertion.
insertion_number = 1

block_rest = {"experiment_name": experiment_name, "insertion_number": insertion_number}

blocks = (ephys.EphysBlock & block_rest).to_dicts()

block_info = (
    (ephys.EphysBlockInfo & block_rest).proj("probe_type", "electrode_config_name").to_dicts(limit=1)
)

probe_type = block_info[0]["probe_type"]
electrode_config_name = block_info[0]["electrode_config_name"]

electrode_groups = spike_sorting.ElectrodeGroup & {"electrode_config_name": electrode_config_name}

insert_count = 0
for block in blocks:
    for electrode_group in electrode_groups:
        task_key = {
            "experiment_name": block["experiment_name"],
            "subject": block["subject"],
            "insertion_number": block["insertion_number"],
            "block_start": block["block_start"],
            "block_end": block["block_end"],
            "probe_type": probe_type,
            "electrode_config_name": electrode_config_name,
            "electrode_group": electrode_group["electrode_group"],
            "paramset_id": paramset_id_str,
        }
        spike_sorting.SortingTask.insert1(task_key, skip_duplicates=True)
