import pandas as pd
import requests
import streamlit as st
import folium
from folium import Tooltip
from datetime import datetime, timedelta
import locale
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
from datetime import datetime
from monitor_folium import mt_folium
from streamlit_modal import Modal
import streamlit.components.v1 as components

# A configuração da página e o CSS devem ser os primeiros comandos executados no script.
st.set_page_config(page_icon="⛅", layout="wide", page_title="Monitoramento", initial_sidebar_state="expanded")


# Código para carregar o CSS diretamente no Streamlit
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Carregando o arquivo CSS no Streamlit
local_css("style.css")

def get_id_weather(weather_condition):
    def get_legend_html(ranges_colors, type, medida):
        legend_items = []
        for i, (range_value, color) in enumerate(ranges_colors):
            legend_items.append(f'<div style="display: flex; align-items: center; padding: 1px 0;"><div style="width: 20px; height: 20px; background-color: {color};"></div><span style="color: #000;margin-left: 5px">{f">= {range_value[0]}{medida}" if i > 0 else ""} {f"< {range_value[1]}{medida}" if i < len(ranges_colors) - 1  else ""}</span></div>')
        no_data = '<div style="display: flex; align-items: center; padding: 1px 0;"><div style="width: 20px; height: 20px; background-color: gray;"></div><span style="color: #000;margin-left: 5px">Sem dados</span></div>'
        return '<div style="display: flex; flex-direction: column; padding: 0 10px;">'+ f'<div style="color: #2C8153; text-align: center; font-weight: bold; font-size: 16px">{type}</div>' + ''.join(legend_items)+ no_data+ '</div>'

    def get_color(value, ranges_colors):
        if value is None:
            return "gray"
        for range_value, color in ranges_colors:
            if range_value[0] <= value < range_value[1]:
                return color
        return "darkviolet"

    def get_color_rain(rainfall_value):
        ranges_colors = [
            ((-float("inf"), 20), "lightblue"),
            ((20, 25), "lightgreen"),
            ((25, 50), "green"),
            ((50, 75), "orange"),
            ((75, 100), "red"),
            ((100, float("inf")), "darkviolet")
        ]
        return get_color(rainfall_value, ranges_colors), get_legend_html(ranges_colors, "Chuva", "mm")

    def get_color_tempeture(temperature_value):
        ranges_colors = [
            ((-float("inf"), 10), "#0101EE"),
            ((10, 15), "#1998FD"),
            ((15, 20), "#8CCBE8"),
            ((20, 25), "#E7DF3B"),
            ((25, 30), "#ED3A3B"),
            ((30, float("inf")), "#A6272E")
        ]
        return get_color(temperature_value, ranges_colors), get_legend_html(ranges_colors, "Temperatura", "°")
    
    def get_color_wind(wind_value):
        return "gray", """
                <div style="display: flex; flex-direction: column; padding: 0 10px;">
                    <div style="color: #2C8153; text-align: center; font-weight: bold; font-size: 16px">Vento</div>
                    <div style="display: flex; align-items: center; padding: 1px 0;">
                        <div style="width: 20px; height: 20px; background-color: gray;"></div>
                            <span style="color: #000;margin-left: 5px">Vento padrão</span>
                    </div>
                </div>
    """
 

    def get_color_humidity(humidity_value):
        ranges_colors = [
            ((-float("inf"), 20), "#FC0000"),
            ((20, 30), "#FC7715"),
            ((30, 40), "#FBC92A"),
            ((40, 50), "#2CDD5D"),
            ((50, 60), "#2CDDB2"),
            ((60, 70), "#2CDDB2"),
            ((70, 75), "#28C6C5"),
            ((75, 80), "#32FFFE"),
            ((80, 85), "#2BDAFD"),
            ((85, 90), "#1B91FC"),
            ((90, 95), "#1700F9"),
            ((95, float("inf")), "#1900B0")
        ]
        return get_color(humidity_value, ranges_colors), get_legend_html(ranges_colors, "Umidade", "%")

    
    if weather_condition == "CHUVA":
        return 15, get_color_rain
    elif weather_condition == "TEMPERATURA":
        return 2, get_color_tempeture
    elif weather_condition == "VENTO":
        return 14, get_color_wind
    elif weather_condition == "UMIDADE":
        return 6, get_color_humidity
    else:
        return None

