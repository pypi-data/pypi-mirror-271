class EXlogger:

    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        pass


class Hkeys(object):
    DATA01 = {"quiet": True,  "no_warnings": True, "logger": EXlogger()}
    DATA02 = "%(title,fulltitle,alt_title)s%(season_number& |)s%(season_number&S|)s%(season_number|)02d%(episode_number&E|)s%(episode_number|)02d.%(ext)s"
  
