import dataclasses
import nlopt
from lasertools_tracefit.models.base import ModelComparison
import numpy as np


@dataclasses.dataclass
class SettingsLocal:
    initial_guesses: np.ndarray
    initial_guess_fractional_bound: float = 5
    method: object = nlopt.LN_NELDERMEAD
    stop_time_seconds: float = 10
    stop_tolerance_change: float = 0.000005


def local_optimize(model_comparison: ModelComparison, settings: SettingsLocal):
    opt = nlopt.opt(settings.method, len(settings.initial_guesses))

    bounds = True
    lower_bounds = np.zeros_like(settings.initial_guesses)
    upper_bounds = np.zeros_like(settings.initial_guesses)
    for k, initial_guess in enumerate(settings.initial_guesses):
        if initial_guess > 0:
            lower_bounds[k] = (
                initial_guess / settings.initial_guess_fractional_bound
            )
            upper_bounds[k] = (
                initial_guess * settings.initial_guess_fractional_bound
            )
        elif initial_guess < 0:
            lower_bounds[k] = (
                initial_guess * settings.initial_guess_fractional_bound
            )
            upper_bounds[k] = (
                initial_guess / settings.initial_guess_fractional_bound
            )
        elif initial_guess == 0:
            bounds = False
    if bounds:
        opt.set_lower_bounds(lower_bounds)
        opt.set_upper_bounds(upper_bounds)

    def calculate_fitness_local(x, grad):
        return model_comparison.calculate_fitness(x)

    opt.set_max_objective(calculate_fitness_local)

    opt.set_ftol_abs(settings.stop_tolerance_change)
    opt.set_maxtime(settings.stop_time_seconds)

    return opt.optimize(settings.initial_guesses)
