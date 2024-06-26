import os.path
import subprocess
from urllib.parse import urlparse
from babel.support import Translations
from pytube import YouTube
import customtkinter as ctk

from config import Config


config = Config()

LOCALE_PATH = 'translations'
translations = Translations.load(LOCALE_PATH, [config.LANGUAGE])
_ = translations.gettext
# https://youtu.be/z0dxfnr-HjY?si=lR-Xcd2t3-6K5I2n


class NavFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(index=0, weight=30)
        self.columnconfigure(index=1, weight=1)
        self.columnconfigure(index=2, weight=2)

        lang_var = ctk.StringVar()
        self.language_menu = ctk.CTkOptionMenu(self, values=["PL", "EN"], variable=lang_var, command=self.change_language,
                                               corner_radius=0, width=20, button_color=("grey", "black"),
                                               fg_color=("grey", "black"), button_hover_color=("grey", "black"))
        self.language_menu.set(_("Language"))
        self.language_menu.grid(row=0, column=1, padx=0, pady=0, sticky=ctk.EW)

        self.appearance_mode_menu = ctk.CTkOptionMenu(self, values=["Light", "Dark", "System"],
                                                      command=self.change_appearance_mode, corner_radius=0, width=30,
                                                      button_color=("grey", "black"), fg_color=("grey", "black"),
                                                      button_hover_color=("grey", "black"))
        self.appearance_mode_menu.set(_("Theme"))
        self.appearance_mode_menu.grid(row=0, column=2, padx=0, pady=0, sticky=ctk.EW)

    def change_language(self, lang_var):
        config.LANGUAGE = lang_var
        global translations
        global _
        translations = Translations.load(LOCALE_PATH, [lang_var])
        _ = translations.gettext
        self.master.reload_frames()

    @staticmethod
    def change_appearance_mode(new_appearance_mode):
        ctk.set_appearance_mode(new_appearance_mode)


class UrlFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0)

        self.url_label = ctk.CTkLabel(self, text=_("Link to video"), fg_color="transparent", height=20)
        self.url_label.grid(row=0, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.url_text_box = ctk.CTkTextbox(self, height=20)
        self.url_text_box.grid(row=0, column=1, padx=10, pady=10, sticky=ctk.NSEW)

        self.get_video_info_button = ctk.CTkButton(self, command=lambda: self.generate_frame_video(),
                                                   text=_("Get video info"), height=20)
        self.get_video_info_button.grid(row=0, column=2, padx=10, pady=10, sticky=ctk.NSEW)

    def generate_frame_video(self):
        url = self.url_text_box.get("0.0", "end")
        try:
            result = urlparse(url)
            self.master.video = VideoFrame(self.master, url)
            self.master.video.grid(row=2, column=0, padx=10, pady=10, sticky=ctk.NSEW)
        except ValueError:
            return False


def download_video(yt, extension, file_type, abr, resolution):
    if file_type == "audio":
        stream = yt.streams.filter(mime_type=extension, abr=abr).first()
    else:
        stream = yt.streams.filter(mime_type=extension, resolution=resolution).first()
    extension_name = extension.split("/")[1]
    stream.download(filename=f"{yt.title} - {file_type}.{extension_name}")
    current_path = os.path.curdir
    subprocess.Popen(f'explorer /select, "{current_path}"')


class VideoFrame(ctk.CTkFrame):

    def __init__(self, master, url):
        super().__init__(master)

        yt = YouTube(url)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)

        self.title_label = ctk.CTkLabel(self, text=yt.title, fg_color="transparent", height=20, justify=ctk.CENTER,
                                        font=("Arial", 18))
        self.title_label.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky=ctk.NSEW)

        video_description = yt.description
        video_author = yt.author
        video_keywords = yt.keywords
        video_views = yt.views
        video_vid_info = yt.vid_info
        video_rating = yt.rating
        video_publish_date = yt.publish_date
        video_length = yt.length

        self.author_label = ctk.CTkLabel(self, text=_("Author"), fg_color="transparent", height=20,
                                         justify=ctk.RIGHT)
        self.author_label.grid(row=2, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.author_label_value = ctk.CTkLabel(self, text=f"{video_author}", fg_color="transparent", height=20,
                                               justify=ctk.RIGHT)
        self.author_label_value.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.publish_date_label = ctk.CTkLabel(self, text=_("Publish date"), fg_color="transparent", height=20)
        self.publish_date_label.grid(row=3, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.publish_date_label_value = ctk.CTkLabel(self, text=f"{video_publish_date}", fg_color="transparent", height=20)
        self.publish_date_label_value.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.length_label = ctk.CTkLabel(self, text=_("Length"), fg_color="transparent", height=20)
        self.length_label.grid(row=4, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.length_label_value = ctk.CTkLabel(self, text=f"{video_length}s", fg_color="transparent", height=20)
        self.length_label_value.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.description_label = ctk.CTkLabel(self, text=_("Description"), fg_color="transparent", height=20)
        self.description_label.grid(row=5, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.description_label_value = ctk.CTkLabel(self, text=f"{video_description}", fg_color="transparent", height=20)
        self.description_label_value.grid(row=5, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.views_label = ctk.CTkLabel(self, text=_("Views"), fg_color="transparent", height=20)
        self.views_label.grid(row=6, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.views_label_value = ctk.CTkLabel(self, text=f"{video_views}", fg_color="transparent", height=20)
        self.views_label_value.grid(row=6, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.vid_info_label = ctk.CTkLabel(self, text=_("Rating"), fg_color="transparent", height=20)
        self.vid_info_label.grid(row=7, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.vid_info_label_value = ctk.CTkLabel(self, text=f"{video_rating}", fg_color="transparent", height=20)
        self.vid_info_label_value.grid(row=7, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.keywords_label = ctk.CTkLabel(self, text=_("Keywords"), fg_color="transparent", height=20)
        self.keywords_label.grid(row=8, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        self.keywords_label_value = ctk.CTkLabel(self, text=f"{video_keywords}", fg_color="transparent", height=20)
        self.keywords_label_value.grid(row=8, column=1, columnspan=2, padx=10, pady=10, sticky=ctk.NSEW)

        type_var = ctk.StringVar()
        self.type_label = ctk.CTkLabel(self, text=_("Type"), fg_color="transparent", height=20)
        self.type_label.grid(row=10, column=0, padx=10, pady=(50, 10), sticky=ctk.NSEW)

        self.type_radio_button_audio = ctk.CTkRadioButton(self, variable=type_var, value="audio", text=_("audio"),
                                                          command=lambda: switch_options("audio"))
        self.type_radio_button_audio.grid(row=10, column=1, padx=10, pady=(50, 10), sticky=ctk.NSEW)

        self.type_radio_button_video = ctk.CTkRadioButton(self, variable=type_var, value="video", text=_("video"),
                                                          command=lambda: switch_options("video"))
        self.type_radio_button_video.grid(row=10, column=2, padx=10, pady=(50, 10), sticky=ctk.NSEW)

        resolution_list = []
        abr_list = []

        for stream in yt.streams:
            if stream.type == "video":
                resolution_list.append(stream.resolution)
            else:
                abr_list.append(stream.abr)

        resolution_list = list(dict.fromkeys(resolution_list))
        abr_list = list(dict.fromkeys(abr_list))

        self.abr_label = ctk.CTkLabel(self, text=_("ABR"), fg_color="transparent", height=20)
        self.abr_label.grid(row=15, column=0, padx=10, pady=(40, 10), sticky=ctk.NSEW)

        self.resolution_label = ctk.CTkLabel(self, text=_("Resolution"), fg_color="transparent", height=20)
        self.resolution_label.grid(row=15, column=1, padx=10, pady=(50, 10), sticky=ctk.NSEW)

        self.extension_label = ctk.CTkLabel(self, text=_("Extension"), fg_color="transparent", height=20)
        self.extension_label.grid(row=15, column=2, padx=10, pady=(50, 10), sticky=ctk.NSEW)

        abr_var = ctk.StringVar()
        self.abr_options = ctk.CTkOptionMenu(self, values=abr_list, variable=abr_var)
        self.abr_options.set(abr_list[0])
        self.abr_options.configure(state=ctk.DISABLED)
        self.abr_options.grid(row=16, column=0, padx=10, pady=10, sticky=ctk.NSEW)

        resolution_var = ctk.StringVar()
        self.resolution_options = ctk.CTkOptionMenu(self, values=resolution_list, variable=resolution_var)
        self.resolution_options.set(resolution_list[0])
        self.resolution_options.configure(state=ctk.DISABLED)
        self.resolution_options.grid(row=16, column=1, padx=10, pady=10, sticky=ctk.NSEW)

        extension_var = ctk.StringVar()
        self.extension_options = ctk.CTkOptionMenu(self, variable=extension_var)
        self.extension_options.grid(row=16, column=2, padx=10, pady=10, sticky=ctk.NSEW)

        self.download_button = ctk.CTkButton(self, text=_("Download"),
                                             command=lambda: download_video(yt, extension_var.get(),
                                                                            type_var.get(), abr_var.get(),
                                                                            resolution_var.get()))
        self.download_button.configure(state=ctk.DISABLED)
        self.download_button.grid(row=25, column=0, columnspan=3, padx=10, pady=10, sticky=ctk.NSEW)

        def switch_options(file_type):
            extension_list = []
            if file_type == "audio":
                for video_stream in yt.streams.filter(only_audio=True):
                    extension_list.append(video_stream.mime_type)
                self.resolution_options.configure(state=ctk.DISABLED)
                self.abr_options.configure(state=ctk.ACTIVE)
            if file_type == "video":
                for video_stream in yt.streams.filter(only_video=True):
                    extension_list.append(video_stream.mime_type)
                self.abr_options.configure(state=ctk.DISABLED)
                self.resolution_options.configure(state=ctk.ACTIVE)
            self.download_button.configure(state=ctk.ACTIVE)

            extension_list = list(dict.fromkeys(extension_list))
            self.extension_options.configure(values=extension_list)
            self.extension_options.set(extension_list[0])


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        translations = Translations.load(LOCALE_PATH, [config.LANGUAGE])
        _ = translations.gettext

        self.title("YouTube downloader")
        self.geometry(config.GEOMETRY)
        ctk.set_appearance_mode(config.MODE)

        self.navigation = NavFrame(self)
        self.navigation.grid_rowconfigure(0, weight=1)
        self.navigation.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10), sticky=ctk.NSEW)

        self.frame = UrlFrame(self)
        self.columnconfigure(index=0, weight=1)
        self.frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky=ctk.NSEW)

        self.video = None

    def destroy(self):
        ctk.CTk.destroy(self)

    def quit(self):
        ctk.CTk.quit(self)

    def reload_frames(self):
        self.navigation.destroy()
        self.frame.destroy()

        self.navigation = NavFrame(self)
        self.navigation.grid_rowconfigure(0, weight=1)
        self.navigation.grid(row=0, column=0, columnspan=2, padx=0, pady=(0, 10), sticky=ctk.NSEW)
        self.frame = UrlFrame(self)
        self.columnconfigure(index=0, weight=1)
        self.frame.grid(row=1, column=0, padx=10, pady=(10, 0), sticky=ctk.NSEW)
        if self.video:
            self.video.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
