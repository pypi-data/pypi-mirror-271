"""Fitting using a genetic algorithm"""

import dataclasses
import random
import pygad
import numpy as np
from lasertools_tracefit import models


@dataclasses.dataclass
class SettingsGA:
    """Class to store genetic algorithm settings"""

    generations_count: int
    parent_count: int
    population_size: int
    mutation_probability: float
    elitism: int


class ModelComparisonGA:
    """Class to handle comparison between fit and measurement"""

    def __init__(self, model_comparison: models.base.ModelComparison):
        self.model_comparison = model_comparison

    def ga_calculate_fitness(self, ga_instance, solution, solution_idx):
        """Return fitness for GA"""

        return self.model_comparison.calculate_fitness(solution)


def ga_initialize(
    population_size,
    parameters_ranges_dicts,
):
    """Initialize a population with random parameters within ranges"""

    parameters_ranges = []
    for parameter_ranges_dict in parameters_ranges_dicts:
        parameters_ranges.append(
            [parameter_ranges_dict["low"], parameter_ranges_dict["high"]]
        )
    population = np.zeros((population_size, len(parameters_ranges_dicts)))
    for i in range(population_size):
        population[i, :] = np.array(
            [random.uniform(a, b) for (a, b) in parameters_ranges]
        )
    return population


def ga_optimize(
    model_comparison: ModelComparisonGA,
    settings: SettingsGA,
):
    ga_instance = pygad.GA(
        num_generations=settings.generations_count,
        num_parents_mating=settings.parent_count,
        num_genes=len(
            model_comparison.model_comparison.fit_model.settings.variables_fitting_ranges
        ),
        fitness_func=model_comparison.ga_calculate_fitness,
        initial_population=ga_initialize(
            settings.population_size,
            model_comparison.model_comparison.fit_model.settings.variables_fitting_ranges,
        ),
        mutation_type="random",
        mutation_probability=settings.mutation_probability,
        crossover_type="uniform",
        parent_selection_type="sss",
        parallel_processing=8,
        keep_elitism=settings.elitism,
        save_best_solutions=True,
        suppress_warnings=True,
        gene_space=(
            model_comparison.model_comparison.fit_model.settings.variables_fitting_ranges
        ),
    )
    ga_instance.run()
    return ga_instance
