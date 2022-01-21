import pandas as pd

from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

# inspo: https://github.com/tanul-mathur/music-through-the-ages/blob/40ce59fc8575dbed8e12e3c13752c4ac9aad9382/Helper.py#L10

def draw_num_pages_histogram(df):

    fig = go.Figure()

    df_ = df[["num_pages", "is_finished", "title"]]
    df_["is_finished"].replace({True: "Finished", False: "Not Finished"}, inplace=True)
    # df_["weeks_to_finish"] = df_["days_to_finish"] / 7

    pivot_df = df_.groupby(['num_pages','is_finished'])['title'].count()

    pivot_df = pivot_df.unstack()
    pivot_df.fillna(0, inplace = True)

    color_dict = {"Finished": "lightgreen", "Not Finished": "lightpink"}

    print(pivot_df)

    #plot params
    labels = pivot_df.columns

    # labels = df["is_finished"].unique()/

    for i, label_name in enumerate(labels):
        # print(pivot_df.iloc[:,i])
        # i=1
        print(i)
        print(pivot_df.iloc[:,i])

        x = pivot_df.iloc[:,i].index
        fig.add_trace(go.Histogram( # df_,
                                    x = df_[df_["is_finished"]==label_name]["num_pages"],
                                    #x=pivot_df.iloc[:,i],
                                    # color="is_finished"
                                    #y = pivot_df.iloc[:,i],
                                    name = label_name,
                                    hovertemplate='# Pages: %{x}, # Books: %{y}',
                                    marker_color = color_dict.get(label_name),
                                    # alignmentgroup="a"
                                    # marker_color = pd.Series([label_name]*len(x)).map(color_dict),
                                    # legendgroup = 'grp2',
                                    # showlegend=True))
                                    ))
        # break
    # fig.update_traces(bingroup="a")
    fig.update_layout(barmode="stack")
    fig.update_yaxes(title_text = '# Books',linecolor = 'grey', mirror = True,
                        title_standoff = 0, gridcolor = 'grey', gridwidth = 0.1,
                        zeroline = False)
    fig.update_xaxes(title_text = '# Pages', linecolor = 'grey', mirror = True) # , dtick = 5)

    return fig
