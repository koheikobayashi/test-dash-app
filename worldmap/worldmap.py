from django_plotly_dash import DjangoDash  # DjangoDash を使用
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# データの準備
# （データ準備部分は元のコードを使用します）
# ここではサンプルデータを使用しています

# サンプルデータ
time = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
heartbeat = [80, 85, 70, 75, 90, 95, 100, 110, 105]

app1 = DjangoDash('WorldMap', external_stylesheets=[dbc.themes.BOOTSTRAP])

# 例: time が [55, 57, 61, 68, 77, 79, 82, 85] などの想定
# もし time が datetime なら、画像風の “%ラベル” には合わないので別調整が必要

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=time,
        y=heartbeat,                     # ここを「スコア推移」などに置き換え
        mode="lines+markers",
        name="",                         # 凡例出さない
        line=dict(color="#0ea5e9", width=4),
        marker=dict(size=9, color="#0ea5e9"),
        fill="tozeroy",
        fillcolor="rgba(14,165,233,0.15)",
        hovertemplate="%{x}<br>%{y}<extra></extra>",
    )
)

fig.update_layout(
    # 余白・背景
    margin=dict(l=50, r=20, t=10, b=40),
    paper_bgcolor="white",
    plot_bgcolor="white",
    showlegend=False,

    # グラフの高さ（カードに合わせやすい）
    height=260,
)

# 軸スタイル（画像っぽく薄いグリッド）
fig.update_xaxes(
    title_text="",                      # 画像は軸タイトルなし
    showgrid=True,
    gridcolor="rgba(15,23,42,0.08)",    # 薄いグレー
    zeroline=False,
    showline=True,
    linecolor="rgba(15,23,42,0.20)",
    tickfont=dict(color="rgba(15,23,42,0.70)", size=12),
)

fig.update_yaxes(
    title_text="",
    showgrid=True,
    gridcolor="rgba(15,23,42,0.08)",
    zeroline=False,
    showline=True,
    linecolor="rgba(15,23,42,0.20)",
    tickfont=dict(color="rgba(15,23,42,0.70)", size=12),
)

# x が数値なら「%」表示に寄せる（文字列ならそのまま表示される）
# 例: 55 -> "55%"
fig.update_xaxes(tickformat=".0f")      # 数値表示を整数に
# xが数値のときだけsuffixを付けたい場合は tickprefix/ticksuffix が楽
fig.update_xaxes(ticksuffix="%")

# y も % っぽく見せたい場合（画像は左に % っぽい値が並んでいる）
fig.update_yaxes(ticksuffix="%")

app1.layout = html.Div(
    children=[
        dcc.Graph(
            id="line-plot",
            config={"displayModeBar": False},
            figure=fig,
            style={"width": "100%"},
        )
    ]
)

def make_ring_figure_blue(value: int, color="#1d4ed8", rest_color="#7ec8d6"):
    value = max(0, min(100, int(value)))

    fig = go.Figure(
        data=[
            go.Pie(
                values=[value, 100 - value],
                hole=0.86,                 # リング細め（画像寄せ）
                sort=False,
                direction="clockwise",
                rotation=270,              # 下あたり始点っぽく
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=[color, rest_color],
                    line=dict(color="white", width=2),
                ),
                showlegend=False,
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        # autosize=True,
        annotations=[
            dict(
                text=f"<b>{value}%</b>",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=36, color="#111827"),
            )
        ],
    )
    return fig

app5 = DjangoDash("InnovationGauge", external_stylesheets=[dbc.themes.BOOTSTRAP])

app5.layout = html.Div(
    children=[
        dcc.Graph(
            id="innovation-gauge",
            config={"displayModeBar": False},
            figure=make_ring_figure_blue(91),
            style={"width": "100%", "height": "120px"},
        ),
    ],
    style={
        "width": "100%", 
        "height": "100%",
        "background": "white",
        "display": "grid",
        "placeItems": "center",
    },
)

def make_ring_figure(value: int, color="#f59e0b", rest_color="#fde68a"):
    value = max(0, min(100, int(value)))

    fig = go.Figure(
        data=[
            go.Pie(
                values=[value, 100 - value],
                hole=0.86,                 # リングを細めに（画像っぽく）
                sort=False,
                direction="clockwise",
                rotation=270,              # 下あたりから始まる雰囲気に寄せる
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=[color, rest_color],
                    line=dict(color="white", width=2),
                ),
                showlegend=False,
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        # autosize=True,
        annotations=[
            dict(
                text=f"<b>{value}%</b>",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=36, color="#111827"),
            )
        ],
    )
    return fig

app7 = DjangoDash("ExecutionSpeed", external_stylesheets=[dbc.themes.BOOTSTRAP])

app7.layout = html.Div(
    children=[
        dcc.Graph(
            id="innovation-gauge",
            config={"displayModeBar": False},
            figure=make_ring_figure(75),     # ← 画像は 75%
            style={"width": "100%", "height": "120px"},
        ),
    ],
    style={
        "width": "100%", 
        "height": "100%",
        "background": "white",
        "display": "grid",
        "placeItems": "center",
    },
)

