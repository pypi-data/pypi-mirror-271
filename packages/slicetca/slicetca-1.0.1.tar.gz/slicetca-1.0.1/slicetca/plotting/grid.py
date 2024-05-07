import numpy as np

from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

from typing import Literal, Sequence


def plot_grid(loss_grid: np.ndarray,
              min_rank: Sequence = (0, 0, 0),
              data: np.ndarray = None,
              quantile: float = 0.0,
              vmin: float = None,
              vmax: float = None,
              reduction: Literal['mean', 'min'] = 'min',
              variables: Sequence[str] = ('trial', 'neuron', 'time'),
            ):
    """
    :param min_rank: minimum ranks of the gridsearch (default (0, 0, 0))
    :param loss_grid: (trial x neuron x time x batch) grid of cross-validated losses as a function of the number of components
    :param quantile:
    :param vmin:
    :param vmax:
    :param reduction:
    :param variables:
    :return:
    """

    max_rank = tuple(np.array(min_rank)+np.array(loss_grid.shape[:3]))

    match reduction:
        case 'mean':
            reduced_loss_grid = loss_grid.mean(axis=-1)
        case 'min':
            reduced_loss_grid = loss_grid.min(axis=-1)
        case _:
            raise Exception('Reduction should be mean or min.')

    min_index = np.unravel_index(np.argmin(reduced_loss_grid), reduced_loss_grid.shape)

    if data is not None:
        elbow_threshold = np.min(reduced_loss_grid)*0.9+np.mean(data**2)*0.1

    nb_plot = reduced_loss_grid.shape[0]
    if vmin is None: vmin = np.quantile(reduced_loss_grid, quantile)
    if vmax is None: vmax = np.quantile(reduced_loss_grid, 1-quantile)
    print('vmin:', vmin, 'vmax:', vmax)

    fig = plt.figure(figsize=(3*nb_plot,3), constrained_layout=True)
    axes = [fig.add_subplot(1, nb_plot, i+1) for i in range(nb_plot)]

    for i in range(nb_plot):
        im = axes[i].imshow(reduced_loss_grid[i], cmap='pink_r', origin='lower',
                            vmin=vmin, vmax=vmax, extent=(min_rank[2]-0.5, max_rank[2]-0.5, min_rank[1]-0.5, max_rank[1]-0.5))

        if data is not None:
            elbow_neuron = np.argmax(reduced_loss_grid[i] < elbow_threshold, axis=1).astype(float)
            elbow_time = np.argmax(reduced_loss_grid[i] < elbow_threshold, axis=0).astype(float)
            elbow_time[np.all(reduced_loss_grid[i] >= elbow_threshold, axis=0)] = np.nan
            elbow_neuron[np.all(reduced_loss_grid[i] >= elbow_threshold, axis=1)] = np.nan
            axes[i].plot(np.arange(min_rank[2], max_rank[2]), min_rank[1]+elbow_time, color=(0, 0, 0), alpha=0.3, linewidth=2.0)
            axes[i].plot(min_rank[2]+elbow_neuron, np.arange(min_rank[1], max_rank[1]), color=(0, 0, 0), alpha=0.3, linewidth=2.0)

        axes[i].set_aspect('equal')
        axes[i].set_title('$R_{'+variables[0]+'}='+f'{min_rank[0]+i}$')
        axes[i].set_ylabel('$R_{'+variables[1]+'}$')
        axes[i].set_xlabel('$R_{'+variables[2]+'}$')

        axes[i].yaxis.set_major_locator(MaxNLocator(integer=True))
        axes[i].xaxis.set_major_locator(MaxNLocator(integer=True))

        fig.colorbar(im,fraction=0.046, pad=0.04)

    axes[min_index[0]].scatter(min_rank[2]+min_index[2], min_rank[1]+min_index[1],
                            color=(0.9,0.2, 0.2), marker='*', s=200)

    if data is not None:
        elbow_index = np.stack(np.meshgrid(*tuple([np.arange(min_rank[i], max_rank[i]) for i in range(3)]), indexing='ij'), axis=-1).sum(axis=-1).astype(float)

        elbow_index[(reduced_loss_grid>=elbow_threshold)] = np.nan
        if not np.all(np.isnan(elbow_index)):
            elbow_index = np.unravel_index(np.argmin(elbow_index, axis=None), elbow_index.shape)
            axes[elbow_index[0]].scatter(min_rank[2]+elbow_index[2], min_rank[1]+elbow_index[1],
                                color=(0.9,0.2, 0.2), marker='*', s=200, facecolor=(1, 1, 1, 0))
