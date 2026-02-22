import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib, Gdk, Gio
import gettext, locale, os, json, time, random
__version__ = "0.1.0"

APP_ID = "se.danielnylander.kladvaljaren"
LOCALE_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'share', 'locale')
if not os.path.isdir(LOCALE_DIR): LOCALE_DIR = '/usr/share/locale'
try:
    locale.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.bindtextdomain(APP_ID, LOCALE_DIR)
    gettext.textdomain(APP_ID)
except Exception: pass
_ = gettext.gettext
def N_(s): return s

WEATHER = [
    {'name': N_('Sunny'), 'icon': '☀️', 'clothes': [N_('T-shirt'), N_('Shorts'), N_('Sandals'), N_('Sunhat')]},
    {'name': N_('Rainy'), 'icon': '🌧️', 'clothes': [N_('Rain jacket'), N_('Rain pants'), N_('Rubber boots'), N_('Umbrella')]},
    {'name': N_('Cold'), 'icon': '❄️', 'clothes': [N_('Winter jacket'), N_('Warm pants'), N_('Boots'), N_('Hat'), N_('Gloves'), N_('Scarf')]},
    {'name': N_('Windy'), 'icon': '💨', 'clothes': [N_('Windbreaker'), N_('Long pants'), N_('Sneakers')]},
    {'name': N_('Cloudy'), 'icon': '☁️', 'clothes': [N_('Sweater'), N_('Jeans'), N_('Sneakers')]},
]

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.set_title(_('Clothes Chooser'))
        self.set_default_size(450, 500)

        header = Adw.HeaderBar()
        menu_btn = Gtk.MenuButton(icon_name='open-menu-symbolic')
        menu = Gio.Menu()
        menu.append(_('About'), 'app.about')
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)

        main = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        main.append(header)

        q = Gtk.Label(label=_('What is the weather like?'))
        q.add_css_class('title-2')
        q.set_margin_top(16)
        main.append(q)

        weather_box = Gtk.FlowBox()
        weather_box.set_max_children_per_line(5)
        weather_box.set_selection_mode(Gtk.SelectionMode.NONE)
        weather_box.set_halign(Gtk.Align.CENTER)
        weather_box.set_margin_start(16)
        weather_box.set_margin_end(16)
        for i, w in enumerate(WEATHER):
            btn = Gtk.Button()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            box.set_margin_top(8)
            box.set_margin_bottom(8)
            box.set_margin_start(8)
            box.set_margin_end(8)
            icon = Gtk.Label(label=w['icon'])
            icon.add_css_class('title-1')
            box.append(icon)
            name = Gtk.Label(label=_(w['name']))
            name.add_css_class('caption')
            box.append(name)
            btn.set_child(box)
            btn.add_css_class('card')
            btn.connect('clicked', self._show_clothes, i)
            weather_box.insert(btn, -1)
        main.append(weather_box)

        self._result_title = Gtk.Label()
        self._result_title.add_css_class('title-3')
        self._result_title.set_margin_top(16)
        main.append(self._result_title)

        self._clothes_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self._clothes_box.set_margin_start(32)
        self._clothes_box.set_margin_end(32)
        main.append(self._clothes_box)

        self.set_content(main)

    def _show_clothes(self, btn, index):
        w = WEATHER[index]
        self._result_title.set_text(f"{w['icon']} {_(w['name'])} — {_('You should wear:')}")
        while child := self._clothes_box.get_first_child():
            self._clothes_box.remove(child)
        for c in w['clothes']:
            row = Gtk.Label(label=f'👕 {_(c)}', xalign=0)
            row.add_css_class('title-4')
            self._clothes_box.append(row)

class App(Adw.Application):
    def __init__(self):
        super().__init__(application_id='se.danielnylander.kladvaljaren')
        self.connect('activate', lambda a: MainWindow(application=a).present())
        about = Gio.SimpleAction.new('about', None)
        about.connect('activate', lambda a,p: Adw.AboutDialog(application_name=_('Clothes Chooser'),
            application_icon=APP_ID, version=__version__, developer_name='Daniel Nylander',
            website='https://github.com/yeager/kladvaljaren', license_type=Gtk.License.GPL_3_0,
            comments=_('Choose clothes by weather')).present(self.get_active_window()))
        self.add_action(about)

def main(): App().run()
if __name__ == '__main__': main()

