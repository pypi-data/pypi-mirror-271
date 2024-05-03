import numpy as np
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches

# Bar graph 
def plot_graph(ax, coefficients, lower_bounds, upper_bounds, p_values=None, variable_names=None,
               standardize=False, xlabel='Coefficients',
               title='Regression Analysis',
               show_yticks=True, 
               custom_levels=None,  
               negative_colour='#fcb4b4', positive_colour='#c4c4fc', input_X=None):
    
    # Standardize values
    if standardize and input_X is not None:
        std_X = np.std(input_X)
        coefficients = coefficients * std_X
        lower_bounds = lower_bounds * std_X
        upper_bounds = upper_bounds * std_X
        
    # Default levels unless user provides levels
    saturation_levels = custom_levels if custom_levels is not None else [0.05, 0.1, 0.2, 0.3, 0.5]

    # Levels based on the given input and p-values
    def saturation_range(p_value, saturation_levels):
        for i, level in enumerate(saturation_levels):
            if p_value <= level:
                return 1 - (i / len(saturation_levels))**2  
        return 0  

    # Plot bar graph
    for i, (lower, higher, p_value) in enumerate(zip(lower_bounds, upper_bounds, p_values)):
        saturation = saturation_range(p_value, saturation_levels) if p_values is not None else 0.5
        color = mcolors.to_rgba(positive_colour if coefficients[i] < 0 else negative_colour, alpha=saturation)
        
        # Set red boarder for p-values < 0.05
        border_color = 'red' if p_value < 0.05 else 'black'  
        bar_style = ax.barh(i, higher - lower, left=lower, color=color, edgecolor=border_color, linewidth=1.2)
        coordinates = (lower + higher) / 2
        ax.plot([coordinates, coordinates], [bar_style[0].get_y(), bar_style[0].get_y() + bar_style[0].get_height()], color=border_color, linewidth=1)  # Set line color same as border color

    # Grey lines in the background
    for idx in range(len(coefficients)):
        ax.axhline(idx + 0.5, color='lightgrey', linestyle='--', alpha=0.6, zorder=0)

    # Black line at 0
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)

    # By default show the y axis ticks 
    if show_yticks:
        ax.set_yticks(np.arange(len(variable_names)) + 0.5)
        ax.set_yticklabels(variable_names)
        ax.set_ylim(-0.5, len(variable_names) - 0.5) 
    else:
        ax.set_yticks([])
        ax.set_ylim(-0.5, len(variable_names) - 0.5) 
        
    # Graph title and label
    ax.set_xlabel(xlabel)
    ax.set_title(title)

    # Legend for red border 
    ax.legend(handles=[mpatches.Patch(edgecolor='red', linewidth=1, facecolor='none', label='P-value < 0.05')],
               loc='lower right', fontsize='small')

    # Create a colour bar
    if p_values is not None:
        sorted_values = sorted(p_values)
        tick_number = 5
        bar_size = len(sorted_values) // tick_number
        bar_values = [sorted_values[i * bar_size] for i in range(tick_number)]
        all_p_values = bar_values + bar_values[::-1]

        level_number = 4.5
        cmap = mcolors.LinearSegmentedColormap.from_list("custom", [negative_colour, '#ffffff', positive_colour], N=level_number*2)
        norm = mcolors.Normalize(vmin=0, vmax=1)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])

        cbar_ax = ax.figure.add_axes([ax.get_position().xmin,  
                                      ax.get_position().ymin - 0.09,  
                                      ax.get_position().width,
                                      0.03])  
        tick_positions = np.linspace(0, 1, len(all_p_values))

        cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal')
        cbar.set_ticks(tick_positions)

        # Show ticks on the colour bar
        cbar.set_ticklabels(["{:.3e}".format(p) for p in all_p_values], rotation=-45)
        cbar.set_label('Negative Coefficients' + ' ' *30 + 'P-value' + ' ' * 30 + 'Positive Coefficients')

