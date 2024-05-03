class ctx:

    _DRY_RUN = False

    @staticmethod
    def set_is_dry_run(is_dry_run: bool):
        ctx._DRY_RUN = is_dry_run

    @staticmethod
    def is_dry_run():
        return ctx._DRY_RUN
