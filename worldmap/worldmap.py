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
time = ['1:00', '2:30', '4:00', '5:30', '7:00', '8:30', '10:00', '11:30', '13:00', '14:30', '16:00', '17:30', '19:00', '20:30', '22:00', '23:30']
heartbeat = [80, 85, 70, 75, 90, 95, 100, 110, 105, 98, 100, 90, 95, 85, 87, 120]
respiration = [20, 22, 19, 18, 21, 23, 22, 24, 20, 19, 21, 18, 19, 17, 19, 25]

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

# サンプルデータの作成（アプリケーション2用）
dates = pd.date_range(start="2024-08-18", end="2024-08-23", freq="D")
data = {
    "Date": np.repeat(dates, 50),
    "Value": np.random.randint(65, 100, size=50 * len(dates)),
}
df = pd.DataFrame(data)

# アプリケーション2: Health
app2 = DjangoDash('Health', external_stylesheets=[dbc.themes.BOOTSTRAP])
app2.layout = html.Div([
    dcc.Graph(id="box-plot",config={"displayModeBar": False}),
    dcc.DatePickerRange(
        id="date-picker",
        start_date=df["Date"].min(),
        end_date=df["Date"].max(),
        display_format="YYYY-MM-DD",
    )
])

@app2.callback(
    Output("box-plot", "figure"),
    [Input("date-picker", "start_date"),
     Input("date-picker", "end_date")]
)
def update_box_plot(start_date, end_date):
    # 日付フィルタリング
    filtered_df = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    # Box Plotの作成
    fig = px.box(filtered_df, x="Date", y="Value")
    fig.update_layout(transition_duration=500)
    return fig

# サンプルデータの作成（アプリケーション3用）
dates = pd.date_range(start="2024-09-01", end="2024-09-30", freq="D")
sleep_time = np.random.randint(5, 10, len(dates))  # 睡眠時間のランダムデータ
active_time = 24 - sleep_time  # 活動時間（24時間 - 睡眠時間）

df_sleep = pd.DataFrame({
    "Date": dates,
    "睡眠時間": sleep_time,
    "活動時間": active_time,
})

# アプリケーション3: Sleep
app3 = DjangoDash('Sleep', external_stylesheets=[dbc.themes.BOOTSTRAP])
app3.layout = html.Div([
    dcc.Graph(id="area-chart",config={"displayModeBar": False}),
    dcc.DatePickerRange(
        id="date-picker",
        start_date=df_sleep["Date"].min(),
        end_date=df_sleep["Date"].max(),
        display_format="YYYY-MM-DD",
        start_date_placeholder_text="開始日を選択",
        end_date_placeholder_text="終了日を選択",
    )
])

@app3.callback(
    Output("area-chart", "figure"),
    [Input("date-picker", "start_date"),
     Input("date-picker", "end_date")]
)
def update_area_chart(start_date, end_date):
    # 日付範囲でデータをフィルタリング
    filtered_df = df_sleep[(df_sleep["Date"] >= start_date) & (df_sleep["Date"] <= end_date)]

    # エリアチャートの作成
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["睡眠時間"],
        mode='lines',
        name='睡眠時間',
        stackgroup='one',
        line=dict(color='skyblue')
    ))
    fig.add_trace(go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["活動時間"],
        mode='lines',
        name='活動時間',
        stackgroup='one',
        line=dict(color='orange')
    ))
    fig.update_layout(
        xaxis_title="日付",
        yaxis_title="時間（時間）",
            legend=dict(
        orientation="h",  # 水平表示に設定
        yanchor="bottom",  # 凡例の垂直位置の基準を下に設定
        y=1.1,  # グラフの上部より少し上に配置
        xanchor="center",  # 凡例の水平位置の基準を中央に設定
        x=0.5  # グラフの中央に配置
    ),
        yaxis=dict(range=[0, 24])
    )
    return fig

# サンプルデータ作成
sleep_week_data = {
    "曜日": ["月曜日", "火曜日", "水曜日", "木曜日", "金曜日", "土曜日", "日曜日"] * 6,
    "週": ["1w"] * 7 + ["2w"] * 7 + ["3w"] * 7 + ["4w"] * 7 + ["5w"] * 7 + ["6w"] * 7,
    "値": [
        1, 3, 5, 7, 2, 4, 6,
        2, 6, 4, 3, 5, 7, 8,
        4, 5, 6, 3, 8, 2, 7,
        6, 8, 2, 5, 7, 4, 3,
        7, 2, 8, 4, 6, 3, 5,
        3, 4, 6, 8, 2, 5, 7,
    ],
}

sleep_week_df = pd.DataFrame(sleep_week_data)

# DjangoDashアプリケーションの作成
app4 = DjangoDash('SleepWeekly', external_stylesheets=[dbc.themes.BOOTSTRAP])

# ピボットテーブルでデータを整形
sleep_week_heatmap_data = sleep_week_df.pivot(index="週", columns="曜日", values="値")

# ヒートマップの作成
fig = go.Figure(
    data=go.Heatmap(
        z=sleep_week_heatmap_data.values,
        x=sleep_week_heatmap_data.columns,
        y=sleep_week_heatmap_data.index,
        colorscale="Blues",  # カラースケールを指定
        colorbar=dict(title="値")
    )
)

# グラフのレイアウトを調整
fig.update_layout(
    xaxis=dict(title="曜日"),
    yaxis=dict(title="週", autorange="reversed"),  # "1w" が上に来るように反転
)

# Dashアプリケーションのレイアウト
app4.layout = html.Div([
    dcc.Graph(figure=fig)
])

def make_ring_figure(value: int, color="#1f77b4", rest_color="#9bd5d6"):
    value = max(0, min(100, int(value)))
    fig = go.Figure(
        data=[
            go.Pie(
                values=[value, 100 - value],
                hole=0.82,  # リングの太さ（大きいほど細くなる）
                sort=False,
                direction="clockwise",
                rotation=90,  # 12時開始
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
        height=220,
        annotations=[
            dict(
                text=f"<b>{value}%</b>",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=40, color="#111827"),
            )
        ],
    )
    return fig

# アプリ（例）
app5 = DjangoDash("InnovationGauge", external_stylesheets=[dbc.themes.BOOTSTRAP])

app5.layout = html.Div(
    children=[
        dcc.Graph(
            id="innovation-gauge",
            config={"displayModeBar": False},
            figure=make_ring_figure(91),
            style={"height": "140px"},
        ),
        html.Div(
            "INNOVATION",
            style={
                "textAlign": "center",
                "fontWeight": "600",
                "letterSpacing": "0.06em",
                "marginTop": "-6px",
            },
        ),
    ],
    style={"width": "200px", "background": "white"},
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
        height=160,
        width=200,
        annotations=[
            dict(
                text=f"<b>{value}%</b>",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=44, color="#111827"),
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
            style={"height": "160px"},
        ),
    ],
    style={
        "width": "200px",
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


def wordcloud_png_base64(freq: dict, width=900, height=320) -> str:
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
                "height": "auto",
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