import plotly.graph_objects as go

def make_ring_figure_green(value: int, color="#16a34a", rest_color="#9bd5d6"):
    value = max(0, min(100, int(value)))

    fig = go.Figure(
        data=[
            go.Pie(
                values=[value, 100 - value],
                hole=0.86,                 # リング細め（画像寄せ）
                sort=False,
                direction="clockwise",
                rotation=270,              # 下あたり始点っぽく
                textinfo="none",
                hoverinfo="skip",
                marker=dict(
                    colors=[color, rest_color],
                    line=dict(color="white", width=2),
                ),
                showlegend=False,
            )
        ]
    )

    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="white",
        plot_bgcolor="white",
        # autosize=True,
        annotations=[
            dict(
                text=f"<b>{value}%</b>",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=36, color="#111827"),
            )
        ],
    )
    return fig

app8 = DjangoDash("CustomerGauge", external_stylesheets=[dbc.themes.BOOTSTRAP])

app8.layout = html.Div(
    children=[
        dcc.Graph(
            id="customer-gauge",
            config={"displayModeBar": False},
            figure=make_ring_figure_green(88),
            style={"width": "100%", "height": "120px"},
        ),
    ],
    style={
        "width": "100%", 
        "height": "100%",
        "background": "white",
        "display": "grid",
        "placeItems": "center",
    },
)

# apps/wordcloud_dash.py など（Django起動時にimportされる場所）
import base64
from io import BytesIO

from django_plotly_dash import DjangoDash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

from wordcloud import WordCloud


def wordcloud_png_base64(freq: dict, width=900, height=600) -> str:
    """
    freq: {"PROACTIVE": 50, "COLLABORATION": 40, ...} のような頻度辞書
    return: data URI に使える base64 文字列
    """
    wc = WordCloud(
        width=width,
        height=height,
        background_color="white",
        prefer_horizontal=0.8,
        random_state=42,
        collocations=False,
        # 日本語を混ぜるなら font_path が必要なことが多い
        # font_path="path/to/NotoSansCJKjp-Regular.otf",
    ).generate_from_frequencies(freq)

    img = wc.to_image()
    buf = BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{b64}"


app_wc = DjangoDash("FeedbackWordCloud")

app_wc.layout = html.Div(
    [
        # 必要なら定期更新（例：30秒）
        dcc.Interval(id="wc-tick", interval=30_000, n_intervals=0),
        html.Img(
            id="wc-image",
            style={
                "width": "100%",
                "height": "100%",
                "display": "block",
                "borderRadius": "12px",
            },
        ),
    ],
    style={
        "background": "white",
        "padding": "10px",
        "borderRadius": "14px",
        "border": "1px solid #e5e7eb",
    },
)


@app_wc.callback(Output("wc-image", "src"), Input("wc-tick", "n_intervals"))
def update_wordcloud(_):
    # 本来はここでAWS等から「単語->頻度」を取得してfreqを作る
    freq = {
        "PROACTIVE": 60,
        "COLLABORATION": 52,
        "ENGAGED": 35,
        "COMMUNICATION": 28,
        "OWNERSHIP": 22,
        "CREATIVE": 18,
        "CONSISTENT": 16,
        "ENERGETIC": 14,
        "AWARENESS": 12,
        "TEAMWORK": 11,
        "RESILIENT": 10,
    }
    return wordcloud_png_base64(freq)

def progress_bar(percent: int):
    p = max(0, min(100, int(percent)))
    return html.Div(
        [
            html.Div(
                [
                    html.Div(
                        style={
                            "width": f"{p}%",
                            "height": "100%",
                            "borderRadius": "999px",
                            "background": "linear-gradient(90deg, #38bdf8, #0ea5e9)",
                            "boxShadow": "0 6px 14px rgba(14,165,233,0.25)",
                        }
                    )
                ],
                style={
                    "flex": "1",
                    "height": "12px",
                    "borderRadius": "999px",
                    "background": "#d1d5db",
                    "overflow": "hidden",
                    "position": "relative",
                    "boxShadow": "inset 0 0 0 1px rgba(0,0,0,0.04)",
                },
                role="progressbar",
                **{"aria-valuenow": str(p), "aria-valuemin": "0", "aria-valuemax": "100"},
            ),
            html.Div(
                f"{p}%",
                style={
                    "fontWeight": "900",
                    "fontSize": "44px",
                    "letterSpacing": "-0.02em",
                    "color": "#111827",
                    "lineHeight": "1",
                    "minWidth": "90px",
                    "textAlign": "right",
                    "textShadow": "-1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff",
                },
            ),
        ],
        style={"display": "flex", "alignItems": "center", "gap": "16px", "width": "100%"},
    )

app6 = DjangoDash("ProgressBar", external_stylesheets=[dbc.themes.BOOTSTRAP])

app6.layout = html.Div([progress_bar(85)], style={"maxWidth":"900px"})