def conseguir_dados_legendas(weather_condition, stations, start_date, end_date,start_time, end_time):
    id_weather_condition, get_color  = get_id_weather(weather_condition)
    start_datetime = datetime.combine(start_date, start_time)

    max_duration = timedelta(hours=96)
    end_datetime = min(start_datetime + max_duration, datetime.combine(end_date, end_time))

    # Formata os datetimes combinados no formato da API
    start_datetime_str = start_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    end_datetime_str = end_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    # Constrói a URL da API com os datetimes formatados
    if end_datetime - start_datetime <= max_duration:
        api_url = f'https://satdes-backend.incaper.es.gov.br/api/v1/records/monitoring/{id_weather_condition}/{start_datetime_str}/{end_datetime_str}'
    else:
        api_url = f'https://satdes-backend.incaper.es.gov.br/api/v1/records/monitoring/{id_weather_condition}/{start_datetime_str}'
    if id_weather_condition is not None:
        response = requests.get(api_url, verify=True)
        if response.status_code == 200:
            data = response.json()['data']
            station_objects = []
            for station_id, station_data in data.items():
                instant_values = [float(entry['instant']) for entry in station_data]
                avg_instant = sum(instant_values)
                if id_weather_condition != 15:
                    avg_instant = avg_instant / len(instant_values)
                station_row = stations[stations['id'] == int(station_id)]
                if not station_row.empty:
                    country_name = station_row.iloc[0]['name_county']
                    color, legend = get_color(avg_instant)
                    station_objects.append({'country_name': country_name, 'color': color, 'avg_instant': avg_instant, 'last_instant': instant_values[0], 'last_moment': station_data[0]['date_hour']})
                else:
                    print(f"Estação com ID {station_id} não encontrada.")
            if len(station_objects) == 0:
                return None, None
            return station_objects, legend

    return None