# Coefficent distrabution 
def coefficient_distribution_plots(ax, coefficients=None, distribution=None, p_values=None, variable_names=None,
                xlabel='Coefficients', title='Regression Analysis',
                show_yticks=True, positive_colour='#c4c4fc', negative_colour='#fcb4b4',
                num_std=None, lower_percentile=0, upper_percentile=1,
                custom_levels=None):  

    # Default levels unless user provides levels
    saturation_levels = custom_levels if custom_levels is not None else [0.05, 0.1, 0.2, 0.3, 0.5]
    
    def saturation_range(p_value, saturation_levels):
        for i, level in enumerate(saturation_levels):
            if p_value <= level:
                return 1 - (i / len(saturation_levels))**2  
        return 0 
    
    # Error Handling
    if coefficients is None:
        raise ValueError("Coefficients needs to be provided.")
    if distribution is None:
        raise ValueError("Distribution needs to be provided.")
    if p_values is None:
        raise ValueError("P-values needs to be provided.")

    # Set default values 
    num_std = num_std or 3
    lower_percentile = lower_percentile or 0.01
    upper_percentile = upper_percentile or 0.99

    # Gap space between the bell curves
    distrabution_gap = 0.2  

    # Plot graph
    for i, (coefficient, distribution, p_value) in enumerate(zip(coefficients, distribution, p_values)):
        color = positive_colour if coefficient >= 0 else negative_colour
        saturation = saturation_range(p_value, saturation_levels)
        saturation_color = mcolors.to_rgba(color, alpha=saturation)
        
        if hasattr(distribution, 'pdf'):
            if num_std is not None:
                std_dev = distribution.std()
                mean = distribution.mean()
                x_values = np.linspace(mean - num_std * std_dev, mean + num_std * std_dev, 100)
            else:
                if lower_percentile is None:
                    lower_percentile = 0
                if upper_percentile is None:
                    upper_percentile = 1
                lower_percentile = max(0, min(lower_percentile, 1))
                upper_percentile = max(0, min(upper_percentile, 1))
                x_values = np.linspace(distribution.ppf(lower_percentile), distribution.ppf(upper_percentile), 100)
            pdf = distribution.pdf(x_values)
        elif hasattr(distribution, 'pmf'):
            x_values = np.arange(distribution.ppf(lower_percentile), distribution.ppf(upper_percentile))
            pdf = distribution.pmf(x_values)
        else:
            raise ValueError("This distrabution type is not supported")
            
        pdf /= pdf.max()
        
        # Position values
        colour_ticks = pdf * 0.8 + i * distrabution_gap
        ax.plot(x_values, colour_ticks, color= 'red' if p_value < 0.05 else 'black', linewidth=1.2)  # Adjust line thickness for outline
        ax.fill_between(x_values, colour_ticks, i * distrabution_gap, color=saturation_color)

    # Grey lines in the background
    for idx in range(len(coefficients)):
        ax.axhline(idx * distrabution_gap, color='lightgrey', linestyle='--', alpha=0.6, zorder=0)

    # Black line at 0
    ax.axvline(x=0, color='black', linestyle='-', linewidth=1)  

    # By default show the y axis ticks 
    if show_yticks:
        ax.set_yticks(np.arange(len(variable_names)) + (distrabution_gap - 0.2))  
        ax.set_yticklabels(variable_names)
        ax.set_ylim(-0, len(variable_names) - 0) 
    else:
        ax.set_yticks([])
        ax.set_ylim(-0, len(variable_names) - 0)  

    # Graph titles 
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    
    # Add legend for red border
    ax.legend(handles=[mpatches.Patch(edgecolor='red', linewidth=1, facecolor='none', label='P-value < 0.05')],
               loc='lower right', fontsize='small')

    # Create a colour bar
    level_number = len(saturation_levels)
    cmap = mcolors.LinearSegmentedColormap.from_list("custom", [negative_colour, '#ffffff', positive_colour], N=level_number*2)  # Swap positive and negative colors
    norm = mcolors.Normalize(vmin=0, vmax=1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cbar_ax = ax.figure.add_axes([ax.get_position().xmin,  
                                  ax.get_position().ymin - 0.09,  
                                  ax.get_position().width,
                                  0.03])  
    
    if p_values is not None:
        sorted_values = sorted(p_values)
        tick_number = 5
        bar_size = len(sorted_values) // tick_number
        bar_values = [sorted_values[i * bar_size] for i in range(tick_number)]
        all_p_values = bar_values + bar_values[::-1]

        level_number = 4.5
        cmap = mcolors.LinearSegmentedColormap.from_list("custom", [negative_colour, '#ffffff', positive_colour], N=level_number*2)
        norm = mcolors.Normalize(vmin=0, vmax=1)
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
        sm.set_array([])
        
        # Remove default labels on colour bar
        cbar_ax.set_xticks([])
        cbar_ax.set_xticklabels([])
        cbar_ax.set_yticks([])

        cbar_ax = ax.figure.add_axes([ax.get_position().xmin,  
                                      ax.get_position().ymin - 0.09,  
                                      ax.get_position().width,
                                      0.03])  
        tick_positions = np.linspace(0, 1, len(all_p_values))

        cbar = plt.colorbar(sm, cax=cbar_ax, orientation='horizontal', pad=0.)
        cbar.set_ticks(tick_positions)
        
        # Colour bar ticks
        cbar.set_ticklabels(["{:.3e}".format(p) for p in all_p_values], rotation=-45)
        cbar.set_label('Negative Coefficients' + ' ' *30 + 'P-value' + ' ' * 30 + 'Positive Coefficients')
        
# Create table
def create_table(ax, data, dependent_variable='y', loc='right', cell_loc='left', font_size=10, bbox=[0, 0, 1, 1], col_widths=None,
                 label_cell_loc='center', labels_bbox=[0, 0, 1, 1]):

    numeric_data = data.select_dtypes(include=[np.number])
    if dependent_variable in data.columns:
        numeric_data = numeric_data.drop(columns=[dependent_variable])

    mean = np.mean(numeric_data, axis=0)
    std = np.std(numeric_data, axis=0)
    table_info = list(zip(numeric_data.columns, np.round(mean, 2), np.round(std, 2)))

    # Reverse the order of rows
    table_info = list(reversed(table_info))

    # Default options
    if table_info:
        col_widths = col_widths or [0.2] * (len(numeric_data.columns) + 1)
        loc = loc or 'center'
        bbox = bbox or [0, 0, 1, 1]

        # Original table size and position
        table_bbox = [-0.1, 0, 0.7, 1]
        table_col_widths = [0.1, 0.05, 0.05]  
        table = ax.table(cellText=table_info, loc=loc, cellLoc=cell_loc, colWidths=table_col_widths, bbox=table_bbox)
        table.auto_set_font_size(False)
        table.set_fontsize(font_size)
        ax.axis('off')

        # Add labels directly above the table
        bbox_x, bbox_y, bbox_width, bbox_height = table_bbox
        label_y = bbox_y + bbox_height + 0

        # Additional labels table without borders
        labels_bbox = [-0.1, 0, 0.7, 1]
        labels_col_widths = [0.1, 0.05, 0.05]
        labels_table_info = [('Variable', 'Mean', 'STD')]
        labels_bbox = [bbox_x, label_y, bbox_width, 0.05]  
        labels_table = ax.table(cellText=labels_table_info, loc='center', cellLoc=label_cell_loc, colWidths=labels_col_widths, bbox=labels_bbox)
        labels_table.auto_set_font_size(False)
        labels_table.set_fontsize(10)
        ax.axis('off')

        # Remove borders from the table cells
        for cell in labels_table._cells:
            labels_table._cells[cell].set_edgecolor('none')

# Extract data from a regression model
def extract_data(model_result=None, coefficients=None, lower_bounds=None, upper_bounds=None,
                            p_values=None, variable_names=None, input_data=None, input_X=None,
                            standardize=False, figsize=(12, 8), xlabel='Coefficients',
                            title='Regression Analysis',
                            positive_colour='#c4c4fc', negative_colour='#fcb4b4',
                            table_kwargs=None, **kwargs):
    
    # Get the values from the model
    if model_result is not None:
        if hasattr(model_result, 'params') and hasattr(model_result, 'confidence_interval'):
            coefficients = model_result.params
            confidence_interval = model_result.confidence_interval()
            try:
                lower_bounds, upper_bounds = confidence_interval.iloc[:, :2].values.T
            except AttributeError:
                confidence_interval_df = pd.DataFrame(confidence_interval, columns=['lower', 'upper'])
                lower_bounds, upper_bounds = confidence_interval_df.iloc[:, :2].values.T
            p_values = model_result.pvalues
        else:
            raise ValueError("Unsupported model result, please use statsmodels")

        return coefficients, lower_bounds, upper_bounds, p_values
    else:
        raise ValueError("Model needs to be passed through.")
            
# Combined code to call bar and bell graph depending on what data is being passed
def regression_plot(ax, model_result=None, coefficients=None, distribution=None,
                     p_values=None, variable_names=None, input_data=None, input_X=None,
                     lower_bounds=None, upper_bounds=None,
                     standardize=False, xlabel='Coefficients', title='Regression Analysis',
                     positive_colour='#c4c4fc', negative_colour='#fcb4b4',
                     table_kwargs=None, ax_table=None, num_std=None,
                     lower_percentile=None, upper_percentile=None, show_yticks=True, **kwargs):
    
    # Error handling for standardizing values
    if standardize and input_X is None:
        raise ValueError("If standardized=True, independent variable (x) needs to be provided.")

    # Fitted regression model passed 
    if model_result is not None:
        coefficients, lower_bounds, upper_bounds, p_values = \
            extract_data(model_result, variable_names=variable_names, input_data=input_data,
                         input_X=input_X, standardize=standardize)

    #  Data for the bell curve is passed
    if coefficients is not None:
        if distribution is not None and p_values is not None:
            coefficient_distribution_plots(ax, coefficients, distribution, p_values, variable_names=variable_names,
                        xlabel=xlabel, title=title, positive_colour=negative_colour,  
                        negative_colour=positive_colour, num_std=num_std,
                        lower_percentile=lower_percentile, upper_percentile=upper_percentile, show_yticks=show_yticks)
            
        # Manual dataset passed
        else:
            plot_graph(ax, coefficients, lower_bounds, upper_bounds, p_values, variable_names=variable_names,
                       standardize=standardize, xlabel=xlabel, title=title,
                       positive_colour=positive_colour, negative_colour=negative_colour, input_X=input_X, show_yticks=show_yticks, **kwargs)
        
    elif lower_bounds is not None and upper_bounds is not None:
        plot_graph(ax, coefficients, lower_bounds, upper_bounds, p_values, variable_names=variable_names,
                   standardize=standardize, xlabel=xlabel, title=title,
                   positive_colour=positive_colour, negative_colour=negative_colour, input_X=input_X, show_yticks=show_yticks, **kwargs)
    else:
        raise ValueError("Coefficients needs to be provided.")
    
    # Table customization 
    if ax_table is not None:
        create_table(ax_table, input_data, **(table_kwargs or {}))
