from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Label
from textual.widgets import Static

from lolcatt.utils.utils import marquee


class LolCattPlaybackInfo(Static):
    label_str = reactive('')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = Label('', id='title')
        self._marquee_gen = None

    def _get_playback_info(self) -> str:
        state = self.app.caster.get_cast_state()
        playing = state.cast_info.get('title')
        display_name = state.info.get('display_name')

        if playing is not None:
            return f'Playing: "{playing}"'
        elif display_name is not None and display_name != 'Backdrop':
            return f'Displaying: "{display_name}"'
        elif state.is_loading:
            return 'Loading...'
        elif state.loading_failed:
            self.app.notify('Loading failed.', severity='warning')
            return 'Nothing is playing.'
        else:
            return 'Nothing is playing.'

    def _update_label(self):
        self.label_str = self._get_playback_info() + ' '
        self.label.update(next(self._marquee_gen))

    def watch_label_str(self, value):
        self._marquee_gen = marquee(value, self.size.width, 2)

    def on_resize(self, value):
        self._marquee_gen = marquee(self.label_str, self.size.width, 2)

    def compose(self):
        yield Container(self.label, id='playback_info')

    def on_mount(self):
        self.set_interval(
            interval=self.app.caster.get_update_interval(), callback=self._update_label
        )
