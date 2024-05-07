from matplotlib import pyplot as plt


def plot(
    rfft_axes,
    parameter_information,
    model_information,
    parameter_scales,
    fourier_scales,
):
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(10, 3.5))
    ax1.pcolormesh(
        parameter_information.axis() * parameter_scales.parameter_factor,
        rfft_axes.frequency_axis * fourier_scales.frequency_factor,
        trace_fit,
        cmap=resources.colormap_jetwhite.create_colormap(),
    )
    ax1.set_xlabel(parameter_scales.parameter_label())
    ax1.set_ylabel("Frequency (" + fourier_scales.frequency_unit + ")")
    ax1.set_xlim(
        (
            parameter_information.axis()[0]
            * parameter_scales.parameter_factor,
            parameter_information.axis()[-1]
            * parameter_scales.parameter_factor,
        )
    )
    ax1.set_ylim(
        (
            model_information.frequency_range_trace[0]
            * fourier_scales.frequency_factor,
            model_information.frequency_range_trace[-1]
            * fourier_scales.frequency_factor,
        )
    )

    ax2.pcolormesh(
        parameter_information.axis() * parameter_scales.parameter_factor,
        rfft_axes.frequency_axis * fourier_scales.frequency_factor,
        trace_processed_interpolated,
        cmap=resources.colormap_jetwhite.create_colormap(),
    )
    ax2.set_xlabel(parameter_scales.parameter_label())
    ax2.set_xlim(
        (
            parameter_information.axis()[0]
            * parameter_scales.parameter_factor,
            parameter_information.axis()[-1]
            * parameter_scales.parameter_factor,
        )
    )
    ax2.set_ylim(
        (
            model_information.frequency_range_trace[0]
            * fourier_scales.frequency_factor,
            model_information.frequency_range_trace[-1]
            * fourier_scales.frequency_factor,
        )
    )

    trace_difference = trace_fit / np.linalg.norm(
        trace_fit
    ) - trace_processed_interpolated / np.linalg.norm(
        trace_processed_interpolated
    )
    trace_difference_max = np.max(np.abs(trace_difference))
    ax3.pcolormesh(
        parameter_information.axis() * parameter_scales.parameter_factor,
        rfft_axes.frequency_axis * fourier_scales.frequency_factor,
        trace_difference,
        cmap="bwr",
        clim=(-trace_difference_max, trace_difference_max),
    )
    ax3.set_xlabel(parameter_scales.parameter_label())
    ax3.set_xlim(
        (
            parameter_information.axis()[0]
            * parameter_scales.parameter_factor,
            parameter_information.axis()[-1]
            * parameter_scales.parameter_factor,
        )
    )
    ax3.set_ylim(
        (
            model_information.frequency_range_trace[0]
            * fourier_scales.frequency_factor,
            model_information.frequency_range_trace[-1]
            * fourier_scales.frequency_factor,
        )
    )
    plt.show()
