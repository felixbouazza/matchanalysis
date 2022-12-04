class MatchStatus:

    CANCELLED = "Annulé"
    DEFERRED = "Reporté"
    PENDING = "En attente"
    FINISHED = "Terminé"
    EXTENDED = "Après Prol."
    SHOOTOUT = "Après TAB"

    @classmethod
    def get_as_choices(cls):
        return [
            (cls.CANCELLED, cls.CANCELLED),
            (cls.DEFERRED, cls.DEFERRED),
            (cls.PENDING, cls.PENDING),
            (cls.FINISHED, cls.FINISHED),
            (cls.EXTENDED, cls.EXTENDED),
            (cls.SHOOTOUT, cls.SHOOTOUT),
        ]

    @classmethod
    def get_draw_status(cls):
        return [cls.EXTENDED, cls.SHOOTOUT]

    @classmethod
    def get_played_status(cls):
        return [cls.FINISHED, cls.EXTENDED, cls.SHOOTOUT]

    @classmethod
    def get_unplayed_status(cls):
        return [cls.CANCELLED, cls.DEFERRED, cls.PENDING]
