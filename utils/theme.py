def apply_dark_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="rgba(0,0,0,0)",  # Fond du graphique transparent
        paper_bgcolor="rgba(0,0,0,0)"  # Fond de la zone autour du graphique transparent
    )
    return fig
