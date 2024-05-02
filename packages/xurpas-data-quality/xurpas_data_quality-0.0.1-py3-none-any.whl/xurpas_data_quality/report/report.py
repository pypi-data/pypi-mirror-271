from xurpas_data_quality.data.descriptions import TableDescription
from xurpas_data_quality.render.renderer import HTMLBase, HTMLContainer, HTMLTable, HTMLVariable, HTMLPlot, HTMLToggle, HTMLCollapse
from xurpas_data_quality.visuals import plot_to_base64, create_tiny_histogram, create_histogram, create_distribution_plot, create_heatmap, create_distribution_from_dataframe

from dataclasses import fields

def get_detailed_variable_info(df, key, details:list):
    bottom = [            
        HTMLContainer(
            type="box",
            name="Statistics",
            id= "stats",
            container_items= [
                HTMLContainer(
                    type="column",
                    container_items=
                        HTMLTable(
                            data=details[0],
                            name="Quantile Statistics"
                        )
                    
                ),
                HTMLContainer(
                    type="column",
                    container_items=
                        HTMLTable(
                            data=details[0],
                            name="Descriptive Statistics"
                        )
                    
                )
            ]
        ),
        HTMLPlot(
            name="Histogram",
            type="large",
            id="histo",
            plot=plot_to_base64(create_histogram(df[key]))
        )
    ]
    if df[key].dtype != 'object':
        bottom.append(            
            HTMLPlot(
                name="Distribution",
                id="distribution",
                type="large",
                plot=plot_to_base64(create_distribution_plot(df[key]))
            ))
    return HTMLContainer(
        type="tabs",
        col=key,
        container_items=bottom
    )

def get_variable_data(data: TableDescription):
    variables = []

    for key, value in data.variables.items():
        split_dict = lambda d: (dict(list(d.items())[:len(d)//2]), dict(list(d.items())[len(d)//2:]))
        table_1, table_2 = split_dict(value['overview'])

        variable_body = {
            'table_1':HTMLTable(table_1),
            'table_2':HTMLTable(table_2),
            'plot': HTMLPlot(plot=plot_to_base64(create_tiny_histogram(data.df[key])))
        }
        btn = HTMLToggle("More details", key)
        variables.append(
                    HTMLVariable(
                        name=key,
                        body = variable_body,
                        bottom = HTMLCollapse(btn, get_detailed_variable_info(data.df,key,data.variables[key]['details']))
                    ))
    
    return variables

def get_report(data: TableDescription, name:str=None)-> HTMLBase:
    content = []

    overview_section = HTMLContainer(
        type="box",
        name="Overview",
        container_items = [
            HTMLContainer(
                type="column",
                container_items = HTMLTable(
                    data=data.df_statistics,
                    name="Dataset Statistics"
                )),
            HTMLContainer(
                type="column",
                container_items =  HTMLTable(
                    data=data.var_types,
                    name="Variable Types"
                )
            )
        ]
    )

    variables_section = HTMLContainer(
        type="box",
        name="Variables",
        container_items = get_variable_data(data)
    )

    corr_df = data.df.corr(numeric_only=True).round(3)
    correlation = HTMLContainer(
        type="box",
        name="Correlation",
        container_items=[
            HTMLContainer(
                type="tabs",
                container_items=[
                    HTMLPlot(plot=plot_to_base64(create_heatmap(corr_df)),
                             type="large",
                             id="corr",
                             name="Heatmap"),
                    HTMLTable(
                        id='sample',
                        name="Table",
                        data=corr_df.to_html(classes="table table-sm", border=0))
                ]
            )
        ]
    )

    samples = HTMLContainer(
        type="box",
        name="Sample",
        container_items=[
            HTMLTable(
                id = "sample",
                data=data.df.head(10).to_html(classes="table table-sm", border=0)
            )
        ]
    )

    distribution = HTMLContainer(
        type="box",
        name="Distribution",
        container_items=[
            HTMLPlot(
                plot= plot_to_base64(create_distribution_from_dataframe(data.df)),
                type="large"
            )
        ]
    )
    
    content.extend([
        overview_section,
        variables_section,
        correlation,
        samples,
        distribution
    ])

    body = HTMLContainer(
        type="sections",
        container_items = content,
    )

    if name is not None:
        return HTMLBase(
            body=body,
            name=name
        )
    
    else:
        return HTMLBase(
            body=body
        )