# Carrega os dados das estações
def conseguir_dados():
    try:
        api_url = 'https://satdes-backend.incaper.es.gov.br/api/v1/stations'
        response = requests.get(api_url, verify=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        if response.status_code == 200:
            stations = response.json()['data']
            stations_data = pd.DataFrame(stations)
            stations_data['latitude'] = stations_data['latitude'].astype(float)
            stations_data['longitude'] = stations_data['longitude'].astype(float)
            stations_data['code'] = stations_data['code'].astype(str)
            return stations_data
        else:
            st.error("Failed to retrieve station data.")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")

def ultimo_marcado_clicado(lat: float, lon: float, localizacao_estacoes) -> str:
    try:
        ultima_estacao = localizacao_estacoes[
            (localizacao_estacoes['latitude'] >= lat - 0.001)
            & (localizacao_estacoes['latitude'] <= lat + 0.001)
            & (localizacao_estacoes['longitude'] >= lon - 0.001)
            & (localizacao_estacoes['longitude'] <= lon + 0.001)
        ].iloc[0]
        st.session_state['ultimo_marcado_marcado'] = ultima_estacao['id']
        return ultima_estacao["id"]
    
    except IndexError:
        return None
    
def ultima_legenda_clicado(estacao_legenda, localizacao_estacoes) -> str:
    try:
        ultima_estacao = localizacao_estacoes[localizacao_estacoes['name_county']==estacao_legenda ].iloc[0]
        st.session_state['ultimo_marcado_marcado'] = ultima_estacao['id']
        return ultima_estacao["id"]
    
    except IndexError:
        return None
    
# Configura a barra lateral
st.sidebar.image("logo.png", use_column_width=True)

def gerar_mapa(stations, selected_institute, start_date, end_date,start_time, end_time, weather_condition, milimetro):
    result = stations  # Retorna todas as linhas se selected_institute for None
    
    if selected_institute is not None:
        result = stations.loc[stations['name_institute'] == selected_institute]
        

    dados_legendas = conseguir_dados_legendas(weather_condition, result,start_date, end_date,start_time, end_time)
    
    
    def find_object_by_country_name(station_objects, target_country_name):
        if not station_objects:
            return None
        dados, _ = station_objects
        if dados is None:
            return None
        for station_object in dados:
            if station_object['country_name'] == target_country_name:
                return station_object
        return None  # Object not found
    def add_marker(station, fg):
        location = [float(station['latitude']), float(station['longitude'])]
        formatted_value = "--"
        color = 'gray'
        dados_filtrados = find_object_by_country_name(dados_legendas, station['name_county'])
        last_moment = "Sem dados de hora"
        if dados_filtrados:
            rainfall_value = dados_filtrados.get('last_instant')  # Obter o valor de chuva média instantânea do dado
            last_moment = dados_filtrados.get('last_moment')  # Obter o valor de chuva média instantânea do dado
            
            if isinstance(last_moment, str):
                last_moment = datetime.strptime(last_moment, "%Y-%m-%dT%H:%M:%S.%fZ") - timedelta(hours=3)
                last_moment = last_moment.strftime("%H:%M %d/%m/%Y")
            if milimetro is not None and rainfall_value < milimetro:
                return
            formatted_value = f"{rainfall_value:.1f}" if rainfall_value is not None else "--"
            color = dados_filtrados.get('color', 'gray')  # Obter a cor do marcador do dado, padrão para 'gray' se não houver cor definida
        elif milimetro is not None and milimetro != 0:
            return
        icon_html = f'''
            <div style="
                width: 60px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
                background-color: {color};
                color: white;
                font-size: 12pt;
                font-weight: bold;
                border-radius: 3px;
            ">
                {formatted_value}
            </div>
        '''
        tooltip_html =f"""
            <ul>
                <li>{station['name_county']}</li>
                <li>{last_moment}</li>
            </ul>
        """
        icon = folium.DivIcon(html=icon_html)
        marker = folium.Marker(location, icon=icon, tooltip=Tooltip(tooltip_html))
        fg.add_child(marker)

    m = folium.Map(location=[-20.3155, -40.3128], zoom_start=8)
    fg = folium.FeatureGroup(name="Markers") 
    for _, station in stations.iterrows():
        if (station['latitude'] == None and station['longitude']== None) :
            pass
        if selected_institute == None or station["name_institute"] in selected_institute:
            add_marker(station, fg)
    dados = None
    legend = None
    if(dados_legendas):
        dados, legend = dados_legendas
        if milimetro is not None and dados is not None:
            dados = [station for station in dados if station['avg_instant'] >= milimetro]

    st_data = mt_folium(m, width=1560, height=890, feature_group_to_add=fg, legends=dados, legend=legend)

    return st_data

def gerar_urls_graficos(data_inicio, data_final, selected_station):
    urls= f"https://satdes-produtos.incaper.es.gov.br/api/v1/mon/grafico?datai={data_inicio}&dataf={data_final}&estacao={selected_station}"
    return urls


def generate_iframe_html(url):
    return components.iframe(url, height=1200, width=1016)

def gerar_tabelas( start_time, end_time, data_inicio, data_final, selected_station):
    urls = f"https://satdes-produtos.incaper.es.gov.br/api/v1/mon/dados?datai={data_inicio}&dataf={data_final}&estacao={selected_station}"

    dados_por_data = {}
    try:
        response = requests.get(urls,verify=True)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                date = item.get('date')
                hour = item.get('hour')
                datetime_str = f"{date} {hour}"
                datetime_obj = pd.to_datetime(datetime_str, format='%Y-%m-%d %H:%M:%S')
                if datetime.combine(data_inicio, start_time) <= datetime_obj <= datetime.combine(data_final, end_time):
                    for item_key, item_value in item.items():
                        if item_key in ['date', 'hour']:
                            continue
                        if datetime_str not in dados_por_data:
                            dados_por_data[datetime_str] = {}
                        dados_por_data[datetime_str][f'{item_key}'] = item_value
        df_novo = pd.DataFrame.from_dict(dados_por_data, orient='index')
        if not df_novo.empty:
            # df_novo.index = pd.to_datetime(df_novo.index)
            # df_novo.index = df_novo.index.strftime("%d/%m/%Y ")
            # df_novo = df_novo.sort_index()
            # df_estilizado = df_novo.style.highlight_max(axis=0, color='red').highlight_min(axis=0, color='blue')
            df_novo['tem_max'] = pd.to_numeric(df_novo['tem_max'], errors='coerce')
            df_novo['sum_pre'] = pd.to_numeric(df_novo['sum_pre'], errors='coerce')
            df_novo['ven_dir'] = pd.to_numeric(df_novo['ven_dir'], errors='coerce')
            df_novo['avg_ven'] = pd.to_numeric(df_novo['avg_ven'], errors='coerce')
            st.write(df_novo)
            df_novo['Medida'] = 'Medida'  # Criar uma coluna constante
            resultados = df_novo.groupby('Medida').agg({'tem_max': 'mean',
                                       'sum_pre': 'sum',
                                       'ven_dir': 'mean',
                                       'avg_ven': 'mean'})
            resultados = resultados.reset_index()  # redefinir o índice para que 'Medida' se torne uma coluna
            df_vertical = resultados.melt(id_vars='Medida', var_name='Variavel', value_name='Valor')
            
            df_res = df_vertical[['Variavel', 'Valor']]
            st.write(df_res)
        else:
            st.write(df_novo)
            
    except ValueError:
        st.error("----")

def gerar_graficos(urls_graficos):
    st.title('Gráficos Climáticos')
    generate_iframe_html(urls_graficos)

def criar_modal():
    modal = Modal(
        "Dados Meteorologicos", 
    key="dados-meteorologicos",
    
    padding=20,    
    max_width=1024 
    )
    return modal

def selecionar_instituto(stations_data):
    institutes = stations_data['name_institute'].unique()
    weather_condition = st.session_state["weather_condition"]
    
    if weather_condition == "TEMPERATURA":
        institutes = institutes[institutes != "ANA"]
    
    institute_stations = {institute: [] for institute in institutes}

    for _, station in stations_data.iterrows():
        name_institute = station['name_institute']
        if name_institute in institute_stations:
            institute_stations[name_institute].append(station['code'])

    selected_institute = st.sidebar.selectbox('Entidades', ['Escolha uma Entidade'] + list(institutes))
    
    if selected_institute == 'Escolha uma Entidade':
        return None, institute_stations
    
    return selected_institute,institute_stations

def selecionar_estacao(institute_stations,selected_institute,stations_data):
    if selected_institute is not None:
        selected_stations = institute_stations[selected_institute]
        id_station_codes = {station['id']: station['code'] for index, station in stations_data.iterrows() if station['code'] in selected_stations}
        st.session_state["selected_state"] = st.sidebar.selectbox('Escolha a Estação', id_station_codes.keys(), format_func=lambda x:id_station_codes[x], index=0)

def aplicar_filtro(modal,data_inicio, data_final, start_time, end_time):
    mostrar_modal(st.session_state["selected_state"],modal,data_inicio, data_final , start_time, end_time)

def mostrar_modal(estacaoId, modal,data_inicio, data_final, start_time, end_time):
    st.session_state["ultimo_marcado_marcado"] = estacaoId
    if not modal.is_open():
        modal.open()
    if modal.is_open():
        with modal.container():
            tab2, tab1 = st.tabs(["Gráficos", "Tabelas"])
            with tab1:
                with st.spinner("Carregando gráficos..."):  # Adiciona o spinner enquanto carrega a tabela
                    gerar_tabelas( start_time, end_time,data_inicio, data_final, estacaoId)

            with tab2:
                with st.spinner("Carregando tabela..."):  # Adiciona o spinner enquanto carrega os gráficos
                    urls = gerar_urls_graficos(data_inicio, data_final, estacaoId)
                    gerar_graficos(urls)
                    
def criar_condicoes(instituto_selecionado):
    if instituto_selecionado == "ANA":
        return st.sidebar.selectbox("Condições climáticas", ["CHUVA"])
    return st.sidebar.selectbox("Condições climáticas", ["CHUVA","TEMPERATURA","VENTO", "UMIDADE"])
    
def main():
    if "last_object_clicked" not in st.session_state:
        st.session_state["last_object_clicked"] = None
    if "last_legend_clicked" not in st.session_state:
        st.session_state["last_legend_clicked"] = None
    if "ultimo_marcado_marcado" not in st.session_state:
        st.session_state["ultimo_marcado_marcado"] = None
    if 'selected_state' not in st.session_state:
        st.session_state["selected_state"] = None   
    if 'weather_condition' not in st.session_state:
        st.session_state["weather_condition"] = None   
        
    data_estacoes = conseguir_dados()
    
    instituto_selecionado, todos_institutos = selecionar_instituto(data_estacoes)
    selecionar_estacao(todos_institutos, instituto_selecionado, data_estacoes)
    modal = criar_modal()
    weather_condition = criar_condicoes(instituto_selecionado)
    if weather_condition != st.session_state["weather_condition"]:
        st.session_state["weather_condition"]= weather_condition
        st.rerun()
    
    milimetro = None 
    if weather_condition == "CHUVA":
        milimetro = st.sidebar.selectbox("Quantidade em mm", [0, 1, 5, 10, 30, 50, 70, 100, 120], format_func=lambda x: f">= {x} mm")
    
    # Aqui você subtrai 4 dias da data atual para definir como valor padrão
    default_start_date = datetime.now() - timedelta(days=4)
    
    # Definindo o valor padrão para o date_input
    start_date = st.sidebar.date_input("Data de Início", value=default_start_date, format='DD/MM/YYYY')
    end_date = st.sidebar.date_input("Data Final", value=datetime.now(), format='DD/MM/YYYY')
    
    now = datetime.now()

# Arredonda para baixo a hora atual para o intervalo de 15 minutos mais próximo
    minute_rounded = 15 * (now.minute // 15)
# Define o horário final padrão para a hora atual arredondada para o intervalo de 15 minutos mais próximo
    default_end_time = now.replace(minute=minute_rounded, second=0, microsecond=0).time()

# Define o horário de início padrão para uma hora antes do horário final arredondado
    default_start_time = (now.replace(minute=minute_rounded, second=0, microsecond=0) - timedelta(hours=1)).time()

# Utiliza os valores padrão no seletor de horário
    start_time = st.sidebar.time_input("Hora de Início", value=default_start_time)
    end_time = st.sidebar.time_input("Hora Final", value=default_end_time)
    out = gerar_mapa(data_estacoes, instituto_selecionado, start_date, end_date,start_time, end_time, weather_condition, milimetro)
    st.sidebar.write(out)
    if ((st.session_state["last_object_clicked"] != out["last_object_clicked"] and out["last_object_clicked"] ) or (out["last_object_clicked"] and st.session_state["last_object_clicked"] == None) ):
        id = ultimo_marcado_clicado(*out["last_object_clicked"].values(), data_estacoes)
        if id:
            mostrar_modal(id,modal, start_date, end_date, start_time, end_time)    
            pass
        st.session_state["last_object_clicked"] = out["last_object_clicked"]
    
    if ((st.session_state["last_legend_clicked"] != out["last_legend_clicked"] and out["last_legend_clicked"] ) or (out["last_legend_clicked"] and st.session_state["last_legend_clicked"] == None) ):
        id = ultima_legenda_clicado(out["last_legend_clicked"], data_estacoes)
        if id:
            mostrar_modal(id,modal, start_date, end_date, start_time, end_time)    
            pass
        st.session_state["last_legend_clicked"] = out["last_legend_clicked"]
    
    if st.sidebar.button('Buscar dados' if st.session_state['ultimo_marcado_marcado'] == st.session_state['selected_state'] else "Buscar estação"):
        aplicar_filtro(modal, start_date, end_date,  start_time, end_time)

if __name__ == "__main__":
    main()