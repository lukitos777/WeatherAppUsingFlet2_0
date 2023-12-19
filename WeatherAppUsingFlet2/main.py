import flet
import requests


def main(page: flet.page) -> None:
    page.vertical_alignment = flet.alignment.center
    page.theme_mode = 'dark'
    city_enter = flet.TextField(autofocus=True, width=300,
                                border_color=flet.colors.BLACK,
                                color=flet.colors.WHITE)

    txt_1, txt_2, txt_3, txt_4 = flet.Text(value='', color=flet.colors.WHITE), \
        flet.Text(value='', color=flet.colors.WHITE), \
        flet.Text(value='', color=flet.colors.WHITE), \
        flet.Text(value='', color=flet.colors.WHITE)

    def change_theme(e):
        page.theme_mode = 'light' if page.theme_mode == 'dark' else 'dark'
        txt_1.color = txt_2.color = txt_3.color = txt_4.color = \
            flet.colors.BLACK \
                if page.theme_mode == 'light' else flet.colors.WHITE
        page.update()

    def get_data(e) -> None:
        nonlocal txt_1, txt_2, txt_3, txt_4
        city = city_enter.value
        url = 'https://api.openweathermap.org/data/2.5/weather?q=' \
              + city + \
              '&units=metric&lang=ru&appid=79d1ca96933b0328e1c7e3e7a26cb347'

        weather_data = requests.get(url).json()

        try:
            temperature = round(weather_data['main']['temp'])
        except KeyError:
            return

        temperature_feels = round(weather_data['main']['feels_like'])
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        txt_1.value = f'Temperature in {city} is {str(temperature)} C'
        txt_2.value = f'Temperature feels like {str(temperature_feels)} C'
        txt_3.value = f'Humidity is {str(humidity)}'
        txt_4.value = f'Wind speed is {str(wind_speed)} m/sec'

        city_enter.value = ''
        page.update()

    run_button = flet.ElevatedButton('get data', on_click=get_data)

    changer = flet.IconButton(icon=flet.icons.SUNNY, on_click=change_theme)

    row, column = flet.Row(controls=[city_enter, run_button, changer],
                           alignment=flet.alignment.center), \
        flet.Column(controls=[txt_1, txt_2, txt_3, txt_4],
                    alignment=flet.alignment.center)

    page.add(row)
    page.add(column)


if __name__ == '__main__':
    flet.app(target=main, name='Weather app', view=flet.AppView.FLET_APP)
