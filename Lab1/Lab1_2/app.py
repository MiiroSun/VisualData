import os
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_draggable

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')
df = df[['country', 'continent', 'year', 'lifeExp', 'pop', 'gdpPercap']]

# Список уникальных стран для заполнения выпадающего списка
all_countries = df['country'].unique()

# Данные за последний год для начальных фигур при загрузке
df_2007 = df[df.year == 2007]

# При открытии страницы пользователь сразу видит данные за 2007
# Как только он наведёт на линейный график, сработает кросс-фильтр
# и остальные три графика переключатся на выбранный год

fig_bubble_init = px.scatter(
    df_2007, x='gdpPercap', y='lifeExp', size='pop',
    color='continent', hover_name='country',
    log_x=True, size_max=60,
    title='Пузырьковая диаграмма за 2007 год'
)

top15_init = df_2007.nlargest(15, 'pop')
fig_top15_init = px.bar(
    top15_init, x='pop', y='country', orientation='h',
    title='Топ-15 стран по населению (2007)',
    labels={'pop': 'Население', 'country': ''}
)

fig_top15_init.update_layout(yaxis={'categoryorder': 'total ascending'})

pop_cont_init = df_2007.groupby('continent', as_index=False)['pop'].sum()
fig_pie_init = px.pie(
    pop_cont_init, values='pop', names='continent',
    title='Доля населения по континентам (2007)'
)

app = dash.Dash(__name__)
server = app.server

# растягиваем каждый график на весь свой блок в сетке
style_graph = {"height": "100%", "width": "100%"}

app.layout = html.Div([
    html.H1("Дашборд демографии", style={'textAlign': 'center'}),

    # делаем так, чтобы блоки можно было двигать и растягивать мышкой
    dash_draggable.ResponsiveGridLayout(
        id='dashboard-grid',
        children=[
            # Панель фильтров
            html.Div([
                html.H3("Фильтры"),

                # мультивыбор стран
                dcc.Dropdown(
                    id='country-dropdown',
                    options=[{'label': c, 'value': c} for c in all_countries],
                    value=['Canada', 'United States', 'China'],
                    multi=True,                      
                    placeholder="Выберите страны..."
                ),
                html.Br(),

                # ось Y для линейного графика
                dcc.Dropdown(
                    id='yaxis-dropdown-line',
                    options=[
                        {'label': 'Продолжительность жизни', 'value': 'lifeExp'},
                        {'label': 'ВВП на душу населения', 'value': 'gdpPercap'},
                        {'label': 'Население', 'value': 'pop'}
                    ],
                    value='lifeExp'
                ),
                html.Br(),

                # ось X для пузырьковой диаграммы
                dcc.Dropdown(
                    id='xaxis-dropdown-bubble',
                    options=[
                        {'label': 'ВВП на душу населения', 'value': 'gdpPercap'},
                        {'label': 'Продолжительность жизни', 'value': 'lifeExp'},
                        {'label': 'Население', 'value': 'pop'}
                    ],
                    value='gdpPercap'
                ),
                html.Br(),

                # ось Y для пузырьковой диаграммы
                dcc.Dropdown(
                    id='yaxis-dropdown-bubble',
                    options=[
                        {'label': 'Продолжительность жизни', 'value': 'lifeExp'},
                        {'label': 'ВВП на душу населения', 'value': 'gdpPercap'},
                        {'label': 'Население', 'value': 'pop'}
                    ],
                    value='lifeExp'
                ),
                html.Br(),

                # радиус пузырьков
                dcc.Dropdown(
                    id='size-dropdown-bubble',
                    options=[
                        {'label': 'Население', 'value': 'pop'},
                        {'label': 'ВВП на душу населения', 'value': 'gdpPercap'},
                        {'label': 'Продолжительность жизни', 'value': 'lifeExp'}
                    ],
                    value='pop'
                ),
                html.Br(),
                html.Small("Наведите на линейный график - "
                           "три правых диаграммы переключатся на этот год.")
            ], style={'padding': '20px'}),

            # линейный график
            dcc.Graph(id='line-chart', style=style_graph),

            # пузырьковая диаграмма
            dcc.Graph(id='bubble-chart', figure=fig_bubble_init, style=style_graph),

            # топ 15
            dcc.Graph(id='top15-chart', figure=fig_top15_init, style=style_graph),

            # круговая диаграмма
            dcc.Graph(id='pie-chart', figure=fig_pie_init, style=style_graph),
        ]
    )
])

# Линейный график
@app.callback(
    Output('line-chart', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('yaxis-dropdown-line', 'value')]
)
def update_line_chart(selected_countries, selected_yaxis):

    if not selected_countries:
        return px.line(title="Выберите хотя бы одну страну")

    dff = df[df['country'].isin(selected_countries)]

    # Делаем отедльную линию на каждую страну
    fig = px.line(
        dff, x='year', y=selected_yaxis, color='country',
        title=f'Динамика «{selected_yaxis}» по годам',
        labels={'year': 'Год', selected_yaxis: selected_yaxis}
    )
    return fig

# Пузырьковая диаграмма
@app.callback(
    Output('bubble-chart', 'figure'),
    [Input('line-chart', 'hoverData'),
     Input('xaxis-dropdown-bubble', 'value'),
     Input('yaxis-dropdown-bubble', 'value'),
     Input('size-dropdown-bubble', 'value')]
)
def update_bubble_chart(hover_data, x_axis, y_axis, size_axis):
    # Год: если было наведение - берём оттуда, иначе 2007
    if hover_data and 'points' in hover_data and len(hover_data['points']) > 0:
        year = int(hover_data['points'][0]['x'])
    else:
        year = 2007

    dff = df[df.year == year]

    # нужна только для ВВП (иначе точки слипаются у нуля)
    use_log_x = (x_axis == 'gdpPercap')
    use_log_y = (y_axis == 'gdpPercap')

    fig = px.scatter(
        dff, x=x_axis, y=y_axis, size=size_axis,
        color='continent', hover_name='country',
        log_x=use_log_x, log_y=use_log_y,
        size_max=60,
        title=f'Пузырьковая диаграмма за {year} год'
    )
    return fig

# топ-15 и круговая диаграмма
@app.callback(
    [Output('top15-chart', 'figure'),
     Output('pie-chart', 'figure')],
    [Input('line-chart', 'hoverData')],
    prevent_initial_call=True
)
def update_top15_pie(hover_data):
    # Нет валидного наведения - ничего не меняем
    if not hover_data or 'points' not in hover_data or len(hover_data['points']) == 0:
        return dash.no_update, dash.no_update

    year = int(hover_data['points'][0]['x'])
    dff = df[df.year == year]

    # топ-15
    top15 = dff.nlargest(15, 'pop')
    bar_fig = px.bar(
        top15, x='pop', y='country', orientation='h',
        title=f'Топ-15 стран по населению ({year})',
        labels={'pop': 'Население', 'country': ''}
    )
    bar_fig.update_layout(yaxis={'categoryorder': 'total ascending'})

    # Круговая диаграмма
    pop_by_cont = dff.groupby('continent', as_index=False)['pop'].sum()
    pie_fig = px.pie(
        pop_by_cont, values='pop', names='continent',
        title=f'Доля населения по континентам ({year})'
    )

    return bar_fig, pie_fig

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))
    app.run(host='0.0.0.0', port=port, debug=False)