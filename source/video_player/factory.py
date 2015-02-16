
from player_list.models import Video, Jam, Bout

class VideoPlayerFactory():
    '''
    Populate the database with the bare minimum necessary for a video_player page to properly render
    '''
    def __init__(self, save=False):
        self.bout = Bout()
        self.bout.save()

        self.video = Video()
        self.video.save()

        self.jam = Jam(bout=self.bout)
        self.jam.save()
