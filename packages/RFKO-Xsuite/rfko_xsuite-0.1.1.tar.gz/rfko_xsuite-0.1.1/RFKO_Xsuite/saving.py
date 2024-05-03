import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import datetime
from . import plotting1

def save_bench(outdict, parent_dir='Benchmark_dir', save_data=True, extramessage='',monitor=False,part0=None):
    # ASSERT BENCHMARKS_DIR EXIST
    if not os.path.exists(parent_dir):
        os.mkdir(parent_dir)
    date_time = datetime.now().strftime("%d%h___time_%H_%M")
    extr_part_for_message = np.sum(outdict['particles'].at_turn < outdict['params']['n_turns'])
    message = f"__part{outdict['params']['n_part']}__turns{outdict['params']['n_turns']}__extr_part{extr_part_for_message}" + f'__{extramessage}'
    filename = f'{parent_dir}/{date_time}___{message}'
    if not os.path.exists(date_time):
        os.mkdir(filename)
    else:
        date_time = datetime.now().strftime("%d%h___time_%H_%M_%S")
        filename = f'{parent_dir}/{date_time}___{message}'
        os.mkdir(filename)
        return None

    ### SAVING parameters in a text file
    params_str = [f'{key} = {val} \n' for key, val in outdict['params'].items()]
    if message is not None:
        params_str.insert(0, str(message)+'\n')  # this will add the message as the first string on the param.txt file
    with open(f'{filename}/params.txt', 'w') as f:
        f.writelines(params_str)

    if monitor:
        plotting1.plot_flex(outdict)

    plotting1.plot_extracted(outdict, beam_loss=True)
    plt.savefig(f'{filename}/extracted_intensity')

    ## Saving datas if True
    if save_data:
        np.save(f'{filename}/part_at_turn.npy', outdict['particles'].at_turn)
        np.save(f'{filename}/part_id.npy', outdict['particles'].particle_id)

        # SAVE THE MONITOR
        if monitor:
            np.save(f'{filename}/monitor_x.npy', outdict['monitor'].x)
            np.save(f'{filename}/monitor_px.npy', outdict['monitor'].px)
            np.save(f'{filename}/monitor_dpp.npy', outdict['monitor'].delta)
        if part0 is not None:
            np.save(f'{filename}/part0_x.npy',part0.x)
            np.save(f'{filename}/part0_px.npy',part0.px)
            np.save(f'{filename}/part0_delta.npy',part0.delta)
            # This will probably be not that useful
            np.save(f'{filename}/part0_id.npy',part0.particle_id)