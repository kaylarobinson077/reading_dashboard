import plotly.graph_objects as go

# inspo: https://github.com/tanul-mathur/music-through-the-ages/blob/40ce59fc8575dbed8e12e3c13752c4ac9aad9382/Helper.py#L10

def draw_num_pages_histogram(df):

    fig = go.Figure()

    df_ = df[["num_pages", "is_finished", "title"]]
    df_["is_finished"].replace({True: "Finished", False: "Not Finished"}, inplace=True)

    color_dict = {"Finished": "lightgreen", "Not Finished": "lightpink"}

    #plot params
    labels = df_["is_finished"].unique()

    for label_name in labels:

        fig.add_trace(go.Histogram( 
                                    x = df_[df_["is_finished"]==label_name]["num_pages"],
                                    name = label_name,
                                    hovertemplate='# Pages: %{x}, # Books: %{y}',
                                    marker_color = color_dict.get(label_name),
                                    ))

    fig.update_layout(barmode="stack")
    fig.update_yaxes(title_text = '# Books',linecolor = 'grey', mirror = True,
                        title_standoff = 0, gridcolor = 'grey', gridwidth = 0.1,
                        zeroline = False)
    fig.update_xaxes(title_text = '# Pages', linecolor = 'grey', mirror = True)

    return fig

def plot_time_read_versus_duration(df):

    df_ = df[["title", "time_read", "time_to_finish"]]
    
    # cast time read, time to finish to days
    df_["days_read"] = df_["time_read"].dt.days
    df_["days_to_finish"] = df_["days_to_finish"].dt.days

    pass